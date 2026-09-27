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
| Browser regression | In progress | Release branch CI covers responsive overflow, accessibility, navigation, images, filters, layout persistence, preview Back/Escape and no-JS links |
| Deployment and live verification | Pending | Publish after regression checks, then verify public rendering and interactions |

## Verification and rollback

The existing browser suite is extended for Gallery persistence and preview Back/scroll/focus restoration. Its no-JavaScript check now accepts enhanced anchors because they remain working case-study links. The suite crawls reachable pages and checks 390, 768 and 1440px widths, with axe WCAG A/AA checks. Browser-only checks are run in GitHub CI because the local workspace has no browser executable.

Production baseline before this release: 785a96a85c6361bafcc329f8cefc3eb108f0775a. Rollback can restore the changed files from that commit in a new commit without deleting history. Planning artifacts remain on the separate planning branch.
