import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArchivePhoto } from "@/components/archive-photo";
import { EraTimeline } from "@/components/era-timeline";
import { getEraImages } from "@/lib/archive-images";
import { eras, formatYears, getEra } from "@/lib/eras";

type EraPageProps = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return eras.map((era) => ({ slug: era.id }));
}

export async function generateMetadata({ params }: EraPageProps): Promise<Metadata> {
  const { slug } = await params;
  const era = getEra(slug);
  return era ? { title: era.title } : { title: "الحقبة غير موجودة" };
}

export default async function EraPage({ params }: EraPageProps) {
  const { slug } = await params;
  const era = getEra(slug);
  if (!era) notFound();

  const previousEra = eras[era.order - 2];
  const nextEra = eras[era.order];
  const archiveImages = getEraImages(era.id);

  return (
    <main id="main-content" className="page-main era-page">
      <div className="era-back-link"><Link className="text-link" href="/">→ العودة إلى الأرشيف</Link></div>
      <section aria-labelledby="era-title" className="era-hero motion-reveal">
        <p className="eyebrow">الحقبة {String(era.order).padStart(2, "0")} / 17</p>
        <p className="era-years">{formatYears(era)}</p>
        <h1 id="era-title">{era.title}</h1>
      </section>

      <EraTimeline activeEraId={era.id} />

      <article aria-label={`نصوص حقبة ${formatYears(era)}`} className="narrative">
        {era.introParagraphs.map((paragraph, index) => (
          <p className="intro-paragraph" key={`intro-${index}`}>{paragraph}</p>
        ))}

        {era.sections.map((section) => (
          <section className="narrative-section motion-reveal" key={`${era.id}-${section.order}`}>
            <p className="section-index">{String(section.order).padStart(2, "0")}</p>
            <h2>{section.heading}</h2>
            {section.paragraphs.map((paragraph, index) => (
              <p key={`${era.id}-${section.order}-${index}`}>{paragraph}</p>
            ))}
          </section>
        ))}

        <section aria-labelledby="images-heading" className="media-section">
          <h2 id="images-heading">صور من الأرشيف</h2>
          {archiveImages.length > 0 ? (
            <div className="image-list">
              {archiveImages.map((image) => (
                <ArchivePhoto image={image} key={image.id} />
              ))}
            </div>
          ) : (
            <p className="media-empty">لم تُضف صور أرشيفية لهذه الحقبة بعد.</p>
          )}
        </section>

        {era.sources.length > 0 && (
          <section aria-labelledby="sources-heading" className="sources-section">
            <h2 id="sources-heading">المصادر</h2>
            <ul>
              {era.sources.map((source, index) => (
                <li key={`${source.title}-${index}`}>
                  {source.url ? <a href={source.url}>{source.title}</a> : source.title}
                  {source.citation && <span> — {source.citation}</span>}
                </li>
              ))}
            </ul>
          </section>
        )}
      </article>

      <nav aria-label="التنقل بين الحقب" className="era-pagination">
        {previousEra ? (
          <Link href={`/eras/${previousEra.id}`} rel="prev">
            <span>الحقبة السابقة</span><strong>{previousEra.title}</strong>
          </Link>
        ) : <span />}
        {nextEra ? (
          <Link href={`/eras/${nextEra.id}`} rel="next">
            <span>الحقبة التالية</span><strong>{nextEra.title}</strong>
          </Link>
        ) : <Link href="/">العودة إلى كل الحقب</Link>}
      </nav>
    </main>
  );
}
