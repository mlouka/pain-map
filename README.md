# spine

Personal upper-cervical chiropractic record + 3D pain map. Deploys to **spine.louka.cc**.

## Layout

| Path | What | Tracked? |
|-|-|-|
| `app/` | SvelteKit + Convex + Threlte clinical-chart app. Its own git repo. Deploys to spine.louka.cc via Vercel. | Separate repo (this parent ignores it) |
| `legacy/` | Frozen vanilla-HTML predecessors. Reference only — not deployed. | Yes |
| `reference/` | Medical context, project docs, the printable chiro handout, and the script that generates it. | Yes |

## `app/` — the live application

```
cd app && npm install && npm run dev -- --host 0.0.0.0
```

Linked to Vercel project `v3` (`prj_07x0r1XRsCqfLG5IewcKrxFKH8PP`). Convex deployment slug `fleet-crab-984` (project name "spinemap" on team `mario-louka`).

## `legacy/`

| File | Was | Notes |
|-|-|-|
| `louka-nine.html` | original `index.html` deployed to louka-nine.vercel.app and pain-map-louka.vercel.app | Source of truth for porting the brachial-plexus guided tour into `app/`. More advanced than what's currently deployed at pain-map-louka. |
| `test-brachial.html` | API testbed proving 7 Sketchfab Viewer API capabilities (getNodeMap, setCameraLookAt, setUserInteraction, etc.) | Reference for porting layer toggles + camera lock |
| `shoulder-blade-pain-map.html` | older Desktop copy, simpler iframe-only approach | Superseded by `louka-nine.html` |
| `discover.html` | early exploration | Probably stale |

## `reference/`

| File | Purpose |
|-|-|
| `PROJECT-PROGRESS.md` | Comprehensive build log: chronological attempts, Sketchfab API discovery, model UIDs, world-coordinate decisions |
| `FINDINGS.md` | Medical findings notes |
| `Dorsal-Scapular-Nerve-Pain-Map.pdf` | Printable chiro-visit handout |
| `Mario Louka - Adjustment Sheet.xlsx` | Adjustment history spreadsheet |
| `scripts/make-chiro-pdf.py` | ReportLab generator for the handout PDF. Run with `python3 reference/scripts/make-chiro-pdf.py` — output goes to `reference/Dorsal-Scapular-Nerve-Pain-Map.pdf` |
| `docs/` | Superpowers brainstorming artifacts |

## Sketchfab models in use

The brachial plexus model UID `12e0591a2e794b159576510ddf61abae` (3D Atlas of Neurological Surgery, CC BY-SA) is the source for the "Pain Map" tab planned in `app/`. The guided tour data structure lives in `legacy/louka-nine.html` (search for `step.eye`, `step.target`, `step.detail`).
