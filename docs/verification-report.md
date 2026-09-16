# Release verification and handoff

Verified on 16 September 2026.

## Delivered release

- Live site: https://samp2411.github.io/
- Implementation commit: `38dba1a0253fac74efce456d9615f1a8f920f20c`.
- [Release regression: passed](https://github.com/SAMP2411/SAMP2411.github.io/actions/runs/35119941301).
- [GitHub Pages deployment: successful](https://github.com/SAMP2411/SAMP2411.github.io/actions/runs/35120177478).
- [Initial complete screenshot suite: passed](https://github.com/SAMP2411/SAMP2411.github.io/actions/runs/35070804270).
- Rollback branch: `backup-before-portfolio-redesign-2026-09-15`, original commit `d2efd1781c07c497fcd8147e38e4aae4f08fb66c`.

## Automated evidence

The suite covers 21 route visits at 390, 768 and 1440 CSS pixels, image decoding, browser errors, responsive overflow, axe WCAG A/AA checks, filters, quick views, keyboard focus, no-JavaScript content and the custom 404 page. Initial screenshots were inspected for desktop and mobile layout. Expanded keyboard tests found reverse-Tab escaping the project dialog; explicit wrapping corrected the behavior and the full release regression passed.

All 64 original image/SVG asset blobs match the baseline repository. Three corrupt published image references were replaced with valid existing historical variants under new filenames, preserving the original files. All 28 used image/SVG assets decoded successfully during verification.

## Live browser evidence

- Redesigned homepage, navigation and robotics scene rendered on the production domain.
- Pause motion changed to Resume motion with its pressed state active.
- Project explorer showed 13 projects; Industrial AI filtering reduced the set to four.
- IIoT quick view opened and linked to its full case study.
- The reviewed IIoT architecture SVG loaded at 1100 × 940 after navigating to architecture.
- Industrial Robot Operations Intelligence loaded its recovered hero image at 1600 × 900 from the new `-hd-v2.webp` path.
- Offscreen images remain lazy-loaded intentionally; automated route checks confirm decoding when brought into view.

## Architecture and maintenance

Content lives in `data/projects.json`; `scripts/build_site.py` generates static HTML and metadata. Local CSS and small progressive JavaScript provide responsive design, filters, dialogs and motion. There is no runtime framework, database or external asset dependency. GitHub Pages serves the repository root. Regenerate after content changes and run the documented validation before promoting future releases.

See [the complete plan and milestone tracker](../PROJECT_PLAN.md), [engineering decisions](engineering-decisions.md), [technical audit](technical-audit.md) and [asset audit](asset-audit.md).

## Boundaries

Automated accessibility checks are not a guarantee of universal accessibility; manual keyboard and visual checks supplement them. No Lighthouse score is claimed. The robotics scene is an SVG/CSS dimensional illustration, not a WebGL simulation. Existing upscaled AI imagery is labelled illustrative. No original CV PDF was available, so the résumé is a printable web edition. Original large photographs are preserved and lazy-loaded where appropriate; further lossy optimization is optional future work.
