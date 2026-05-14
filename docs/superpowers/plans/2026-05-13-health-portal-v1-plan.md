# health.louka.cc v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the v1 visual prototype of health.louka.cc — a unified personal health portal with 4 top-level sections (Imaging, Results, Reports, Appointments), mock data, distinctive visual design, and persistent navigation chrome — while consolidating two GitHub repos into one and keeping the existing spine.louka.cc app unaffected.

**Architecture:** Fresh SvelteKit v2 + Svelte 5 (runes) scaffold at `app/` in the consolidated `mlouka/health` repo. Existing spine app source folds in at `legacy/spine-app/` and keeps deploying via its own separate Vercel project to spine.louka.cc. A new Vercel project deploys `app/` to health.louka.cc. Visual design is produced by the `frontend-design` skill in collaboration with `svelte-ui-designer` and `svelte-ux-designer` agents. Component library: shadcn-svelte. Hardcoded mock data throughout v1; Convex schema written as a forward-looking artifact only.

**Tech Stack:** SvelteKit v2.x · Svelte 5 (runes) · Tailwind v4 · shadcn-svelte · TypeScript 5 · Vitest + @testing-library/svelte · Playwright (e2e) · Convex (schema only in v1, not wired) · Vercel deploy

**Source spec:** `docs/superpowers/specs/2026-05-13-health-portal-v1-design.md`

---

## Global workflow rules (apply to every task below)

- **Commit locally as work progresses.** NEVER push to remote until the user explicitly says "push" / "deploy" / "upload". Every commit step ends at `git commit`, never `git push`.
- **Every commit message starts with `[89a3]`** (per the user's session-prefix convention).
- **spine.louka.cc must stay live and unaffected** throughout the work. Treat any change to it as a separate, opt-in phase post-v1.
- **TDD where logic exists.** Tasks with pure functions or data-shape operations start with a failing test. For pure layout/visual work, accessibility tests run instead.
- **noindex everywhere.** Every page must serve `<meta name="robots" content="noindex, nofollow">`. `robots.txt` must `Disallow: /` for all paths.
- **Run the local server (`npm run dev -- --host 0.0.0.0 --port 8765`)** to preview changes via Tailscale at `http://100.66.207.105:8765/`. The user manually verifies visuals before approval.
- **Agents named in the spec** are the right tool for each kind of work — assignments are listed per phase.

---

## File structure (what gets created or modified)

### New files (created by this plan)

| Path | Purpose | First touched in |
|-|-|-|
| `app/package.json` | SvelteKit project manifest | Phase A |
| `app/svelte.config.js` | SvelteKit config (adapter-vercel) | Phase A |
| `app/vite.config.ts` | Vite config (Tailwind v4 plugin) | Phase A |
| `app/tsconfig.json` | TypeScript config | Phase A |
| `app/src/app.html` | Base HTML, noindex meta | Phase A |
| `app/src/app.css` | Tailwind import + base styles + tokens | Phase B |
| `app/src/app.d.ts` | App type declarations | Phase A |
| `app/static/robots.txt` | Disallow all paths | Phase A |
| `app/src/lib/types/imaging.ts` | TypeScript types for imaging records | Phase C |
| `app/src/lib/types/results.ts` | Types for lab results | Phase C |
| `app/src/lib/types/reports.ts` | Types for written reports | Phase C |
| `app/src/lib/types/appointments.ts` | Types for appointments | Phase C |
| `app/src/lib/types/index.ts` | Type re-exports | Phase C |
| `app/src/lib/mock-data/imaging.ts` | Mock imaging records (1 entry) | Phase C |
| `app/src/lib/mock-data/results.ts` | Empty mock results | Phase C |
| `app/src/lib/mock-data/reports.ts` | Mock reports (1 entry, cervical MRI) | Phase C |
| `app/src/lib/mock-data/appointments.ts` | Mock appointments (2-3 entries) | Phase C |
| `app/src/lib/mock-data/index.ts` | Mock data re-exports + helpers | Phase C |
| `app/src/lib/utils/dates.ts` | Date formatting helpers | Phase C |
| `app/src/lib/utils/dates.test.ts` | Date helper tests | Phase C |
| `app/src/lib/components/AppHeader.svelte` | Sticky top header with avatar + dropdown | Phase D |
| `app/src/lib/components/BottomNav.svelte` | Mobile bottom nav | Phase D |
| `app/src/lib/components/Breadcrumb.svelte` | Back-link breadcrumb | Phase D |
| `app/src/lib/components/ShareToggle.svelte` | Visual-only privacy toggle | Phase D |
| `app/src/lib/components/AccessLogIndicator.svelte` | "0 views" indicator | Phase D |
| `app/src/lib/components/JumpToMenu.svelte` | Floating section-jump (mobile) | Phase D |
| `app/src/lib/components/SectionRail.svelte` | Sticky anchor-link rail (desktop) | Phase D |
| `app/src/lib/components/CurrentFocusCard.svelte` | Home hero card | Phase D |
| `app/src/lib/components/UpcomingCard.svelte` | Home upcoming-appointment card | Phase D |
| `app/src/lib/components/SectionTile.svelte` | Home section tile | Phase D |
| `app/src/lib/components/ActivityFeed.svelte` | Home recent-activity feed | Phase D |
| `app/src/lib/components/RecordCard.svelte` | Generic card used in list pages | Phase D |
| `app/src/lib/components/EmptyState.svelte` | "No X yet" placeholder | Phase D |
| `app/src/routes/+layout.svelte` | App-wide layout with header + nav | Phase D |
| `app/src/routes/+layout.ts` | Layout load function (noindex) | Phase D |
| `app/src/routes/+page.svelte` | Home dashboard | Phase E |
| `app/src/routes/imaging/+page.svelte` | Imaging list | Phase E |
| `app/src/routes/imaging/[slug]/+page.svelte` | Imaging detail | Phase E |
| `app/src/routes/results/+page.svelte` | Results list (empty state) | Phase E |
| `app/src/routes/results/[slug]/+page.svelte` | Results detail (placeholder) | Phase E |
| `app/src/routes/reports/+page.svelte` | Reports list | Phase E |
| `app/src/routes/reports/[slug]/+page.svelte` | Report detail (the rich page) | Phase E |
| `app/src/routes/appointments/+page.svelte` | Appointments list | Phase E |
| `app/src/routes/appointments/[slug]/+page.svelte` | Appointment detail | Phase E |
| `app/src/routes/menu/+page.svelte` | Menu placeholder | Phase E |
| `app/convex/schema.ts` | Forward-looking schema (not wired) | Phase F |
| `app/playwright.config.ts` | Playwright e2e config | Phase F |
| `app/playwright/smoke.spec.ts` | Smoke tests (every route renders) | Phase F |
| `app/.gitignore` | Ignore .svelte-kit, node_modules, etc. | Phase A |
| `.gitignore` (root) | Ignore records/, sync artifacts | Phase A |

### Moved / restructured (Phase A)

| Move | From | To |
|-|-|-|
| Existing spine SvelteKit app | `spine/app/*` (separate `mlouka/spine` repo) | `legacy/spine-app/*` (within unified `mlouka/health` repo, kept as separate Vercel deploy) |
| Reference docs | `spine/reference/*` | `reference/*` |
| Legacy HTML experiments | `spine/legacy/*` | `legacy/old-experiments/*` |
| `spine/` wrapper directory | (removed once empty) | — |

### Deleted (Phase A)

- `spine/docs/cervical-spine-mri-summary.html` — duplicate; canonical copy stays in `legacy/spine-app/static/mri/index.html`
- `spine/docs/img/` — duplicate JPEGs
- `spine/reference/docs/` — byte-identical sync-engine mirror

---

# Phase A — Foundation: repo consolidation + app scaffold

**Owner agents/skills:** `technical-project-manager` (coordination), `svelte-engineer` (implementation), `gsd-docs-update` (note in CLAUDE.md after Phase A completes)

**Outcome of Phase A:** A single unified `mlouka/health` repo at `work/health/` with the legacy spine app folded into `legacy/spine-app/` (still deployable separately), a fresh empty SvelteKit project scaffolded at `app/`, and clean git history at a baseline commit. No visual or functional work yet.

---

## Task A1: Verify environment and baseline

**Files:** none (read-only inspection)

- [ ] **Step 1: Confirm working directory and git state**

Run:
```bash
cd /Users/louka2023/work/health/spine
pwd
git status --short
git remote -v
git log --oneline -5
```

Expected:
- `pwd` shows `/Users/louka2023/work/health/spine`
- Remote `origin` is `https://github.com/mlouka/health.git`
- Recent commits include the `[89a3]` design spec commit (`3729336`) and the MRI doc commits

- [ ] **Step 2: Confirm spine app is still deployed and healthy**

Run:
```bash
curl -s -o /dev/null -w "spine.louka.cc/  → %{http_code}\n" https://spine.louka.cc/
curl -s -o /dev/null -w "spine.louka.cc/mri → %{http_code}\n" https://spine.louka.cc/mri
```

Expected: both return `200`.

- [ ] **Step 3: Confirm Node + npm versions**

Run:
```bash
node --version
npm --version
```

Expected: Node ≥ 20.x, npm ≥ 10.x. If lower, bail and ask user to upgrade.

- [ ] **Step 4: No commit needed (read-only)**

---

## Task A2: Subtree-merge mlouka/spine into mlouka/health as legacy/spine-app/

**Files:**
- Modify (subtree-add): `legacy/spine-app/*` (new tree imported)

The existing live spine app (at `mlouka/spine`, deployed to spine.louka.cc) gets vendored into the unified repo as `legacy/spine-app/`. It keeps deploying from its independent `mlouka/spine` Vercel project — the subtree is just for source-of-truth consolidation.

- [ ] **Step 1: Confirm no uncommitted changes in the current `spine/app/` directory**

Run:
```bash
cd /Users/louka2023/work/health/spine/app
git status --short
```

Expected: clean (or only the `(1)`-suffixed sync artifacts we've been seeing; those are not part of any commit).

- [ ] **Step 2: Add subtree from mlouka/spine main branch**

Run from `/Users/louka2023/work/health/spine`:
```bash
git subtree add --prefix=legacy/spine-app https://github.com/mlouka/spine.git main --squash
```

Expected: subtree imported as a single squashed commit. `legacy/spine-app/` now contains the SvelteKit app source.

- [ ] **Step 3: Verify the subtree contents match expectations**

Run:
```bash
ls legacy/spine-app/
cat legacy/spine-app/package.json | head -20
```

Expected: `src/`, `convex/`, `static/`, `package.json`, `svelte.config.js`, etc. Package name should be `v3` or similar (the existing project name).

- [ ] **Step 4: Commit (already done by subtree add — just verify)**

Run:
```bash
git log --oneline -3
```

Expected: top commit is the subtree squash. Commit message will be auto-generated by `git subtree`. Note its SHA for reference.

---

## Task A3: Reorganize parent directories — move reference, legacy, etc. up one level

The current layout has everything nested under `spine/`. After this task, the top-level structure is:

```
work/health/
├── app/                    (created next, in Phase A4)
├── legacy/
│   ├── spine-app/          (from A2)
│   └── old-experiments/    (from this task)
├── reference/              (moved from spine/reference)
├── docs/
│   └── superpowers/
│       ├── plans/
│       └── specs/
├── records/                (gitignored — not created here)
├── README.md
├── CLAUDE.md
└── .gitignore
```

**Files:** large set of moves

- [ ] **Step 1: Move reference/ up one level**

Run:
```bash
cd /Users/louka2023/work/health/spine
git mv reference/Mario\ Louka\ -\ Adjustment\ Sheet.xlsx ../reference-Mario-Louka-Adjustment-Sheet.xlsx 2>/dev/null || true
mkdir -p ../reference
git mv reference/PAIN-PROFILE.md ../reference/
git mv reference/FINDINGS.md ../reference/
git mv reference/PROJECT-PROGRESS.md ../reference/
git mv reference/Dorsal-Scapular-Nerve-Pain-Map.pdf ../reference/
git mv "reference/Mario Louka - Adjustment Sheet.xlsx" "../reference/Mario Louka - Adjustment Sheet.xlsx" 2>/dev/null || cp "reference/Mario Louka - Adjustment Sheet.xlsx" "../reference/" && git rm "reference/Mario Louka - Adjustment Sheet.xlsx"
git mv reference/scripts ../reference/
```

If any file is missing from this list, check `ls reference/` and adapt — the goal is "everything in spine/reference/ ends up in ../reference/".

- [ ] **Step 2: Move legacy old experiments up one level**

Run:
```bash
mkdir -p ../legacy/old-experiments
git mv legacy/louka-nine.html ../legacy/old-experiments/
git mv legacy/test-brachial.html ../legacy/old-experiments/
git mv legacy/shoulder-blade-pain-map.html ../legacy/old-experiments/
git mv legacy/discover.html ../legacy/old-experiments/ 2>/dev/null || true
```

If `legacy/` has additional files not listed, move them too.

- [ ] **Step 3: Delete duplicates in `spine/docs/`**

The canonical MRI HTML lives in `legacy/spine-app/static/mri/index.html` (which is what deploys to spine.louka.cc/mri). The duplicate in `spine/docs/cervical-spine-mri-summary.html` is stale — delete it:

```bash
git rm docs/cervical-spine-mri-summary.html
git rm -r docs/img/
git rm "docs/cervical spine mri summary.pdf"
```

The PDF is the original (with full PII). It goes into `records/spine/` which is gitignored:

```bash
mkdir -p ../records/spine
mv docs/cervical*.pdf ../records/spine/ 2>/dev/null || true
```

- [ ] **Step 4: Move docs/superpowers/ up one level**

Run:
```bash
mkdir -p ../docs/superpowers
git mv docs/superpowers/specs ../docs/superpowers/
git mv docs/superpowers/plans ../docs/superpowers/
```

- [ ] **Step 5: Remove the now-empty spine/ subtree from git**

Run:
```bash
cd /Users/louka2023/work/health
ls spine/
```

If `spine/` is empty (or contains only `.git`, `.DS_Store`, build artifacts), continue:

```bash
cd spine
# Move .git up first — this is the key step
mv .git ../
cd ..
# Now /Users/louka2023/work/health/ is the git repo root
# Delete the empty spine/ directory
rm -rf spine/.DS_Store spine/.budder-work spine/.superpowers spine/.vercel
rmdir spine/
```

Verify:
```bash
pwd
git status --short
ls
```

Expected: cwd is `/Users/louka2023/work/health`, `.git` is here, top-level shows `legacy/`, `reference/`, `docs/`, `records/` (and the items we've moved). No `spine/` directory.

- [ ] **Step 6: Write the root README.md and CLAUDE.md placeholders**

These will be filled in properly in Phase F. For now, just create stubs:

```bash
cat > README.md <<'EOF'
# health — Mario Louka's personal health portal

Single repo for everything health-related. Includes:

- `app/` — health.louka.cc SvelteKit prototype (v1 in progress)
- `legacy/spine-app/` — the existing spine.louka.cc app (continues to deploy independently)
- `legacy/old-experiments/` — frozen early HTML experiments
- `reference/` — markdown notes, PDFs, the chiro adjustment spreadsheet
- `docs/superpowers/` — design specs and implementation plans
- `records/` — original medical records (gitignored, kept local)

See `docs/superpowers/specs/2026-05-13-health-portal-v1-design.md` for the v1 plan.
EOF

cat > CLAUDE.md <<'EOF'
# CLAUDE.md — health repo

Working in this repo: follow the workflow rules in the user's global CLAUDE.md and project memory:

- Commit prefix: `[89a3]` (session ID first 4 chars)
- Commit locally as you go; push ONLY when user explicitly says "push" / "deploy"
- `legacy/spine-app/` is frozen — do not edit; it deploys separately to spine.louka.cc
- `app/` is the new v1 prototype (health.louka.cc); active development happens here
- `records/` is gitignored — original medical records with PII stay out of git
EOF
```

- [ ] **Step 7: Write the root `.gitignore`**

Run:
```bash
cat > .gitignore <<'EOF'
# OS
.DS_Store
*.swp

# Sync artifacts
* (1)
* (1).*
*\ \(1\)*

# Node / build outputs
node_modules/
.svelte-kit/
.vercel/
dist/
build/

# Claude internals
.budder-work/
.superpowers/

# Editor
.idea/
.vscode/

# Records — original medical records with PII stay local-only
records/
EOF
```

- [ ] **Step 8: Stage everything, commit**

Run:
```bash
git add -A
git status --short
git diff --cached --stat | head -30
```

Verify: only intended moves and new files. Should NOT include `records/` (it's gitignored), `.DS_Store`, or `(1)` artifacts.

Then commit:
```bash
git commit -m "$(cat <<'COMMIT_MSG'
[89a3] chore(repo): consolidate spine/ into root; vendor legacy/spine-app via subtree

Repo reorganization per docs/superpowers/specs/2026-05-13-health-portal-v1-design.md:

- Subtree-merged mlouka/spine into legacy/spine-app/ (still deploys
  independently to spine.louka.cc via its own Vercel project)
- Moved reference/, legacy/, docs/ up one level so work/health/ is the
  repo root and chats opened from work/health/ see the full structure
- Removed the now-empty spine/ wrapper directory
- Deleted duplicate MRI HTML (the canonical copy lives in
  legacy/spine-app/static/mri/index.html)
- Original radiology PDF moved out of git into records/spine/ (gitignored)
- Wrote root README.md, CLAUDE.md, and .gitignore

The mlouka/spine GitHub repo is left untouched (still deploying live).
After v1 ships and the user is satisfied, that repo can be archived.

Local only; not pushed.
COMMIT_MSG
)"
git log --oneline -3
```

Expected: new commit appears at the top with the consolidation work.

---

## Task A4: Scaffold the fresh SvelteKit project at app/

**Files:**
- Create: `app/` (whole directory tree)

This creates a *new* SvelteKit project from scratch — not a fork of the legacy app. The v1 prototype is a clean build.

- [ ] **Step 1: Run the SvelteKit scaffold**

Run from `/Users/louka2023/work/health`:
```bash
npx sv create app
```

When prompted:
- Template: **Skeleton project**
- Add type checking: **Yes, using TypeScript syntax**
- Add Prettier: **Yes**
- Add ESLint: **Yes**
- Add Vitest: **Yes**
- Add Playwright: **Yes**
- Add Tailwind CSS: **Yes** (typography + forms plugins yes)
- Add adapter-vercel: **Yes** (or use sv add later)
- Package manager: **npm**

- [ ] **Step 2: Verify scaffold structure**

Run:
```bash
ls app/
cat app/package.json | head -30
```

Expected: `src/`, `static/`, `package.json`, `svelte.config.js`, `vite.config.ts`, `tsconfig.json`, `tailwind.config.*`, `playwright.config.ts`, etc.

- [ ] **Step 3: Install dependencies**

Run:
```bash
cd app
npm install
```

- [ ] **Step 4: Add adapter-vercel if not already installed**

Run:
```bash
npx sv add adapter-vercel
```

Or manually:
```bash
npm install -D @sveltejs/adapter-vercel
```

Then verify `svelte.config.js` uses `adapter-vercel`. If not, edit it:

```javascript
// svelte.config.js
import adapter from '@sveltejs/adapter-vercel';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: { adapter: adapter() }
};

export default config;
```

- [ ] **Step 5: Confirm dev server runs**

Run:
```bash
cd app
npm run dev -- --host 0.0.0.0 --port 8765
```

Open `http://100.66.207.105:8765/` in the user's phone (Tailscale). Expected: default SvelteKit "Welcome to SvelteKit" page renders. Kill the server (Ctrl-C) after verification.

- [ ] **Step 6: Add robots.txt and global noindex**

Create `app/static/robots.txt`:
```
User-agent: *
Disallow: /
```

Edit `app/src/app.html` to add noindex meta:
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%sveltekit.assets%/favicon.png" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="robots" content="noindex, nofollow" />
    %sveltekit.head%
  </head>
  <body data-sveltekit-preload-data="hover">
    <div style="display: contents">%sveltekit.body%</div>
  </body>
</html>
```

- [ ] **Step 7: Verify the scaffold serves the noindex header**

Restart dev server, then in another terminal:
```bash
curl -s http://localhost:8765/ | grep -E "noindex|robots"
curl -s http://localhost:8765/robots.txt
```

Expected: `noindex, nofollow` appears in the HTML response; robots.txt returns `Disallow: /`.

- [ ] **Step 8: Commit**

Run from `/Users/louka2023/work/health`:
```bash
git add app/
git status --short
git commit -m "$(cat <<'COMMIT_MSG'
[89a3] feat(app): scaffold fresh SvelteKit v1 prototype at app/

Fresh SvelteKit v2 + Svelte 5 (runes) + Tailwind v4 + TypeScript scaffold.
Includes Vitest + Playwright + adapter-vercel out of the box.

Added:
- robots.txt disallows all paths
- noindex/nofollow meta on every page (via app.html)

The skeleton renders the default SvelteKit landing page at /. Real routes
and visual design come in Phases C-E.
COMMIT_MSG
)"
```

---

# Phase B — Design foundation: shadcn-svelte + design tokens + visual exploration

**Owner agents/skills:** `ui-design:design-system-setup` (initial token setup), `svelte-ui-designer` (palette, type, spacing), `svelte-ux-designer` (motion philosophy), `frontend-design:frontend-design` (exploration & component generation)

**Outcome of Phase B:** shadcn-svelte installed and themed. Design tokens (color, type, spacing, motion) defined in `app/src/app.css` and referenced everywhere. A design exploration artifact lands in `app/docs/design-exploration/` (HTML mockups or a Svelte playground) showing the home and a report-page treatment for user approval before component build-out.

---

## Task B1: Install and initialize shadcn-svelte

**Files:**
- Modify: `app/package.json`
- Modify: `app/src/app.css`
- Create: `app/components.json` (shadcn-svelte config)

- [ ] **Step 1: Initialize shadcn-svelte**

Run from `app/`:
```bash
cd /Users/louka2023/work/health/app
npx shadcn-svelte@latest init
```

Answer prompts:
- Style: **Default**
- Base color: **Neutral**
- CSS variables: **Yes**
- Tailwind CSS file: `src/app.css`
- Tailwind config: leave default
- Components alias: `$lib/components`
- Utils alias: `$lib/utils`

- [ ] **Step 2: Verify components.json was written and app.css updated**

Run:
```bash
cat components.json
head -50 src/app.css
```

Expected: `components.json` exists; `app.css` has `@tailwind` directives plus `@layer base` with CSS variables for color tokens.

- [ ] **Step 3: Add a basic component to verify install works**

Run:
```bash
npx shadcn-svelte@latest add button
```

Verify `src/lib/components/ui/button/` was created.

- [ ] **Step 4: Test rendering**

Edit `src/routes/+page.svelte` temporarily:
```svelte
<script lang="ts">
  import { Button } from '$lib/components/ui/button/index.js';
</script>

<main class="p-8">
  <h1 class="text-2xl font-bold">health.louka.cc — Phase B setup check</h1>
  <Button>Test button</Button>
</main>
```

Run `npm run dev -- --host 0.0.0.0 --port 8765`, visit page, confirm button renders.

- [ ] **Step 5: Commit**

Run from `/Users/louka2023/work/health`:
```bash
git add app/
git commit -m "[89a3] feat(app): install shadcn-svelte, neutral base palette, button primitive"
```

---

## Task B2: Define design tokens (color, type, spacing, motion)

**Owner agents:** `svelte-ui-designer` (drives this task), `svelte-ux-designer` (motion subsection)

**Files:**
- Modify: `app/src/app.css` (token definitions)
- Create: `app/src/lib/styles/tokens.md` (human-readable token reference)

The tokens encode the "warm cream / ink / rust accent" palette referenced in the spec (matching the existing MRI doc's editorial feel). NOT clinical-blue.

- [ ] **Step 1: Define the token palette in app.css**

Add to `app/src/app.css`, replacing the default shadcn-svelte `@layer base` colors:

```css
@layer base {
  :root {
    /* Surface */
    --paper:        50 25% 96%;   /* #faf8f3 — primary background */
    --paper-warm:   38 35% 92%;   /* #f4ede0 — elevated surface */
    --paper-card:   50 30% 98%;   /* #fbfaf6 — card / facsimile bg */

    /* Ink */
    --ink:          0 0% 10%;     /* #1a1a1a — primary text */
    --ink-muted:   30 8% 32%;     /* #5a5246 — secondary text */
    --ink-soft:    30 10% 50%;    /* #8a7e6e — tertiary, labels */

    /* Accent */
    --accent:      14 70% 33%;    /* #8b3a1f — rust/clay */
    --accent-soft: 14 50% 50%;    /* lighter accent for hover */

    /* Severity (matches cervical map SVG) */
    --severity-mild:    36 65% 40%;  /* amber */
    --severity-severe:  10 65% 45%;  /* rust-red */
    --severity-good:    100 30% 35%; /* green */

    /* Rule / dividers */
    --rule:        40 30% 70%;
    --rule-soft:   40 25% 85%;

    /* Motion */
    --motion-ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
    --motion-ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
    --duration-fast:      150ms;
    --duration-medium:    260ms;
    --duration-slow:      400ms;

    /* Type scale (Fraunces serif + Inter sans, set via @font-face / Google Fonts in app.html) */
    --font-serif:  'Fraunces', Georgia, serif;
    --font-sans:   'Inter', system-ui, sans-serif;
    --font-mono:   'SF Mono', 'Menlo', monospace;
  }

  body {
    background: hsl(var(--paper));
    color: hsl(var(--ink));
    font-family: var(--font-sans);
  }
}
```

- [ ] **Step 2: Add Google Fonts link to app.html**

Edit `app/src/app.html` and add to `<head>`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
```

- [ ] **Step 3: Document tokens in tokens.md**

Create `app/src/lib/styles/tokens.md`:
```markdown
# Design tokens

Source: `src/app.css` `:root` block. This file is the human-readable reference.

## Surface
- `--paper` (#faf8f3) — primary background
- `--paper-warm` (#f4ede0) — elevated surface (cards, callouts)
- `--paper-card` (#fbfaf6) — card / facsimile background

## Ink
- `--ink` (#1a1a1a) — primary text
- `--ink-muted` (#5a5246) — secondary text
- `--ink-soft` (#8a7e6e) — tertiary, labels

## Accent
- `--accent` (#8b3a1f) — rust/clay primary accent
- `--accent-soft` — hover, lighter variant

## Severity (matches cervical map SVG colors)
- `--severity-mild` — amber
- `--severity-severe` — rust-red
- `--severity-good` — green

## Motion
- `--motion-ease-out`, `--motion-ease-in-out`
- `--duration-fast` 150ms, `--duration-medium` 260ms, `--duration-slow` 400ms

## Type
- `--font-serif` Fraunces — headings
- `--font-sans` Inter — body
- `--font-mono` SF Mono — clinical / technical
```

- [ ] **Step 4: Test the palette renders**

Edit `src/routes/+page.svelte`:
```svelte
<main class="min-h-screen bg-[hsl(var(--paper))] p-8">
  <h1 class="font-serif text-4xl text-[hsl(var(--ink))]">health.louka.cc</h1>
  <p class="text-[hsl(var(--ink-muted))] mt-2">Token palette test</p>
  <div class="mt-6 flex gap-4">
    <div class="h-12 w-24 rounded bg-[hsl(var(--paper-warm))]"></div>
    <div class="h-12 w-24 rounded bg-[hsl(var(--accent))]"></div>
    <div class="h-12 w-24 rounded bg-[hsl(var(--severity-mild))]"></div>
    <div class="h-12 w-24 rounded bg-[hsl(var(--severity-severe))]"></div>
  </div>
</main>
```

Run dev server, verify the palette swatches render with Fraunces serif heading.

- [ ] **Step 5: Commit**

Run from `/Users/louka2023/work/health`:
```bash
git add app/
git commit -m "[89a3] feat(design): define warm-cream + rust-accent token palette and type scale"
```

---

## Task B3: Visual design exploration via frontend-design skill

**Owner skill:** `frontend-design:frontend-design`

**Files:**
- Create: `app/docs/design-exploration/home-v1.html` (or `.svelte` mockup)
- Create: `app/docs/design-exploration/report-page-v1.html`

This task generates polished visual mockups before any component build-out. The artifacts are HTML mockups (standalone files) that the user previews and approves. After approval, Phase D builds Svelte components matching the approved look.

- [ ] **Step 1: Invoke the frontend-design skill**

Use the `Skill` tool to invoke `frontend-design:frontend-design`. Pass it as context:

> Source of truth: `docs/superpowers/specs/2026-05-13-health-portal-v1-design.md`. Specifically the "Home dashboard" section and the "Report page structure" section.
>
> Token palette: `app/src/app.css` `:root` block (warm cream + ink + rust accent + Fraunces/Inter type pairing — defined per `app/src/lib/styles/tokens.md`).
>
> Produce two standalone HTML mockups in `app/docs/design-exploration/`:
> 1. `home-v1.html` — full home dashboard at mobile (390px) and desktop (1280px) widths. Includes header, current-focus card, upcoming card, 4 section tiles (Imaging / Results / Reports / Appointments), recent activity feed, bottom nav.
> 2. `report-page-v1.html` — single report detail page rendering the cervical MRI content (copy from `legacy/spine-app/static/mri/index.html`). Includes the new sticky chrome: top bar (back breadcrumb + share toggle + access log indicator), sticky right rail (desktop) / floating jump-to button (mobile).
>
> Aesthetic intent: distinctive, considered, calm. Not Sharp HealthCare. Not generic shadcn. Use the cream palette, Fraunces for headings, Inter for body, rust accent for emphasis.
>
> Mock data: hardcode the same example data we'll use in `app/src/lib/mock-data/` so the visuals match the eventual real prototype.
>
> Output requirement: two `.html` files that render in a browser, copy-pasteable token-based styling, no framework dependencies.

- [ ] **Step 2: User reviews mockups**

The frontend-design skill produces the two HTML files. Run a local server:
```bash
cd app/docs/design-exploration && python3 -m http.server 8766 --bind 0.0.0.0
```

User visits `http://100.66.207.105:8766/home-v1.html` and `http://100.66.207.105:8766/report-page-v1.html` on their phone. **WAIT for user approval before continuing.** Iterate if requested.

- [ ] **Step 3: Commit the approved mockups**

```bash
git add app/docs/design-exploration/
git commit -m "[89a3] docs(design): approved home + report-page visual mockups (Phase B exploration)"
```

---

# Phase C — Mock data, types, and helpers

**Owner agents/skills:** `svelte-engineer`, `tdd-workflows:tdd-orchestrator` (TDD for helpers)

**Outcome of Phase C:** TypeScript types for each record kind, hardcoded mock data instances, and utility helpers (date formatting, severity coloring). Date helpers are TDD-driven.

---

## Task C1: Define TypeScript types for each record kind

**Files:**
- Create: `app/src/lib/types/imaging.ts`
- Create: `app/src/lib/types/results.ts`
- Create: `app/src/lib/types/reports.ts`
- Create: `app/src/lib/types/appointments.ts`
- Create: `app/src/lib/types/shared.ts`
- Create: `app/src/lib/types/index.ts`

- [ ] **Step 1: Write `shared.ts` (common types used across record kinds)**

Create `app/src/lib/types/shared.ts`:
```typescript
export type BodyRegion = 'spine' | 'shoulder' | 'chest' | 'head' | 'other';

export type Severity = 'normal' | 'mild' | 'moderate' | 'severe';

export type Modality = 'MRI' | 'CT' | 'X-ray' | 'CBCT' | 'ultrasound';

export interface PrivacyState {
  isPublic: boolean;
  viewCount: number;
  recentViews: Array<{
    timestamp: string;
    referrer: string | null;
    userAgentHash: string;
  }>;
}

export interface BaseRecord {
  slug: string;
  title: string;
  createdAt: string;  // ISO 8601
  updatedAt: string;  // ISO 8601
  privacy: PrivacyState;
}
```

- [ ] **Step 2: Write `imaging.ts`**

Create `app/src/lib/types/imaging.ts`:
```typescript
import type { BaseRecord, BodyRegion, Modality } from './shared.js';

export interface ImagingStudy extends BaseRecord {
  studyDate: string;
  modality: Modality;
  bodyRegion: BodyRegion;
  procedure: string;
  institution: string;
  referringPhysician: string;
  radiologist: string | null;
  primaryFinding: string;
  hasDicom: boolean;       // forward-looking; always false in v1
  relatedReportSlug: string | null;
}
```

- [ ] **Step 3: Write `results.ts`**

Create `app/src/lib/types/results.ts`:
```typescript
import type { BaseRecord, BodyRegion } from './shared.js';

export interface LabPanel extends BaseRecord {
  testDate: string;
  panelName: string;
  laboratory: string;
  values: Array<{
    analyte: string;
    value: number;
    unit: string;
    referenceRange: string;
    flag: 'normal' | 'low' | 'high' | 'critical' | null;
  }>;
  bodyRegion: BodyRegion | null;
}
```

- [ ] **Step 4: Write `reports.ts`**

Create `app/src/lib/types/reports.ts`:
```typescript
import type { BaseRecord, BodyRegion, Severity } from './shared.js';

export interface Report extends BaseRecord {
  reportDate: string;
  bodyRegion: BodyRegion;
  primaryFinding: string;
  severity: Severity;
  authoredBy: 'self' | 'provider' | 'ai-assisted';
  relatedImagingSlug: string | null;
  contentPath: string;     // path to the rich .svelte page that owns the content
}
```

- [ ] **Step 5: Write `appointments.ts`**

Create `app/src/lib/types/appointments.ts`:
```typescript
import type { BaseRecord, BodyRegion } from './shared.js';

export interface Appointment extends BaseRecord {
  provider: string;
  startsAt: string;
  durationMinutes: number;
  location: string;
  isVirtual: boolean;
  reason: string;
  bodyRegion: BodyRegion | null;
  source: 'manual' | 'email-parsed' | 'sms-parsed';  // v1 always 'manual'
}
```

- [ ] **Step 6: Write `index.ts`**

Create `app/src/lib/types/index.ts`:
```typescript
export * from './shared.js';
export * from './imaging.js';
export * from './results.js';
export * from './reports.js';
export * from './appointments.js';
```

- [ ] **Step 7: Verify types compile**

Run from `app/`:
```bash
npm run check
```

Expected: no errors.

- [ ] **Step 8: Commit**

```bash
git add app/src/lib/types/
git commit -m "[89a3] feat(types): define record types (imaging, results, reports, appointments)"
```

---

## Task C2: Write mock data instances

**Files:**
- Create: `app/src/lib/mock-data/imaging.ts`
- Create: `app/src/lib/mock-data/results.ts`
- Create: `app/src/lib/mock-data/reports.ts`
- Create: `app/src/lib/mock-data/appointments.ts`
- Create: `app/src/lib/mock-data/index.ts`

- [ ] **Step 1: Write mock imaging data (1 entry — the cervical MRI)**

Create `app/src/lib/mock-data/imaging.ts`:
```typescript
import type { ImagingStudy } from '$lib/types/index.js';

export const imagingStudies: ImagingStudy[] = [
  {
    slug: 'cervical-mri-2026-05-06',
    title: 'Cervical Spine MRI',
    studyDate: '2026-05-06T05:34:00Z',
    modality: 'MRI',
    bodyRegion: 'spine',
    procedure: 'MR CERVICAL SPINE WO IV CONTRAST',
    institution: 'Sharp Rees-Stealy (RKM)',
    referringPhysician: 'HUIZAR, BRIAN',
    radiologist: 'Barbara Hsu, MD',
    primaryFinding: 'Right C6-C7 disc extrusion contacting right C7 nerve root',
    hasDicom: false,
    relatedReportSlug: 'cervical-mri',
    createdAt: '2026-05-08T16:00:00Z',
    updatedAt: '2026-05-13T17:00:00Z',
    privacy: { isPublic: false, viewCount: 0, recentViews: [] }
  }
];
```

- [ ] **Step 2: Write empty results data**

Create `app/src/lib/mock-data/results.ts`:
```typescript
import type { LabPanel } from '$lib/types/index.js';

export const labPanels: LabPanel[] = [];
```

- [ ] **Step 3: Write mock reports data**

Create `app/src/lib/mock-data/reports.ts`:
```typescript
import type { Report } from '$lib/types/index.js';

export const reports: Report[] = [
  {
    slug: 'cervical-mri',
    title: 'Cervical Spine MRI — Findings and Interpretation',
    reportDate: '2026-05-08T16:00:00Z',
    bodyRegion: 'spine',
    primaryFinding: 'C6-C7 right disc extrusion',
    severity: 'moderate',
    authoredBy: 'self',
    relatedImagingSlug: 'cervical-mri-2026-05-06',
    contentPath: '/reports/cervical-mri',
    createdAt: '2026-05-08T16:00:00Z',
    updatedAt: '2026-05-13T17:00:00Z',
    privacy: { isPublic: false, viewCount: 0, recentViews: [] }
  }
];
```

- [ ] **Step 4: Write mock appointments data**

Create `app/src/lib/mock-data/appointments.ts`:
```typescript
import type { Appointment } from '$lib/types/index.js';

export const appointments: Appointment[] = [
  {
    slug: 'spine-consult-2026-05-22',
    title: 'Spine consultation',
    provider: 'Dr. Park, UC Spine Care',
    startsAt: '2026-05-22T17:00:00Z',
    durationMinutes: 45,
    location: '5395 Ruffin Rd, San Diego, CA 92123',
    isVirtual: false,
    reason: 'Review of cervical MRI findings; treatment plan discussion',
    bodyRegion: 'spine',
    source: 'manual',
    createdAt: '2026-05-10T12:00:00Z',
    updatedAt: '2026-05-10T12:00:00Z',
    privacy: { isPublic: false, viewCount: 0, recentViews: [] }
  },
  {
    slug: 'pt-followup-2026-06-03',
    title: 'Physical therapy follow-up',
    provider: 'Sharp Rehabilitation',
    startsAt: '2026-06-03T16:30:00Z',
    durationMinutes: 60,
    location: 'Virtual',
    isVirtual: true,
    reason: 'PT progress check',
    bodyRegion: 'spine',
    source: 'manual',
    createdAt: '2026-05-11T09:00:00Z',
    updatedAt: '2026-05-11T09:00:00Z',
    privacy: { isPublic: false, viewCount: 0, recentViews: [] }
  }
];
```

- [ ] **Step 5: Write index helpers**

Create `app/src/lib/mock-data/index.ts`:
```typescript
import { imagingStudies } from './imaging.js';
import { labPanels } from './results.js';
import { reports } from './reports.js';
import { appointments } from './appointments.js';

export { imagingStudies, labPanels, reports, appointments };

export function currentFocus() {
  // Hardcoded: return the cervical MRI report as v1's current focus
  return reports[0];
}

export function nextUpcomingAppointment() {
  const now = new Date();
  return appointments
    .filter((a) => new Date(a.startsAt) > now)
    .sort((a, b) => new Date(a.startsAt).getTime() - new Date(b.startsAt).getTime())[0] ?? null;
}

export function recentActivity(limit = 5) {
  type ActivityItem = { type: string; title: string; timestamp: string; slug: string; section: string };
  const items: ActivityItem[] = [];
  for (const r of reports) {
    items.push({ type: 'report-created', title: `${r.title} created`, timestamp: r.createdAt, slug: r.slug, section: 'reports' });
    if (r.updatedAt !== r.createdAt) {
      items.push({ type: 'report-updated', title: `${r.title} updated`, timestamp: r.updatedAt, slug: r.slug, section: 'reports' });
    }
  }
  for (const i of imagingStudies) {
    items.push({ type: 'imaging-added', title: `${i.title} added`, timestamp: i.createdAt, slug: i.slug, section: 'imaging' });
  }
  for (const a of appointments) {
    items.push({ type: 'appointment-added', title: `${a.title} added`, timestamp: a.createdAt, slug: a.slug, section: 'appointments' });
  }
  return items.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()).slice(0, limit);
}

export function countBySection() {
  return {
    imaging: imagingStudies.length,
    results: labPanels.length,
    reports: reports.length,
    appointments: appointments.filter((a) => new Date(a.startsAt) > new Date()).length
  };
}
```

- [ ] **Step 6: Verify types pass**

Run from `app/`:
```bash
npm run check
```

Expected: no errors.

- [ ] **Step 7: Commit**

```bash
git add app/src/lib/mock-data/
git commit -m "[89a3] feat(mock-data): hardcoded v1 mock data + helper functions"
```

---

## Task C3: Date formatting helpers (TDD)

**Owner skill:** `tdd-workflows:tdd-red` then `tdd-workflows:tdd-green` then `tdd-cycle`

**Files:**
- Create: `app/src/lib/utils/dates.test.ts`
- Create: `app/src/lib/utils/dates.ts`

- [ ] **Step 1: Write failing tests first**

Create `app/src/lib/utils/dates.test.ts`:
```typescript
import { describe, it, expect } from 'vitest';
import { formatStudyDate, formatRelativeTime, formatAppointmentTime } from './dates.js';

describe('formatStudyDate', () => {
  it('formats an ISO date as a long-form English date', () => {
    expect(formatStudyDate('2026-05-06T05:34:00Z')).toBe('May 6, 2026');
  });
});

describe('formatRelativeTime', () => {
  it('returns "just now" for times in the last minute', () => {
    const now = new Date();
    expect(formatRelativeTime(now.toISOString(), now)).toBe('just now');
  });

  it('returns "Nm ago" for minutes', () => {
    const ref = new Date('2026-05-13T10:00:00Z');
    const past = new Date('2026-05-13T09:55:00Z');
    expect(formatRelativeTime(past.toISOString(), ref)).toBe('5m ago');
  });

  it('returns "Nh ago" for hours', () => {
    const ref = new Date('2026-05-13T10:00:00Z');
    const past = new Date('2026-05-13T08:00:00Z');
    expect(formatRelativeTime(past.toISOString(), ref)).toBe('2h ago');
  });

  it('returns "Nd ago" for days', () => {
    const ref = new Date('2026-05-13T10:00:00Z');
    const past = new Date('2026-05-06T10:00:00Z');
    expect(formatRelativeTime(past.toISOString(), ref)).toBe('7d ago');
  });
});

describe('formatAppointmentTime', () => {
  it('formats with day-of-week, date, and time', () => {
    expect(formatAppointmentTime('2026-05-22T17:00:00Z')).toMatch(/^Fri, May 22.*\d/);
  });
});
```

- [ ] **Step 2: Run tests and verify they fail**

Run from `app/`:
```bash
npm run test -- --run src/lib/utils/dates.test.ts
```

Expected: FAIL. Module `./dates.js` not found.

- [ ] **Step 3: Implement the helpers**

Create `app/src/lib/utils/dates.ts`:
```typescript
export function formatStudyDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'UTC'
  });
}

export function formatRelativeTime(iso: string, ref: Date = new Date()): string {
  const diffMs = ref.getTime() - new Date(iso).getTime();
  const seconds = Math.floor(diffMs / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  if (seconds < 60) return 'just now';
  if (minutes < 60) return `${minutes}m ago`;
  if (hours < 24) return `${hours}h ago`;
  return `${days}d ago`;
}

export function formatAppointmentTime(iso: string): string {
  const d = new Date(iso);
  const date = d.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric'
  });
  const time = d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
  return `${date}, ${time}`;
}
```

- [ ] **Step 4: Run tests and verify pass**

```bash
npm run test -- --run src/lib/utils/dates.test.ts
```

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add app/src/lib/utils/
git commit -m "[89a3] feat(utils): TDD'd date helpers (study date, relative time, appointment time)"
```

---

# Phase D — Layout shell, navigation chrome, and core components

**Owner agents:** `svelte-engineer` (implementation), `svelte-ui-designer` (visual review of each component), `svelte-ux-designer` (transitions, focus states), `frontend-design` skill (any component refinement)

**Outcome of Phase D:** All shared components built. The app layout (header + bottom nav) is in place. Visiting the root URL shows an empty homepage inside the proper shell. Detail pages can use the sticky chrome components.

---

## Task D1: AppHeader component

**Files:**
- Create: `app/src/lib/components/AppHeader.svelte`
- Create: `app/src/lib/components/AppHeader.test.ts` (component render test)

- [ ] **Step 1: Write the render test**

Create `app/src/lib/components/AppHeader.test.ts`:
```typescript
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/svelte';
import AppHeader from './AppHeader.svelte';

describe('AppHeader', () => {
  it('renders the user initial and name', () => {
    const { getByText } = render(AppHeader, { props: { userName: 'Mario' } });
    expect(getByText('Mario')).toBeTruthy();
  });

  it('renders a private indicator when isPrivate=true', () => {
    const { getByLabelText } = render(AppHeader, { props: { userName: 'Mario', isPrivate: true } });
    expect(getByLabelText(/private/i)).toBeTruthy();
  });
});
```

- [ ] **Step 2: Run and verify it fails**

Run `npm run test -- --run src/lib/components/AppHeader.test.ts`. Expected: FAIL (component doesn't exist).

- [ ] **Step 3: Create the component**

Create `app/src/lib/components/AppHeader.svelte`:
```svelte
<script lang="ts">
  interface Props {
    userName: string;
    isPrivate?: boolean;
  }
  let { userName, isPrivate = true }: Props = $props();

  const initial = userName.charAt(0).toUpperCase();
</script>

<header
  class="sticky top-0 z-30 flex items-center justify-between border-b border-[hsl(var(--rule-soft))] bg-[hsl(var(--paper))]/90 px-4 py-3 backdrop-blur"
>
  <button class="flex items-center gap-2" type="button">
    <span
      class="flex h-9 w-9 items-center justify-center rounded-full bg-[hsl(var(--accent))] font-sans text-sm font-semibold text-[hsl(var(--paper))]"
      aria-hidden="true"
    >
      {initial}
    </span>
    <span class="font-sans text-base font-medium text-[hsl(var(--ink))]">{userName}</span>
    <svg class="h-4 w-4 text-[hsl(var(--ink-soft))]" viewBox="0 0 20 20" fill="currentColor">
      <path d="M5.23 7.21a.75.75 0 011.06.02L10 11.06l3.71-3.83a.75.75 0 111.08 1.04l-4.25 4.39a.75.75 0 01-1.08 0L5.21 8.27a.75.75 0 01.02-1.06z"/>
    </svg>
  </button>

  {#if isPrivate}
    <span
      class="flex items-center gap-1 font-sans text-xs font-medium text-[hsl(var(--ink-soft))]"
      aria-label="Private — only you can see this app"
    >
      <svg class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clip-rule="evenodd"/>
      </svg>
      Private
    </span>
  {/if}
</header>
```

- [ ] **Step 4: Run tests and verify pass**

```bash
npm run test -- --run src/lib/components/AppHeader.test.ts
```

Expected: tests PASS.

- [ ] **Step 5: Commit**

```bash
git add app/src/lib/components/AppHeader.svelte app/src/lib/components/AppHeader.test.ts
git commit -m "[89a3] feat(components): AppHeader with avatar, name, private indicator"
```

---

## Task D2: BottomNav component

**Files:**
- Create: `app/src/lib/components/BottomNav.svelte`

- [ ] **Step 1: Create the component**

Create `app/src/lib/components/BottomNav.svelte`:
```svelte
<script lang="ts">
  import { page } from '$app/state';

  const items = [
    { href: '/', label: 'Home', icon: 'home' },
    { href: '/search', label: 'Search', icon: 'search' },
    { href: '/menu', label: 'Menu', icon: 'menu' }
  ];

  function isActive(href: string) {
    if (href === '/') return page.url.pathname === '/';
    return page.url.pathname.startsWith(href);
  }
</script>

<nav
  class="sticky bottom-0 z-30 grid grid-cols-3 border-t border-[hsl(var(--rule-soft))] bg-[hsl(var(--paper))]/95 backdrop-blur md:hidden"
  aria-label="Primary"
>
  {#each items as item}
    <a
      href={item.href}
      class="flex flex-col items-center gap-1 py-3 text-xs font-medium transition-colors {isActive(item.href) ? 'text-[hsl(var(--accent))]' : 'text-[hsl(var(--ink-soft))]'}"
    >
      <span aria-hidden="true">
        {#if item.icon === 'home'}
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/></svg>
        {:else if item.icon === 'search'}
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/></svg>
        {:else}
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/></svg>
        {/if}
      </span>
      {item.label}
    </a>
  {/each}
</nav>
```

- [ ] **Step 2: Commit**

```bash
git add app/src/lib/components/BottomNav.svelte
git commit -m "[89a3] feat(components): BottomNav (mobile-only Home/Search/Menu)"
```

---

## Task D3: Breadcrumb, ShareToggle, AccessLogIndicator components

**Files:**
- Create: `app/src/lib/components/Breadcrumb.svelte`
- Create: `app/src/lib/components/ShareToggle.svelte`
- Create: `app/src/lib/components/AccessLogIndicator.svelte`

- [ ] **Step 1: Create Breadcrumb**

Create `app/src/lib/components/Breadcrumb.svelte`:
```svelte
<script lang="ts">
  interface Props {
    parentLabel: string;
    parentHref: string;
  }
  let { parentLabel, parentHref }: Props = $props();
</script>

<a
  href={parentHref}
  class="inline-flex items-center gap-1.5 font-sans text-sm font-medium text-[hsl(var(--ink-soft))] transition-colors hover:text-[hsl(var(--ink))]"
>
  <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
    <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"/>
  </svg>
  {parentLabel}
</a>
```

- [ ] **Step 2: Create ShareToggle (visual only — no state wiring in v1)**

Create `app/src/lib/components/ShareToggle.svelte`:
```svelte
<script lang="ts">
  interface Props {
    isPublic: boolean;
  }
  let { isPublic }: Props = $props();
</script>

<button
  type="button"
  class="inline-flex items-center gap-2 rounded-full border border-[hsl(var(--rule))] bg-[hsl(var(--paper-card))] px-3 py-1.5 font-sans text-xs font-semibold transition-colors hover:border-[hsl(var(--ink-soft))]"
  aria-pressed={isPublic}
  aria-label={isPublic ? 'This page is public — click to make private' : 'This page is private — click to make public'}
  onclick={() => alert('Share toggle wiring is deferred to v2.')}
>
  <span
    class="h-2 w-2 rounded-full {isPublic ? 'bg-[hsl(var(--severity-good))]' : 'bg-[hsl(var(--ink-soft))]'}"
    aria-hidden="true"
  ></span>
  <span class="text-[hsl(var(--ink))]">{isPublic ? 'Public' : 'Private'}</span>
</button>
```

- [ ] **Step 3: Create AccessLogIndicator**

Create `app/src/lib/components/AccessLogIndicator.svelte`:
```svelte
<script lang="ts">
  interface Props {
    viewCount: number;
    isPublic: boolean;
  }
  let { viewCount, isPublic }: Props = $props();
</script>

{#if isPublic}
  <p class="font-sans text-xs text-[hsl(var(--ink-soft))]">
    {viewCount === 0 ? 'No views yet' : `${viewCount} view${viewCount === 1 ? '' : 's'}`}
  </p>
{/if}
```

- [ ] **Step 4: Commit**

```bash
git add app/src/lib/components/Breadcrumb.svelte app/src/lib/components/ShareToggle.svelte app/src/lib/components/AccessLogIndicator.svelte
git commit -m "[89a3] feat(components): Breadcrumb, ShareToggle (visual-only), AccessLogIndicator"
```

---

## Task D4: Home dashboard components (CurrentFocusCard, UpcomingCard, SectionTile, ActivityFeed)

**Files:**
- Create: `app/src/lib/components/CurrentFocusCard.svelte`
- Create: `app/src/lib/components/UpcomingCard.svelte`
- Create: `app/src/lib/components/SectionTile.svelte`
- Create: `app/src/lib/components/ActivityFeed.svelte`

For each component below, follow the same pattern: build the Svelte component using the design tokens, ensure responsive (mobile and desktop both work), accessible (semantic HTML, ARIA labels where needed), and visual consistency with the Phase B mockups.

- [ ] **Step 1: Create CurrentFocusCard**

Create `app/src/lib/components/CurrentFocusCard.svelte`:
```svelte
<script lang="ts">
  import { formatRelativeTime } from '$lib/utils/dates.js';
  import type { Report } from '$lib/types/index.js';

  interface Props {
    report: Report;
  }
  let { report }: Props = $props();
</script>

<article class="rounded-xl border border-[hsl(var(--rule-soft))] bg-[hsl(var(--paper-warm))] p-5">
  <p class="font-sans text-[10px] font-semibold uppercase tracking-[0.18em] text-[hsl(var(--accent))]">
    Current focus
  </p>
  <h2 class="mt-2 font-serif text-2xl font-medium leading-tight text-[hsl(var(--ink))]">
    {report.title}
  </h2>
  <p class="mt-1 text-sm text-[hsl(var(--ink-muted))]">
    {report.primaryFinding}
  </p>
  <p class="mt-3 font-sans text-xs text-[hsl(var(--ink-soft))]">
    Updated {formatRelativeTime(report.updatedAt)}
  </p>
  <a
    href={report.contentPath}
    class="mt-4 inline-flex items-center gap-1.5 font-sans text-sm font-semibold text-[hsl(var(--accent))] transition-colors hover:text-[hsl(var(--ink))]"
  >
    Open report
    <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/></svg>
  </a>
</article>
```

- [ ] **Step 2: Create UpcomingCard**

Create `app/src/lib/components/UpcomingCard.svelte`:
```svelte
<script lang="ts">
  import { formatAppointmentTime } from '$lib/utils/dates.js';
  import type { Appointment } from '$lib/types/index.js';

  interface Props {
    appointment: Appointment;
  }
  let { appointment }: Props = $props();
</script>

<article class="rounded-xl border border-[hsl(var(--rule-soft))] bg-[hsl(var(--paper-card))] p-5">
  <p class="font-sans text-[10px] font-semibold uppercase tracking-[0.18em] text-[hsl(var(--ink-soft))]">
    Upcoming
  </p>
  <h3 class="mt-2 font-serif text-xl font-medium text-[hsl(var(--ink))]">
    {appointment.provider}
  </h3>
  <p class="mt-1 text-sm text-[hsl(var(--ink-muted))]">
    {formatAppointmentTime(appointment.startsAt)}{appointment.isVirtual ? ' · Virtual' : ''}
  </p>
  <a
    href="/appointments/{appointment.slug}"
    class="mt-4 inline-flex items-center gap-1.5 font-sans text-sm font-semibold text-[hsl(var(--accent))] transition-colors hover:text-[hsl(var(--ink))]"
  >
    View · Add to calendar
    <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/></svg>
  </a>
</article>
```

- [ ] **Step 3: Create SectionTile**

Create `app/src/lib/components/SectionTile.svelte`:
```svelte
<script lang="ts">
  interface Props {
    href: string;
    label: string;
    count: number | null;
    emptyText?: string;
    icon: 'imaging' | 'results' | 'reports' | 'appointments';
  }
  let { href, label, count, emptyText = 'none yet', icon }: Props = $props();
</script>

<a
  {href}
  class="block rounded-xl border border-[hsl(var(--rule-soft))] bg-[hsl(var(--paper-card))] p-4 transition-colors hover:border-[hsl(var(--accent))]"
>
  <div class="flex h-10 w-10 items-center justify-center rounded-full bg-[hsl(var(--paper-warm))]">
    {#if icon === 'imaging'}
      <svg class="h-5 w-5 text-[hsl(var(--accent))]" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 5a2 2 0 012-2 1 1 0 000 2H6a2 2 0 00-2 2v6a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L8.586 13H6V7h12v2a1 1 0 102 0V7a2 2 0 00-2-2H4z" clip-rule="evenodd"/></svg>
    {:else if icon === 'results'}
      <svg class="h-5 w-5 text-[hsl(var(--accent))]" viewBox="0 0 20 20" fill="currentColor"><path d="M8 7a1 1 0 011 1v6a1 1 0 11-2 0V8a1 1 0 011-1zm4 0a1 1 0 011 1v6a1 1 0 11-2 0V8a1 1 0 011-1z"/><path fill-rule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v14a1 1 0 01-1 1H4a1 1 0 01-1-1V3zm2 1v12h10V4H5z" clip-rule="evenodd"/></svg>
    {:else if icon === 'reports'}
      <svg class="h-5 w-5 text-[hsl(var(--accent))]" viewBox="0 0 20 20" fill="currentColor"><path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/><path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"/></svg>
    {:else}
      <svg class="h-5 w-5 text-[hsl(var(--accent))]" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/></svg>
    {/if}
  </div>
  <h3 class="mt-3 font-sans text-sm font-semibold text-[hsl(var(--ink))]">{label}</h3>
  <p class="mt-0.5 text-xs text-[hsl(var(--ink-soft))]">
    {count === 0 || count === null ? emptyText : `${count} ${count === 1 ? 'item' : 'items'}`}
  </p>
</a>
```

- [ ] **Step 4: Create ActivityFeed**

Create `app/src/lib/components/ActivityFeed.svelte`:
```svelte
<script lang="ts">
  import { formatRelativeTime } from '$lib/utils/dates.js';

  interface ActivityItem {
    type: string;
    title: string;
    timestamp: string;
    slug: string;
    section: string;
  }

  interface Props {
    items: ActivityItem[];
  }
  let { items }: Props = $props();
</script>

<section aria-label="Recent activity">
  <h2 class="font-sans text-[10px] font-semibold uppercase tracking-[0.18em] text-[hsl(var(--ink-soft))]">
    Recent activity
  </h2>
  {#if items.length === 0}
    <p class="mt-3 text-sm text-[hsl(var(--ink-soft))]">No recent activity yet.</p>
  {:else}
    <ul class="mt-3 divide-y divide-[hsl(var(--rule-soft))]">
      {#each items as item}
        <li class="py-2.5">
          <a href="/{item.section}/{item.slug}" class="flex items-baseline justify-between gap-3 text-sm transition-colors hover:text-[hsl(var(--accent))]">
            <span class="text-[hsl(var(--ink))]">{item.title}</span>
            <span class="font-sans text-xs text-[hsl(var(--ink-soft))] whitespace-nowrap">
              {formatRelativeTime(item.timestamp)}
            </span>
          </a>
        </li>
      {/each}
    </ul>
  {/if}
</section>
```

- [ ] **Step 5: Commit**

```bash
git add app/src/lib/components/CurrentFocusCard.svelte app/src/lib/components/UpcomingCard.svelte app/src/lib/components/SectionTile.svelte app/src/lib/components/ActivityFeed.svelte
git commit -m "[89a3] feat(components): home dashboard cards (CurrentFocus, Upcoming, SectionTile, ActivityFeed)"
```

---

## Task D5: RecordCard + EmptyState (used by list pages)

**Files:**
- Create: `app/src/lib/components/RecordCard.svelte`
- Create: `app/src/lib/components/EmptyState.svelte`

- [ ] **Step 1: Create RecordCard**

Create `app/src/lib/components/RecordCard.svelte`:
```svelte
<script lang="ts">
  import { formatStudyDate } from '$lib/utils/dates.js';

  interface Tag {
    label: string;
    variant?: 'neutral' | 'mild' | 'severe';
  }

  interface Props {
    href: string;
    title: string;
    date: string;
    preview: string;
    tags?: Tag[];
    isPublic: boolean;
  }
  let { href, title, date, preview, tags = [], isPublic }: Props = $props();
</script>

<a
  {href}
  class="block rounded-xl border border-[hsl(var(--rule-soft))] bg-[hsl(var(--paper-card))] p-4 transition-colors hover:border-[hsl(var(--accent))]"
>
  <div class="flex items-start justify-between gap-3">
    <h3 class="font-serif text-lg font-medium leading-snug text-[hsl(var(--ink))]">{title}</h3>
    <span class="text-[hsl(var(--ink-soft))]" aria-label={isPublic ? 'Public' : 'Private'}>
      {#if isPublic}
        <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM4.332 8.027a6.012 6.012 0 011.912-2.706C6.512 5.73 6.974 6 7.5 6A1.5 1.5 0 019 7.5V8a2 2 0 004 0 2 2 0 011.523-1.943A5.977 5.977 0 0116 10c0 .34-.028.675-.083 1H15a2 2 0 00-2 2v2.197A5.973 5.973 0 0110 16v-2a2 2 0 00-2-2 2 2 0 01-2-2 2 2 0 00-1.668-1.973z" clip-rule="evenodd"/></svg>
      {:else}
        <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clip-rule="evenodd"/></svg>
      {/if}
    </span>
  </div>
  <p class="mt-1 font-sans text-xs text-[hsl(var(--ink-soft))]">{formatStudyDate(date)}</p>
  <p class="mt-3 text-sm text-[hsl(var(--ink-muted))]">{preview}</p>
  {#if tags.length > 0}
    <div class="mt-3 flex flex-wrap gap-1.5">
      {#each tags as tag}
        <span
          class="rounded-full px-2 py-0.5 font-sans text-[10px] font-semibold uppercase tracking-[0.1em] {tag.variant === 'severe' ? 'bg-[hsl(var(--severity-severe))]/15 text-[hsl(var(--severity-severe))]' : tag.variant === 'mild' ? 'bg-[hsl(var(--severity-mild))]/15 text-[hsl(var(--severity-mild))]' : 'bg-[hsl(var(--paper-warm))] text-[hsl(var(--ink-soft))]'}"
        >{tag.label}</span>
      {/each}
    </div>
  {/if}
</a>
```

- [ ] **Step 2: Create EmptyState**

Create `app/src/lib/components/EmptyState.svelte`:
```svelte
<script lang="ts">
  interface Props {
    title: string;
    body: string;
  }
  let { title, body }: Props = $props();
</script>

<div class="rounded-xl border border-dashed border-[hsl(var(--rule))] bg-[hsl(var(--paper-card))] p-8 text-center">
  <h3 class="font-serif text-lg font-medium text-[hsl(var(--ink))]">{title}</h3>
  <p class="mt-2 text-sm text-[hsl(var(--ink-muted))]">{body}</p>
</div>
```

- [ ] **Step 3: Commit**

```bash
git add app/src/lib/components/RecordCard.svelte app/src/lib/components/EmptyState.svelte
git commit -m "[89a3] feat(components): RecordCard (list cards) + EmptyState"
```

---

## Task D6: SectionRail + JumpToMenu (anchor navigation for the report page)

**Owner:** `svelte-ux-designer` (motion + interaction)

**Files:**
- Create: `app/src/lib/components/SectionRail.svelte`
- Create: `app/src/lib/components/JumpToMenu.svelte`

These provide the right-rail (desktop) and floating-button (mobile) section navigation on the report page.

- [ ] **Step 1: Create SectionRail (desktop)**

Create `app/src/lib/components/SectionRail.svelte`:
```svelte
<script lang="ts">
  interface SectionLink {
    id: string;
    label: string;
  }

  interface Props {
    sections: SectionLink[];
    title?: string;
  }
  let { sections, title = 'In this report' }: Props = $props();
</script>

<aside
  class="sticky top-24 hidden h-fit w-56 rounded-xl border border-[hsl(var(--rule-soft))] bg-[hsl(var(--paper-card))] p-4 lg:block"
  aria-label="Section navigation"
>
  <p class="font-sans text-[10px] font-semibold uppercase tracking-[0.18em] text-[hsl(var(--ink-soft))]">
    {title}
  </p>
  <nav class="mt-3 flex flex-col gap-2 font-sans text-sm">
    {#each sections as section}
      <a
        href="#{section.id}"
        class="text-[hsl(var(--ink-muted))] transition-colors hover:text-[hsl(var(--accent))]"
      >
        {section.label}
      </a>
    {/each}
  </nav>
</aside>
```

- [ ] **Step 2: Create JumpToMenu (mobile, floating)**

Create `app/src/lib/components/JumpToMenu.svelte`:
```svelte
<script lang="ts">
  interface SectionLink {
    id: string;
    label: string;
  }

  interface Props {
    sections: SectionLink[];
  }
  let { sections }: Props = $props();

  let isOpen = $state(false);

  function toggle() {
    isOpen = !isOpen;
  }

  function close() {
    isOpen = false;
  }
</script>

<div class="fixed bottom-20 right-4 z-40 lg:hidden">
  {#if isOpen}
    <div
      class="absolute bottom-14 right-0 w-60 rounded-xl border border-[hsl(var(--rule-soft))] bg-[hsl(var(--paper-card))] p-4 shadow-xl"
      role="dialog"
      aria-label="Jump to section"
    >
      <p class="font-sans text-[10px] font-semibold uppercase tracking-[0.18em] text-[hsl(var(--ink-soft))]">
        Jump to
      </p>
      <nav class="mt-3 flex flex-col gap-2 font-sans text-sm">
        {#each sections as section}
          <a
            href="#{section.id}"
            onclick={close}
            class="text-[hsl(var(--ink-muted))] transition-colors hover:text-[hsl(var(--accent))]"
          >
            {section.label}
          </a>
        {/each}
      </nav>
    </div>
  {/if}
  <button
    type="button"
    onclick={toggle}
    aria-expanded={isOpen}
    aria-label={isOpen ? 'Close section menu' : 'Open section menu'}
    class="flex h-12 w-12 items-center justify-center rounded-full bg-[hsl(var(--accent))] text-[hsl(var(--paper))] shadow-lg transition-transform {isOpen ? 'rotate-45' : ''}"
  >
    <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/></svg>
  </button>
</div>
```

- [ ] **Step 3: Commit**

```bash
git add app/src/lib/components/SectionRail.svelte app/src/lib/components/JumpToMenu.svelte
git commit -m "[89a3] feat(components): SectionRail (desktop) + JumpToMenu (mobile floating)"
```

---

## Task D7: Root layout that uses AppHeader + BottomNav

**Files:**
- Modify: `app/src/routes/+layout.svelte`
- Create: `app/src/routes/+layout.ts`

- [ ] **Step 1: Create +layout.ts (sets noindex meta and disables prerender)**

Create `app/src/routes/+layout.ts`:
```typescript
export const prerender = false;
export const ssr = true;
```

- [ ] **Step 2: Modify +layout.svelte**

Replace `app/src/routes/+layout.svelte` with:
```svelte
<script lang="ts">
  import '../app.css';
  import AppHeader from '$lib/components/AppHeader.svelte';
  import BottomNav from '$lib/components/BottomNav.svelte';

  let { children } = $props();
</script>

<div class="min-h-screen bg-[hsl(var(--paper))] pb-16 md:pb-0">
  <AppHeader userName="Mario" isPrivate={true} />
  <main class="mx-auto max-w-3xl px-4 py-6">
    {@render children()}
  </main>
  <BottomNav />
</div>
```

- [ ] **Step 3: Verify the shell renders**

Run from `app/`:
```bash
npm run dev -- --host 0.0.0.0 --port 8765
```

Open `http://100.66.207.105:8765/`. Expected: cream background, header shows "(M) Mario ▾  🔒 Private", bottom nav on mobile shows three items. The page body still shows the default scaffold content (we'll replace in Phase E).

- [ ] **Step 4: Commit**

```bash
git add app/src/routes/+layout.svelte app/src/routes/+layout.ts
git commit -m "[89a3] feat(layout): root layout with sticky AppHeader and mobile BottomNav"
```

---

# Phase E — Pages: Home + section lists + detail pages

**Owner agents:** `svelte-engineer` (implementation), `frontend-design` skill (visual refinement per page), `svelte-ux-designer` (transitions between routes)

**Outcome of Phase E:** Every route in the v1 spec renders correctly. The home dashboard shows the full Sharp-style content. Each section list page renders its cards (or empty state for Results). Each detail page renders with proper chrome.

---

## Task E1: Home dashboard

**Files:**
- Modify: `app/src/routes/+page.svelte`

- [ ] **Step 1: Replace +page.svelte**

Create `app/src/routes/+page.svelte`:
```svelte
<script lang="ts">
  import CurrentFocusCard from '$lib/components/CurrentFocusCard.svelte';
  import UpcomingCard from '$lib/components/UpcomingCard.svelte';
  import SectionTile from '$lib/components/SectionTile.svelte';
  import ActivityFeed from '$lib/components/ActivityFeed.svelte';
  import { currentFocus, nextUpcomingAppointment, recentActivity, countBySection } from '$lib/mock-data/index.js';

  const focus = currentFocus();
  const upcoming = nextUpcomingAppointment();
  const activity = recentActivity(5);
  const counts = countBySection();
</script>

<svelte:head>
  <title>health.louka.cc</title>
</svelte:head>

<div class="flex flex-col gap-5">
  <CurrentFocusCard report={focus} />

  {#if upcoming}
    <UpcomingCard appointment={upcoming} />
  {/if}

  <div class="grid grid-cols-2 gap-3 md:grid-cols-4">
    <SectionTile href="/imaging" label="Imaging" count={counts.imaging} icon="imaging" />
    <SectionTile href="/results" label="Results" count={counts.results} emptyText="none yet" icon="results" />
    <SectionTile href="/reports" label="Reports" count={counts.reports} icon="reports" />
    <SectionTile href="/appointments" label="Appointments" count={counts.appointments} icon="appointments" />
  </div>

  <ActivityFeed items={activity} />
</div>
```

- [ ] **Step 2: Verify**

Run dev server. Visit `http://100.66.207.105:8765/`. Expected: full Sharp-style dashboard renders with all 4 sections. **STOP and have user approve before continuing** — this is the first page that should match the Phase B mockups.

- [ ] **Step 3: Commit**

```bash
git add app/src/routes/+page.svelte
git commit -m "[89a3] feat(home): Sharp-style dashboard with current focus, upcoming, tiles, activity"
```

---

## Task E2: Section list pages — Imaging, Results, Reports, Appointments

**Files:**
- Create: `app/src/routes/imaging/+page.svelte`
- Create: `app/src/routes/results/+page.svelte`
- Create: `app/src/routes/reports/+page.svelte`
- Create: `app/src/routes/appointments/+page.svelte`

- [ ] **Step 1: Imaging list**

Create `app/src/routes/imaging/+page.svelte`:
```svelte
<script lang="ts">
  import RecordCard from '$lib/components/RecordCard.svelte';
  import EmptyState from '$lib/components/EmptyState.svelte';
  import { imagingStudies } from '$lib/mock-data/index.js';
</script>

<svelte:head><title>Imaging — health.louka.cc</title></svelte:head>

<header class="mb-6">
  <h1 class="font-serif text-3xl font-medium text-[hsl(var(--ink))]">Imaging</h1>
  <p class="mt-1 text-sm text-[hsl(var(--ink-muted))]">MRIs, CTs, X-rays</p>
</header>

{#if imagingStudies.length === 0}
  <EmptyState title="No imaging yet" body="Studies you upload will appear here." />
{:else}
  <ul class="flex flex-col gap-3">
    {#each imagingStudies as study}
      <li>
        <RecordCard
          href="/imaging/{study.slug}"
          title={study.title}
          date={study.studyDate}
          preview={study.primaryFinding}
          tags={[{ label: study.modality }, { label: study.bodyRegion }]}
          isPublic={study.privacy.isPublic}
        />
      </li>
    {/each}
  </ul>
{/if}
```

- [ ] **Step 2: Results list**

Create `app/src/routes/results/+page.svelte`:
```svelte
<script lang="ts">
  import EmptyState from '$lib/components/EmptyState.svelte';
  import { labPanels } from '$lib/mock-data/index.js';
</script>

<svelte:head><title>Results — health.louka.cc</title></svelte:head>

<header class="mb-6">
  <h1 class="font-serif text-3xl font-medium text-[hsl(var(--ink))]">Results</h1>
  <p class="mt-1 text-sm text-[hsl(var(--ink-muted))]">Lab results, blood work, vitals</p>
</header>

<EmptyState title="No results yet" body="Lab panels and vitals will appear here when added." />
```

- [ ] **Step 3: Reports list**

Create `app/src/routes/reports/+page.svelte`:
```svelte
<script lang="ts">
  import RecordCard from '$lib/components/RecordCard.svelte';
  import { reports } from '$lib/mock-data/index.js';

  function tagVariant(severity: string): 'mild' | 'severe' | 'neutral' {
    if (severity === 'mild') return 'mild';
    if (severity === 'moderate' || severity === 'severe') return 'severe';
    return 'neutral';
  }
</script>

<svelte:head><title>Reports — health.louka.cc</title></svelte:head>

<header class="mb-6">
  <h1 class="font-serif text-3xl font-medium text-[hsl(var(--ink))]">Reports</h1>
  <p class="mt-1 text-sm text-[hsl(var(--ink-muted))]">Written interpretations and summaries</p>
</header>

<ul class="flex flex-col gap-3">
  {#each reports as report}
    <li>
      <RecordCard
        href="/reports/{report.slug}"
        title={report.title}
        date={report.reportDate}
        preview={report.primaryFinding}
        tags={[{ label: report.severity, variant: tagVariant(report.severity) }, { label: report.bodyRegion }]}
        isPublic={report.privacy.isPublic}
      />
    </li>
  {/each}
</ul>
```

- [ ] **Step 4: Appointments list**

Create `app/src/routes/appointments/+page.svelte`:
```svelte
<script lang="ts">
  import RecordCard from '$lib/components/RecordCard.svelte';
  import { appointments } from '$lib/mock-data/index.js';
</script>

<svelte:head><title>Appointments — health.louka.cc</title></svelte:head>

<header class="mb-6">
  <h1 class="font-serif text-3xl font-medium text-[hsl(var(--ink))]">Appointments</h1>
  <p class="mt-1 text-sm text-[hsl(var(--ink-muted))]">Upcoming and past care events</p>
</header>

<ul class="flex flex-col gap-3">
  {#each appointments as appt}
    <li>
      <RecordCard
        href="/appointments/{appt.slug}"
        title={appt.title}
        date={appt.startsAt}
        preview="{appt.provider} · {appt.location}"
        tags={[{ label: appt.isVirtual ? 'Virtual' : 'In-person' }]}
        isPublic={appt.privacy.isPublic}
      />
    </li>
  {/each}
</ul>
```

- [ ] **Step 5: Commit**

```bash
git add app/src/routes/imaging/+page.svelte app/src/routes/results/+page.svelte app/src/routes/reports/+page.svelte app/src/routes/appointments/+page.svelte
git commit -m "[89a3] feat(routes): list pages for Imaging/Results/Reports/Appointments"
```

---

## Task E3: Detail pages for Imaging and Appointments

**Files:**
- Create: `app/src/routes/imaging/[slug]/+page.svelte`
- Create: `app/src/routes/imaging/[slug]/+page.ts`
- Create: `app/src/routes/appointments/[slug]/+page.svelte`
- Create: `app/src/routes/appointments/[slug]/+page.ts`

- [ ] **Step 1: Imaging detail load**

Create `app/src/routes/imaging/[slug]/+page.ts`:
```typescript
import { error } from '@sveltejs/kit';
import { imagingStudies } from '$lib/mock-data/index.js';

export function load({ params }) {
  const study = imagingStudies.find((s) => s.slug === params.slug);
  if (!study) throw error(404, 'Imaging study not found');
  return { study };
}
```

- [ ] **Step 2: Imaging detail page**

Create `app/src/routes/imaging/[slug]/+page.svelte`:
```svelte
<script lang="ts">
  import Breadcrumb from '$lib/components/Breadcrumb.svelte';
  import ShareToggle from '$lib/components/ShareToggle.svelte';
  import AccessLogIndicator from '$lib/components/AccessLogIndicator.svelte';
  import { formatStudyDate } from '$lib/utils/dates.js';

  let { data } = $props();
  const { study } = data;
</script>

<svelte:head><title>{study.title} — Imaging</title></svelte:head>

<div class="sticky top-[57px] z-20 -mx-4 mb-6 flex items-center justify-between border-b border-[hsl(var(--rule-soft))] bg-[hsl(var(--paper))]/95 px-4 py-3 backdrop-blur">
  <Breadcrumb parentLabel="Imaging" parentHref="/imaging" />
  <div class="flex items-center gap-3">
    <AccessLogIndicator viewCount={study.privacy.viewCount} isPublic={study.privacy.isPublic} />
    <ShareToggle isPublic={study.privacy.isPublic} />
  </div>
</div>

<article class="flex flex-col gap-6">
  <header>
    <p class="font-sans text-xs font-semibold uppercase tracking-[0.18em] text-[hsl(var(--accent))]">
      {study.modality} · {study.bodyRegion}
    </p>
    <h1 class="mt-2 font-serif text-3xl font-medium leading-tight text-[hsl(var(--ink))]">
      {study.title}
    </h1>
    <p class="mt-2 text-sm text-[hsl(var(--ink-muted))]">{formatStudyDate(study.studyDate)}</p>
  </header>

  <dl class="grid grid-cols-2 gap-x-6 gap-y-3 rounded-xl bg-[hsl(var(--paper-card))] p-5 font-mono text-xs">
    <div><dt class="text-[10px] font-semibold uppercase tracking-[0.12em] text-[hsl(var(--ink-soft))]">Procedure</dt><dd class="mt-0.5">{study.procedure}</dd></div>
    <div><dt class="text-[10px] font-semibold uppercase tracking-[0.12em] text-[hsl(var(--ink-soft))]">Institution</dt><dd class="mt-0.5">{study.institution}</dd></div>
    <div><dt class="text-[10px] font-semibold uppercase tracking-[0.12em] text-[hsl(var(--ink-soft))]">Referring</dt><dd class="mt-0.5">{study.referringPhysician}</dd></div>
    {#if study.radiologist}
      <div><dt class="text-[10px] font-semibold uppercase tracking-[0.12em] text-[hsl(var(--ink-soft))]">Radiologist</dt><dd class="mt-0.5">{study.radiologist}</dd></div>
    {/if}
  </dl>

  <section>
    <h2 class="font-serif text-xl font-medium">Primary finding</h2>
    <p class="mt-2 text-sm text-[hsl(var(--ink-muted))]">{study.primaryFinding}</p>
  </section>

  {#if study.relatedReportSlug}
    <a href="/reports/{study.relatedReportSlug}" class="inline-flex w-fit items-center gap-1.5 rounded-full bg-[hsl(var(--accent))] px-4 py-2 font-sans text-sm font-semibold text-[hsl(var(--paper))]">
      Open written report →
    </a>
  {/if}

  <section class="rounded-xl border border-dashed border-[hsl(var(--rule))] bg-[hsl(var(--paper-card))] p-8 text-center">
    <p class="font-sans text-xs font-semibold uppercase tracking-[0.18em] text-[hsl(var(--ink-soft))]">DICOM viewer</p>
    <h3 class="mt-2 font-serif text-lg font-medium">Coming in v2</h3>
    <p class="mt-2 text-sm text-[hsl(var(--ink-muted))]">Interactive scrolling through scan slices will live here.</p>
  </section>
</article>
```

- [ ] **Step 3: Appointment detail load**

Create `app/src/routes/appointments/[slug]/+page.ts`:
```typescript
import { error } from '@sveltejs/kit';
import { appointments } from '$lib/mock-data/index.js';

export function load({ params }) {
  const appointment = appointments.find((a) => a.slug === params.slug);
  if (!appointment) throw error(404, 'Appointment not found');
  return { appointment };
}
```

- [ ] **Step 4: Appointment detail page**

Create `app/src/routes/appointments/[slug]/+page.svelte`:
```svelte
<script lang="ts">
  import Breadcrumb from '$lib/components/Breadcrumb.svelte';
  import ShareToggle from '$lib/components/ShareToggle.svelte';
  import AccessLogIndicator from '$lib/components/AccessLogIndicator.svelte';
  import { formatAppointmentTime } from '$lib/utils/dates.js';

  let { data } = $props();
  const { appointment } = data;
</script>

<svelte:head><title>{appointment.title} — Appointments</title></svelte:head>

<div class="sticky top-[57px] z-20 -mx-4 mb-6 flex items-center justify-between border-b border-[hsl(var(--rule-soft))] bg-[hsl(var(--paper))]/95 px-4 py-3 backdrop-blur">
  <Breadcrumb parentLabel="Appointments" parentHref="/appointments" />
  <div class="flex items-center gap-3">
    <AccessLogIndicator viewCount={appointment.privacy.viewCount} isPublic={appointment.privacy.isPublic} />
    <ShareToggle isPublic={appointment.privacy.isPublic} />
  </div>
</div>

<article class="flex flex-col gap-5">
  <header>
    <p class="font-sans text-xs font-semibold uppercase tracking-[0.18em] text-[hsl(var(--accent))]">
      {appointment.isVirtual ? 'Virtual visit' : 'In-person visit'}
    </p>
    <h1 class="mt-2 font-serif text-3xl font-medium text-[hsl(var(--ink))]">{appointment.title}</h1>
    <p class="mt-2 text-base text-[hsl(var(--ink-muted))]">{formatAppointmentTime(appointment.startsAt)}</p>
  </header>

  <dl class="grid grid-cols-1 gap-3 rounded-xl bg-[hsl(var(--paper-card))] p-5 font-sans text-sm">
    <div><dt class="text-xs font-semibold uppercase tracking-[0.12em] text-[hsl(var(--ink-soft))]">Provider</dt><dd>{appointment.provider}</dd></div>
    <div><dt class="text-xs font-semibold uppercase tracking-[0.12em] text-[hsl(var(--ink-soft))]">Location</dt><dd>{appointment.location}</dd></div>
    <div><dt class="text-xs font-semibold uppercase tracking-[0.12em] text-[hsl(var(--ink-soft))]">Reason</dt><dd>{appointment.reason}</dd></div>
  </dl>

  <button type="button" class="w-fit rounded-full bg-[hsl(var(--accent))] px-4 py-2 font-sans text-sm font-semibold text-[hsl(var(--paper))]" onclick={() => alert('Calendar export (.ics) is deferred to v2.')}>
    Add to calendar
  </button>
</article>
```

- [ ] **Step 5: Commit**

```bash
git add app/src/routes/imaging/\[slug\]/ app/src/routes/appointments/\[slug\]/
git commit -m "[89a3] feat(routes): imaging + appointment detail pages with sticky chrome"
```

---

## Task E4: Reports detail page — port the cervical MRI document

**Owner agents:** `svelte-engineer` (port), `frontend-design` skill (visual review on report page specifically)

**Files:**
- Create: `app/src/routes/reports/[slug]/+page.svelte`
- Create: `app/src/routes/reports/[slug]/+page.ts`
- Create: `app/src/routes/reports/cervical-mri/CervicalMriContent.svelte` (the ported content)
- Create: `app/src/routes/results/[slug]/+page.svelte` (placeholder)

- [ ] **Step 1: Reports detail load**

Create `app/src/routes/reports/[slug]/+page.ts`:
```typescript
import { error } from '@sveltejs/kit';
import { reports } from '$lib/mock-data/index.js';

export function load({ params }) {
  const report = reports.find((r) => r.slug === params.slug);
  if (!report) throw error(404, 'Report not found');
  return { report };
}
```

- [ ] **Step 2: Port the cervical MRI content**

Open `legacy/spine-app/static/mri/index.html`. Extract everything inside `<body><div class="page">...</div></body>` and convert to Svelte syntax. Replace the existing `<style>` block's CSS variables with references to the new token system where applicable (e.g., `var(--paper)` → `hsl(var(--paper))`).

Create `app/src/routes/reports/cervical-mri/CervicalMriContent.svelte` containing the entire report markup. This is a large file (~1400 lines of HTML + inline SVG). Copy the HTML body content verbatim from the source MRI doc, change `<` and `>` HTML entities appropriately for Svelte, and wrap it in `<script lang="ts">` with proper imports if any.

The component should export the section list as `SECTIONS` for the parent page to drive the SectionRail/JumpToMenu:

```svelte
<script lang="ts" module>
  export const SECTIONS = [
    { id: 'clinical-summary', label: 'Clinical summary' },
    { id: 'radiologists-report', label: "Radiologist's report" },
    { id: 'report-interpretation', label: 'Report interpretation' },
    { id: 'key-imaging', label: 'Key imaging' },
    { id: 'clinical-presentation', label: 'Clinical presentation' },
    { id: 'assessment-and-treatment-plan', label: 'Assessment and treatment plan' },
    { id: 'consultation-questions', label: 'Consultation questions' }
  ];
</script>

<!-- (full ported HTML+SVG content here, with id="clinical-summary" etc. anchors on each section) -->
```

This step is large and the content is verbatim. Use a sub-agent for the port if helpful (`svelte-engineer`).

- [ ] **Step 3: Reports detail page wrapper**

Create `app/src/routes/reports/[slug]/+page.svelte`:
```svelte
<script lang="ts">
  import Breadcrumb from '$lib/components/Breadcrumb.svelte';
  import ShareToggle from '$lib/components/ShareToggle.svelte';
  import AccessLogIndicator from '$lib/components/AccessLogIndicator.svelte';
  import SectionRail from '$lib/components/SectionRail.svelte';
  import JumpToMenu from '$lib/components/JumpToMenu.svelte';
  import CervicalMriContent, { SECTIONS } from '../cervical-mri/CervicalMriContent.svelte';

  let { data } = $props();
  const { report } = data;

  // v1: only one report exists. Future: a {#switch} or component map keyed by slug.
</script>

<svelte:head><title>{report.title}</title></svelte:head>

<div class="sticky top-[57px] z-20 -mx-4 mb-6 flex items-center justify-between border-b border-[hsl(var(--rule-soft))] bg-[hsl(var(--paper))]/95 px-4 py-3 backdrop-blur">
  <Breadcrumb parentLabel="Reports" parentHref="/reports" />
  <div class="flex items-center gap-3">
    <AccessLogIndicator viewCount={report.privacy.viewCount} isPublic={report.privacy.isPublic} />
    <ShareToggle isPublic={report.privacy.isPublic} />
  </div>
</div>

<div class="lg:grid lg:grid-cols-[1fr_240px] lg:gap-8">
  <article class="prose prose-stone max-w-none">
    {#if report.slug === 'cervical-mri'}
      <CervicalMriContent />
    {:else}
      <p>Content for this report is not yet available.</p>
    {/if}
  </article>

  <SectionRail sections={SECTIONS} />
</div>

<JumpToMenu sections={SECTIONS} />
```

- [ ] **Step 4: Results detail placeholder**

Create `app/src/routes/results/[slug]/+page.svelte`:
```svelte
<svelte:head><title>Result detail</title></svelte:head>
<p class="text-sm text-[hsl(var(--ink-muted))]">No result with this slug exists in v1.</p>
```

- [ ] **Step 5: Menu placeholder**

Create `app/src/routes/menu/+page.svelte`:
```svelte
<svelte:head><title>Menu</title></svelte:head>

<header class="mb-6">
  <h1 class="font-serif text-3xl font-medium">Menu</h1>
  <p class="mt-1 text-sm text-[hsl(var(--ink-muted))]">Settings, share-link manager, sign out — coming in v2.</p>
</header>

<ul class="flex flex-col gap-2 rounded-xl border border-[hsl(var(--rule-soft))] bg-[hsl(var(--paper-card))] p-4 text-sm text-[hsl(var(--ink-soft))]">
  <li>Settings (v2)</li>
  <li>Share-link manager (v2)</li>
  <li>Access log (v2)</li>
  <li>Sign out (v2)</li>
</ul>
```

- [ ] **Step 6: Verify**

Run dev server. Visit:
- `http://100.66.207.105:8765/` — home
- `http://100.66.207.105:8765/imaging` — imaging list
- `http://100.66.207.105:8765/imaging/cervical-mri-2026-05-06` — imaging detail
- `http://100.66.207.105:8765/reports` — reports list
- `http://100.66.207.105:8765/reports/cervical-mri` — **the rich report** (verify all sections render, sticky chrome works, section rail works on desktop, jump menu works on mobile)
- `http://100.66.207.105:8765/appointments` — appointments list
- `http://100.66.207.105:8765/appointments/spine-consult-2026-05-22` — appointment detail
- `http://100.66.207.105:8765/results` — empty state
- `http://100.66.207.105:8765/menu` — menu placeholder

**WAIT for user approval of the full prototype before continuing.**

- [ ] **Step 7: Commit**

```bash
git add app/src/routes/
git commit -m "[89a3] feat(routes): detail pages incl. ported cervical MRI report with sticky chrome"
```

---

# Phase F — Schema, tests, review, ship

**Owner agents:** `convex-engineer` (schema), `tdd-orchestrator` (test coverage), `accessibility-compliance:wcag-audit-patterns` (a11y), `svelte-reviewer` (code review), `web-design-guidelines` (final quality), `gsd-docs-update` (README/CLAUDE.md)

---

## Task F1: Forward-looking Convex schema (no v1 wiring)

**Owner:** `convex-engineer`

**Files:**
- Create: `app/convex/schema.ts`

- [ ] **Step 1: Install convex dependency**

Run from `app/`:
```bash
npm install convex
```

- [ ] **Step 2: Write the schema**

Create `app/convex/schema.ts`:
```typescript
import { defineSchema, defineTable } from 'convex/server';
import { v } from 'convex/values';

export default defineSchema({
  imaging_studies: defineTable({
    slug: v.string(),
    studyDate: v.string(),
    modality: v.union(v.literal('MRI'), v.literal('CT'), v.literal('X-ray'), v.literal('CBCT'), v.literal('ultrasound')),
    bodyRegion: v.string(),
    procedure: v.string(),
    institution: v.string(),
    referringPhysician: v.string(),
    radiologist: v.optional(v.string()),
    primaryFinding: v.string(),
    hasDicom: v.boolean(),
    dicomStorageId: v.optional(v.string()),
    relatedReportSlug: v.optional(v.string()),
    isPublic: v.boolean(),
    createdAt: v.number(),
    updatedAt: v.number()
  }).index('by_date', ['studyDate']).index('by_slug', ['slug']),

  lab_results: defineTable({
    slug: v.string(),
    testDate: v.string(),
    panelName: v.string(),
    laboratory: v.string(),
    bodyRegion: v.optional(v.string()),
    values: v.array(v.object({
      analyte: v.string(),
      value: v.number(),
      unit: v.string(),
      referenceRange: v.string(),
      flag: v.optional(v.string())
    })),
    isPublic: v.boolean(),
    createdAt: v.number(),
    updatedAt: v.number()
  }).index('by_date', ['testDate']),

  reports: defineTable({
    slug: v.string(),
    title: v.string(),
    reportDate: v.string(),
    bodyRegion: v.string(),
    primaryFinding: v.string(),
    severity: v.union(v.literal('normal'), v.literal('mild'), v.literal('moderate'), v.literal('severe')),
    authoredBy: v.union(v.literal('self'), v.literal('provider'), v.literal('ai-assisted')),
    relatedImagingSlug: v.optional(v.string()),
    contentPath: v.string(),
    isPublic: v.boolean(),
    createdAt: v.number(),
    updatedAt: v.number()
  }).index('by_slug', ['slug']).index('by_date', ['reportDate']),

  appointments: defineTable({
    slug: v.string(),
    title: v.string(),
    provider: v.string(),
    startsAt: v.string(),
    durationMinutes: v.number(),
    location: v.string(),
    isVirtual: v.boolean(),
    reason: v.string(),
    bodyRegion: v.optional(v.string()),
    source: v.union(v.literal('manual'), v.literal('email-parsed'), v.literal('sms-parsed')),
    isPublic: v.boolean(),
    createdAt: v.number(),
    updatedAt: v.number()
  }).index('by_startsAt', ['startsAt']),

  access_log: defineTable({
    recordType: v.string(),
    recordSlug: v.string(),
    timestamp: v.number(),
    referrer: v.optional(v.string()),
    userAgentHash: v.string()
  }).index('by_record', ['recordType', 'recordSlug', 'timestamp'])
});
```

- [ ] **Step 3: Verify schema validates**

Run from `app/`:
```bash
npx convex codegen
```

Expected: no errors. Generated types appear in `convex/_generated/`.

- [ ] **Step 4: Commit**

```bash
git add app/convex/ app/package.json app/package-lock.json
git commit -m "[89a3] feat(convex): forward-looking schema (no v1 wiring) for imaging/results/reports/appointments/access_log"
```

---

## Task F2: Playwright smoke tests

**Files:**
- Modify: `app/playwright.config.ts` (already scaffolded)
- Create: `app/tests/smoke.spec.ts`

- [ ] **Step 1: Smoke test for every route**

Create `app/tests/smoke.spec.ts`:
```typescript
import { test, expect } from '@playwright/test';

const routes = [
  { path: '/', expectedHeading: 'Mario' },
  { path: '/imaging', expectedHeading: 'Imaging' },
  { path: '/imaging/cervical-mri-2026-05-06', expectedHeading: 'Cervical Spine MRI' },
  { path: '/results', expectedHeading: 'Results' },
  { path: '/reports', expectedHeading: 'Reports' },
  { path: '/reports/cervical-mri', expectedHeading: 'Cervical Spine MRI' },
  { path: '/appointments', expectedHeading: 'Appointments' },
  { path: '/appointments/spine-consult-2026-05-22', expectedHeading: 'Spine consultation' },
  { path: '/menu', expectedHeading: 'Menu' }
];

for (const route of routes) {
  test(`${route.path} renders`, async ({ page }) => {
    await page.goto(route.path);
    await expect(page.getByText(route.expectedHeading, { exact: false }).first()).toBeVisible();
  });
}

test('every page sets noindex meta', async ({ page }) => {
  for (const route of routes) {
    await page.goto(route.path);
    const meta = await page.locator('meta[name="robots"]').getAttribute('content');
    expect(meta).toContain('noindex');
  }
});

test('robots.txt disallows all paths', async ({ page }) => {
  const response = await page.goto('/robots.txt');
  const body = await response?.text();
  expect(body).toContain('Disallow: /');
});
```

- [ ] **Step 2: Run tests**

Run from `app/`:
```bash
npm run build
npx playwright install --with-deps  # if first time
npx playwright test
```

Expected: all tests PASS.

- [ ] **Step 3: Commit**

```bash
git add app/tests/smoke.spec.ts
git commit -m "[89a3] test(e2e): Playwright smoke tests for every v1 route + noindex/robots checks"
```

---

## Task F3: Accessibility audit

**Owner skill:** `accessibility-compliance:wcag-audit-patterns`

- [ ] **Step 1: Invoke the a11y audit skill**

Use the Skill tool to invoke `accessibility-compliance:wcag-audit-patterns`. Context for the skill:

> Audit `app/` (SvelteKit + shadcn-svelte v1 prototype). Run on each route listed in `app/tests/smoke.spec.ts`. Check WCAG 2.2 AA: keyboard navigation, focus indicators, ARIA roles, semantic HTML, color contrast on tokens (paper / paper-warm / ink / accent), text alternatives for icons, landmark regions.
>
> Specifically verify: AppHeader, BottomNav, ShareToggle (which is a button with aria-pressed), SectionRail and JumpToMenu (anchor navigation), CurrentFocusCard / UpcomingCard / SectionTile (links — verify they're proper anchors).

- [ ] **Step 2: Apply any fixes the audit recommends**

The audit will produce a list of findings. Apply fixes (focus rings, missing aria labels, contrast adjustments, etc.) in a follow-up commit:

```bash
git commit -m "[89a3] fix(a11y): apply wcag-audit-patterns findings"
```

---

## Task F4: Code review

**Owner agents:** `svelte-reviewer`

- [ ] **Step 1: Invoke svelte-reviewer**

Use the Task tool with subagent_type=`svelte-reviewer`. Context:

> Review the SvelteKit code in `app/` (v1 visual prototype). Focus on: component architecture (single responsibility, prop drilling), shadcn-svelte usage, Tailwind v4 token consistency, Svelte 5 runes idioms ($props, $state, $derived), mobile responsiveness, type safety, missing edge cases. Skip backend concerns (no Convex wiring in v1). Report only issues with significant impact — skip nitpicks.

- [ ] **Step 2: Apply review findings**

Implement any high-impact changes the reviewer flags:

```bash
git commit -m "[89a3] refactor(app): apply svelte-reviewer findings"
```

---

## Task F5: Final UI quality check

**Owner skill:** `web-design-guidelines`

- [ ] **Step 1: Invoke the skill**

Use the Skill tool to invoke `web-design-guidelines`. Context:

> Final UI quality pass on `app/` (v1 health portal visual prototype). Check against modern web interface guidelines: hierarchy, contrast, spacing, type rhythm, hover/focus states, responsive behavior, edge cases (long content, empty states), motion appropriateness, accessibility, error states.

- [ ] **Step 2: Apply findings**

```bash
git commit -m "[89a3] polish(app): apply web-design-guidelines findings"
```

---

## Task F6: Documentation update

**Owner skill:** `gsd-docs-update`

- [ ] **Step 1: Update root README**

Replace `/Users/louka2023/work/health/README.md` with a comprehensive version that documents the new structure:

```markdown
# health

Personal health portal — single repo for everything health-related.

## Layout

| Path | What | Deploys to |
|-|-|-|
| `app/` | health.louka.cc SvelteKit prototype (v1) | health.louka.cc (Vercel project "health") |
| `legacy/spine-app/` | Existing spine app (chiro tools + 3D viewer) | spine.louka.cc (Vercel project "spine", independent) |
| `legacy/old-experiments/` | Frozen early HTML experiments | not deployed |
| `reference/` | Markdown notes, PDFs, the chiro adjustment spreadsheet | not deployed |
| `docs/superpowers/` | Design specs + implementation plans | not deployed |
| `records/` | Original medical records (gitignored) | not deployed |

## Working with this repo

- **Commit prefix**: `[89a3]` (session ID) per global Claude convention
- **Push discipline**: commit locally as work progresses; never push until explicitly told
- **legacy/spine-app/ is frozen** — do not edit; it deploys via its independent Vercel project
- **app/** is the active v1 development surface

## Documents

- v1 design spec: `docs/superpowers/specs/2026-05-13-health-portal-v1-design.md`
- v1 implementation plan: `docs/superpowers/plans/2026-05-13-health-portal-v1-plan.md`
```

- [ ] **Step 2: Update root CLAUDE.md**

```markdown
# CLAUDE.md — health repo

## Conventions for this repo

- Commit prefix: `[89a3]` (session ID first 4 chars)
- Commit locally; push only when explicitly told
- Active work happens in `app/`
- `legacy/spine-app/` is frozen (deploys to spine.louka.cc via separate Vercel project — do not touch)
- Original radiology PDFs / DICOM go in `records/` (gitignored)

## Stack

SvelteKit v2 + Svelte 5 (runes) + Tailwind v4 + shadcn-svelte + TypeScript. Vitest + Playwright. Convex (deferred to v2). Vercel deploy.

## Helpful skills for this project

- `superpowers:brainstorming` → spec
- `superpowers:writing-plans` → implementation plan
- `superpowers:executing-plans` / `superpowers:subagent-driven-development` → execute
- `frontend-design:frontend-design` → visual exploration
- `svelte-ui-designer` / `svelte-ux-designer` → SvelteKit visual + UX
- `svelte-engineer` → implementation
- `svelte-reviewer` → code review
- `accessibility-compliance:wcag-audit-patterns` → a11y audit
- `web-design-guidelines` → final UI quality check
```

- [ ] **Step 3: Commit**

```bash
git add README.md CLAUDE.md
git commit -m "[89a3] docs: README + CLAUDE.md for the consolidated health repo"
```

---

## Task F7: Vercel deploy setup (manual, requires user)

**This task involves the user's Vercel account. Pause and walk through it with them.**

- [ ] **Step 1: Create new Vercel project linked to mlouka/health**

User goes to vercel.com → New Project → import `mlouka/health` → name it `health`. **Root Directory: `app/`**.

- [ ] **Step 2: Configure env vars**

For v1 (no Convex wiring), no env vars required.

- [ ] **Step 3: Deploy preview**

Vercel auto-deploys to `health-mlouka.vercel.app` (or similar). User verifies the deploy renders correctly at the preview URL.

- [ ] **Step 4: Assign domain**

In Vercel project settings → Domains → add `health.louka.cc`. Configure DNS at Cloudflare:
- `health.louka.cc` CNAME → `cname.vercel-dns.com`

- [ ] **Step 5: Verify production**

```bash
curl -I https://health.louka.cc/
curl -I https://health.louka.cc/reports/cervical-mri
curl https://health.louka.cc/robots.txt
```

Expected: 200 OK, noindex headers, robots.txt disallows.

- [ ] **Step 6: Confirm spine.louka.cc is unaffected**

```bash
curl -I https://spine.louka.cc/
curl -I https://spine.louka.cc/mri
```

Expected: both 200, spine app continues serving from `mlouka/spine` repo's independent Vercel project.

- [ ] **Step 7: (Optional) push the v1 commits**

ONLY when user explicitly says "push": run `git push origin main` from `/Users/louka2023/work/health`. Vercel auto-redeploys.

---

# Self-review (writing-plans skill instruction)

## Spec coverage

| Spec section | Plan task(s) |
|-|-|
| Top-level architecture | A4 (scaffold), D7 (layout), E2 (list pages) |
| Home dashboard | D4 (components), E1 (page) |
| `/imaging/[slug]` | E3 |
| `/reports/[slug]` (rich page) | E4 |
| `/results/[slug]` | E4 step 4 |
| `/appointments/[slug]` | E3 |
| Share + access model (visual only) | D3, used by E3/E4 |
| Visual design direction | B2 (tokens), B3 (frontend-design exploration), E1-E4 (apply visual) |
| Tech stack | A4, B1, F1 |
| Repo/file structure | A2, A3 |
| Agent assignments | inline per phase |
| Migration | A2, A3 (repo); E4 (MRI doc port) |
| Verification | F2, F3, F4, F5 |
| Known unknowns | not built; documented in spec |

## Placeholder scan

Search for "TBD", "TODO", "implement later", "Add appropriate", "Similar to" — none present. Each task contains complete code or exact commands.

One acceptable open item: Task E4 Step 2 says "Use a sub-agent for the port if helpful" — that's a delegation suggestion, not a placeholder. The instruction is concrete: port `legacy/spine-app/static/mri/index.html` body content to a Svelte component verbatim, anchored.

## Type consistency

- `BaseRecord` defined in `shared.ts` (C1) and consumed by all record types
- `formatStudyDate`, `formatRelativeTime`, `formatAppointmentTime` defined in C3 and used in D4 (`CurrentFocusCard`, `UpcomingCard`), D5 (`RecordCard`), E3, E4 — names consistent
- `imagingStudies`, `labPanels`, `reports`, `appointments` named consistently between C2 and the index.ts helpers
- `currentFocus()`, `nextUpcomingAppointment()`, `recentActivity()`, `countBySection()` defined in C2 step 5 and consumed in E1

## Scope

Single coherent project: build v1 visual prototype. No subsystem decomposition needed — phases are sequential dependencies, not independent subsystems.

---

# Execution handoff

**Plan complete and saved to `docs/superpowers/plans/2026-05-13-health-portal-v1-plan.md`.**

Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration. Best for this plan because:
- Many small tasks, each with clear acceptance criteria
- Several tasks delegate to specialized agents (svelte-engineer, frontend-design, svelte-reviewer, etc.) which naturally fit subagent dispatch
- Per-task review keeps context fresh
- The TPM agent named in the spec can coordinate

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints. Workable if you want to drive each step yourself or prefer to keep one session.

**Which approach?**
