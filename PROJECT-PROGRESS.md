# 3D Pain Map — Dorsal Scapular Nerve Visualization

## Project Goal
Create an interactive 3D anatomical visualization to help Mario explain his chronic shoulder blade pain to his upper cervical chiropractor. The pain is sharp, located at the medial border of the right scapula, worsens with right cervical rotation and neck extension, and is relieved ~70% of the time by upper cervical adjustment.

## Medical Context
- **Pain location**: Medial border of right scapula (inner edge of shoulder blade), rhomboid area
- **Pain type**: Sharp, nerve-like — NOT muscular
- **Aggravating motions**: Right cervical rotation, cervical extension (tilting neck up)
- **Likely cause**: Dorsal scapular nerve irritation originating from C3-C5 nerve roots
- **Nerve path**: Dorsal scapular nerve originates C3-C5 → pierces middle scalene muscle → descends under levator scapulae → runs along medial scapular border (innervating rhomboid major/minor)
- **Why upper cervical adjustment helps**: C1/C2 correction relieves compensatory strain at C3-C5, decompressing the dorsal scapular nerve root
- **The 70% success rate**: Sometimes the subluxation vector doesn't fully decompress that specific nerve root
- **Chiro script**: "Sharp nerve pain at the medial border of my right scapula, reproducing with right cervical rotation and extension. I believe it follows the dorsal scapular nerve distribution, originating from C3-C5 irritation secondary to upper cervical subluxation."

## Deployment
- **Live URL**: https://louka-nine.vercel.app
- **Vercel project**: louka/louka
- **Local path**: `/Users/louka2023/Desktop/pain-map/`
- **Git tag for safe revert**: `v1-mobile-responsive` (before custom annotations were added)
- **Local HTTP server was used for testing**: `python3 -m http.server 8765` from `/Users/louka2023/Desktop`

## Current State (latest deployed)
Single HTML file (`index.html`) with:
1. **Three switchable 3D models** via Sketchfab embeds:
   - **"Scapular Muscles + Nerves"** (PRIMARY) — 3D Atlas of Neurological Surgery model (UID: `eec158baf9ef45dba5d23a07d1f7d7e8`). Uses Sketchfab Viewer API to load model AND add 4 custom pain annotations programmatically
   - **"Spine + Nerves"** — Ebers "Nerves with a skeletal cross-section" (UID: `c6bde6cd35764f108dde933ad2c34142`). Simple iframe embed
   - **"Full Body Anatomy"** — Novaky "Male Anatomy - medical model" (UID: `4f706245d70a49c99bafb48e04b965e0`). Simple iframe embed
2. **Side panel** with pain explanation, legend (red/orange/blue/yellow dots), "why adjustment works ~70%" tip, and "tell your chiropractor" script
3. **Annotation toggle** (ON/OFF buttons) — for API model uses `hideAnnotation/showAnnotation`, for iframe models reloads with `ui_annotations=0/1`
4. **Mobile responsive** — stacked layout on <768px, collapsible info panel with "Show Info" toggle button, scrollable tabs, `100dvh` for iOS Safari
5. **Panel starts collapsed** on mobile for maximum 3D viewer space

## Custom Annotations on the Atlas Model (indices 41-44)
Added via Sketchfab Viewer API `createAnnotationFromWorldPosition()` using world coordinates discovered from existing annotations:

| # | Name | World Position [X,Y,Z] | Purpose |
|---|------|----------------------|---------|
| 41 | ⚠️ PAIN ZONE — Medial Scapular Border | [-75, -1135, -15] | Primary pain location — medial scapula, rhomboid area |
| 42 | ⚠️ PAIN ZONE (lower) — Rhomboid Area | [-85, -1100, -10] | Lower extension of pain down medial border |
| 43 | 🟠 Levator Scapulae Insertion | [-80, -1160, 20] | Secondary tension point at superior scapular angle |
| 44 | 🔵 NERVE ORIGIN — C3-C5 | [-28, -1210, 130] | Where dorsal scapular nerve originates |

### Coordinate System (Atlas model world space)
- X: lateral (more negative = more right/lateral)
- Y: vertical (more negative = lower on the body)
- Z: anterior-posterior (positive = anterior, negative = posterior)

### Key Reference Annotations (from the neurosurgeon, world coords)
| # | Name | World [X, Y, Z] |
|---|------|-----------------|
| 6 | Middle scalene m. | [-40, -1205, 119] |
| 8 | C5 | [-18, -1203, 140] |
| 20 | Dorsal scapular n. | [-40, -1123, 28] |
| 21 | Dorsal scapular a. | [-57, -1115, 21] |
| 22 | Supraspinatus m. | [-114, -1150, 67] |
| 23 | Infraspinatus m. | [-132, -1131, 33] |
| 24 | Teres minor m. | [-159, -1140, 20] |

### Full list of the model's 41 original annotations:
0: Brachiocephalic trunk, 1: Common carotid a., 2: Internal jugular v., 3: Vertebral a., 4: Thyrocervical trunk, 5: Anterior scalene m., 6: Middle scalene m., 7: Posterior scalene m., 8: C5, 9: C6, 10: C7, 11: C8, 12: Th1, 13: Superior trunk, 14: Middle trunk, 15: Inferior trunk, 16: Anterior division, 17: Anterior division, 18: Posterior division, 19: Suprascapular a., 20: Dorsal scapular n., 21: Dorsal scapular a., 22: Supraspinatus m., 23: Infraspinatus m., 24: Teres minor m., 25: Axillary n., 26: Posterior circumflex humeral a. and v., 27: Radial nerve (cut), 28: Thoracodorsal n. and a., 29: Long thoracic nerve, 30: Lateral pectoral n, 31: Medial pectoral n., 32: Bicep (and others truncated at 32+)

## What Was Tried (Chronological)

### Attempt 1: 2D Canvas Annotation on User's Image
- User provided a posterior anatomy muscle image and asked to circle the pain zone
- Created `/Users/louka2023/Desktop/shoulder-blade-pain-map.html` with an HTML canvas overlay
- Drew circles/labels on a dark background (silhouette) since we couldn't hotlink the original image
- **Result**: User said they didn't see an image — the canvas-drawn anatomy wasn't clear enough

### Attempt 2: Full 2D Canvas Anatomical Drawing
- Rewrote the file with a complete canvas-drawn posterior anatomy: trapezius, deltoids, lats, rhomboids, erector spinae, teres major, scapula outlines, spine vertebrae
- Added three annotation zones: red (pain), orange (levator scapulae), blue dashed (C3-C5 nerve origin)
- Blue dashed nerve path line from C3-C5 down to scapula with arrow
- Spine level labels (C1-T12)
- **Result**: User could see it but said the head looked off and proportions were wrong. Wanted 3D with Three.js

### Attempt 3: mannequin.js (Three.js Mannequin)
- Searched for free 3D human body models
- Found mannequin.js library — articulated human figure built on Three.js, available via CDN
- Fetched docs from `https://boytchev.github.io/mannequin.js/docs/userguide.html`
- Built full Three.js scene with: Male(1.80) mannequin, OrbitControls, CSS2DRenderer for labels, anatomical coloring via `man.recolor()`, three annotation zones (red rings, orange sphere, blue dashed ring), nerve path via CatmullRomCurve3 + TubeGeometry, spine labels, side indicator
- Import map: three@0.170.0 + mannequin-js@latest via jsdelivr CDN
- Initial marker positions: painMarker at (-0.08, 1.32, -0.10), etc.
- **Result**: Markers were floating in front of the body, not aligned. User could see this clearly

### Attempt 3b: Adjusted mannequin.js Positions
- Pushed markers back (Z: -0.10 → -0.16), shifted laterally (X: -0.08 → -0.14)
- Adjusted spine dots and labels
- **Result**: Still not aligned — the mannequin's rounded geometry made it impossible to place flat annotations accurately without raycasting. User said "All of your annotations are not even on the body"

### Attempt 4: Sketchfab Embedded Models (breakthrough)
User asked for a real skeleton/nerves model, suggested using a free 3D model. Searched extensively:

#### Models Discovered:
1. **University of Dundee "The Nervous System"** (UID: `2e6be1399756494b9f185ce8c5900911`) — CNS, spinal cord, vertebral column. CC BY-SA. NoAI tag. **Problem**: No scapulae or body context, just spine/brain
2. **UBC Medicine "Muscles of Upper Back"** (UID: `85159e313b434023ac044011ea752a10`) — Real plastinated cadaver scan, 6M triangles. Shows posterior shoulder muscles. 8 annotations. **Later removed** per user request
3. **AERO3D "Human Nervous and Cardiovascular System"** (UID: `0a9c32d586ba4493ae61f90af4fb102d`) — Full body, nervous + cardiovascular. User found this themselves. **Problem**: Doesn't show spine properly
4. **3D Atlas of Neurological Surgery "Scapular muscles"** (UID: `eec158baf9ef45dba5d23a07d1f7d7e8`) — **THE WINNER**. Skeleton + muscles + nerves (yellow) + arteries + veins. 550k triangles. 35 annotations from a neurosurgeon. Has the actual dorsal scapular nerve labeled (#20). CC BY-SA
5. **Ebers "Nerves with a skeletal cross-section"** (UID: `c6bde6cd35764f108dde933ad2c34142`) — Vertebral column with individual vertebrae visible, spinal nerves branching from each level. Skull cross-section. 5 annotations. Paid model but embeddable
6. **Novaky "Male Anatomy - medical model"** (UID: `4f706245d70a49c99bafb48e04b965e0`) — Complete anatomy study, 1.8M triangles, 19.7k views. Left side shows internals, right side has skin removed. Free, embeddable. System-based annotations

#### Sketchfab Viewer API Approach — First Attempt (Failed)
- Loaded Sketchfab Viewer API script v1.12.1
- Tried using `new Sketchfab(iframe)` → `client.init(uid, options)` for the Dundee nervous system model
- Added `createAnnotationFromWorldPosition()` calls in the `viewerready` callback
- Used relative offsets from `getCameraLookAt()` target
- **Result**: Model loaded via API but camera positioning was wrong (weird lateral angle). Annotations placed in wrong spots because coordinate system was unknown. Also the Dundee model had no scapulae

#### Sketchfab Simple Iframe Embed Approach (Worked)
- Switched to simple iframe embeds: `https://sketchfab.com/models/UID/embed?params`
- Embed params: `autostart=1&ui_theme=dark&ui_stop=0&ui_inspector=0&ui_watermark=0&ui_hint=0&ui_ar=0&ui_vr=0&ui_help=0&ui_settings=0&ui_annotations=1&scrollwheel=1&transparent=0&preload=1`
- Built tabbed interface with three models + side panel
- **Result**: All three models loaded and worked perfectly. Orbit/zoom/pan all functional. Built-in annotations clickable

#### Browser Testing via Chrome Automation
- Used Claude-in-Chrome MCP tools throughout for testing
- Started local server: `python3 -m http.server 8765` from Desktop
- Navigated to `http://localhost:8765/shoulder-blade-pain-map.html` (later `pain-map/index.html`)
- Sketchfab models needed a click to start despite `autostart=1` (Chrome autoplay policy)
- Verified all three model tabs worked: Atlas, AERO3D full body, UBC cadaver

#### User Found Embed Settings in Sketchfab
- User opened the Sketchfab embed dialog for the Novaky model
- Showed 4 tabs: General (wrench), Presentation, Buttons (eye), Annotations (pin)
- I guided settings: enable autostart, disable animated entrance, enable preload textures, dark theme ON, disable most UI buttons (help/settings/inspector/VR/AR/viewer stop), keep fullscreen + annotations
- Some options (remove watermark) were greyed out (paid feature)
- User didn't have time to apply all changes

### Attempt 5: Sketchfab Viewer API for Custom Annotations (Current)
User wanted custom pain zone annotations on the Atlas model specifically.

#### API Init Issue
- First attempt: API `client.init()` produced a blank/black viewer
- Root cause: Was setting `iframe.src = ''` before init, but API needs iframe with NO src attribute
- Fixed: Used `iframe.removeAttribute('src')` before calling `client.init()`
- Added fallback: If API fails, fall back to simple iframe embed
- **Result**: API loaded the model successfully on second attempt

#### Coordinate Discovery Process
1. Used `api.getAnnotationList()` to get all 41 annotation names — discovered the model already labels the dorsal scapular nerve (#20), middle scalene (#6), C5 (#8), etc.
2. Used `api.getAnnotation(index)` to get annotation details. Key fields: `name`, `content`, `position`, `eye`, `target`, `lastComputedWorldPosition`
3. **Critical discovery**: `position` field = scene coordinates, `lastComputedWorldPosition` = world coordinates. `createAnnotationFromWorldPosition` uses WORLD coordinates, not scene coordinates
4. First annotation placement used scene coordinates → annotations landed in the lumbar area (too low)
5. Re-fetched coordinates using `lastComputedWorldPosition` field
6. Recalculated all custom annotation positions relative to known landmarks
7. **Result**: Annotations now placed in the correct cervical/scapular region

#### Annotation Cleanup
- Added `removeAnnotation()` loop to clear custom annotations (indices >= 41) before adding new ones, preventing duplicates on page reload
- 300ms delay after removal before placing new annotations

### Vercel Deployment
- Installed Vercel CLI: `npm install -g vercel`
- Created project at `/Users/louka2023/Desktop/pain-map/` with `index.html`
- First deploy: `vercel --yes --name louka` → `https://louka-nine.vercel.app`
- Subsequent deploys: `vercel --prod --yes`
- Detected as static site (no framework), 12KB total
- Multiple deploys made for iterations

### Mobile Responsiveness
Added responsive CSS:
- `@media (max-width: 768px)`: topbar stacks vertically, main layout switches to column, viewer gets min-height 45dvh, panel becomes full-width with max-height 40dvh, collapsible with `.collapsed` class
- `@media (max-width: 380px)`: smaller fonts/padding for tiny phones
- Panel toggle button (`.panel-toggle`) only visible on mobile, positioned bottom-right
- Panel starts collapsed on mobile (JS checks `window.innerWidth <= 768`)
- Used `100dvh` (dynamic viewport height) for iOS Safari address bar handling
- Scrollable model tabs with hidden scrollbar (`-webkit-overflow-scrolling: touch`)
- `user-scalable=no` on viewport meta to prevent accidental zoom while interacting with 3D model

## Known Issues / TODO
1. **Custom annotation positions need fine-tuning** — Pain zone annotations (#41, #42) are close but slightly too anterior. Need to adjust Z coordinate to be more negative (more posterior) to sit on the back surface of the scapula rather than near the ribs
2. **Sketchfab autostart doesn't always work** — Chrome autoplay policy may require first user click. The API-loaded Atlas model seems more reliable than the simple iframe embed for this
3. **Annotation filtering is basic** — ON/OFF toggle only. Could add "relevant only" filter using keyword matching against annotation names (RELEVANT_KEYWORDS array exists in code but isn't wired up since we switched from full API to hybrid approach)
4. **The Ebers spine model is a paid model** — Embedding works but downloading won't
5. **Sketchfab embed settings weren't fully customized** — User ran out of time before applying the settings I suggested for the Novaky model embed dialog
6. **No custom domain** — Still on `louka-nine.vercel.app`

## Files
- `/Users/louka2023/Desktop/pain-map/index.html` — the single-file app (also deployed to Vercel)
- `/Users/louka2023/Desktop/pain-map/.vercel/` — Vercel config
- `/Users/louka2023/Desktop/shoulder-blade-pain-map.html` — older version (on Desktop, not in the pain-map project)

## Dependencies (CDN-loaded)
- Sketchfab Viewer API v1.12.1: `https://static.sketchfab.com/api/sketchfab-viewer-1.12.1.js`
- Sketchfab embed iframes load from `https://sketchfab.com/models/UID/embed`
- No npm dependencies, no build step, pure static HTML
