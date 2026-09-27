# Cyber portfolio visual concept

Status: visual review ready, 2026-09-27. Static compositions, not interactive screenshots. Production is unchanged.

## Review files

- [Desktop, 1440px](cyber-desktop-concept.webp)
- [Mobile, 390px](cyber-mobile-concept.webp)
- [Project preview content](cyber-preview-concept.webp)

Keep the existing dark cyber identity, cyan accents and project images. No new image assets were generated. Illustrative imagery must retain provenance labels and must not imply photographic evidence of constructed hardware.

## Architecture

The homepage contains identity, all 13 projects, experience, about and contact. Recommended projects appear first within the collection. Navigation anchors lead to sections; existing case-study URLs remain valid. Project data remains in data/projects.json, HTML in the existing Python build pipeline, styling in existing CSS and interactions in progressive JavaScript. No framework migration is needed.

Overview is the default collection view; Gallery offers larger imagery. Category filters and view state persist while opening and closing project previews. Desktop previews use a side panel, mobile previews use a full-screen dialog. The separate preview composition specifies content hierarchy, not the final panel width. Direct links continue to work without JavaScript. Back and Escape close the preview and restore focus and scroll.

## Dimensions and implementation rules

| Element | Proposed rule |
| --- | --- |
| Desktop canvas | 1440px reference; 32px side gutters; max content width 1440px |
| Overview grid | 4 columns wide desktop, 3 laptop, 2 tablet, 1 narrow mobile |
| Overview cards | 332 × 208px desktop reference; 350 × 208px mobile reference; height grows for text zoom |
| Grid spacing | 16px gaps; consistent 16px card inset |
| Overview images | 88 × 66px, 4:3 crop; preserve subject visibility |
| Gallery images | 16:9 region; use existing originals and responsive sources |
| Hero | Unboxed name; natural letter spacing; no trailing square |
| Colors | Background #080f17, surface #101c28, border #26394a, text #edf4f7, muted #a5b6c6, cyan #7ee4eb |
| Touch controls | Implementation target at least 44px; static concept buttons are 40px |
| Text | Implement readable body text, flexible wrapping and 200% zoom; small mockup labels are indicative |

All 13 projects are available on one page; they will require scrolling at ordinary viewport heights. Avoid claiming all cards fit above the fold. Content takes priority over rigid card heights. Use supplied images at sufficient intrinsic resolution; upscaling cannot recover missing detail.

## Recruiter walkthrough (design review, not user testing)

Identity and specialization are explicit in the hero. Résumé and contact are visible immediately. The collection exposes the breadth of work with one primary action per card. The preview puts problem, contribution and validation ahead of secondary detail. Scope labels distinguish simulation, hardware, software and work in development. Experience wording and all project claims must be reconciled against existing source content before implementation. B. Braun stays excluded from public output.

## Milestones and acceptance gates

| Milestone | Status | Evidence / completion gate |
| --- | --- | --- |
| M1 Architecture and low-fidelity structure | Approved | Prior planning README and three wireframes |
| M2 Cyber visual concept | Complete for review | Three rendered compositions and this specification |
| M3 Visual approval | Pending | User accepts visual direction or requests revisions |
| M4 Local implementation | Pending | Responsive collection, filters, preview, navigation and documentation |
| M5 Verification | Pending | Keyboard and focus behavior, mobile/desktop checks, no-JS links, image clarity, content audit and build pass |
| M6 Publish and verify | Pending | Authorized main update, deployment completes, live commit and representative pages verified |

Efficient execution: batch local edits, perform one focused verification pass, resolve only concrete failures, then publish a consolidated change. Do not generate assets or repeat research without a specific unresolved decision.

## Reproduce

Run `python3 docs/planning/build_visual_concept.py` from the repository with Pillow and DejaVu fonts installed. The script uses the current project data and existing local imagery. These files are review artifacts only and must not replace the production website.
