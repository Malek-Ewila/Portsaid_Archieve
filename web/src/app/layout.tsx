import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { SiteHeader } from "@/components/site-header";

const notoNaskhArabic = localFont({
  src: "../../public/fonts/noto-naskh-arabic-variable.woff2",
  display: "swap",
  variable: "--font-naskh",
  weight: "400 700",
});

const ibmPlexSansArabic = localFont({
  src: [
    { path: "../../public/fonts/ibm-plex-sans-arabic-400.woff2", weight: "400" },
    { path: "../../public/fonts/ibm-plex-sans-arabic-600.woff2", weight: "600" },
    { path: "../../public/fonts/ibm-plex-sans-arabic-700.woff2", weight: "700" },
  ],
  display: "swap",
  variable: "--font-plex",
});

export const metadata: Metadata = {
  title: {
    default: "أرشيف بورسعيد — حكاية مدينة على ضفاف القناة",
    template: "%s | أرشيف بورسعيد",
  },
  description: "قراءة في تاريخ بورسعيد عبر سبع عشرة حقبة زمنية.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html className={`${notoNaskhArabic.variable} ${ibmPlexSansArabic.variable}`} lang="ar" dir="rtl" data-scroll-behavior="smooth">
      <body>
        <a className="skip-link" href="#main-content">انتقل إلى المحتوى</a>
        <SiteHeader />
        {children}
        <footer className="site-footer">
          <span>أرشيف بورسعيد</span>
          <span>حفظٌ لحكايات المدينة وذاكرتها</span>
        </footer>
      </body>
    </html>
  );
}
