# health.louka.cc v1 — Design Spec

**Date:** 2026-05-13
**Status:** Brainstorm complete; ready for implementation planning
**Scope:** Visual prototype with hardcoded mock data
**Owner:** Mario Louka

---

## Context

Mario currently has two GitHub repos for what should be one project (`mlouka/health` parent + `mlouka/spine` deploy) and a working SvelteKit app at `spine.louka.cc` that includes a 3D CBCT spine viewer, two chiropractic intake forms (`/ucspinecare`, `/rickards`), a Convex-backed visits log, and a rich static MRI summary at `/mri`. The current organization served when the project was a single 3D experiment but does not scale to the broader vision: shoulder MRI, chest MRI, X-rays, blood work, written reports, and eventually appointments — all curated by Mario, all private by default, with selective public sharing per item.

The desired end state is a single repo (`mlouka/health`) and a single primary deployment (`health.louka.cc`) that holds *everything*. The existing spine app remains as a legacy specialty tool at `spine.louka.cc` (kept alive for now), with its source folded into the unified repo. This document defines **v1** — a polished visual prototype that establishes the shape, with real data wiring deferred to v2.

---

## Goals

1. **Truly distinctive visual design** — not a Sharp HealthCare clone, not a generic shadcn template. Produce a feel that signals "this is mine, curated by me, for the long term."
2. **Three-section architecture** organized by record type: Imaging, Results, Reports — with Appointments as a fourth surface for upcoming care events.
3. **Private by default, per-page public toggle** with `noindex` everywhere — even on "public" share URLs.
4. **Forward-aware**: every component decision in v1 should make the v2 features (real auth, real Convex data, share toggles wired, DICOM viewer integration, AI-parsed appointment ingestion) drop-in additions, not retrofits.
5. **Migrate the existing cervical MRI document** into the new shell as the canonical example of a rich report page.

## Non-goals (deferred to v2+)

- Real authentication
- Convex data wiring (everything is hardcoded mock data in v1)
- Functional share toggles (visual only in v1)
- Access logging
- DICOM viewer integration
- AI appointment-parsing pipeline
- Migration of the chiro visit log out of spine.louka.cc
- Real lab/blood data import

---

## Top-level architecture

```
health.louka.cc/
│
├── /                          ← Home dashboard
├── /imaging                   ← Raw imaging studies (MRIs, X-rays, CTs)
│   └── /imaging/[slug]            single study + future DICOM viewer
├── /results                   ← Blood work, labs (numerical, empty in v1)
│   └── /results/[slug]            single panel with reference ranges
├── /reports                   ← Written interpretations + the rich MRI doc
│   └── /reports/[slug]            long-form document with sticky chrome
├── /appointments              ← Upcoming + past appointments
│   └── /appointments/[slug]       single appointment detail
└── /menu                      ← Settings, share-link manager, sign out
```

### Why this partition

Every encounter with the healthcare system produces exactly one of these three artifact types: a scan (Imaging), a number (Results), or a written interpretation (Reports). Appointments is the fourth surface because it is fundamentally different — it is about *future* care events, not the records produced by past ones. Mixing record types under one umbrella confuses people because the *affordances* needed differ: imaging is visual + scrollable, results are numeric + trend-able, reports are narrative + figure-laden, appointments are time-bound + actionable.

### What does not get a top-level slot in v1

- ❌ Visits / clinic intake forms — stays in spine.louka.cc
- ❌ Medications — Mario won't track these here
- ❌ Body region as nav (e.g., Spine, Shoulder) — region becomes a *tag* on records rather than a top-level
- ❌ Notes — could nest inside a report if needed; not its own section
- ❌ Messages / alerts — no notification source

---

## Home dashboard

A single scrollable column on mobile, broader layout on desktop. From top to bottom:

1. **Header** (sticky): avatar (`M`) + "Mario ▾" dropdown + a subtle `🔒 Private` indicator on the right
2. **Current focus card**: surfaces the most relevant thing right now. v1 hardcodes this to the cervical MRI finding. Future: auto-computed (latest unread imaging, flagged item, or manual pin).
3. **Upcoming card**: next appointment if any. v1 hardcodes one mock appointment.
4. **Section tiles**: four tiles for Imaging / Results / Reports / Appointments. Each shows section name, count or status text ("1 study", "none yet", "1 doc", "1 upcoming"), and tap into the section.
5. **Recent activity feed**: chronological list of recent additions/edits to the archive ("Cervical MRI report updated · 2h ago", "Cervical MRI report created · 7d ago"). v1 shows 3 hardcoded mock entries.
6. **Bottom nav (mobile only)**: Home / Search / Menu — three items. Search is a placeholder; eventually a global search across all records.

### Why a "Current focus" card replaces Sharp's Alerts+Appointments hero

Sharp's hero area is reactive (provider pushed something). Mario's hero is curatorial — the *one* item that should be top of mind in his archive right now. Having one clearly-prioritized item at the top of home gives the dashboard a sense of "what's happening" rather than feeling like a static index. In v1 it is hardcoded; in v2 it can auto-compute or accept a manual pin.

---

## Section pages

### `/imaging`, `/results`, `/reports`, `/appointments`

Each section page shows a list of records as cards. Each card displays:

- Title (e.g., "Cervical Spine MRI")
- Date / scheduled time
- Tag chips (body region, modality, severity, etc.)
- One-line preview (primary finding, key result, abstract, location)
- Privacy indicator (lock if private, world icon if public)

Cards are tappable → go to the detail page. Filter chips at the top (by region, by modality, etc.) for sections with multiple records. Empty state ("No imaging yet — your records will appear here when added") for sections with no records (Results in v1).

### `/imaging/[slug]` — Single imaging study detail page (v1)

Mock content for the cervical MRI:

- Header bar (sticky): `< Imaging` breadcrumb, share toggle, access log indicator
- Metadata block: Date, Modality, Body region tag, Procedure, Institution, Referring
- "View report" CTA linking to the corresponding `/reports/cervical-mri` doc
- Placeholder section: "DICOM viewer (v2)" — empty box with a "Coming in v2" label

The DICOM viewer is **not** built in v1; the page just demonstrates where it will live.

### `/reports/[slug]` — The rich report page (the most important screen)

This is where the existing `/mri` document moves. The whole document content (Clinical summary → Radiologist's report → Report interpretation with the SVG cervical map + axial cross-section + dermatome figures → Key imaging with 3 JPEGs → Clinical presentation → Assessment and treatment plan → Consultation questions) carries over verbatim into the new shell.

**Persistent navigation chrome**:

- **Sticky top bar**: `< Reports` breadcrumb on the left, share toggle on the right, access log indicator (`0 views since publish` when public, hidden when private)
- **Sticky right rail (desktop ≥ 1024px)**: anchor-link table of contents for each report section. Click jumps to that section.
- **Floating "Jump to..." button (mobile)**: same anchor-link navigation, opens as a bottom sheet

**Layout**: one continuous scroll, figures inline. No tabs. The reader sees the report top to bottom or jumps via section nav. This preserves the document feel Mario likes while making navigation between report content, embedded figures, and other parts of the app one click each.

**Future**: a DICOM viewer or 3D Threlte component slots in as another inline section (e.g., between "Report interpretation" and "Key imaging") without restructuring the layout.

### `/results/[slug]` — Blood work record (placeholder in v1)

Schema-friendly but visually empty in v1. Will eventually show:

- Test panel name + date
- Result table with reference ranges and color-coded indicators (within/outside range)
- Trend line over time if the panel has prior runs

### `/appointments/[slug]` — Single appointment detail

Shows: provider, date/time, location, type (in-person / virtual), notes, source (which email/text this came from, when AI parsing is built). v1 has two mock entries (e.g., Dr. Park spine consult, follow-up imaging). Includes "Add to calendar" CTA (mock) that will later produce a real `.ics` file.

---

## Share + access model

- **Clean canonical URLs everywhere**. No `/share/random-token-XYZ`. Each record lives at a stable URL like `/reports/cervical-mri`.
- **Per-page `is_public` toggle** visible only to admin. Default: `false` (auth required).
- **`noindex, nofollow` headers on every route regardless of public/private state**, plus `robots.txt` blocking all paths. Mario's records never appear in Google.
- **Access tracking** (v2): when a public page is viewed, log timestamp + browser + referrer + IP hash. Show the count + last few accesses inline on the page when admin views it.
- **Revoke = toggle back to private**. Cuts off all recipients simultaneously (acceptable trade-off given low share volume).
- **v1 visual treatment only**: the toggle is rendered, the access log indicator is rendered with mock data ("0 views"), but the underlying state is not actually wired.

---

## Visual design direction (handed off to frontend-design)

The visual treatment is intentionally *not* specified in this spec — that work is owned by the `frontend-design` skill in a separate phase. Constraints handed forward:

- **Aesthetic intent**: distinctive, considered, calm, signals "long-term personal archive" rather than "busy consumer app." Sharp HealthCare was an information-architecture reference, not a visual style reference. Do not copy Sharp.
- **Type**: serif headings (likely Fraunces, matching the existing MRI doc's editorial feel) + sans body (Inter)
- **Color**: warm cream/ink palette with one accent (rust/clay tone, matching the existing MRI doc) — do *not* default to medical-blue clinical-app palette
- **Density**: airy, not dense. Reading the report should feel like reading a thoughtful document, not parsing a hospital portal
- **Component library**: shadcn-svelte primitives, custom-themed via Tailwind v4 tokens — not raw shadcn defaults
- **Motion**: subtle, purposeful — no animation-for-animation's-sake
- **Accessibility**: WCAG 2.2 AA baseline, keyboard navigation, screen reader pass

The `frontend-design` skill will produce the actual visual treatment in a follow-up phase.

---

## Tech stack

| Concern | Choice |
|-|-|
| Framework | SvelteKit v2 + Svelte 5 (runes) |
| Styling | Tailwind v4 |
| Component library | shadcn-svelte |
| Backend | Convex (deferred to v2 — v1 uses hardcoded data) |
| 3D / image | Threlte (existing) for future 3D viewer integration; Cornerstone3D for future DICOM |
| Deploy | Vercel project `health`, deploys `app/` subdirectory of `mlouka/health` |
| Domain | `health.louka.cc` (new), `spine.louka.cc` (legacy, separate Vercel project) |

---

## Repo and file structure

```
work/health/                              (= mlouka/health repo root, single .git here)
├── app/                                  ← SvelteKit app, deploys to health.louka.cc
│   ├── src/routes/
│   │   ├── +page.svelte                       Home dashboard
│   │   ├── imaging/
│   │   │   ├── +page.svelte                   list page
│   │   │   └── [slug]/+page.svelte            detail page
│   │   ├── results/
│   │   │   ├── +page.svelte
│   │   │   └── [slug]/+page.svelte
│   │   ├── reports/
│   │   │   ├── +page.svelte
│   │   │   └── [slug]/+page.svelte            the rich long-form page
│   │   ├── appointments/
│   │   │   ├── +page.svelte
│   │   │   └── [slug]/+page.svelte
│   │   ├── menu/+page.svelte
│   │   └── +layout.svelte                     persistent header + nav
│   ├── src/lib/
│   │   ├── components/                        UI components (shadcn-svelte + custom)
│   │   ├── mock-data/                         hardcoded v1 mock data
│   │   │   ├── imaging.ts
│   │   │   ├── results.ts
│   │   │   ├── reports.ts
│   │   │   └── appointments.ts
│   │   └── stores/
│   ├── static/
│   │   └── robots.txt                         disallow: /
│   └── package.json
│
├── legacy/
│   └── spine-app/                        ← migrated source from old mlouka/spine repo
│                                            (deploys separately to spine.louka.cc)
│
├── records/                              ← gitignored: original PDFs, DICOM, etc.
├── reference/                            ← existing notes, PDFs
├── docs/
│   └── superpowers/specs/                ← this document and future specs
└── README.md, CLAUDE.md, .gitignore
```

The repo consolidation (moving `spine/app/` up to root `app/` and folding `mlouka/spine` into the unified repo) is part of v1's implementation work but is invisible to the user — it happens in git plumbing, not in the app surface.

---

## Agent assignments and workflow

This build pulls in multiple specialized agents and skills. The order is roughly: plan → design → implement → review.

### Planning & coordination

- **`technical-project-manager` agent** — owns the project breakdown. Translates this spec into a sequenced list of stories with clear acceptance criteria. Coordinates handoffs between design and implementation agents. Reports progress.
- **`tdd-workflows:tdd-orchestrator` agent** — enforces test-first discipline across the implementation phase. Every story that has business logic (data shaping, share-toggle state, search filtering) starts with failing tests via `tdd-workflows:tdd-red`, gets minimal implementation via `tdd-workflows:tdd-green`, then refactors with safety. For pure layout/visual work, TDD is relaxed but accessibility tests still run.

### Design

- **`frontend-design:frontend-design` skill** — produces the distinctive visual treatment for each screen (home, list pages, detail pages, report page). Generates polished code that avoids generic AI aesthetics. Works from this spec's "Visual design direction" constraints.
- **`svelte-ui-designer` agent** — owns visual design within the SvelteKit context: color tokens, typography scale, spacing system, design tokens, shadcn-svelte theme configuration. Establishes the design system foundation that all components inherit.
- **`svelte-ux-designer` agent** — owns interaction design: Svelte transitions between routes, micro-interactions on the share toggle, animation of the "Jump to..." floating menu on mobile, touch behavior on cards, scroll-driven reveal of report sections.
- **`ui-design:design-system-setup` skill** — initializes the shadcn-svelte token system at the start of implementation.

### Implementation

- **`svelte-engineer` agent** — primary implementer. Builds components, pages, layouts. Knows the SvelteKit + shadcn-svelte + Tailwind v4 patterns. Implements the route structure, mock-data stores, share-toggle UI (visual only), accessibility primitives.
- **`convex-engineer` agent** — designs the v2 Convex schema (`imaging_studies`, `lab_results`, `reports`, `appointments`, `body_regions`, `share_links`, `access_log`) as a forward-looking artifact, even though wiring is deferred to v2. Produces a stub `schema.ts` in `app/convex/` so the v1 prototype can demonstrate the data shape without queries.

### Review

- **`svelte-reviewer` agent** — reviews implementation for SvelteKit patterns, component architecture, shadcn-svelte usage, mobile responsiveness, design system compliance.
- **`accessibility-compliance:wcag-audit-patterns` skill** — WCAG 2.2 audit after each major surface lands.
- **`web-design-guidelines` skill** — final UI quality check before declaring v1 complete.

### Documentation

- **`gsd-docs-update` skill** — updates README.md and CLAUDE.md after v1 ships to reflect the new structure.

---

## Migration: from current state to v1

The implementation will need to handle repo consolidation as part of the work. Order:

1. **Repo consolidation** (no app change yet) — subtree-merge `mlouka/spine` into `mlouka/health` as `app/`. Move `spine/legacy/` contents up to root `legacy/`. Move `spine/reference/` up to `reference/`. Delete the now-empty `spine/` wrapper.
2. **Existing spine app source migration** — under `legacy/spine-app/`, keep the old SvelteKit project that still deploys to `spine.louka.cc`. Don't break it.
3. **New `app/` scaffold** — create the v1 prototype shell as the *new* SvelteKit project at `app/`. This is a fresh build, not a refactor of the legacy app.
4. **Cervical MRI doc migration** — copy `legacy/spine-app/static/mri/index.html` content into `app/src/routes/reports/cervical-mri/+page.svelte` as Svelte markup wrapped in the new shell. Inline SVG figures port over directly.
5. **Vercel project setup** — new project `health`, Root Directory `app/`, domain `health.louka.cc`. The existing `spine.louka.cc` Vercel project stays untouched.
6. **DNS** — `health.louka.cc` points to the new Vercel project. `spine.louka.cc` stays pointed at the old project.

---

## Verification

After v1 deploys:

- `curl https://health.louka.cc/` returns the home dashboard HTML containing the current-focus card, upcoming appointment card, 4 section tiles, and activity feed
- All 4 section pages return 200 and render their respective list cards (or empty state for Results)
- `/reports/cervical-mri` renders the full cervical MRI document with sticky chrome and section anchor nav
- `/imaging/cervical-mri-2026-05-06` renders the imaging detail page with the DICOM viewer placeholder
- Every page has `<meta name="robots" content="noindex, nofollow">` and `robots.txt` returns `Disallow: /`
- Bottom nav (mobile) has Home / Search / Menu
- All routes are accessible at mock data; no broken images
- Visual: matches the design language produced by `frontend-design` (subjective but checkable against the captured design artifacts)
- Accessibility: passes `wcag-audit-patterns` automated checks; manual keyboard navigation works end to end
- `spine.louka.cc` is unaffected throughout — continues to deploy from its independent Vercel project

---

## Known unknowns

- **Auth provider choice for v2** (Convex Auth vs Clerk vs magic link). Deferred until v2 planning.
- **DICOM hosting strategy for v2** — Convex file storage vs object storage (S3-compatible) vs local-only. Affects whether large DICOM files round-trip through Convex bandwidth.
- **AI appointment ingestion endpoint** — Email forwarding to a special address vs SMS-to-API webhook. Both work; depends on which providers Mario's care comes from.
- **Whether to also build a search index in v2** or rely on simple `LIKE` queries over Convex tables (probably the latter at this data scale).
