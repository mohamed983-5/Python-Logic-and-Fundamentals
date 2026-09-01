[README_session_tracker.md](https://github.com/user-attachments/files/31669037/README_session_tracker.md)
# Session Tracker

A small script that reconstructs "who is currently logged in, on which
machine" from a raw, unordered list of login/logout events.

## What it does

- Takes a list of `Event` objects (timestamp, type, machine, user)
- Sorts them chronologically, since events may arrive out of order
- Replays them in order to build a per-machine set of currently
  logged-in users
- Prints a clean report of active users per machine

## Why it's built this way

- **Sorting before processing**: events aren't guaranteed to arrive in
  time order, so the first step is always to sort by timestamp — this
  avoids subtle bugs where a logout is processed before its login.
- **Set per machine**: using a `set` for each machine's users makes
  "add on login / remove on logout" a natural, efficient operation and
  avoids duplicate entries.
- **Separation of concerns**: parsing/state-building (`current_users`)
  is kept separate from presentation (`generate_report`), so either can
  be changed independently.

## Run it

```bash
python session_tracker.py
```

## Possible next steps

- Handle a logout event with no matching prior login gracefully
- Read events from a log file instead of a hardcoded list
- Add timestamps to the report output
