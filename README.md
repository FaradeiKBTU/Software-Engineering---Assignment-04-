# Smart Campus Room Availability Checker (Assignment #04)

Python 3.9+ (tested on 3.13), standard library only. No installation of packages is needed.

## Install
```
cd smart_campus
python3 --version
```

## Run the app
```
python3 run.py 8000        # then open http://127.0.0.1:8000
```

## Run the tests (48 tests)
```
python3 -m unittest discover -s tests -t . -v
```
Baseline (my original Assignment #03 tests, 23 tests):
```
cd baseline && python3 -m unittest test_booking -v
```

## Structure
| Path | Responsibility |
|---|---|
| `src/smart_campus/models.py` | immutable `Room` type |
| `src/smart_campus/rooms_data.py` | fictional catalog (5 rooms), fixed current time 09:00 |
| `src/smart_campus/rules.py` | AC1-AC5, the only implementation of the rules |
| `src/smart_campus/filtering.py` | F1-F4 capacity / equipment / blocked / empty |
| `src/smart_campus/messages.py` | user-facing wording |
| `src/smart_campus/service.py` | strict input parsing, combines the layers (F5) |
| `src/smart_campus/server.py` | thin HTTP layer |
| `static/` | UI only (HTML, CSS, JS) |
| `baseline/` | Assignment #03 starting point: `booking.py`, `test_booking.py`, Bolt.new `roomChecker.ts` (project https://bolt.new/p/72186442) |
| `tests/test_a3_regression.py` | my 23 A3 tests run against the refactored rules |
| `docs/` | report, AI evidence, test logs, screenshots, diagrams |
