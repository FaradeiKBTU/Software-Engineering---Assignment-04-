# AI Evidence Appendix - Assignment #04

| Item | Value |
|---|---|
| Tool / model | Claude Sonnet 5.5 (Claude Code session on claude.ai) |
| Date | 8 November 2026 |
| Student | Zhutanov Farkhat |

## Exchanges

| # | Key prompt (summary) | AI output used | Problems found | Change made | How I checked |
|---|---|---|---|---|---|
| 1 | Sent the Assignment #04 PDF and asked "what must I do" | Summary of the 6 tasks, deliverables, e-mail subject rule, deadline | none | none | compared with the PDF |
| 2 | Sent my A3 report, then my real `booking.py`, `test_booking.py` and Bolt `roomChecker.ts` | Analysis of the real files, risks R1-R5, plan | an earlier draft assumed a reconstructed baseline with literals repeated in page text; the real files already use named constants, so the metric was redone | baseline replaced by my originals, metrics recounted | ran my 23 A3 tests (23/23), ran `roomChecker.ts` on key cases with Node 22 (results matched) |
| 3 | Build catalog + filters, split into modules, keep AC1-AC5 | `src/smart_campus/*`, `static/*` | first filter design hid blocked rooms | blocked rooms shown with status "blocked" (F3) | read the code, ran tests, opened the page at 360 px |
| 4 | Write 10+ tests incl. boundaries and one integration test; reuse my A3 tests | 25 new tests + my 23 A3 tests rerun on the new rules = 48 | 2 tests failed on first run because of wrong F5 test data (570-630 overlaps Sunset 600-660) | test interval changed to 560-590; code untouched | rerun: 48/48 OK, log in `docs/test_run_final.txt` |
| 5 | Measure duplication and structure | counts of rule implementations and constants | stray literals (1440 in a message, `540 + 60` in data) in my own first code | replaced with `rules.MINUTES_PER_DAY` and plain numbers | recounted by reading and grep: 12 -> 6 rule implementations, 4 -> 2 constants |

## Commands run (real)
```
python3 -m unittest discover -s tests -t . -v      -> Ran 48 tests ... OK
cd baseline && python3 -m unittest test_booking -v -> Ran 23 tests ... OK
```
Screenshots in `docs/img/` were taken with Playwright at 360 px width from the running app.

## Student's own verification
- I read every module and ran the commands above myself.
- I opened the app in my browser and tried 1e3, 0700, 660-720, 720-841 and a blocked room.
