"use client";

import Link from "next/link";
import { useState } from "react";

export function SiteHeader({ activePath }: { activePath?: string }) {
  const [menuOpen, setMenuOpen] = useState(false);

  const navItems = [
    { href: "/start", label: "Start here" },
    { href: "/sops", label: "Athlete SOPs", highlight: true },
    { href: "/window", label: "Window Calc" },
    { href: "/auditor", label: "Camp & Aid Test" },
    { href: "/offers", label: "10 Offers", highlight: true },
    { href: "/sports", label: "By sport" },
    { href: "/calendar", label: "Calendar" },
    { href: "/playbooks", label: "Playbooks" },
    { href: "/price", label: "Price" },
  ];

  return (
    <header className="border-[#e5e0d6] border-b bg-[#f7f5f0]/95 backdrop-blur supports-[backdrop-filter]:bg-[#f7f5f0]/85 sticky top-0 z-40">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3.5 sm:px-6">
        <Link
          aria-label="The Commit Book home"
          className="flex shrink-0 items-center gap-2"
          href="/"
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            alt="The Commit Book"
            height={30}
            src="/assets/logo/lockup-horizontal-light.svg"
            width={135}
          />
        </Link>

        <nav
          aria-label="Main navigation"
          className="hidden items-center gap-5 lg:flex"
        >
          {navItems.map((item) => {
            const isActive = activePath === item.href;
            return (
              <Link
                className={`text-[13.5px] transition-colors ${
                  isActive
                    ? "font-semibold text-[#141413] underline decoration-[#1d4ed8] decoration-2 underline-offset-4"
                    : item.highlight
                      ? "font-semibold text-[#1d4ed8] hover:text-[#1e3a8a]"
                      : "font-medium text-[#57534e] hover:text-[#141413]"
                }`}
                href={item.href}
                key={item.href}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-2.5">
          <button
            className="cb-header-ask-btn"
            onClick={() => {
              window.dispatchEvent(new CustomEvent("commitbook:ask", { detail: {} }));
            }}
            type="button"
          >
            Ask Guide
          </button>

          <button
            aria-expanded={menuOpen}
            aria-label="Toggle navigation menu"
            className="rounded-lg border border-[#e5e0d6] bg-[#ffffff] px-3 py-1.5 font-mono text-xs font-medium text-[#141413] lg:hidden"
            onClick={() => setMenuOpen((v) => !v)}
            type="button"
          >
            {menuOpen ? "Close" : "Menu"}
          </button>
        </div>
      </div>

      {menuOpen && (
        <nav
          aria-label="Mobile navigation"
          className="border-[#e5e0d6] border-t bg-[#ffffff] px-4 py-3 lg:hidden"
        >
          <div className="grid grid-cols-2 gap-2">
            {navItems.map((item) => (
              <Link
                className="rounded-lg border border-[#e5e0d6] bg-[#f7f5f0] px-3 py-2 text-xs font-medium text-[#141413]"
                href={item.href}
                key={item.href}
                onClick={() => setMenuOpen(false)}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </nav>
      )}
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="border-[#e5e0d6] border-t bg-[#141413] text-[#f7f5f0]">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            alt="The Commit Book"
            height={40}
            src="/assets/logo/lockup-horizontal-dark.svg"
            width={180}
          />
          <div className="flex flex-wrap gap-3 font-mono text-xs text-[#f7f5f0]/80">
            <Link className="hover:text-[#ffffff] underline-offset-4 hover:underline" href="/sops">
              Athlete SOPs
            </Link>
            <span>·</span>
            <Link className="hover:text-[#ffffff] underline-offset-4 hover:underline" href="/window">
              Window Calculator
            </Link>
            <span>·</span>
            <Link className="hover:text-[#ffffff] underline-offset-4 hover:underline" href="/auditor">
              Camp & Aid Test
            </Link>
            <span>·</span>
            <Link className="hover:text-[#ffffff] underline-offset-4 hover:underline" href="/offers">
              10 Recruiting Offers
            </Link>
            <span>·</span>
            <Link className="hover:text-[#ffffff] underline-offset-4 hover:underline" href="/calendar">
              Calendar
            </Link>
            <span>·</span>
            <Link className="hover:text-[#ffffff] underline-offset-4 hover:underline" href="/sports">
              By Sport
            </Link>
            <span>·</span>
            <Link className="hover:text-[#ffffff] underline-offset-4 hover:underline" href="/price">
              Price
            </Link>
            <span>·</span>
            <Link className="hover:text-[#ffffff] underline-offset-4 hover:underline" href="/start">
              Start Free
            </Link>
          </div>
        </div>
        <p className="max-w-4xl text-xs text-[#f7f5f0]/65 leading-relaxed">
          Education, not legal advice. We do not recruit or place athletes, and nobody here contacts your kid. No scholarship, offer, or roster spot is promised. Every sample athlete named here is illustrative. Rules, dates, and roster caps come from public NCAA, NAIA, and NJCAA rulebooks verified November 2026. Not affiliated with or endorsed by the NCAA, NAIA, NJCAA, or any college.
        </p>
      </div>
    </footer>
  );
}
