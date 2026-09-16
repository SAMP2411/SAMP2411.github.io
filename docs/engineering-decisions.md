# Portfolio redesign — engineering decisions

## Architecture

Static multipage HTML remains the deployment artifact. `scripts/build_site.py` reads reviewed `data/projects.json`, then renders all pages using shared templates. No client framework, CDN, router, CMS, analytics or hosting change is required. GitHub Pages continues publishing the repository root. Keep `.nojekyll`.

`site.css` defines the visual system; `refinements.css` holds composition refinements. `site.js` progressively enhances navigation, filters and native-dialog quick views. All text, projects, source links and case-study navigation are present without JavaScript. `scene.css`/`scene.js` enhance a repository-owned SVG robot workspace.

## Design rationale

Lead with identity and three established projects: TurtleBot3 navigation, embedded state-estimation infrastructure and UR10 manipulation. Distinguish ongoing work and simulation from completed implementation. Skill evidence points to projects instead of self-assigned proficiency bars. Case studies expose summaries first, with contribution, architecture, implementation, decisions and validation below.

Graphite surfaces, warm-white typography, restrained cyan actions and orange technical labels create a robotics-lab identity. The robot scene is explicitly conceptual, not fake live telemetry. A dimensional SVG/CSS scene was selected instead of WebGL to keep the runtime small and provide a static fallback.

## Accessibility and performance

- Semantic landmarks, native links, skip link, visible focus and labelled navigation.
- Native modal dialog, Escape close, focus restoration and safe text-based content insertion.
- Reduced motion, manual pause, offscreen and hidden-tab animation suspension.
- Eager hero content; lazy project media; explicit intrinsic image dimensions.
- No external font, icon, CSS or JavaScript requests at runtime.
- System fonts avoid font downloads and font-swap layout shifts.
- Separate full-size architecture diagrams with equivalent expandable text.

## Content corrections and preservation

All 13 projects and their existing routes remain. Objectives and detailed diagrams remain separate from hero images. The IIoT flow is corrected to source-backed local inference followed by MQTT alert publication, with offline Matplotlib analysis. Unsupported numerical accuracy/latency claims are not promoted. Johnson & Johnson is explicitly a Forage virtual job simulation under experience.

Incoming B. Braun work is labelled as planned for October 2026, not completed employment. The résumé is a printable web edition, not a purported original uploaded CV.

## Images

Original image blobs remain unchanged. Three industrial media files in the original main branch failed to decode. Existing valid 1600×900 variants were recovered from commit `835584084349e96809a81be2d7ac912b5d997ae3` under separate `-hd-v2.webp` names; old corrupt files remain unreferenced for preservation. Existing AI illustrations are labelled as illustrations. See `asset-audit.md` and `asset-manifest.json` for provenance and limitations.

## Research informing implementation

- https://www.nngroup.com/articles/how-people-read-online/
- https://www.nngroup.com/articles/progressive-disclosure/
- https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/showModal
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

These principles inform scannability, progressive disclosure, native interaction semantics and Pages reliability. They do not establish a universal recruiter scan time.

## Maintenance and rollback

1. Edit project data and shared templates.
2. Run `python3 scripts/build_site.py` and `python3 scripts/validate_site.py`.
3. Serve locally with `python3 -m http.server 8000`; run browser tests through npm or GitHub Actions.
4. Commit the generated HTML together with source changes.
5. Verify the Pages deployment and live routes.

The former mutating image/page generation workflow is replaced with read-only QA so it cannot overwrite the redesign. Legacy generator scripts remain for historical reference but are not used by CI.

Rollback branch: `backup-before-portfolio-redesign-2026-09-15`, original commit `d2efd1781c07c497fcd8147e38e4aae4f08fb66c`. Restore its tree with a new commit on main rather than deleting history or force-pushing.
