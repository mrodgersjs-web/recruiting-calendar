import type { Metadata } from "next";
import { JetBrains_Mono, Newsreader, Plus_Jakarta_Sans } from "next/font/google";
import CommitBookChatLauncher from "@/components/chat/commitbook-chat-launcher";
import "./globals.css";

const newsreader = Newsreader({
  subsets: ["latin"],
  variable: "--font-cb-serif",
  display: "swap",
});

const plusJakarta = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-cb-sans",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-cb-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "The Commit Book: real paths to a college roster",
  description:
    "Five divisions, 12 sports, verified NCAA/NAIA/NJCAA contact dates, official Athlete SOP playbooks, and a grounded recruiting guide.",
  icons: {
    icon: [
      { url: "/assets/logo/favicon.svg", type: "image/svg+xml" },
      { url: "/assets/logo/favicon-32.png", sizes: "32x32" },
    ],
    apple: "/assets/logo/favicon-256.png",
  },
  openGraph: {
    images: ["https://recruiting-calendar.vercel.app/assets/logo/social-card-dark.png"],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      className={`${newsreader.variable} ${plusJakarta.variable} ${jetbrainsMono.variable}`}
      lang="en"
    >
      <body className="min-h-screen bg-[#f7f5f0] font-sans text-[#141413] antialiased">
        {children}
        <CommitBookChatLauncher />
      </body>
    </html>
  );
}
