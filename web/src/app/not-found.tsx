import Link from "next/link";

export default function NotFound() {
  return (
    <main className="page-main not-found" id="main-content">
      <p className="eyebrow">404 · الأرشيف</p>
      <h1>هذه الحقبة غير موجودة</h1>
      <p>قد يكون رابط الصفحة غير صحيح.</p>
      <Link className="text-link" href="/">العودة إلى الصفحة الرئيسية</Link>
    </main>
  );
}
