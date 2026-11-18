import type { Metadata } from "next";
import { notFound } from "next/navigation";
import LegacyPageScripts from "@/components/layout/legacy-page-scripts";
import { listAllLegacyStaticSlugs, parseLegacyHtmlFile } from "@/lib/site-data";

export function generateStaticParams(): { slug: string[] }[] {
  return listAllLegacyStaticSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string[] }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const relPath = `${slug.join("/")}/index.html`;
  const parsed = parseLegacyHtmlFile(relPath);
  if (!parsed) {
    return { title: "Page Not Found | The Commit Book" };
  }
  return {
    title: parsed.title,
    description: parsed.description || undefined,
  };
}

export default async function LegacyCatchAllPage({
  params,
}: {
  params: Promise<{ slug: string[] }>;
}) {
  const { slug } = await params;
  const relPath = `${slug.join("/")}/index.html`;
  const parsed = parseLegacyHtmlFile(relPath);
  if (!parsed) {
    notFound();
  }

  return (
    <>
      {parsed.extraStylesheets.map((href) => (
        <link href={href} key={href} rel="stylesheet" />
      ))}
      <div
        dangerouslySetInnerHTML={{ __html: parsed.bodyHtmlWithoutScripts }}
      />
      <LegacyPageScripts
        dataPage={parsed.dataPage}
        externalScripts={parsed.externalScripts}
        inlineScripts={parsed.inlineScripts}
      />
    </>
  );
}
