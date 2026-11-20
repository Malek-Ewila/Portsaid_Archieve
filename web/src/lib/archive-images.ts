import archiveImageData from "@/data/archive-images.json";

export type ArchiveImage = {
  id: string;
  localFilename: string;
  src: string;
  alt: string;
  caption: string;
  historicalDate: string;
  creator: string;
  credit: string;
  license: string;
  sourceUrl: string;
  sourceRecordUrl: string;
};

type ArchiveImageRegistry = {
  homeHero: ArchiveImage;
  eras: Record<string, ArchiveImage[]>;
};

const registry = archiveImageData as ArchiveImageRegistry;

export const homeHeroImage = registry.homeHero;

export function getEraImages(eraId: string): ArchiveImage[] {
  return registry.eras[eraId] ?? [];
}
