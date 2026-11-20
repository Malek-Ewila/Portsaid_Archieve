import Link from "next/link";

export function SiteHeader() {
  return (
    <header className="site-header px-5 sm:px-10 lg:px-20">
      <Link aria-label="أرشيف بورسعيد — الصفحة الرئيسية" className="brand" href="/">
        <span aria-hidden="true" className="brand-mark">ب</span>
        <span>
          <span className="brand-name">أرشيف بورسعيد</span>
          <span className="brand-subtitle">حكاية مدينة على ضفاف القناة</span>
        </span>
      </Link>
      <span className="header-note">1859 — اليوم</span>
    </header>
  );
}
