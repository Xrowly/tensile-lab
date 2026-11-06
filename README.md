[README.md](https://github.com/user-attachments/files/34501594/README.md)
# Tensile Lab
 ## ⚠️ DISCONTINUED — LEGACY PROJECT — USE AT YOUR OWN RISK
>
> **This project is discontinued.** It is a legacy codebase kept public for
> reference and archival purposes only. It is **not actively maintained**,
> **not supported**, and **not accepting issues or pull requests**.
>
> **It is known to be buggy.** Expect crashes, silent failures, incorrect
> geometry, and undocumented edge cases. Some bugs have been fixed in later
> versions; others have not. There is no guarantee that any specimen, mold,
> or scaling operation produces a physically correct result.
>
> **The dimensional data may be inaccurate.** Specimen dimensions in the JSON
> library have been transcribed from secondary sources and, in some cases,
> corrected against primary standard documents — but **not all entries have
> been independently verified**. Entries marked `verified: false`, and even
> some marked `verified: true`, may contain transcription errors, stale
> editions, or representational choices rather than the literal standard text.
>
> **DO NOT use this add-on for certification, compliance, or production
> work.** If you need specimen geometry for a regulated test, build it from
> the official standard document directly. Use this tool only as a rough
> starting point, a teaching aid, or a reference for how a parametric
> specimen generator might be structured.
>
> **No warranty. No support. No liability.** This code is provided under the
> MIT License, "as is", without warranty of any kind. You are solely
> responsible for anything you do with it. If it breaks your Blender file,
> produces a wrong specimen, or wastes your time — that's on you, not on the
> authors.
>
> If you want a maintained, verified tool for this job, look elsewhere.
> If you want to read a discontinued Blender add-on to learn from its
> architecture and mistakes, you're in the right place.
![Blender](https://img.shields.io/badge/Blender-3.6%2B-orange)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Beta-yellow)
![Version](https://img.shields.io/badge/Version-1.3.0-informational)

> Parametric tensile test specimen generator for Blender.
> 27 standard dog-bone specimens across ISO, ASTM, DIN, JIS, GOST, and AS/NZS.
> Data-driven JSON library. Optional mold output with configurable cavity depth.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [UI Reference](#ui-reference)
  - [Specimen Selection](#specimen-selection)
  - [Information](#information)
  - [Mode](#mode)
  - [Dimensions](#dimensions)
  - [Scaling](#scaling)
  - [Output](#output)
  - [Geometry](#geometry)
  - [Library](#library)
- [Workflows](#workflows)
  - [Plain Specimen](#plain-specimen)
  - [Scaled Specimen](#scaled-specimen)
  - [Simple Mold](#simple-mold-specimen-flush-with-cavity)
  - [Deep-Pocket Mold](#deep-pocket-mold-custom-cavity-depth)
- [JSON Library](#json-library)
  - [Structure](#structure)
  - [Adding a Specimen](#adding-a-specimen)
  - [Load-Time Validator](#load-time-validator)
- [Adding a New Geometry Type](#adding-a-new-geometry-type)
- [Verification Status](#verification-status)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Publishing to GitHub](#publishing-to-github)
- [License](#license)

---

## Features

- **27 standard specimens** across six families:
  - ISO 37, ISO 527-2 (Types 1A, 1B, 1, 1A, 2, 3, 4)
  - ASTM D638 (Types I–V), ASTM D412 (Die C)
  - DIN 53504 (S1, S1A, S2, S3, S3A)
  - JIS K6251 (No. 3, 5, 6, 7 — with correct ISO correspondence)
  - GOST 11262-80 (Types 1, 2, 3)
  - AS 1145.1:2001 (Types A, B)
- **Two geometry types**: `two_radius_symmetric` (ISO 37, ASTM D412, DIN, JIS, GOST T1) and `single_radius_symmetric` (ASTM D638, ISO 527-2, AS 1145).
- **Exact math** — arcs are solved from `(r_E + r_F)·(1 − cos α) = h` and `r·(1 − cos α) = h`, not approximated.
- **Length scaling** — scale by target overall length, XY-only by default, optional Z.
- **Mold output** — block with specimen cavity, with configurable margin, floor, and cavity depth.
- **Standard / Custom modes** — reference dimensions are protected; edits are flagged.
- **JSON library** — add specimens without touching Python.
- **Load-time validator** — geometrically infeasible entries are rejected before they reach the UI.
- **Source provenance** — every entry carries a `source.document` and `source.table` citation.
- **User library** — custom specimens persist across add-on updates.

---

## Installation

### From a release ZIP (recommended)

1. Download the latest `tensile_lab.zip` from the [Releases](https://github.com/Xrowly/tensile-lab/releases) page.
2. Open Blender → **Edit → Preferences → Add-ons**.
3. Click **Install…**, select the ZIP, and tick the checkbox next to **Tensile Lab**.
4. Press `N` in the 3D viewport → open the **Tensile Lab** tab on the right sidebar.

### From source (development)

```bash
git clone https://github.com/YOUR-USERNAME/tensile-lab.git
```

Then in Blender: **Edit → Preferences → Add-ons → Install…** → pick the cloned `tensile_lab` folder (Blender accepts folders, not just ZIPs). Or zip it yourself:

```bash
cd tensile-lab
zip -r tensile_lab.zip tensile_lab/
```

### Requirements

- Blender **3.6 LTS** or newer (tested on 4.x).
- No external Python packages.
- No internet connection required after installation.

---

## Quick Start

1. Open the **Tensile Lab** tab in the 3D viewport sidebar (`N`).
2. **Family**: pick `ISO`.
3. **Standard**: pick `ISO 37`.
4. **Specimen**: pick `Type 2`.
5. Click **Generate**.

You have a 75 mm dog-bone in the scene. The panel shows the specimen's ID, edition, source table, and verification status.

To make a mold instead:

1. Scroll to the **Output** box.
2. Click **Mold**.
3. Click **Generate** again.

You now have a rectangular block with the specimen shape cut into its top face.

---

## UI Reference

The panel is organized top-to-bottom into eight boxes. This section documents each one.

### Specimen Selection

```
┌─ Specimen Selection ─────────────┐
│ Family:    ISO                    │
│ Standard:  ISO 37                 │
│ Specimen:  Type 2                 │
└───────────────────────────────────┘
```

Three cascading dropdowns populated from the JSON library.

- Changing **Family** re-populates **Standard**.
- Changing **Standard** re-populates **Specimen**.
- Changing **Specimen** auto-loads its dimensions into the Dimensions box.

The specimen dropdown's tooltip shows the standard number, specimen type, category, and description.

### Information

Read-only summary of the selected specimen:

```
ID:          ISO37_TYPE2
Standard:    ISO 37 (2024)
Type:        Type 2
Geometry:    two_radius_symmetric
Source:      ISO 37:2024 / Table 2
Status:      ✓ Verified
Description: Standard rubber dumbbell...
```

If `source.verified` is `false` in the JSON, the status line reads **UNVERIFIED** with a question-mark icon instead.

### Mode

```
○ Standard    ● Custom
```

- **Standard** — Dimensions box is read-only. The specimen's reference values are protected.
- **Custom** — Dimensions box is editable. Any change flags the specimen as `CUSTOM / MODIFIED`.

Switching back to **Standard** restores the reference values immediately.

### Dimensions

Shows only the fields the selected geometry actually uses. For `two_radius_symmetric`, you see:

- Overall Length
- End Width
- Narrow Length
- Narrow Width
- Radius E (inner)
- Radius F (outer)
- Thickness
- Arc Segments

For `single_radius_symmetric`, you see:

- Overall Length
- End Width
- Narrow Length
- Narrow Width
- Transition Radius
- Thickness
- Arc Segments

The panel hides irrelevant fields automatically — you never see `radius_e` when editing an ASTM D638 specimen.

### Scaling

```
┌─ Scaling ─────────────────────────┐
│ [ ] Enable Scaling                │
│     Target Length:  100.0 mm      │
│     Factor: x1.333 (base 75.0 mm) │
│     Effective thickness: 2.000 mm │
│ [ ] Scale Z (thickness)           │
│     (Save as Custom uses base)    │
└───────────────────────────────────┘
```

When **Enable Scaling** is off, all scaling controls are greyed out and the specimen uses its library dimensions unchanged.

When **Enable Scaling** is on:

- `factor = target_length / base_overall_length`
- All XY dimensions are multiplied by `factor`
- Thickness is multiplied by `factor` **only if** **Scale Z (thickness)** is also on
- The panel displays the factor and effective thickness so you can confirm before generating

Scaling is a **generation-time transform only**. It does not modify the JSON library, and **Save as Custom** always writes the base (unscaled) values.

### Output

```
┌─ Output ──────────────────────────┐
│ [ Specimen ] [ Mold ] [ Both ]    │
└───────────────────────────────────┘
```

Three exclusive buttons:

| Mode | Produces |
|---|---|
| **Specimen** | One solid specimen object |
| **Mold** | One rectangular block with a cavity cut from the top face |
| **Both** | Two separate objects — the specimen and its mold |

When **Mold** or **Both** is active, additional controls appear:

```
│ Mold Margin:  5.0 mm              │
│ Mold Floor:   2.0 mm              │
│ [ ] Use Custom Cavity Depth       │
│     Cavity Depth:  10.0 mm        │
```

- **Mold Margin** — wall thickness around the specimen in X and Y.
- **Mold Floor** — solid material below the cavity.
- **Use Custom Cavity Depth** — off by default. When off, cavity depth equals specimen thickness (exact fit). When on, cavity depth equals the **Cavity Depth** field, and the block auto-extends downward to keep **Mold Floor** solid below the cavity.

See [Deep-Pocket Mold](#deep-pocket-mold-custom-cavity-depth) for a worked example.

### Geometry

```
[ Generate ]          Adds a new object (or two in Both mode)
[ Update Selected ]   Rebuilds the active specimen/mold
[ Reset to Standard ] Restores the reference dimensions
```

**Update Selected** works on any object carrying a `tensile_role` property. In **Both** mode, the two objects update independently — select the one you want to refresh.

### Library

```
│ Name: [ Custom 3mm ]              │
│ [ Save as Custom ]                │
│ [ Delete Custom Specimen ]        │
│ [ Reload Library ]                │
```

- **Save as Custom** — appends the current base dimensions to the user library as a new specimen under the same standard. The library entry's ID gets a `_CUSTOM` suffix.
- **Delete Custom Specimen** — removes the selected specimen from the user library, but only if it was created as a custom entry. Bundled specimens cannot be deleted.
- **Reload Library** — re-reads both the bundled and user JSON files from disk.

Custom specimens are stored in Blender's user-config directory and survive add-on updates:

- **Linux**: `~/.config/blender/<version>/config/tensile_lab/user_library.json`
- **macOS**: `~/Library/Application Support/Blender/<version>/config/tensile_lab/user_library.json`
- **Windows**: `%APPDATA%\Blender Foundation\Blender\<version>\config\tensile_lab\user_library.json`

The bundled reference library ships inside the add-on ZIP and lives at `tensile_lab/data/specimen_library.json`.

---

## Workflows

### Plain Specimen

The default path.

1. Pick Family / Standard / Specimen.
2. Ensure **Mode = Standard** and **Output = Specimen**.
3. Click **Generate**.

Result: one object, dimensions exactly as in the JSON.

### Scaled Specimen

Get a 150 mm specimen from the 75 mm ISO 37 Type 2.

1. Pick ISO 37 Type 2.
2. In **Scaling**: tick **Enable Scaling**, set **Target Length = 150**.
3. Leave **Scale Z** off (thickness stays 2 mm).
4. Click **Generate**.

The panel shows `Factor: ×2.000` and `Effective thickness: 2.000 mm` before you click. The object's X dimensions are 2× the base; the thickness is unchanged.

Tick **Scale Z** to make the thickness 4 mm as well.

### Simple Mold (specimen flush with cavity)

1. Pick a specimen.
2. **Output = Mold**.
3. Leave **Use Custom Cavity Depth** off.
4. Click **Generate**.

Result: a block with a cavity whose depth exactly equals the specimen thickness. The specimen (if you also generate it via **Both**) sits flush in the cavity, its top surface level with the mold's top face.

### Deep-Pocket Mold (custom cavity depth)

You want a 2 mm specimen in a mold whose cavity is 10 mm deep, so the specimen sits at the top of a pocket with 8 mm of air below it.

1. Pick ISO 37 Type 2 (thickness 2 mm).
2. **Output = Mold**.
3. Tick **Use Custom Cavity Depth**.
4. Set **Cavity Depth = 10.0**.
5. Click **Generate**.

Result: cavity 10 mm deep. Block height = `10 + mold_floor` = 12 mm. Specimen sits in the top 2 mm; 8 mm of empty cavity below; 2 mm of solid floor under that.

If you set **Cavity Depth** smaller than the specimen thickness, the panel shows a red warning row and **Generate** refuses with:

```
Error: cavity depth (5.000 mm) < specimen thickness (10.000 mm); specimen would not fit
```

This is intentional. The specimen must fit inside the cavity, or the mold is not a mold of that specimen.

---

## JSON Library

### Structure

The library is a single JSON file at `tensile_lab/data/specimen_library.json`:

```json
{
  "version": "1.3",
  "specimens": [
    {
      "id": "ISO37_TYPE2",
      "standard": "ISO",
      "standard_number": "ISO 37",
      "edition": "2024",
      "specimen_type": "Type 2",
      "name": "ISO 37 Type 2",
      "category": "Rubber",
      "description": "Standard rubber dumbbell.",
      "geometry": "two_radius_symmetric",
      "dimensions": {
        "overall_length": 75.0,
        "end_width": 12.5,
        "narrow_length": 25.0,
        "narrow_width": 4.0,
        "radius_e": 8.0,
        "radius_f": 12.5,
        "thickness": 2.0
      },
      "settings": { "arc_segments": 32, "unit": "mm" },
      "source": {
        "document": "ISO 37:2024",
        "table": "Table 2",
        "page": 6,
        "verified": true
      },
      "library": { "type": "official_reference", "editable": false }
    }
  ]
}
```

### Required Fields

| Field | Type | Notes |
|---|---|---|
| `id` | string | unique across the whole library |
| `standard` | string | family name (e.g. `"ISO"`) |
| `standard_number` | string | full number (e.g. `"ISO 527-2"`) |
| `specimen_type` | string | type designation (e.g. `"Type 1A"`) |
| `geometry` | string | one of the registered geometry identifiers |
| `dimensions` | object | numeric values, keys depend on geometry |

### Recommended Fields

| Field | Purpose |
|---|---|
| `edition` | distinguish `GOST 11262-80` from `GOST 11262-2017` |
| `name` | human-readable label (defaults to `specimen_type`) |
| `category` | material class (Rubber, Plastic, Foam, Metal) |
| `description` | shown in tooltip and Information box |
| `settings.arc_segments` | default arc resolution |
| `settings.unit` | defaults to `"mm"` |
| `source` | document, table, page, verified — **strongly recommended** |
| `library.type` | `"official_reference"` or `"custom"` |

### Adding a Specimen

You can add specimens two ways.

**Option 1 — UI:** pick an existing specimen, edit its dimensions in Custom mode, then click **Save as Custom**. The new entry goes into your user library (`user_library.json` in Blender's config dir).

**Option 2 — edit the JSON:** open `tensile_lab/data/specimen_library.json`, add an object to the `specimens` array, save, then click **Reload Library** in the panel.

Either way, the new specimen appears in the cascade:

1. Its `standard` becomes a Family option (or is added to an existing Family).
2. Its `standard_number` becomes a Standard option.
3. Its `specimen_type` becomes a Specimen option.

No Python changes required — as long as the specimen reuses a registered `geometry` and only uses dimensions that already exist as PropertyGroup fields.

### Load-Time Validator

On `load_library()`, every specimen passes two validations:

**Schema validation** — required fields present, types correct, geometry identifier registered.

**Feasibility validation** — for each specimen, the validator recomputes the tangent angle `α`, the transition length, and the required overall length. If the transition doesn't fit inside `overall_length / 2`, the specimen is **rejected** with a printed reason and never reaches the UI:

```
[TensileLab] REJECTED ISO527-2_2012_TYPE1B: transition (15.63 mm/side)
does not fit inside overall_length=170
```

This is what prevents broken dimensions from silently producing a malformed mesh. Add a specimen to the JSON with dimensions that don't close, and it will simply not appear in the dropdowns — instead of building a broken shape.

---

## Adding a New Geometry Type

If a standard needs a topology that `two_radius_symmetric` or `single_radius_symmetric` cannot represent (e.g., multi-radius, rectangular with shoulders, plate with a central hole), add a generator:

1. **Create** `tensile_lab/geometry/generators/my_geometry.py` with:

   ```python
   from ..outline import build_my_outline

   DIMENSION_KEYS = (
       "overall_length",
       "end_width",
       # ... only the dimensions your geometry consumes
   )

   def build_outline(dims, arc_segments=32):
       return build_my_outline(dims, arc_segments)
   ```

2. **Implement** the outline builder in `tensile_lab/geometry/outline.py` — must return a closed CCW list of `(x, y)` tuples.

3. **Register** it in `tensile_lab/geometry/generators/__init__.py`:

   ```python
   from .my_geometry import build_outline as _build_my, DIMENSION_KEYS as _MY_KEYS

   GENERATORS = {
       "two_radius_symmetric":    (_build_two_radius,    _TWO_RADIUS_KEYS),
       "single_radius_symmetric": (_build_single_radius, _SINGLE_RADIUS_KEYS),
       "my_geometry":             (_build_my,            _MY_KEYS),
   }
   ```

4. **If you introduced new dimension names**, add matching `FloatProperty` fields to `TensileLabProperties` in `properties/specimen.py` and append the keys to `ALL_DIMENSION_KEYS` in `core/constants.py`.

5. **Add specimens** to the JSON using `"geometry": "my_geometry"`.

The parameter panel auto-discovers `DIMENSION_KEYS` from the generator — no UI changes needed.

---

## Verification Status

The bundled library is a **mix** of verified and unverified entries. The `source.verified` flag in each specimen reflects the level of confidence:

| Standard family | Status | Notes |
|---|---|---|
| ISO 37 | ✓ Verified | Table 2, tolerances included |
| ISO 527-2 | ✓ Verified | Radius corrected to 24 / 60 mm |
| ASTM D638 | ✓ Verified | Types I–V, all radii transcribed |
| ASTM D412 | ✓ Verified | Die C, matches ISO 37 Type 1 envelope |
| DIN 53504 | ✓ Verified | S1 outer radius 20 mm (differs from ISO) |
| JIS K6251 | ✓ Verified | Correct ISO correspondence (No. 3↔1A, No. 5↔1, No. 6↔2, No. 7↔4) |
| GOST 11262-80 | ✓ Verified | Own envelope (115 / 150 / 250 mm), not ISO 527-2 |
| AS 1145.1:2001 | ✓ Verified | Identical in principle to ISO 527-1:1993 |

Every entry in the bundled library carries `verified: true` **with a source citation**. If you transcribe new entries from summaries or secondary sources, set `verified: false` until you've checked the primary standard document.

> **Warning.** Some standards specify tolerances (± 0.1 mm, ± 1 mm, etc.) or minimum dimensions (`≥ 115 mm`) rather than single nominal values. The JSON uses representative nominals. **Do not use this library as the sole reference for certification work.** Cross-check against the official standard document and, if in doubt, mark the entry `verified: false`.

---

## Architecture

```
tensile_lab/
├── __init__.py              add-on entry point
├── core/
│   ├── config.py            paths, defaults
│   ├── constants.py         dimension key list
│   └── registry.py          in-memory specimen index
├── data/
│   ├── json_loader.py       load bundled + user libraries
│   ├── json_validator.py    schema + feasibility checks
│   └── specimen_library.json  the library itself
├── geometry/
│   ├── arc.py               arc sampling
│   ├── tangency.py          α solvers for two-radius / single-radius
│   ├── symmetry.py          mirror, dedupe
│   ├── outline.py           profile builders
│   ├── mesh.py              extrude + object creation
│   ├── mold.py              block + cavity boolean
│   └── generators/
│       ├── __init__.py      GENERATORS registry
│       ├── two_radius.py    wrapper for two_radius_symmetric
│       └── single_radius.py wrapper for single_radius_symmetric
├── properties/
│   └── specimen.py          TensileLabProperties (all UI fields)
├── operators/
│   ├── generate.py          Generate
│   ├── update.py            Update Selected
│   ├── reset.py             Reset to Standard
│   └── library.py           Save / Delete / Reload
└── interface/
    ├── selectors.py         Family / Standard / Specimen dropdowns
    ├── parameters.py        Dimensions / Scaling / Output boxes
    └── panel.py             the top-level N-panel
```

Nothing in `geometry/`, `data/`, or `properties/` imports from `interface/`. The UI depends on the core, never the reverse. That's what makes the geometry engine testable outside Blender.

---

## Troubleshooting

### "No library" in the Family dropdown

The JSON file failed to load. Open Blender's system console (**Window → Toggle System Console** on Windows, or check the terminal on Linux/macOS) and look for `[TensileLab] Failed to load`. The path to the JSON is printed. Common causes:

- The JSON has a syntax error (missing comma, unescaped quote)
- All entries were rejected by the validator (check for `[TensileLab] REJECTED` lines)

### "Cavity depth < specimen thickness" error

You ticked **Use Custom Cavity Depth** but set a value smaller than `Thickness`. Either increase **Cavity Depth** or decrease **Thickness**. The panel shows a red warning row above the button when this state is active.

### "Unknown geometry identifier"

You added a JSON entry with a `"geometry"` value that isn't registered in `GENERATORS`. Check `geometry/generators/__init__.py`.

### "transition does not fit inside overall_length"

The specimen's radii and width differences produce a transition longer than the straight section allows. Either the `overall_length` is too short or the radii are too large. The validator will print the required length. This is a **data error**, not a code error — fix the JSON.

### Generate works but the mesh is inverted / inside-out

The Boolean cut failed silently. Check the system console for `[TensileLab] Mold boolean failed`. This is rare with the `EXACT` solver, but if it happens, try regenerating. If it persists, the outline is likely self-intersecting — check for a specimen where `narrow_length > overall_length` or similar.

### Custom specimens disappear after updating the add-on

They don't — they live in `user_library.json` under Blender's config dir, not in the add-on folder. Click **Reload Library** after re-enabling the add-on.

### The panel shows "UNVERIFIED" for a specimen

The `source.verified` flag is `false` in the JSON. This is intentional for entries transcribed from secondary sources. Don't assume it means the specimen is wrong — it means the transcription hasn't been checked against the primary document.

