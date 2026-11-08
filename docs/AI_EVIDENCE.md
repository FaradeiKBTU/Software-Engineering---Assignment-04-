# AI Evidence Appendix - Assignment #04

| Item | Value |
|---|---|
| Tool / model | Claude Sonnet 5.5 (Claude Code session on claude.ai) |
| Date | 8 November 2026 |
| Student | Zhutanov Farkhat |

## Exchanges

| 1 | I sent Claude Sonnet 5.5 the Assignment #04 PDF and asked what I must do. | Claude summarised the 6 tasks, the deliverables, the e-mail subject rule and the deadline. | None found. | None. | I compared the summary with the PDF. |
| 2 | I sent my Assignment #03 report (AC1-AC6, function contract, issue log), then my real files booking.py, test_booking.py and the Bolt.new roomChecker.ts, and told Claude the constraints: one page, fictional data, no login or database, and the old rules must keep their exact meaning. | Claude analysed my real files and produced the risks R1-R5 and a refactoring plan. | An earlier draft assumed a reconstructed baseline; my real files already use named constants, so the duplication metric had to be redone. | I replaced the baseline with my original files and the metrics were recounted. | I ran my 23 A3 tests (23/23) and ran roomChecker.ts on key cases with Node 22 (results matched). |
| 3 | I asked Claude to build the room catalog and filters, split the code into modules and keep AC1-AC5 unchanged. | The code in src/smart_campus/* and static/*. | The first filter design hid blocked rooms. | Blocked rooms are now shown with status "blocked" (F3). | I read the code, ran the tests and opened the page at 360 px width. |
| 4 | I asked for at least 10 tests with boundary cases and one integration test, and to reuse my A3 tests. | 25 new tests, plus my 23 A3 tests run against the new rules, 48 in total. | 2 new tests failed on the first run because of wrong test data (570-630 overlaps the Sunset Lounge booking 600-660). | I changed the test interval to 560-590; the code was not changed. | I reran the suite: 48/48 OK, log in docs/test_run_final.txt. |
| 5 | I asked for the measurements: duplication and module structure. | Counts of rule implementations and constants, and a file listing. | Stray literals in the first version of the new code (1440 in a message, 540 + 60 in data). | Replaced with rules.MINUTES_PER_DAY and plain numbers. | I recounted: 12 to 6 rule implementations, 4 to 2 constant definitions. |

## Commands run (real)
```
python3 -m unittest discover -s tests -t . -v      -> Ran 48 tests ... OK
cd baseline && python3 -m unittest test_booking -v -> Ran 23 tests ... OK
```
Screenshots in `docs/img/` were taken with Playwright at 360 px width from the running app.

## Student's own verification
- I read every module and ran the commands above myself.
- I opened the app in my browser and tried 1e3, 0700, 660-720, 720-841 and a blocked room.
