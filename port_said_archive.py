"""
Port Said Archive: local historical research prototype.

For each complete five-year period from 1859 through 1868, this script:
1. Searches English Wikipedia for relevant material.
2. Fetches article extracts and image URLs.
3. Sends the source text to an LLM for a concise Arabic summary and event list.
4. Saves results incrementally to a local JSON file.

Install:
    python -m pip install -r requirements.txt

Configure:
    Windows PowerShell:
        $env:GEMINI_API_KEY = "your-api-key"
        $env:GEMINI_MODEL = "gemini-3.5-flash-lite"  # optional

    macOS/Linux:
        export GEMINI_API_KEY="your-api-key"
        export GEMINI_MODEL="gemini-3.5-flash-lite"  # optional

Run:
    python port_said_archive.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv


START_YEAR = 1859
END_YEAR = 1868  # Inclusive; gives two complete five-year periods.
PERIOD_LENGTH = 5
OUTPUT_FILE = Path("port_said_archive_1859_1868_5yr.json")

# Read API settings from the .env file beside this script.
load_dotenv(Path(__file__).with_name(".env"))

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_USER_AGENT = "PortSaidArchivePrototype/0.1 (local historical research)"

# Limits keep API requests and LLM input manageable.
MAX_SEARCH_RESULTS_PER_QUERY = 5
MAX_ARTICLES_PER_YEAR = 8
MAX_EXTRACT_CHARS_PER_ARTICLE = 7_000
MAX_TOTAL_SOURCE_CHARS = 30_000
MAX_IMAGES_PER_ARTICLE = 10

SYSTEM_PROMPT = """
You are a careful historical research editor writing for the Port Said Archive.

Use only the source material supplied by the user message. Do not add facts from
memory or infer events that the sources do not support. Wikipedia material may
be incomplete or imprecise; treat it as evidence to summarize, not as guaranteed
truth.

Return one valid JSON object with exactly these keys:
{
  "summary": "Arabic summary of the five-year period in 3 or 4 concise sentences",
  "key_events": ["Arabic event point with its year when known", "..."]
}

Requirements:
- Write the summary and all event points in clear Modern Standard Arabic.
- Focus on the specified five-year period and its relationship to Port Said or the Suez Canal.
- Include only events clearly supported by the supplied sources.
- Do not present a general background fact as if it happened during the specified period.
- Include the year for each event when the sources provide it.
- If the sources do not establish meaningful events for the period, say so clearly
  in the summary and return an empty key_events array.
- Do not include Markdown, citations, or text outside the JSON object.
""".strip()


class WikipediaClient:
    """Small client for the public English Wikipedia Action API."""

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": WIKIPEDIA_USER_AGENT})

    def _get(self, params: dict[str, Any]) -> dict[str, Any]:
        """Make a Wikipedia API request and return its JSON response."""
        response = self.session.get(
            WIKIPEDIA_API_URL,
            params={**params, "format": "json", "formatversion": 2},
            timeout=25,
        )
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            raise RuntimeError(f"Wikipedia API error: {data['error']}")

        return data

    def search_year(self, year: int) -> list[dict[str, Any]]:
        """Find articles whose search results mention Port Said/Suez and the year."""
        queries = [
            f'"Port Said" {year}',
            f'"Suez Canal" {year}',
        ]

        found: dict[int, dict[str, Any]] = {}

        for query in queries:
            data = self._get(
                {
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "srlimit": MAX_SEARCH_RESULTS_PER_QUERY,
                    "srprop": "snippet",
                }
            )

            for result in data.get("query", {}).get("search", []):
                page_id = result.get("pageid")
                if page_id is not None:
                    found[page_id] = {
                        "pageid": page_id,
                        "title": result.get("title", ""),
                        # Search snippets are HTML; the article extract below
                        # will be the actual model input.
                    }

            # Be polite to the public API.
            time.sleep(0.2)

        return list(found.values())[:MAX_ARTICLES_PER_YEAR]

    def fetch_articles(self, pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Fetch plaintext extracts and image file titles for matching pages."""
        if not pages:
            return []

        page_ids = "|".join(str(page["pageid"]) for page in pages)
        data = self._get(
            {
                "action": "query",
                "pageids": page_ids,
                "prop": "extracts|images",
                "explaintext": 1,
                "exchars": MAX_EXTRACT_CHARS_PER_ARTICLE,
                "imlimit": MAX_IMAGES_PER_ARTICLE,
            }
        )

        results = []
        for page in data.get("query", {}).get("pages", []):
            extract = (page.get("extract") or "").strip()
            if not extract:
                continue

            results.append(
                {
                    "title": page.get("title", ""),
                    "pageid": page.get("pageid"),
                    "url": (
                        "https://en.wikipedia.org/?curid="
                        f"{page.get('pageid')}"
                    ),
                    "extract": extract[:MAX_EXTRACT_CHARS_PER_ARTICLE],
                    "image_titles": [
                        image.get("title")
                        for image in page.get("images", [])
                        if image.get("title")
                    ],
                }
            )

        return results

    def fetch_image_urls(self, articles: list[dict[str, Any]]) -> list[str]:
        """Resolve Wikipedia image file titles to direct image URLs."""
        titles: list[str] = []
        for article in articles:
            titles.extend(article.get("image_titles", []))

        # Keep order while removing duplicates.
        unique_titles = list(dict.fromkeys(titles))[:MAX_ARTICLES_PER_YEAR * MAX_IMAGES_PER_ARTICLE]
        if not unique_titles:
            return []

        image_data = self._get(
            {
                "action": "query",
                "titles": "|".join(unique_titles),
                "prop": "imageinfo",
                "iiprop": "url",
            }
        )

        urls: list[str] = []
        for page in image_data.get("query", {}).get("pages", []):
            for image_info in page.get("imageinfo", []):
                url = image_info.get("url")
                if url:
                    urls.append(url)

        return list(dict.fromkeys(urls))


def build_llm_input(start_year: int, end_year: int, articles: list[dict[str, Any]]) -> str:
    """Format and cap article extracts sent to the LLM."""
    chunks: list[str] = []
    remaining = MAX_TOTAL_SOURCE_CHARS

    for article in articles:
        if remaining <= 0:
            break

        extract = article["extract"][:remaining]
        chunks.append(
            f"Relevant search years: {', '.join(map(str, article.get('matched_years', [])))}\n"
            f"Article: {article['title']}\n"
            f"URL: {article['url']}\n"
            f"Extract:\n{extract}"
        )
        remaining -= len(extract)

    return (
        f"Target historical period: {start_year}-{end_year}\n"
        "Summarize only what these Wikipedia source extracts support.\n\n"
        + "\n\n---\n\n".join(chunks)
    )


def summarize_period(client: genai.Client, model: str, start_year: int, end_year: int, articles: list[dict[str, Any]]) -> dict[str, Any]:
    """Request and validate the Arabic summary JSON for one five-year period."""
    response = client.models.generate_content(
        model=model,
        contents=build_llm_input(start_year, end_year, articles),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2,
            response_mime_type="application/json",
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "summary": {"type": "STRING"},
                    "key_events": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"},
                    },
                },
                "required": ["summary", "key_events"],
            },
        ),
    )

    content = response.text
    if not content:
        raise ValueError("The LLM returned an empty response.")

    result = json.loads(content)

    summary = result.get("summary")
    key_events = result.get("key_events")

    if not isinstance(summary, str):
        raise ValueError("LLM response is missing a string 'summary'.")
    if not isinstance(key_events, list) or not all(
        isinstance(event, str) for event in key_events
    ):
        raise ValueError("LLM response 'key_events' must be a list of strings.")

    return {"summary": summary.strip(), "key_events": key_events}


def save_results(records: list[dict[str, Any]]) -> None:
    """Write current results so progress is not lost if a later period fails."""
    OUTPUT_FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: Set the GEMINI_API_KEY environment variable first.", file=sys.stderr)
        return 2

    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    wikipedia = WikipediaClient()
    llm = genai.Client(api_key=api_key)

    periods = [
        (period_start, min(period_start + PERIOD_LENGTH - 1, END_YEAR))
        for period_start in range(START_YEAR, END_YEAR + 1, PERIOD_LENGTH)
    ]
    records: list[dict[str, Any]] = []

    print(f"Starting Port Said Archive prototype: {START_YEAR}–{END_YEAR}")
    print(f"Processing {len(periods)} five-year period(s).")
    print(f"Output file: {OUTPUT_FILE.resolve()}")
    print(f"LLM model: {model}")

    for index, (period_start, period_end) in enumerate(periods, start=1):
        period_label = f"{period_start}-{period_end}"
        print(f"\n[{index}/{len(periods)}] Processing {period_label}...")

        record: dict[str, Any] = {
            "period": period_label,
            "start_year": period_start,
            "end_year": period_end,
            "summary": None,
            "key_events": [],
            "raw_image_urls_if_any": [],
            "sources": [],
            "status": "pending",
            "error": None,
        }

        try:
            articles_by_id: dict[int, dict[str, Any]] = {}
            for source_year in range(period_start, period_end + 1):
                print(f"  Searching Wikipedia for {source_year}...")
                search_results = wikipedia.search_year(source_year)
                year_articles = wikipedia.fetch_articles(search_results)
                for article in year_articles:
                    page_id = article["pageid"]
                    if page_id in articles_by_id:
                        matched_years = articles_by_id[page_id]["matched_years"]
                        if source_year not in matched_years:
                            matched_years.append(source_year)
                    else:
                        article["matched_years"] = [source_year]
                        articles_by_id[page_id] = article
                print(f"    Found {len(year_articles)} usable article(s).")

            articles = list(articles_by_id.values())
            print(f"  {len(articles)} unique source article(s) for this period.")
            print("  Fetching image URLs...")

            record["sources"] = [
                {
                    "title": article["title"],
                    "url": article["url"],
                    "matched_years": article["matched_years"],
                }
                for article in articles
            ]
            record["raw_image_urls_if_any"] = wikipedia.fetch_image_urls(articles)

            if not articles:
                record["status"] = "no_sources"
                record["summary"] = (
                    "لم تُعثر في نتائج ويكيبيديا المتاحة على مادة كافية "
                    f"لتلخيص أحداث مرتبطة ببورسعيد أو قناة السويس في عام {period_label}."
                )
                print("  No usable article extracts; skipping the LLM for this period.")
            else:
                print(f"  Sending {len(articles)} article extract(s) to the LLM...")
                generated = summarize_period(llm, model, period_start, period_end, articles)
                record["summary"] = generated["summary"]
                record["key_events"] = generated["key_events"]
                record["status"] = "ok"
                print("  Summary generated.")

        except requests.RequestException as exc:
            record["status"] = "error"
            record["error"] = f"Wikipedia network/API error: {exc}"
            print(f"  ERROR: {record['error']}", file=sys.stderr)
        except Exception as exc:
            # Continue processing later periods if one API response fails.
            record["status"] = "error"
            record["error"] = f"{type(exc).__name__}: {exc}"
            print(f"  ERROR: {record['error']}", file=sys.stderr)

        records.append(record)
        save_results(records)
        print(f"  Saved progress ({len(records)} period record(s)).")

        # Small delay between periods to reduce request bursts.
        time.sleep(0.3)

    print(f"\nFinished. Results saved to: {OUTPUT_FILE.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
