# Submission Logistics — UniHack (Unilog × Hack2Skill)

**Ticket:** wayfinder #2 — "Submission logistics"
**Date of research:** 2026-08-20
**Status:** VERIFIED — competition identified; most logistics confirmed from primary sources; a few items UNKNOWN (marked below).

---

## 1. Competition identity

This is **NOT** the Australian UNIHACK (unihack.net, Monash, "The Imagination Hackathon") nor Sri Lanka's Cardano UniHack, nor UniHack Europe. It is:

- **Official name:** UniHack — "AI-Powered Product Intelligence for Industrial Commerce" (Unilog's AI innovation hackathon)
- **Organizer:** **Unilog** (Unilog Content Services, unilogcorp.com — AI-powered content & commerce solutions for industrial businesses), run on the **Hack2Skill** platform
- **Official event page (rules/source of truth):** https://hack2skill.com/event/unilog2026
- **Short link used in promo:** https://rebrand.ly/unilog
- **Eligibility:** undergraduate engineering students at recognized colleges/universities across India; teams of 1–4; free
- **Prizes:** ₹5,00,000 pool — Winner ₹2,00,000 / 1st RU ₹1,50,000 / 2nd RU ₹1,00,000 / two Special Awards ₹25,000 each; winners may be considered for internships/PPOs/full-time at Unilog
- **IP clause:** "Ownership of the IP rights for winning solutions will be transferred to the program organizers upon confirmation of the award." (published on the event page)
- **Contact:** support+unihack@hack2skill.com (event support); support@hack2skill.com (platform)
- **Challenge statement (from event page + launch post):** turn minimal product info (manufacturer part number, brand, one line of description) into rich, structured, commerce-ready product intelligence. Tracks: AI Powered Product Intelligence / Industrial Commerce / Generative AI. No prescribed implementation ("Whatever architecture you can defend" — AI agents, RAG, knowledge graphs, VLM, confidence scoring...)

The dataset this team uses ("Unihack_ Sample Dataset - Input.csv") is the official sample input; the sanctioned evidence source is the reference workbook ("Unihack_ Expected Output - Delivery Format.csv", the 252-column Unilog delivery format).

---

## 2. Sources

Primary (official):
- Event page: https://hack2skill.com/event/unilog2026 — full text (About, Who Can Participate, Challenge Statement, Journey, FAQs, prizes, IP note, "Last Date to Register: Sun 23 Aug 2026")
- Unilog homepage: https://www.unilogcorp.com (organizer identity; referenced on event page)

Corroborating listings (same data, independent):
- https://hiretoday.in/competitiondetails/40000127 — Registration opens Jul 29, closes **Aug 23, 2026**; event ends Sep 4, 2026; judging criteria; allowed tools; contact
- https://www.campulsy.in/opportunities/fe329161-72e1-4b95-8fc2-22b1b42ace29 — "Register on the Hack2Skill platform before 23 August 2026 … Submit your prototype through the hackathon portal before the submission deadline"
- https://www.instagram.com/p/DbXrNOjAUZy/ (hack2skill, 2026-07-29) — launch post: "Registrations & submissions: 29 July – 23 August", open to India engineering students
- https://www.instagram.com/p/DbsnBBsmP4j/ (hack2skill) — Introductory & Problem Statement Explainer Session, 7 Aug 2026, 4:00 PM IST, with Unilog VPs (Shaji Jose V — VP Product Engineering; Ramachandra Raje Urs — VP Content Services)

Behavioral evidence (other teams' public submissions — for data-practice section only, not official rules):
- https://github.com/sustik78/Unihack_Hackathon (contains both CSVs + "[EXT] UniHack-Protoype Template .pptx" + demo video)
- https://github.com/vishwabhishek/UniHack
- https://github.com/dev-1067/UNI-Hack (contains "Unihack_ Expected Output - Delivery Format.csv")
- https://github.com/suryaprakashsiddina/unihack-product-intelligence

Searches performed: "UniHack 2026 hackathon", "UniHack catalog", "UniHack data hackathon submission", "Unihack_ Sample Dataset", "Unilog UniHack challenge submission deadline 2026", "unilog unihack hack2skill solution guide / delivery format / github / prototype", "UniHack unilog prototype template / solution guide / demo video".

---

## 3. Deadline — CONFIRMED: 23 August 2026

- Event page: "Last Date to Register: **Sun 23 Aug 2026**"; journey shows **Registrations Open: 29 Jul – 23 Aug 2026** AND **Prototype Submission: 29 Jul – 23 Aug 2026** (same window — register and submit through the portal).
- HireToday: Registration closes **Aug 23, 2026**.
- Campulsy: register before **23 August 2026**; submit prototype before the submission deadline.
- Hack2Skill Instagram (launch post): "Registrations & submissions: **29 July – 23 August**".

The assumed deadline (Aug 23 2026) is **CONFIRMED**, with an important nuance: **registration also closes on Aug 23** — registration and submission share the same end date, so a team must be registered on the Hack2Skill portal before Aug 23, 2026 or its submission won't count.

Post-submission timeline (event page): Evaluations 24 Aug – 1 Sep 2026; Finale / winners announced 4 Sep 2026.

---

## 4. Submission format

Verified from the event page:
- **Portal:** submission is made **through the Hack2Skill hackathon portal** (hack2skill.com/event/unilog2026 → registered teams' dashboard). Campulsy: "Submit your prototype through the hackathon portal before the submission deadline."
- **What must be built:** an "AI-powered MVP or POC addressing the challenge statement" (prototype), using the recommended stack (AI/ML, GenAI, Python, LLMs, NLP, cloud, APIs, etc.).
- **Resources on the portal:** "**Solution Guide is now live on your dashboard!** Head to the **Resources** section to access it." → the official solution guide (and any templates, incl. the "[EXT] UniHack-Prototype Template.pptx" seen in a competitor's repo) lives **behind the registration wall** — not publicly crawlable.
- **Expected deliverable format:** input CSV (6 columns) → enriched output in the "Unihack_ Expected Output - Delivery Format.csv" / 252-column Unilog delivery format (per the reference workbook and every competitor repo; this is also what the organizers' "values are already represented within the columns of the provided datasets" note implies).
- There is also an **Introductory & Problem Statement Explainer Session** (7 Aug 2026, 4:00 PM IST) — presumably recorded/replayable on the portal.

**UNKNOWN / not published publicly:**
- Whether the portal submission requires a **GitHub repo link, demo video, or written report**. The public event page names none of these — it only says "submit your prototype through the hackathon portal." (Contrast: other Hack2Skill events, e.g. BRINHACK, explicitly require GitHub repo + demo video; UniHack's public page does not.) The solution guide (portal Resources) almost certainly specifies the exact deliverable checklist — that is the authoritative source once a team is registered.
- Whether a live demo is required at evaluation (finale is virtual; no demo-day requirement published).
- A Facebook repost (aamir.hussainji.1) claims an early round used "PDF via Google Form, no coding required" — this contradicts the official journey (prototype submission via portal) and is treated as NOT authoritative / likely about a different Unilog initiative or stale content.

**Operational recommendation:** have the repo public, a short demo video, and a README ready anyway — the official page doesn't forbid them, and other Hack2Skill events' norms suggest they may be requested in the portal's submission form. Confirm via the portal's "Solution Guide" / Resources section immediately after registering.

---

## 5. Data rules

**No official public rule found** on whether the provided dataset (or the reference workbook) may be committed to a public GitHub repo. Specifically:

- The event page, FAQ, and listing pages publish **no data-usage or confidentiality terms** for the sample dataset / reference workbook.
- The platform's "Initiative Terms & Conditions" link exists on the event page (footer) but its contents were not crawlable → UNKNOWN.
- The IP clause published applies only to **winning solutions** ("IP rights for winning solutions will be transferred to the program organizers upon confirmation of the award") — it says nothing about datasets.
- **Behavioral evidence:** at least four competing teams have already committed BOTH the input CSV and the expected-output/delivery-format workbook to **public** GitHub repos (sustik78/Unihack_Hackathon, vishwabhishek/UniHack, dev-1067/UNI-Hack, suryaprakashsiddina/unihack-product-intelligence) with no visible takedown — indicating the organizers have not objected to public hosting of the sample files.
- Organizer communication (per team context): "values are already represented within the columns of the provided datasets" — consistent with the workbook being derivable from the provided columns, i.e., the data is provided for contestants to work with.

**Verdict:** publicly committing the provided sample dataset and reference workbook appears to be tolerated in practice and is not prohibited by anything published; the only way to fully close this is the portal's Terms & Conditions / Solution Guide (registration-gated). Prudent default: keep the raw input CSV out of the repo or commit it (other teams did); the team's existing practice (using the workbook as a dev-time evidence source, not shipping it as an artifact) is safe either way.

---

## 6. Judging criteria

Published (event page + listings), no weights or detailed rubric:
- Event page journey: "evaluated based on **innovation, technical implementation, business relevance, and overall impact**"
- Event page FAQ #6: "**innovation, technical implementation, business relevance, scalability, and overall impact**"
- HireToday: Innovation / Technical Implementation / Business Relevance / Overall Impact

No scoring weights, rubric, or panel list published publicly (finale judging panel TBA). The 7 Aug explainer session is the venue where organizers described "exactly what it takes to stand out."

---

## 7. Unknowns (explicitly)

1. **Exact portal submission fields** (repo link? video? report?) — the public event page doesn't say; authoritative answer is the registration-gated "Solution Guide" in the portal's Resources section.
2. **Initiative Terms & Conditions content** (hack2skill footer) — includes the definitive data-usage and IP terms; not crawlable.
3. **Whether a demo video / live demo is required** — not stated publicly.
4. **Detailed judging rubric/weights and judge identities** — not published.
5. **Exact submission cutoff time on Aug 23, 2026** (e.g., 11:59 PM IST?) — not published.
6. **Whether the deadline may be extended** — no extension published as of research date.