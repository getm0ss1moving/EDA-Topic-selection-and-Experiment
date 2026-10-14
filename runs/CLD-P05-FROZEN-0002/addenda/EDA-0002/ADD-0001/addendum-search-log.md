# EDA-0002 addendum search log (ADD-0001)

Times are true UTC on 2026-10-13, computed as host clock + 54,000 s (see `evidence-addendum.md` E1). Query numbering continues from round 0 (Q01-Q27).

## Inputs for this run

- The human owner's acquisition note `EDA_Source_Access_Guide.md`, checked 2026-10-13. It is used only as a list of URLs and access hints. Its topic summaries were checked against the primary pages; it states no novelty verdict and none was taken from it.
- Public GitHub repository state for the PR #13 transport check (`transport-check.md`).

## Queries and retrievals

| ID | Time | Engine / route | Query or target | Result | Used as |
|---|---|---|---|---|---|
| Q28 | 10:41 | curl | `https://www.eecg.toronto.edu/~najm/papers/dac11-sari.pdf` | Timed out after 150 s; a retry over IPv4 showed the proxy tunnel established and the TLS handshake timing out | Access failure |
| Q29 | 10:41 | curl | `tauworkshop.com/2018/contest.html`, `/2018/slides/TAU18_Contest.pdf`, `/2019/contest.html`, `/2019/slides/TAU%202019%20Contest.pdf` | HTTP 200 for all four; the slide SHA-256 values match the access guide | SRC-053 to SRC-056 |
| Q30 | 10:42-10:46 | WebFetch (twice), curl to the `eecg.utoronto.ca` alias, Wayback availability API | Same PDF | WebFetch timed out (60 s and 300 s); alias connection timed out; availability API returned HTTP 429 | Access failures |
| Q31 | 10:47 | Wayback raw capture `web.archive.org/web/2024id_/…/dac11-sari.pdf` | Same PDF | HTTP 200; redirected to capture 20240203144300; 284,451 bytes; 6 pages | SRC-012 (full) |
| Q32 | 10:54 | Crossref API | `works/10.1145/2024724.2024899` | Title, authors, pages 777-782 and date 2011-06-05 match; 21 citing works | SRC-012 metadata |
| Q33 | 10:54 | Semantic Scholar API | Citations of `DOI:10.1145/2024724.2024899` (limit 100) | 23 citing works, titles screened | Expansion 3 |
| Q34 | 10:54-10:55 | WebSearch (3 queries) | NIO (ICSICT 2014); One-for-All (ICCAD 2024); FACT (MLCAD 2024) | No relevant hits for any of the three | None |
| Q35 | 10:55 | Semantic Scholar API (single-paper GETs; one earlier batch request returned HTTP 429) | The same three DOIs | Abstracts for One-for-All and FACT; NIO abstract withheld by the publisher | SRC-057, SRC-058; U10 |

## Expansion 3 (forward, from SRC-012)

Inclusion rule: titles indicating multi-corner or PVT timing analysis or reduction. Of 23 citing works, 6 were included (see `evidence-addendum.md` § 3). Excluded by title as not about multi-corner STA methods: process sensors, clock-skew minimization under interconnect variation, hold fixing by buffer insertion or metal segments, FPGA routing, GPU-accelerated STA, setup/hold characterization, ML for OCV libraries or multiple-input switching, and SoC design.

Limitations:

- Screening was at title level except for two abstracts.
- Forward citations of SRC-013, SRC-016 and SRC-017 were not searched.
- Google Scholar was not attempted.

## Stop rationale for this run

Both access-guide items are resolved: SRC-012 in full text, and the TAU 2018/2019 topics from official summaries. One forward expansion was documented. The run stops because the human's request (check the transport and use the access guide) is satisfied. It does not stop on search exhaustion: the residual items U10 and the forward citations of SRC-013, SRC-016 and SRC-017 are carried forward.
