import Link from "next/link";
import { ArchivePhoto } from "@/components/archive-photo";
import { EraTimeline } from "@/components/era-timeline";
import { homeHeroImage } from "@/lib/archive-images";
import { eras, formatYears } from "@/lib/eras";

export default function HomePage() {
  return (
    <main id="main-content" className="page-main">
      <section aria-labelledby="home-title" className="hero-section mx-auto grid max-w-[1440px] overflow-hidden lg:grid-cols-[0.92fr_1.08fr]">
        <div className="hero-copy-panel order-1 flex flex-col justify-center px-6 py-14 sm:px-10 lg:px-16 lg:py-24">
          <p className="eyebrow">ذاكرة المكان <span aria-hidden="true">·</span> من 1859 إلى اليوم</p>
          <h1 className="hero-title" id="home-title">مدينةٌ ترويها <span>حكاياتها</span></h1>
          <p className="hero-copy">
            اقرأ تاريخ بورسعيد عبر سبع عشرة حقبة، من نصوص الأرشيف المرتبة زمنيًا.
          </p>
          <a className="hero-link inline-flex w-fit items-center gap-3" href="#eras">
            ابدأ من الخط الزمني <span aria-hidden="true">↓</span>
          </a>
        </div>
        <div className="hero-image-panel order-2">
          <ArchivePhoto image={homeHeroImage} variant="hero" />
        </div>
      </section>

      <section aria-labelledby="timeline-heading" className="timeline-section mx-auto max-w-[1440px] px-5 py-16 sm:px-10 lg:px-20" id="eras">
        <div className="section-heading">
          <div>
            <p className="eyebrow">مسار عبر الزمن</p>
            <h2 id="timeline-heading">الحقب التاريخية</h2>
          </div>
          <p className="section-note">17 حقبة · اختر فترة لقراءة تفاصيلها</p>
        </div>
        <EraTimeline />
      </section>

      <section aria-labelledby="eras-list-title" className="eras-list-section mx-auto max-w-[1440px] px-5 pb-24 sm:px-10 lg:px-20">
        <div className="section-heading">
          <div>
            <p className="eyebrow">تصفّح الأرشيف</p>
            <h2 id="eras-list-title">من التأسيس إلى الحاضر</h2>
          </div>
        </div>
        <ol className="era-grid">
          {eras.map((era) => (
            <li key={era.id}>
              <Link className="era-card" href={`/eras/${era.id}`}>
                <span className="card-order">{String(era.order).padStart(2, "0")}</span>
                <span className="card-content">
                  <span className="card-years">{formatYears(era)}</span>
                  <span className="card-title">{era.title}</span>
                </span>
                <span aria-hidden="true" className="card-arrow">←</span>
              </Link>
            </li>
          ))}
        </ol>
      </section>
    </main>
  );
}
