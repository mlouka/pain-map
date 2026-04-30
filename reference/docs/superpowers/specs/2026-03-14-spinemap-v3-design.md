# SpineMap V3 — Clinical Pain Intelligence

**Date:** March 14, 2026
**Domain:** back.louka.cc
**Stack:** SvelteKit + Tailwind + shadcn-svelte + Threlte + Convex + Vercel

---

## Purpose

Patient intelligence dashboard for Mario Louka's cervical spine condition. Combines a 3D model of his actual spine (from CBCT scan), radiology findings, adjustment history across two providers, nerve corridor analysis, and a visit logging portal — into a single clinical tool.

Primary audience: Mario (99% of views) and his two chiropractors (Dr Park at UC Spine Care, Dr Rickards at Rickards Chiropractic).

## Routes

| Route | Purpose | Who uses it |
|-|-|-|
| `/` | Full dashboard — 3D viewer + tabbed clinical panel | Mario, either chiro on desktop |
| `/ucspinecare` | Visit log input form for Dr Park's clinic | Receptionist or Dr Park |
| `/rickards` | Visit log input form for Dr Rickards' clinic | Receptionist or Dr Rickards |

## Layout

### Desktop (`/`)
- **Left panel (50%):** 3D spine viewer (dark background, Threlte/Three.js)
  - Loads `spine.glb` — Mario's actual cervical spine from CBCT, decimated to ~80-150k faces
  - Layer toggles: Bone (default), Nerves (approximate overlay), Pain regions, Labels
  - Camera presets: Lateral, Posterior, C5 Closeup
  - Orbit/zoom/pan controls
  - Label: "CBCT · Feb 2026 · Dr Park"
- **Right panel (50%):** Tabbed clinical panel (light background)
  - Tabs: Findings, Imaging, History, Nerves, Log Visit

### Mobile (`/`)
- **Top:** 3D viewer (touch to orbit)
- **Bottom:** Same tabs, scrollable content
- Log Visit tab is the quick-log form (no separate route needed)

### Provider routes (`/ucspinecare`, `/rickards`)
- Clean, focused input form only
- Fields: Date, Adjustments (free text), LLI (fraction + side), Pain before/after, Notes
- Provider name pre-filled based on route
- Submit saves to Convex
- No dashboard, no clinical data — just the input

## Theme

- **Light mode primary** (default)
- **Dark mode** toggle available
- **Color scheme:** Blues and blacks
  - Primary: `#1e3a5f` (deep navy)
  - Accent: `#3b82f6` (blue-500)
  - Alert/pain: `#dc2626` (red-600) / `#ef4444` (red-500)
  - Success: `#22c55e` (green-500)
  - Warning: `#f59e0b` (amber-500)
  - Background: `#f0f2f5` (light) / `#0a0f1a` (dark)
  - Surface: `#ffffff` (light) / `#111827` (dark)

## Tab Content

### Findings
- **Alert card:** C5 Compression Fracture Deformity (from radiology report, Dr Robert Haynes, Feb 17 2026)
  - "Irregularity and anterior marginal spur, superior endplate of C5. Minor disc narrowing C4-C5."
- **Key result card:** 9 → 4-5 /10 scapular pain after C5 adjustment (Mar 13, Dr Park)
- **Current pain levels:** Scapular (4-5), Deltoid (2), Biceps (0) — horizontal bar visualization
- **Primary complaint:** Right medial scapular border, constant dull ache + nerve pain on right head rotation

### Imaging
- Annotated X-ray panels (zoomable images from Synapse Mobility screenshots)
- Cervical: lateral, AP, open-mouth views
- Lumbar: lateral, AP views
- Source annotations on each image

### History
- Adjustment log table: Date, Adjustments, Provider, Result
- C5 adjustments highlighted in red
- Pattern analysis box: C3 PRI frequency, C5 rarity but highest result, PIL every Rickards visit
- Data from both Convex (new entries) and static seed data (Dr Rickards Excel history)

### Nerves
- C5-C6 Corridor breakdown
- Four nerve cards with color dots:
  - Dorsal Scapular Nerve (C5) — red — scapular pain
  - Suprascapular Nerve (C5-C6) — amber — deep shoulder pain
  - Axillary Nerve (C5-C6) — blue — deltoid radiation
  - Musculocutaneous Nerve (C5-C7) — purple — biceps radiation
- "Why Head Position Triggers Pain" explanation box
- Clicking a nerve highlights exit point on 3D model (stretch goal)

### Log Visit
- Date (defaults to today)
- Provider selector (Dr Park / Dr Rickards)
- LLI: fraction input + side (Left/Right)
- Adjustments: free text textarea
- Pain before/after: number inputs /10
- Notes: optional textarea
- Save button → Convex mutation

## Data Model (Convex)

### visits table
```
{
  date: string,           // "2026-03-14"
  provider: string,       // "park" | "rickards"
  adjustments: string,    // "C5 right side up"
  lli_value: string?,     // "1/2"
  lli_side: string?,      // "Right"
  pain_before: number?,   // 0-10
  pain_after: number?,    // 0-10
  notes: string?,
  created_at: number      // timestamp
}
```

### Seed data
Dr Rickards' adjustment history (from Excel) loaded as initial records.

## 3D Pipeline

1. Existing OBJ (1.9M vertices) → Open3D quadric decimation → ~80k faces
2. Export as GLB with vertex normals
3. Serve from `/static/spine.glb`
4. Threlte loads via `<GLTF>` component
5. Bone material: warm ivory/cream tone matching Dr Park's golden renders
6. Camera: OrbitControls, preset positions for lateral/posterior/C5 views

## Listing Notation Reference

- **PRI** — Posterior Right Inferior
- **ARS** — Anterior Right Superior
- **ALS** — Anterior Left Superior
- **PIL** — Posterior Inferior Left (cervical adjustment direction)
- **IQ** — Inferior Quarter
- **LLI** — Leg Length Inequality (inches, indirect atlas indicator)

## Files Structure

```
pain-map/
  src/
    routes/
      +page.svelte          # Main dashboard
      +layout.svelte        # App shell, theme toggle
      ucspinecare/
        +page.svelte        # Dr Park input form
      rickards/
        +page.svelte        # Dr Rickards input form
    lib/
      components/
        SpineViewer.svelte   # Threlte 3D viewer
        FindingsTab.svelte
        ImagingTab.svelte
        HistoryTab.svelte
        NervesTab.svelte
        LogVisitTab.svelte
        ProviderForm.svelte  # Shared form for provider routes
      data/
        seed-visits.ts       # Dr Rickards Excel data as static array
        findings.ts          # Radiology findings, nerve data
      stores/
        theme.ts             # Light/dark toggle
  static/
    spine.glb               # Decimated 3D model
    xrays/                   # X-ray images (copied from Chiro folder)
  convex/
    schema.ts               # Convex schema
    visits.ts               # Queries and mutations
  tailwind.config.ts
  svelte.config.js
```

## Future (not today)

- Claude AI chat (Anthropic SDK) querying Convex data
- DICOM re-processing with better thresholding for higher quality 3D model
- Nerve path overlays on 3D model (approximate tubes from C5-C6 exit points)
- Multi-patient generalization (ChiroTouch competitor direction)
- 2016 vs 2026 angle comparison overlay
- PDF export for insurance documentation
