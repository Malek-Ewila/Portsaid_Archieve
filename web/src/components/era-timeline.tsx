import Link from "next/link";
import { eras, formatYears } from "@/lib/eras";

type EraTimelineProps = {
  activeEraId?: string;
};

export function EraTimeline({ activeEraId }: EraTimelineProps) {
  return (
    <nav aria-label="الخط الزمني لحقب بورسعيد" className="timeline-shell">
      <div className="timeline-scroll" tabIndex={0}>
        <ol className="timeline-list">
          {eras.map((era) => (
            <li className="timeline-item" key={era.id}>
              <Link
                aria-current={era.id === activeEraId ? "page" : undefined}
                className="timeline-link"
                href={`/eras/${era.id}`}
              >
                <span className="timeline-order">{String(era.order).padStart(2, "0")}</span>
                <span className="timeline-years">{formatYears(era)}</span>
                <span className="timeline-title">{era.title}</span>
              </Link>
            </li>
          ))}
        </ol>
      </div>
      <p className="timeline-hint">اسحب أفقيًا لاستكشاف الحقب. استخدم Tab ثم Enter للتنقل.</p>
    </nav>
  );
}
