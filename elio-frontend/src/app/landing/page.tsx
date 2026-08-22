"use client";

import { useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";
import {
  ArrowLeftRight,
  BadgeCheck,
  Braces,
  Factory,
  FileOutput,
  GitCompareArrows,
  ListChecks,
  ShieldAlert,
  ShieldCheck,
  ShieldOff,
  TableProperties,
  UserRoundCheck,
  Workflow,
  type LucideIcon,
} from "lucide-react";

if (typeof window !== "undefined") {
  gsap.registerPlugin(ScrollTrigger, useGSAP);
}

export default function LandingPage() {
  const mainRef = useRef<HTMLDivElement>(null);
  const orb1Ref = useRef<HTMLDivElement>(null);
  const orb2Ref = useRef<HTMLDivElement>(null);
  const orb3Ref = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    // ── 1. Ambient Background Orbs Parallax & Drift ──────────────────────────
    if (orb1Ref.current && orb2Ref.current) {
      const xTo1 = gsap.quickTo(orb1Ref.current, "x", { duration: 1.2, ease: "power2.out" });
      const yTo1 = gsap.quickTo(orb1Ref.current, "y", { duration: 1.2, ease: "power2.out" });
      const xTo2 = gsap.quickTo(orb2Ref.current, "x", { duration: 1.6, ease: "power2.out" });
      const yTo2 = gsap.quickTo(orb2Ref.current, "y", { duration: 1.6, ease: "power2.out" });

      const handleMouseMove = (e: MouseEvent) => {
        const { innerWidth, innerHeight } = window;
        const normX = (e.clientX / innerWidth - 0.5) * 50;
        const normY = (e.clientY / innerHeight - 0.5) * 50;
        xTo1(normX * 0.8);
        yTo1(normY * 0.8);
        xTo2(-normX * 0.6);
        yTo2(-normY * 0.6);
      };

      window.addEventListener("mousemove", handleMouseMove, { passive: true });

      // Organic continuous breathing drift
      gsap.to(orb1Ref.current, {
        scale: 1.08,
        rotation: 8,
        duration: 7,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut",
      });

      gsap.to(orb2Ref.current, {
        scale: 1.12,
        rotation: -10,
        duration: 9,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut",
        delay: 1,
      });

      if (orb3Ref.current) {
        gsap.to(orb3Ref.current, {
          scale: 1.15,
          duration: 6,
          repeat: -1,
          yoyo: true,
          ease: "sine.inOut",
          delay: 0.5,
        });
      }
    }

    // ── 2. Hero Entrance Master Timeline (fromTo + clearProps) ─────────────────
    const heroTl = gsap.timeline({ defaults: { ease: "power3.out" } });

    heroTl
      .fromTo(
        ".hero-nav",
        { y: -20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.7, clearProps: "transform,opacity" }
      )
      .fromTo(
        ".hero-badge",
        { y: 15, opacity: 0, scale: 0.95 },
        { y: 0, opacity: 1, scale: 1, duration: 0.55, clearProps: "transform,opacity" },
        "-=0.3"
      )
      .fromTo(
        ".hero-title",
        { y: 30, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.8, ease: "power4.out", clearProps: "transform,opacity" },
        "-=0.35"
      )
      .fromTo(
        ".hero-sub",
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.7, clearProps: "transform,opacity" },
        "-=0.5"
      )
      .fromTo(
        ".hero-cta-btn",
        { y: 15, opacity: 0, scale: 0.96 },
        { y: 0, opacity: 1, scale: 1, stagger: 0.08, duration: 0.6, ease: "back.out(1.2)", clearProps: "transform,opacity" },
        "-=0.4"
      )
      .fromTo(
        ".hero-stat-card",
        { y: 25, opacity: 0, scale: 0.98 },
        { y: 0, opacity: 1, scale: 1, stagger: 0.1, duration: 0.65, clearProps: "opacity" },
        "-=0.3"
      )
      .fromTo(
        ".hero-proof-item",
        { y: 10, opacity: 0 },
        { y: 0, opacity: 1, stagger: 0.06, duration: 0.5, clearProps: "transform,opacity" },
        "-=0.2"
      );

    // Continuous floating hover physics on hero stat cards
    gsap.to(".hero-stat-card-1", {
      y: -6,
      duration: 3,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut",
    });

    gsap.to(".hero-stat-card-2", {
      y: -8,
      duration: 3.4,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut",
      delay: 0.4,
    });

    // ── 3. ScrollTrigger Section Reveals with fromTo + clearProps ────────────
    const scrollReveal = (selector: string, triggerSelector: string, stagger = 0.08) => {
      const els = document.querySelectorAll(selector);
      if (els.length > 0) {
        gsap.fromTo(
          els,
          { opacity: 0, y: 30 },
          {
            opacity: 1,
            y: 0,
            duration: 0.65,
            stagger,
            ease: "power2.out",
            clearProps: "transform,opacity",
            scrollTrigger: {
              trigger: triggerSelector,
              start: "top 88%",
              toggleActions: "play none none none",
              once: true,
            },
          }
        );
      }
    };

    scrollReveal(".features-reveal-item", "#features", 0.1);
    scrollReveal(".bento-card-item", ".bento-grid-container", 0.12);
    scrollReveal(".capabilities-reveal-item", "#capabilities", 0.1);
    scrollReveal(".capability-item-card", ".capability-grid-container", 0.05);
    scrollReveal(".integrations-reveal-item", "#integrations", 0.1);
    scrollReveal(".integration-logo-badge", ".integration-logos-strip", 0.06);
    scrollReveal(".integration-item-card", ".integration-grid-container", 0.08);
    scrollReveal(".cta-container-box", "#cta", 0);

    // Refresh ScrollTrigger to recalculate exact positions
    ScrollTrigger.refresh();
  }, { scope: mainRef });

  const capabilityItems: { icon: LucideIcon; title: string; desc: string }[] = [
    { icon: BadgeCheck, title: "Evidence Provenance", desc: "Every catalog value links to a re-fetchable document snippet and character span, nothing is asserted without a source." },
    { icon: ShieldAlert, title: "Abstention Pipeline", desc: "When evidence criteria fail, the engine refuses to guess and flags the row for human review with a reason." },
    { icon: GitCompareArrows, title: "Dual-Pass Verification", desc: "Two independent passes cross-check every extraction before a value reaches the ledger." },
    { icon: UserRoundCheck, title: "Reviewer Decisions", desc: "Accept or reject escalated rows; manual overrides are applied and logged at export." },
    { icon: Braces, title: "Developer API", desc: "Run the pipeline on your own catalog files through a single HTTP endpoint." },
    { icon: ArrowLeftRight, title: "Dataset Switching", desc: "Flip between demo, full, and uploaded catalogs; every derived number recomputes." },
    { icon: FileOutput, title: "252-Column Export", desc: "Flat delivery projection with formula-injection sanitization and all overrides applied." },
    { icon: ShieldCheck, title: "Formula Sanitization", desc: "Cells starting with =, +, -, or @ are neutralized before the CSV leaves the app." },
    { icon: Workflow, title: "Deterministic DAG", desc: "A fixed intake-to-verification pipeline, never a black box, with counts for every stage." },
  ];

  const integrationCapabilities: { icon: LucideIcon; title: string; desc: string }[] = [
    { icon: Factory, title: "Manufacturer Data Sources", desc: "E1, Unilog, and DIB brand columns resolve against manufacturer documents, not memory." },
    { icon: TableProperties, title: "Structured Output", desc: "Get a flat 252-column projection, not nested JSON, ready for direct ingestion." },
    { icon: ShieldOff, title: "Evidence-Gated Refusals", desc: "The engine abstains rather than guesses when verification criteria fail." },
    { icon: ListChecks, title: "Review Queue Orchestration", desc: "Escalated rows route to a single review queue with pagination and decisions." },
  ];

  return (
    <main ref={mainRef} className="overflow-x-hidden w-full max-w-full min-h-screen relative" style={{ background: "#f0efe8" }}>
      {/* ── Ambient Background Gradient Orbs ─────────────────────────── */}
      <div style={{ position: "fixed", inset: 0, pointerEvents: "none", overflow: "hidden", zIndex: 0 }}>
        {/* Top-left green/lime orb */}
        <div
          ref={orb1Ref}
          style={{
            position: "absolute",
            top: "-15%",
            left: "-8%",
            width: "60vw",
            height: "60vw",
            borderRadius: "50%",
            background: "radial-gradient(circle at 30% 40%, rgba(178,210,80,0.75) 0%, rgba(160,200,60,0.45) 30%, transparent 65%)",
            filter: "blur(70px)",
            willChange: "transform",
          }}
        />
        {/* Bottom-right green orb */}
        <div
          ref={orb2Ref}
          style={{
            position: "absolute",
            bottom: "5%",
            right: "-12%",
            width: "50vw",
            height: "50vw",
            borderRadius: "50%",
            background: "radial-gradient(circle at 60% 50%, rgba(170,205,70,0.65) 0%, rgba(150,195,55,0.35) 35%, transparent 65%)",
            filter: "blur(80px)",
            willChange: "transform",
          }}
        />
        {/* Center soft warm orb */}
        <div
          ref={orb3Ref}
          style={{
            position: "absolute",
            top: "35%",
            left: "35%",
            width: "25vw",
            height: "25vw",
            borderRadius: "50%",
            background: "radial-gradient(circle, rgba(200,215,130,0.3) 0%, transparent 70%)",
            filter: "blur(50px)",
            willChange: "transform",
          }}
        />
      </div>

      {/* ── Navigation ─────────────────────────────────────────────────── */}
      <nav
        className="hero-nav"
        style={{
          position: "relative",
          zIndex: 50,
          display: "flex",
          justifyContent: "center",
          flexWrap: "wrap",
          gap: "12px",
          padding: "20px 24px 0",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            flexWrap: "wrap",
            justifyContent: "center",
            background: "#161612",
            borderRadius: "999px",
            padding: "6px 6px 6px 10px",
            boxShadow: "0 4px 32px rgba(0,0,0,0.22), 0 0 0 1px rgba(255,255,255,0.05)",
            gap: "2px",
          }}
        >
          {/* Logo Icon */}
          <div
            style={{
              width: "30px",
              height: "30px",
              borderRadius: "50%",
              background: "linear-gradient(135deg, #c8d84a, #a8c830)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              marginRight: "10px",
              flexShrink: 0,
            }}
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
              <path d="M3 12L10 5L17 12L10 19L3 12Z" fill="#1a1a0e" />
              <path d="M10 5L17 12L21 8" stroke="#1a1a0e" strokeWidth="1.5" />
            </svg>
          </div>

          {/* Nav Links */}
          {["Features", "Capabilities", "Integrations"].map((link) => (
            <a
              key={link}
              href={`#${link.toLowerCase()}`}
              style={{
                color: "rgba(255,255,255,0.72)",
                textDecoration: "none",
                fontSize: "13px",
                fontWeight: "440",
                padding: "6px 13px",
                borderRadius: "999px",
                transition: "color 0.2s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s cubic-bezier(0.16, 1, 0.3, 1)",
                fontFamily: "var(--font-geist-sans)",
                letterSpacing: "0.005em",
                whiteSpace: "nowrap",
              }}
              onMouseEnter={(e) => {
                const el = e.currentTarget as HTMLElement;
                el.style.color = "#fff";
                el.style.background = "rgba(255,255,255,0.08)";
              }}
              onMouseLeave={(e) => {
                const el = e.currentTarget as HTMLElement;
                el.style.color = "rgba(255,255,255,0.72)";
                el.style.background = "transparent";
              }}
            >
              {link}
            </a>
          ))}

          {/* CTA Button */}
          <a
            href="/app/dashboard"
            style={{
              marginLeft: "6px",
              background: "#f0efe8",
              color: "#161612",
              textDecoration: "none",
              fontSize: "13px",
              fontWeight: "600",
              padding: "8px 18px",
              borderRadius: "999px",
              fontFamily: "var(--font-geist-sans)",
              letterSpacing: "0.005em",
              whiteSpace: "nowrap",
              transition: "background 0.2s cubic-bezier(0.16, 1, 0.3, 1), transform 0.2s cubic-bezier(0.16, 1, 0.3, 1)",
              display: "inline-block",
            }}
            onMouseEnter={(e) => {
              const el = e.currentTarget as HTMLElement;
              el.style.background = "#e2e1d8";
              el.style.transform = "scale(1.03)";
            }}
            onMouseLeave={(e) => {
              const el = e.currentTarget as HTMLElement;
              el.style.background = "#f0efe8";
              el.style.transform = "scale(1)";
            }}
          >
            Get Started
          </a>
        </div>
      </nav>

      {/* ── Hero Section ───────────────────────────────────────────────── */}
      <section
        id="hero"
        style={{
          position: "relative",
          zIndex: 1,
          maxWidth: "1200px",
          margin: "0 auto",
          padding: "72px clamp(28px, 6vw, 48px)",
        }}
      >
        {/* Product Badge */}
        <div className="hero-badge" style={{ marginBottom: "24px" }}>
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "7px",
              border: "1px solid rgba(30,28,20,0.22)",
              borderRadius: "999px",
              padding: "5px 14px",
              fontSize: "12px",
              fontWeight: "500",
              color: "#3a3928",
              background: "rgba(255,255,255,0.55)",
              letterSpacing: "0.01em",
              fontFamily: "var(--font-geist-sans)",
              backdropFilter: "blur(6px)",
            }}
          >
            <span style={{ width: "6px", height: "6px", borderRadius: "50%", background: "#8cac28", flexShrink: 0 }} />
            ELIO Cockpit
          </span>
        </div>

        <h1
          className="hero-title"
          style={{
            maxWidth: "860px",
            fontSize: "clamp(2.2rem, 3.8vw, 3.4rem)",
            lineHeight: "1.12",
            fontWeight: "700",
            color: "#18180e",
            fontFamily: "var(--font-geist-sans)",
            marginBottom: "22px",
            letterSpacing: "-0.022em",
          }}
        >
          Evidence-traced catalog enrichment — for distributors.
        </h1>

        {/* Subtitle */}
        <p
          className="hero-sub"
          style={{
            maxWidth: "540px",
            fontSize: "14.5px",
            lineHeight: "1.65",
            color: "#565644",
            marginBottom: "48px",
            fontFamily: "var(--font-geist-sans)",
            fontWeight: "400",
          }}
        >
          ELIO enriches your product catalog from manufacturer evidence, tracing every value to a
          re-fetchable document snippet, and abstaining, with a reason, when evidence fails.
        </p>

        {/* Primary CTA row */}
        <div style={{ display: "flex", gap: "10px", justifyContent: "flex-start", flexWrap: "wrap", marginBottom: "36px" }}>
          <a
            href="/app/dashboard"
            className="hero-cta-btn"
            style={{
              background: "#c8d84a",
              color: "#18180e",
              borderRadius: "999px",
              padding: "12px 28px",
              fontWeight: 700,
              fontSize: "14px",
              textDecoration: "none",
              display: "inline-block",
              fontFamily: "var(--font-geist-sans)",
              boxShadow: "0 4px 18px rgba(170,205,50,0.32)",
              transition: "transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s ease",
            }}
            onMouseEnter={(e) => {
              const el = e.currentTarget as HTMLElement;
              el.style.transform = "translateY(-2px) scale(1.02)";
              el.style.boxShadow = "0 8px 24px rgba(170,205,50,0.45)";
            }}
            onMouseLeave={(e) => {
              const el = e.currentTarget as HTMLElement;
              el.style.transform = "translateY(0) scale(1)";
              el.style.boxShadow = "0 4px 18px rgba(170,205,50,0.32)";
            }}
          >
            Load demo catalog — 30s
          </a>
          <a
            href="#capabilities"
            className="hero-cta-btn"
            style={{
              background: "rgba(255,255,255,0.7)",
              color: "#18180e",
              border: "1px solid rgba(24,24,14,0.14)",
              borderRadius: "999px",
              padding: "12px 24px",
              fontSize: "14px",
              fontWeight: 600,
              textDecoration: "none",
              display: "inline-block",
              fontFamily: "var(--font-geist-sans)",
              transition: "transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s ease",
            }}
            onMouseEnter={(e) => {
              const el = e.currentTarget as HTMLElement;
              el.style.background = "rgba(255,255,255,0.95)";
              el.style.transform = "translateY(-2px)";
            }}
            onMouseLeave={(e) => {
              const el = e.currentTarget as HTMLElement;
              el.style.background = "rgba(255,255,255,0.7)";
              el.style.transform = "translateY(0)";
            }}
          >
            See how it works
          </a>
        </div>

        {/* Stat Cards */}
        <div style={{ display: "flex", gap: "14px", flexWrap: "wrap" }}>
          {/* Stat Card 1 */}
          <div
            className="hero-stat-card hero-stat-card-1"
            style={{
              background: "rgba(255,255,255,0.88)",
              border: "1px solid rgba(18,18,16,0.09)",
              borderRadius: "14px",
              padding: "16px 24px",
              display: "flex",
              alignItems: "center",
              gap: "14px",
              backdropFilter: "blur(10px)",
              boxShadow: "0 4px 20px rgba(0,0,0,0.04)",
              minWidth: "190px",
              willChange: "transform",
            }}
          >
            <div
              style={{
                width: "38px",
                height: "38px",
                borderRadius: "50%",
                border: "1.5px solid rgba(140,172,40,0.45)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background: "rgba(140,172,40,0.07)",
                flexShrink: 0,
              }}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#8cac28" strokeWidth="2" strokeLinecap="round">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12,6 12,12 16,14" />
              </svg>
            </div>
            <div>
              <div style={{ fontSize: "10.5px", color: "#6a6a58", fontWeight: "500", letterSpacing: "0.05em", textTransform: "uppercase", marginBottom: "2px", fontFamily: "var(--font-geist-sans)" }}>Rows Verified</div>
              <div style={{ fontSize: "21px", fontWeight: "700", color: "#18180e", lineHeight: "1", fontFamily: "var(--font-geist-sans)" }}>50 / 50</div>
            </div>
          </div>

          {/* Stat Card 2 */}
          <div
            className="hero-stat-card hero-stat-card-2"
            style={{
              background: "rgba(255,255,255,0.88)",
              border: "1px solid rgba(18,18,16,0.09)",
              borderRadius: "14px",
              padding: "16px 24px",
              display: "flex",
              alignItems: "center",
              gap: "14px",
              backdropFilter: "blur(10px)",
              boxShadow: "0 4px 20px rgba(0,0,0,0.04)",
              minWidth: "190px",
              willChange: "transform",
            }}
          >
            <div
              style={{
                width: "38px",
                height: "38px",
                borderRadius: "50%",
                border: "1.5px solid rgba(140,172,40,0.45)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background: "rgba(140,172,40,0.07)",
                flexShrink: 0,
              }}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#8cac28" strokeWidth="2" strokeLinecap="round">
                <polyline points="23,6 13.5,15.5 8.5,10.5 1,18" />
                <polyline points="17,6 23,6 23,12" />
              </svg>
            </div>
            <div>
              <div style={{ fontSize: "10.5px", color: "#6a6a58", fontWeight: "500", letterSpacing: "0.05em", textTransform: "uppercase", marginBottom: "2px", fontFamily: "var(--font-geist-sans)" }}>Attrs per Row</div>
              <div style={{ fontSize: "21px", fontWeight: "700", color: "#18180e", lineHeight: "1", fontFamily: "var(--font-geist-sans)" }}>50.0</div>
            </div>
          </div>
        </div>

        {/* Proof strip */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: "10px", justifyContent: "flex-start", alignItems: "center", marginTop: "32px", color: "#6a6a58", fontSize: "12px", fontWeight: "500", letterSpacing: "0.08em", textTransform: "uppercase", fontFamily: "var(--font-geist-sans)" }}>
          <span className="hero-proof-item" style={{ border: "1px solid rgba(106,106,88,0.18)", borderRadius: "999px", padding: "6px 12px", background: "rgba(255,255,255,0.65)" }}>Built for distributors</span>
          <span style={{ opacity: 0.35 }}>·</span>
          <span className="hero-proof-item" style={{ border: "1px solid rgba(106,106,88,0.18)", borderRadius: "999px", padding: "6px 12px", background: "rgba(255,255,255,0.65)" }}>Trusted patterns</span>
          <span style={{ opacity: 0.35 }}>·</span>
          <span className="hero-proof-item" style={{ border: "1px solid rgba(106,106,88,0.18)", borderRadius: "999px", padding: "6px 12px", background: "rgba(255,255,255,0.65)" }}>Evidence-traced</span>
        </div>
      </section>

      {/* ── Features / Bento Section ────────────────────────────────────── */}
      <section
        id="features"
        style={{
          position: "relative",
          zIndex: 1,
          maxWidth: "1200px",
          margin: "0 auto",
          padding: "72px clamp(28px, 6vw, 48px)",
        }}
      >
        <div style={{ textAlign: "center", marginBottom: "48px" }}>
          <div className="features-reveal-item" style={{ marginBottom: "10px" }}>
            <span
              style={{
                fontSize: "12px",
                fontWeight: "600",
                color: "#8cac28",
                letterSpacing: "0.06em",
                fontFamily: "var(--font-geist-sans)",
              }}
            >
              Core Capabilities
            </span>
          </div>

          <h2
            className="features-reveal-item"
            style={{
              textAlign: "center",
              fontSize: "clamp(1.75rem, 2.8vw, 2.4rem)",
              fontWeight: "700",
              color: "#18180e",
              letterSpacing: "-0.018em",
              margin: "0 auto",
              maxWidth: "560px",
              lineHeight: "1.2",
              fontFamily: "var(--font-geist-sans)",
            }}
          >
            Manage and Optimize Your<br />Catalog in One Place
          </h2>
        </div>

        {/* Bento 2x2 Grid */}
        <div
          className="bento-grid-container"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "14px",
            gridAutoFlow: "dense",
          }}
        >
          <BentoCard mockup={<OverviewMockup />} title="Acceptance Dashboard" desc="Real derived metrics: attributes per row, evidence support, and abstention counts, with no invented percentages." />
          <BentoCard mockup={<PipelineMockup />} title="Processing Stage Volumes" desc="Intake, entity resolution, classification, and dual-pass verification counts from the deterministic DAG." />
          <BentoCard mockup={<EvidenceMockup />} title="Evidence Explorer" desc="Every attribute opens a custody chain: source link, page, and the verbatim snippet with the value highlighted." />
          <BentoCard mockup={<IntegrationsMockup />} title="Review & Export" desc="Adjudicate escalated rows, apply manual overrides, then export the sanitized 252-column CSV." />
        </div>
      </section>

      {/* ── Capabilities 3x3 Grid (dark band) ────────────────────────── */}
      <section
        id="capabilities"
        style={{
          position: "relative",
          zIndex: 1,
          maxWidth: "1200px",
          margin: "0 auto",
          padding: "72px clamp(28px, 6vw, 48px)",
          background: "#18180e",
          borderRadius: "18px",
          boxShadow: "0 10px 40px rgba(0,0,0,0.18)",
        }}
      >
        <div style={{ textAlign: "center", marginBottom: "44px" }}>
          <div className="capabilities-reveal-item" style={{ marginBottom: "10px" }}>
            <span
              style={{
                fontSize: "12px",
                fontWeight: "600",
                color: "#8cac28",
                letterSpacing: "0.06em",
                fontFamily: "var(--font-geist-sans)",
              }}
            >
              Why ELIO
            </span>
          </div>

          <h2
            className="capabilities-reveal-item"
            style={{
              textAlign: "center",
              fontSize: "clamp(1.75rem, 2.8vw, 2.4rem)",
              fontWeight: "700",
              color: "#f0efe8",
              letterSpacing: "-0.018em",
              margin: "0 auto",
              maxWidth: "440px",
              lineHeight: "1.2",
              fontFamily: "var(--font-geist-sans)",
            }}
          >
            Built for Catalog<br />Operations
          </h2>
        </div>

        {/* Capabilities: 9 separate dark rounded cards with gap */}
        <div
          className="capability-grid-container"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "12px",
            gridAutoFlow: "dense",
          }}
        >
          {capabilityItems.map((item, i) => {
            const Icon = item.icon;
            return (
            <div
              key={i}
              className="capability-item-card"
              style={{
                background: "rgba(255,255,255,0.045)",
                border: "1px solid rgba(255,255,255,0.09)",
                borderRadius: "12px",
                padding: "24px 20px",
                transition: "background 0.22s cubic-bezier(0.16, 1, 0.3, 1), transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.22s cubic-bezier(0.16, 1, 0.3, 1)",
                willChange: "transform",
              }}
              onMouseEnter={(e) => {
                const el = e.currentTarget as HTMLElement;
                el.style.background = "rgba(255,255,255,0.085)";
                el.style.transform = "translateY(-3px)";
                el.style.boxShadow = "0 8px 28px rgba(0,0,0,0.45)";
              }}
              onMouseLeave={(e) => {
                const el = e.currentTarget as HTMLElement;
                el.style.background = "rgba(255,255,255,0.045)";
                el.style.transform = "translateY(0)";
                el.style.boxShadow = "none";
              }}
            >
              {/* Solid yellow-green icon badge */}
              <div
                style={{
                  width: "34px",
                  height: "34px",
                  borderRadius: "50%",
                  background: "rgba(196,222,72,0.28)",
                  border: "1.5px solid rgba(170,205,50,0.5)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  marginBottom: "14px",
                  fontSize: "11px",
                  fontWeight: "700",
                  color: "#d9e98c",
                  fontFamily: "var(--font-geist-sans)",
                }}
              >
                <Icon size={17} strokeWidth={1.8} aria-hidden="true" />
              </div>
              <div
                style={{
                  fontSize: "13px",
                  fontWeight: "600",
                  color: "#f0efe8",
                  marginBottom: "6px",
                  fontFamily: "var(--font-geist-sans)",
                  lineHeight: "1.3",
                }}
              >
                {item.title}
              </div>
              <div
                style={{
                  fontSize: "12px",
                  color: "#b0b0a0",
                  lineHeight: "1.55",
                  fontFamily: "var(--font-geist-sans)",
                }}
              >
                {item.desc}
              </div>
            </div>
            );
          })}
        </div>
      </section>

      {/* ── Integrations & Extensibility ─────────────────────────────────── */}
      <section
        id="integrations"
        style={{
          position: "relative",
          zIndex: 1,
          maxWidth: "1200px",
          margin: "0 auto",
          padding: "72px clamp(28px, 6vw, 48px)",
        }}
      >
        <div style={{ textAlign: "center", marginBottom: "36px" }}>
          <div className="integrations-reveal-item" style={{ marginBottom: "10px" }}>
            <span
              style={{
                fontSize: "12px",
                fontWeight: "600",
                color: "#8cac28",
                letterSpacing: "0.06em",
                fontFamily: "var(--font-geist-sans)",
              }}
            >
              Plug &amp; Play
            </span>
          </div>

          <h2
            className="integrations-reveal-item"
            style={{
              textAlign: "center",
              fontSize: "clamp(1.75rem, 2.8vw, 2.4rem)",
              fontWeight: "700",
              color: "#18180e",
              letterSpacing: "-0.018em",
              margin: "0 auto 16px",
              maxWidth: "440px",
              lineHeight: "1.2",
              fontFamily: "var(--font-geist-sans)",
            }}
          >
            Data Sources &amp; Outputs
          </h2>

          <p
            className="integrations-reveal-item"
            style={{
              textAlign: "center",
              maxWidth: "380px",
              margin: "0 auto",
              fontSize: "14px",
              color: "#686858",
              lineHeight: "1.6",
              fontFamily: "var(--font-geist-sans)",
            }}
          >
            ELIO ingests standard catalog layouts and emits the 252-column delivery projection.
          </p>
        </div>

        {/* Integration Logo Strip */}
        <div
          className="integration-logos-strip"
          style={{
            display: "flex",
            justifyContent: "center",
            gap: "28px",
            alignItems: "center",
            marginBottom: "44px",
            flexWrap: "wrap",
          }}
        >
          {[
            { name: "E1 Brand", color: "#8cac28" },
            { name: "Unilog", color: "#a8c830" },
            { name: "DIB Brand", color: "#c8d84a" },
            { name: "CSV", color: "#8a8a70" },
            { name: "XLSX", color: "#686858" },
          ].map((brand) => (
            <div
              key={brand.name}
              className="integration-logo-badge"
              style={{
                display: "flex",
                alignItems: "center",
                gap: "6px",
                fontSize: "12.5px",
                fontWeight: "500",
                color: "#5a5a48",
                fontFamily: "var(--font-geist-sans)",
                opacity: 0.85,
              }}
            >
              <div
                style={{
                  width: "16px",
                  height: "16px",
                  borderRadius: "4px",
                  background: brand.color,
                  opacity: 0.8,
                  flexShrink: 0,
                }}
              />
              {brand.name}
            </div>
          ))}
        </div>

        {/* 2x2 Integrations Grid */}
        <div
          className="integration-grid-container"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "14px",
            gridAutoFlow: "dense",
          }}
        >
          {integrationCapabilities.map((cap, i) => {
            const Icon = cap.icon;
            return (
            <div
              key={i}
              className="integration-item-card"
              style={{
                background: "rgba(255,255,255,0.78)",
                border: "1px solid rgba(18,18,16,0.07)",
                borderRadius: "12px",
                padding: "22px",
                backdropFilter: "blur(8px)",
                boxShadow: "0 1px 8px rgba(0,0,0,0.04)",
                transition: "background 0.22s cubic-bezier(0.16, 1, 0.3, 1), transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.22s cubic-bezier(0.16, 1, 0.3, 1)",
                willChange: "transform",
              }}
              onMouseEnter={(e) => {
                const el = e.currentTarget as HTMLElement;
                el.style.background = "rgba(255,255,255,0.97)";
                el.style.transform = "translateY(-3px)";
                el.style.boxShadow = "0 8px 30px rgba(0,0,0,0.08)";
              }}
              onMouseLeave={(e) => {
                const el = e.currentTarget as HTMLElement;
                el.style.background = "rgba(255,255,255,0.78)";
                el.style.transform = "translateY(0)";
                el.style.boxShadow = "0 1px 8px rgba(0,0,0,0.04)";
              }}
            >
              <div
                style={{
                  width: "34px",
                  height: "34px",
                  borderRadius: "50%",
                  background: "rgba(196,222,72,0.28)",
                  border: "1.5px solid rgba(170,205,50,0.5)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  marginBottom: "12px",
                  fontSize: "11px",
                  fontWeight: "700",
                  color: "#d9e98c",
                  fontFamily: "var(--font-geist-sans)",
                }}
              >
                <Icon size={17} strokeWidth={1.8} aria-hidden="true" />
              </div>
              <div style={{ fontSize: "13.5px", fontWeight: "600", color: "#18180e", marginBottom: "6px", fontFamily: "var(--font-geist-sans)" }}>{cap.title}</div>
              <div style={{ fontSize: "12.5px", color: "#686858", lineHeight: "1.55", fontFamily: "var(--font-geist-sans)" }}>{cap.desc}</div>
            </div>
            );
          })}
        </div>
      </section>

      {/* ── CTA Section ──────────────────────────────────────────────────── */}
      <div id="get-started" aria-hidden style={{ position: "absolute", top: 0 }} />
      <section
        id="cta"
        style={{
          position: "relative",
          zIndex: 1,
          maxWidth: "1200px",
          margin: "0 auto 80px",
          padding: "0 clamp(28px, 6vw, 48px)",
        }}
      >
        <div
          className="cta-container-box"
          style={{
            background: "rgba(188,210,130,0.32)",
            border: "1px solid rgba(140,172,40,0.18)",
            borderRadius: "18px",
            padding: "56px 48px",
            textAlign: "center",
            backdropFilter: "blur(8px)",
            boxShadow: "0 10px 36px rgba(170,205,50,0.12)",
          }}
        >
          <h2
            style={{
              fontSize: "clamp(1.7rem, 2.8vw, 2.4rem)",
              fontWeight: "700",
              color: "#18180e",
              letterSpacing: "-0.018em",
              marginBottom: "10px",
              lineHeight: "1.2",
              fontFamily: "var(--font-geist-sans)",
            }}
          >
            See it in Action &amp; Run{" "}
            <em
              style={{
                fontStyle: "italic",
                fontWeight: "400",
                fontFamily: "Georgia, 'Times New Roman', serif",
              }}
            >
              Your Own Catalog
            </em>
          </h2>
          <p
            style={{
              fontSize: "13.5px",
              color: "#565644",
              maxWidth: "360px",
              margin: "0 auto 32px",
              lineHeight: "1.6",
              fontFamily: "var(--font-geist-sans)",
            }}
          >
            Upload a catalog and watch the pipeline trace every value to its source, or explore the demo dataset first.
          </p>
          <div style={{ display: "flex", gap: "10px", justifyContent: "center", flexWrap: "wrap" }}>
            <a
              href="/app/dashboard"
              style={{
                background: "#161612",
                color: "#f0efe8",
                border: "none",
                borderRadius: "999px",
                padding: "11px 26px",
                fontSize: "13.5px",
                fontWeight: "600",
                cursor: "pointer",
                fontFamily: "var(--font-geist-sans)",
                textDecoration: "none",
                display: "inline-block",
                transition: "transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s ease, box-shadow 0.2s ease",
              }}
              onMouseEnter={(e) => {
                const el = e.currentTarget as HTMLElement;
                el.style.background = "#282822";
                el.style.transform = "translateY(-2px) scale(1.02)";
                el.style.boxShadow = "0 6px 20px rgba(0,0,0,0.25)";
              }}
              onMouseLeave={(e) => {
                const el = e.currentTarget as HTMLElement;
                el.style.background = "#161612";
                el.style.transform = "translateY(0) scale(1)";
                el.style.boxShadow = "none";
              }}
            >
              Open the cockpit
            </a>
            <a
              href="/app/dashboard"
              style={{
                background: "rgba(255,255,255,0.72)",
                color: "#18180e",
                border: "1px solid rgba(24,24,14,0.14)",
                borderRadius: "999px",
                padding: "11px 26px",
                fontSize: "13.5px",
                fontWeight: "600",
                cursor: "pointer",
                fontFamily: "var(--font-geist-sans)",
                textDecoration: "none",
                display: "inline-block",
                transition: "transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), background 0.2s ease",
              }}
              onMouseEnter={(e) => {
                const el = e.currentTarget as HTMLElement;
                el.style.background = "#f0efe8";
                el.style.transform = "translateY(-2px) scale(1.02)";
              }}
              onMouseLeave={(e) => {
                const el = e.currentTarget as HTMLElement;
                el.style.background = "rgba(255,255,255,0.72)";
                el.style.transform = "translateY(0) scale(1)";
              }}
            >
              View pipeline
            </a>
          </div>
          <div style={{ marginTop: "16px" }}>
            <a
              href="/app/dashboard"
              style={{
                color: "#565644",
                fontSize: "12px",
                fontWeight: "500",
                fontFamily: "var(--font-geist-sans)",
                textDecoration: "underline",
                textUnderlineOffset: "3px",
                textDecorationColor: "rgba(86,86,68,0.35)",
                display: "inline-block",
                padding: "6px 10px",
                borderRadius: "999px",
                transition: "color 0.18s ease",
              }}
              onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.color = "#18180e"; }}
              onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.color = "#565644"; }}
            >
              Load demo catalog — no upload needed
            </a>
          </div>
        </div>
      </section>

      {/* ── Footer ───────────────────────────────────────────────────────── */}
      <footer
        style={{
          position: "relative",
          zIndex: 1,
          maxWidth: "1200px",
          margin: "0 auto",
          padding: "36px 48px 56px",
          borderTop: "1px solid rgba(18,18,16,0.09)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "16px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "9px" }}>
            <div
              style={{
                width: "26px",
                height: "26px",
                borderRadius: "50%",
                background: "linear-gradient(135deg, #c8d84a, #a8c830)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none">
                <path d="M3 12L10 5L17 12L10 19L3 12Z" fill="#1a1a0e" />
              </svg>
            </div>
            <span style={{ fontSize: "12.5px", color: "#686858", fontFamily: "var(--font-geist-sans)" }}>
              Evidence-gated catalog intelligence
            </span>
          </div>
        </div>
      </footer>
    </main>
  );
}

// ── Sub-components ──────────────────────────────────────────────────────────
function BentoCard({ mockup, title, desc }: { mockup: React.ReactNode; title: string; desc: string }) {
  return (
    <div
      className="bento-card-item"
      style={{
        background: "rgba(255,255,255,0.82)",
        border: "1px solid rgba(18,18,16,0.07)",
        borderRadius: "14px",
        overflow: "hidden",
        backdropFilter: "blur(10px)",
        boxShadow: "0 2px 12px rgba(0,0,0,0.035)",
        transition: "transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.22s cubic-bezier(0.16, 1, 0.3, 1)",
        willChange: "transform",
      }}
      onMouseEnter={(e) => {
        const el = e.currentTarget as HTMLElement;
        el.style.transform = "translateY(-4px)";
        el.style.boxShadow = "0 12px 36px rgba(0,0,0,0.09)";
      }}
      onMouseLeave={(e) => {
        const el = e.currentTarget as HTMLElement;
        el.style.transform = "translateY(0)";
        el.style.boxShadow = "0 2px 12px rgba(0,0,0,0.035)";
      }}
    >
      {/* Mockup area */}
      <div
        style={{
          height: "195px",
          background: "rgba(242,241,235,0.55)",
          borderBottom: "1px solid rgba(18,18,16,0.05)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "14px",
          overflow: "hidden",
        }}
      >
        {mockup}
      </div>
      {/* Card Content */}
      <div style={{ padding: "22px" }}>
        <div style={{ fontSize: "14px", fontWeight: "600", color: "#18180e", marginBottom: "7px", fontFamily: "var(--font-geist-sans)" }}>{title}</div>
        <div style={{ fontSize: "12.5px", color: "#686858", lineHeight: "1.6", fontFamily: "var(--font-geist-sans)" }}>{desc}</div>
      </div>
    </div>
  );
}

// ── Mockup Components ──────────────────────────────────────────────────────
function OverviewMockup() {
  return (
    <div style={{ width: "100%", maxWidth: "272px" }}>
      <div style={{ background: "white", borderRadius: "9px", padding: "11px", border: "1px solid rgba(0,0,0,0.05)", boxShadow: "0 2px 8px rgba(0,0,0,0.05)" }}>
        {[
          { label: "Attributes / Row", val: "50.0", change: "exact", pos: true },
          { label: "Supported", val: "106 / 2500", change: "2394 abstained", pos: false },
          { label: "Abstention", val: "2394", change: "with reasons", pos: true },
        ].map((row, i) => (
          <div key={i} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "7px 0", borderBottom: i < 2 ? "1px solid rgba(0,0,0,0.04)" : "none" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "7px" }}>
              <div style={{ width: "13px", height: "13px", borderRadius: "50%", background: "rgba(140,172,40,0.14)", border: "1px solid rgba(140,172,40,0.28)" }} />
              <span style={{ fontSize: "10.5px", color: "#5c5c48", fontFamily: "var(--font-geist-sans)" }}>{row.label}</span>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "7px" }}>
              <span style={{ fontSize: "11.5px", fontWeight: "600", color: "#18180e", fontFamily: "var(--font-geist-sans)" }}>{row.val}</span>
              <span style={{ fontSize: "9.5px", fontWeight: "500", color: row.pos ? "#00e5d8" : "#fbbf24", background: row.pos ? "rgba(0,229,216,0.1)" : "rgba(251,191,36,0.12)", padding: "1px 5px", borderRadius: "4px" }}>{row.change}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function PipelineMockup() {
  const stages = ["S1", "S2", "S3", "S4", "S5", "S6", "S7"];
  const heights = [52, 38, 62, 48, 88, 43, 58];
  return (
    <div style={{ width: "100%", maxWidth: "272px" }}>
      <div style={{ background: "white", borderRadius: "9px", padding: "12px 11px 8px", border: "1px solid rgba(0,0,0,0.05)", boxShadow: "0 2px 8px rgba(0,0,0,0.05)" }}>
        <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: "10px" }}>
          <div>
            <span style={{ fontSize: "17px", fontWeight: "700", color: "#18180e", fontFamily: "var(--font-geist-sans)" }}>50 rows</span>
            <span style={{ fontSize: "9.5px", color: "#8a8a70", marginLeft: "3px", fontFamily: "var(--font-geist-sans)" }}>demo</span>
          </div>
          <span style={{ fontSize: "9.5px", color: "#00e5d8", fontWeight: "600", background: "rgba(0,229,216,0.1)", padding: "2px 6px", borderRadius: "4px" }}>deterministic DAG</span>
        </div>
        <div style={{ display: "flex", alignItems: "flex-end", gap: "5px", height: "66px" }}>
          {stages.map((stage, i) => (
            <div key={stage} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: "3px" }}>
              <div
                style={{
                  width: "100%",
                  height: `${heights[i]}%`,
                  background: stage === "S7" ? "#f59e0b" : "rgba(0,0,0,0.08)",
                  borderRadius: "3px 3px 0 0",
                  position: "relative",
                  transition: "height 0.4s ease",
                }}
              >
                {stage === "S7" && (
                  <div style={{ position: "absolute", top: "-16px", left: "50%", transform: "translateX(-50%)", background: "#161612", color: "white", fontSize: "10px", padding: "2px 6px", borderRadius: "3px", whiteSpace: "nowrap", fontFamily: "var(--font-geist-sans)" }}>escalated</div>
                )}
              </div>
              <span style={{ fontSize: "10px", color: "#8a8a70", fontFamily: "var(--font-geist-sans)" }}>{stage}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function EvidenceMockup() {
  return (
    <div style={{ width: "100%", maxWidth: "272px" }}>
      <div style={{ background: "white", borderRadius: "9px", padding: "11px", border: "1px solid rgba(0,0,0,0.05)", boxShadow: "0 2px 8px rgba(0,0,0,0.05)" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "9px" }}>
          <span style={{ fontSize: "10.5px", fontWeight: "600", color: "#18180e", fontFamily: "var(--font-geist-sans)" }}>Evidence Chain</span>
          <div style={{ width: "22px", height: "22px", borderRadius: "50%", background: "rgba(140,172,40,0.14)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "9.5px" }}>🔗</div>
        </div>
        {[
          { name: "PDSH4816AF / Series", amount: "p.1 · span 640", red: false },
          { name: "Brand → manufacturer doc", amount: "verification", red: false },
          { name: "Unsupported category", amount: "abstained", red: true },
        ].map((item, i) => (
          <div key={i} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "6px 0", borderBottom: i < 2 ? "1px solid rgba(0,0,0,0.04)" : "none" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "7px" }}>
              <div style={{ width: "20px", height: "20px", borderRadius: "50%", background: "rgba(140,172,40,0.12)", flexShrink: 0 }} />
              <span style={{ fontSize: "10px", color: "#18180e", fontFamily: "var(--font-geist-sans)", fontWeight: "500" }}>{item.name}</span>
            </div>
            <span style={{ fontSize: "10.5px", fontWeight: "600", color: item.red ? "#fbbf24" : "#00e5d8", fontFamily: "var(--font-geist-sans)" }}>{item.amount}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function IntegrationsMockup() {
  return (
    <div style={{ width: "100%", maxWidth: "272px" }}>
      <div style={{ background: "white", borderRadius: "9px", padding: "11px", border: "1px solid rgba(0,0,0,0.05)", boxShadow: "0 2px 8px rgba(0,0,0,0.05)" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "9px" }}>
          <span style={{ fontSize: "10.5px", fontWeight: "600", color: "#18180e", fontFamily: "var(--font-geist-sans)" }}>Catalog Inputs</span>
          <span style={{ fontSize: "8.5px", background: "#c8d84a", color: "#161612", padding: "2px 7px", borderRadius: "999px", fontWeight: "600", fontFamily: "var(--font-geist-sans)" }}>6 required</span>
        </div>
        {[
          { name: "Mfg_Part_Num", bank: "input column", bal: "✓" },
          { name: "E1_Brand", bank: "input column", bal: "✓" },
        ].map((item, i) => (
          <div key={i} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "7px 0", borderBottom: i < 1 ? "1px solid rgba(0,0,0,0.04)" : "none" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "7px" }}>
              <div style={{ width: "22px", height: "22px", borderRadius: "5px", background: "rgba(140,172,40,0.14)", flexShrink: 0 }} />
              <div>
                <div style={{ fontSize: "10.5px", fontWeight: "500", color: "#18180e", fontFamily: "var(--font-geist-sans)" }}>{item.name}</div>
                <div style={{ fontSize: "9px", color: "#8a8a70", fontFamily: "var(--font-geist-sans)" }}>{item.bank}</div>
              </div>
            </div>
            <span style={{ fontSize: "11px", fontWeight: "600", color: "#18180e", fontFamily: "var(--font-geist-sans)" }}>{item.bal}</span>
          </div>
        ))}
        <div style={{ display: "flex", justifyContent: "space-between", marginTop: "8px", paddingTop: "8px", borderTop: "1px solid rgba(0,0,0,0.04)" }}>
          {[{ label: "MPN", val: "✓" }, { label: "Desc", val: "✓" }, { label: "Manuf", val: "✓" }].map((stat) => (
            <div key={stat.label} style={{ textAlign: "center" }}>
              <div style={{ fontSize: "8.5px", color: "#8a8a70", fontFamily: "var(--font-geist-sans)" }}>{stat.label}</div>
              <div style={{ fontSize: "10px", fontWeight: "600", color: "#18180e", fontFamily: "var(--font-geist-sans)" }}>{stat.val}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
