import erasJson from "@/data/eras.json";

export type EraImage = {
  url: string;
  alt: string;
  caption?: string;
  credit?: string;
  license?: string;
};

export type EraSource = {
  title: string;
  type?: string;
  citation?: string;
  url?: string;
};

export type EraSection = {
  order: number;
  heading: string;
  paragraphs: string[];
};

export type Era = {
  id: string;
  title: string;
  startYear: number;
  endYear: number;
  order: number;
  introParagraphs: string[];
  sections: EraSection[];
  images: EraImage[];
  sources: EraSource[];
};

export const eras = erasJson as Era[];

export function getEra(id: string): Era | undefined {
  return eras.find((era) => era.id === id);
}

export function formatYears(era: Era): string {
  return `${era.startYear} – ${era.endYear}`;
}
