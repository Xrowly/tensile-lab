# Changelog

## [1.3.0] — 2026-11-06
### Fixed
- `compute_effective_dims` reads from props (not JSON), so CUSTOM-mode
  thickness edits now reach the mold. Previously the mold silently used
  the library value.

### Added
- Custom cavity depth (`Use Custom Cavity Depth`).
- Inline panel warning when cavity depth < specimen thickness.

## [1.2.0]
### Added
- Length scaling (XY-only by default, optional Z).
- Mold output (`Specimen` / `Mold` / `Both`).

## [1.1.0]
### Fixed
- ISO 527-2 radii corrected (24 mm / 60 mm).
- JIS K6251 mapped by ISO correspondence, not sequential guess.
- GOST 11262-80 given its own envelope.

### Added
- Load-time geometry feasibility validator.
- Source provenance in every library entry.

## [1.0.0]
- Initial release.
```

---

## License

MIT — see [LICENSE](LICENSE).

---

## Credits

Built for parametric modeling of standardized mechanical test specimens.
Dimensional data transcribed from the cited standard tables. Not endorsed by
ISO, ASTM, DIN, JIS, GOST, or Standards Australia.