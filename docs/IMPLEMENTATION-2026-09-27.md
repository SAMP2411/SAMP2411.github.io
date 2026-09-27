# Cyber portfolio implementation

## Goal and architecture

Deliver the approved scan-first portfolio while retaining the dark cyber identity, existing project imagery and stable case-study URLs. The homepage contains identity, the full project collection, experience, an About section with expandable capabilities, and contact. Existing detailed pages remain available.

The Python generator renders static HTML from the existing project JSON. CSS controls a four/three/two/one-column responsive overview and optional gallery. Framework-free JavaScript progressively enhances ordinary project links into a native modal dialog: a desktop side panel and a mobile full-screen view. No image generation or runtime dependencies were added.

Preview content comes from the same project source as the case studies: scope, objective, contribution, validation, outcome, provenance and source links. Text is inserted through textContent. Filters and view selection are URL parameters. Opening a preview adds a history entry; Back, Close and Escape return to the collection and restore focus and scroll. Direct project URLs work without JavaScript, and modified clicks preserve ordinary link behavior.

Images retain their originals. Compact overview thumbnails use a 4:3 frame, gallery images use 16:9, and preview images use contain to retain the full subject. No fixed-height text clipping is used. B. Braun remains commented out in source and excluded from generated public HTML. No new personal details were added.

## Milestones

| Milestone | Status | Evidence |
| --- | --- | --- |
| Architecture and wireframes | Complete | docs/planning on planning/portfolio-architecture |
| Cyber visual concept | Approved | User authorized implementation and publication on 2026-09-27 |
| Implementation | Complete | Generator, refinements.css, site.js and generated pages |
| Local static checks | Passed | Build: 21 documents / 13 case studies; validator: 20 reachable pages, 52 assets, zero errors; JavaScript syntax check |
| Browser regression | Passed | GitHub Actions run 36325562184: responsive overflow, accessibility, navigation, images, filters, layout persistence, preview Back/Escape and no-JS links |
| Deployment and live verification | Complete | Pages run 36325672108 succeeded; public filter, preview, Back, Gallery/Overview and all 13 images verified |

## Verification and rollback

The existing browser suite is extended for Gallery persistence and preview Back/scroll/focus restoration. Its no-JavaScript check now accepts enhanced anchors because they remain working case-study links. The suite crawls reachable pages and checks 390, 768 and 1440px widths, with axe WCAG A/AA checks. Browser-only checks are run in GitHub CI because the local workspace has no browser executable.

Production baseline before this release: 785a96a85c6361bafcc329f8cefc3eb108f0775a. Rollback can restore the changed files from that commit in a new commit without deleting history. Planning artifacts remain on the separate planning branch.


## Release evidence

- Application commit: `39c8cb74db0827eebe7394a7b95c8efbf601b3c1`.
- [Passing regression run](https://github.com/SAMP2411/SAMP2411.github.io/actions/runs/36325562184).
- [Successful Pages deployment](https://github.com/SAMP2411/SAMP2411.github.io/actions/runs/36325672108).
- [Live collection](https://samp2411.github.io/index.html#projects).
- [Captured live layout](qa/cyber-explorer-live.jpg).
- Live Embedded filter returned two projects. Opening Distributed State Estimation displayed its scope, contribution, validation, provenance and source link. Browser Back closed the panel and preserved the selected filter. Gallery and Overview toggled correctly. All 13 images reported successful decoding with original intrinsic widths (887–3000px).

Verification limits: automated browser coverage is Chromium; this is not a substitute for testing every Safari/device combination or a recruiter user study. The collection intentionally scrolls; fitting all 13 readable cards above the fold is not a requirement. Existing images were retained, not regenerated or sharpened artificially.
