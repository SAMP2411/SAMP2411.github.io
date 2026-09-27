# Portfolio architecture and wireframe review

Status: planning only. These drawings are not production pages or final visual designs. They use grayscale intentionally; colors, typography and image art direction are the next stage. The main branch and live website must remain unchanged by this planning work.

## Review the drawings

- [Desktop, 1440px](desktop-wireframe.svg)
- [Mobile, 390px](mobile-wireframe.svg)
- [Project preview: desktop panel and mobile screen](project-preview-wireframe.svg)

## Architecture

One primary homepage: identity → complete project collection → experience → about → contact. Primary navigation: Work, Experience, About, Résumé. Skills are demonstrated within project and experience content. Existing detailed pages retain their URLs and remain optional depth.

All 13 projects appear in one collection, without pagination. The three recommended starting projects are marked in that collection rather than repeated above it. Overview is the default; Gallery is an optional alternate presentation of the same data. Filters and selected view remain stable when opening and closing a project.

The desktop drawing annotates recruiter questions beside the introduction. That annotation is review material, not proposed website copy. Experience rows are schematic groupings; implementation must retain individual employers, roles, dates and the separate virtual-simulation designation.

## Proportions and content

Desktop: 48px main gutter at 1440px, four 325px entries with 16px gaps in the initial wireframe. At narrower widths reduce columns before squeezing titles. Mobile: 20px main gutter and one 350px entry. Media placeholders use 4:3 framing. Final components should grow with text, not clip it to fixed heights. Gallery uses 16:10 media and fewer columns.

Titles, one-sentence purpose and scope must stay readable. Scope distinguishes hardware/simulation/software/ongoing work. The overview drawing uses category labels as placeholders; visual-design stage must accommodate both category and scope without creating a badge wall. Abbreviated display titles in wireframes do not rename project URLs or full case-study titles.

No new assets are required. Use real photographs/screenshots where available, retain diagrams separately, and label conceptual imagery. B. Braun remains unpublished.

## Project preview interaction contract

1. View project opens a desktop side panel or mobile full-screen panel.
2. Show title, scope, representative image with provenance, problem, personal contribution, validation boundaries and source link.
3. Full case study remains an explicit secondary-depth destination.
4. Close, Escape or browser Back returns to the collection with focus and scroll position restored.
5. Trap keyboard focus while the modal panel is open; background is inert. Maintain a visible close button.
6. A copied project URL opens the equivalent case study or addressable preview. No-JavaScript links open the case study directly.
7. No hover-only information, nested panels, scroll hijacking or automatic animation.

## Recruiter evaluation — proposed tests, not measured results

- Ten-second scan: identify target role, technical focus, degree and résumé action.
- Thirty-second task: locate one mobile robotics project and explain why it is relevant.
- Two-minute technical review: identify personal contribution and validation evidence.
- Browse three projects, then return to the same position without re-finding the collection.
- Repeat core tasks with keyboard and a 390px viewport.

Human testing has not occurred. Wireframe review by the assistant is not a substitute for independent recruiter feedback.

## Review decisions

Approve the section order and overview/preview model first. Then design one polished desktop and mobile concept, using actual project content. Review the longest titles and weakest images before building other pages. Only after visual approval should implementation begin.

## Milestones

| Stage | Status | Gate |
|---|---|---|
| Information architecture | Proposed and documented | Review structure |
| Desktop/mobile wireframes | Prepared | Review density and flow |
| Preview interaction | Specified, not implemented | Review navigation model |
| Polished visual direction | Not started | Approve wireframes first |
| Interactive prototype | Not started | Approve visual direction |
| Implementation/deployment | Not authorized in this planning stage | Explicit instruction to proceed |

## References

Research references, not templates to copy: https://brittanychiang.com/ ; https://www.adhamdannaway.com/ ; https://petertarka.com/ ; https://bruno-simon.com/ ; https://www.rleonardi.com/interactive-resume/ . Their project budgets were not verified.

## Review checkpoint — 27 September 2026

Desktop and mobile drawings reviewed locally for title wrapping, spacing and completeness. All 13 project entries are represented. Preview drawing reviewed separately. These remain non-interactive low-fidelity wireframes, with no user testing or final visual-design approval claimed. Planning files are isolated on the `planning/portfolio-architecture` branch; production files are not changed.
