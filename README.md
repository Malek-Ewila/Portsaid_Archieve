# Port Said Archive prototype

This repository contains a read-only Arabic Next.js prototype backed by the 17
owner-supplied Word documents. The Word text is copied into JSON without AI
rewriting. Images and sources are supported by the data model but are empty in
this prototype.

## Verify the Word-to-JSON transfer

From the repository root, run:

```powershell
python scripts/verify_docx_json.py --source-dir "D:\DOWNLOADS\Portsaid_Decades"
```

To create a fresh transfer, use `--write`. It refuses to overwrite either JSON
output file. The original Word documents remain in their source folder.

## Run the website

```powershell
cd web
npm install
npm run dev
```

Open `http://localhost:3000`. The app uses Next.js Server Components and local
JSON files; it does not connect to MySQL or expose API routes.

## Checks

```powershell
# From the repository root
python scripts/verify_docx_json.py --source-dir "D:\DOWNLOADS\Portsaid_Decades"

# From web/
npm run lint
npm run test:e2e
npm run build
```

Playwright browser binaries may need to be installed once with
`npx playwright install chromium`.
