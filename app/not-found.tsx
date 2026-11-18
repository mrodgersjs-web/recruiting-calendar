import Link from "next/link";
import { SiteFooter, SiteHeader } from "@/components/layout/site-chrome";
import { parseLegacyHtmlFile } from "@/lib/site-data";

export default function NotFound() {
  const parsed404 = parseLegacyHtmlFile("404.html");
  if (parsed404) {
    return (
      <div dangerouslySetInnerHTML={{ __html: parsed404.bodyHtmlWithoutScripts }} />
    );
  }
  return (
    <div className="flex min-h-screen flex-col bg-[#f7f5f0]">
      <SiteHeader />
      <main className="mx-auto flex max-w-2xl flex-1 flex-col items-center justify-center px-6 py-20 text-center">
        <p className="font-mono text-xs font-semibold uppercase tracking-widest text-[#b91c1c]">
          404 · Page Not Found
        </p>
        <h1 className="mt-2 font-serif text-3xl font-semibold text-[#141413]">
          That recruiting page is not at this address.
        </h1>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <Link
            className="rounded-xl bg-[#141413] px-4 py-2.5 font-semibold text-sm text-[#f7f5f0]"
            href="/"
          >
            Back to Home
          </Link>
          <Link
            className="rounded-xl border border-[#e5e0d6] bg-white px-4 py-2.5 font-semibold text-sm text-[#141413]"
            href="/sops"
          >
            Open Athlete SOPs
          </Link>
        </div>
      </main>
      <SiteFooter />
    </div>
  );
}
