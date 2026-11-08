I gave Claude Sonnet 5.5 the assignment PDF, my Assignment #03 report with the acceptance criteria AC1-AC6, and the constraints: one page, fictional data, no login or database, and the old rules must keep their exact meaning. I asked for a repository map, risks and a plan before any code.

Useful suggestions: one rules module as the single source of truth, immutable rooms so bookings cannot change, a strict whole-number parser that rejects 1e3 and 0700, and a thin UI that only displays what the service returns. The first version of my F5 tests was wrong: I used 570-630 for "free in Sunset Lounge", but it overlaps Sunset's 600-660 booking. The failing test pointed at the test data, not the rule code, so I corrected the interval to 560-590. I also changed the first filter design, which hid blocked rooms, so blocked rooms are shown with a "blocked" status instead and can never be "available".

What I checked myself: I ran all 48 tests (including my 23 original A3 tests) and the A3 suite on its own, counted rule implementations and constants, opened the page at 360 px width and confirmed there is no sideways scroll, and compared the same time in two rooms. I did not trust a passing test run on its own, since A3 showed that logic tests can pass while the UI is wrong.

Tests drove two decisions: moving all parsing into service.py, and keeping the 120 vs 121 and touching vs overlapping cases as explicit tests during the refactor.

Next I would add a real browser test, store bookings in a file, and let the UI show the reason for each filtered-out room.
