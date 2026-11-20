import Image from "next/image";
import type { ArchiveImage } from "@/lib/archive-images";

type ArchivePhotoProps = {
  image: ArchiveImage;
  variant?: "hero" | "gallery";
};

export function ArchivePhoto({ image, variant = "gallery" }: ArchivePhotoProps) {
  const isHero = variant === "hero";

  return (
    <figure className={`archive-photo archive-photo--${variant}`}>
      <div className="archive-photo-frame">
        <Image
          alt={image.alt}
          className="archive-photo-image"
          fill
          preload={isHero}
          quality={82}
          sizes={isHero ? "(max-width: 800px) 100vw, 58vw" : "(max-width: 700px) 100vw, 50vw"}
          src={image.src}
        />
      </div>
      <figcaption className="archive-photo-caption">
        <span className="archive-photo-title">{image.caption}</span>
        <span className="archive-photo-date">{image.historicalDate}</span>
        <span className="archive-photo-credit">{image.creator} {image.credit}</span>
        <span className="archive-photo-license">{image.license}</span>
        <span className="archive-photo-links">
          <a className="archive-photo-source" href={image.sourceUrl} rel="noreferrer" target="_blank">ملف الصورة ↗</a>
          <a className="archive-photo-source" href={image.sourceRecordUrl} rel="noreferrer" target="_blank">سجل مكتبة الكونغرس ↗</a>
        </span>
      </figcaption>
    </figure>
  );
}
