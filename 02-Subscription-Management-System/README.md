[README_subscription_manager.md](https://github.com/user-attachments/files/31669087/README_subscription_manager.md)
# Subscription Manager

A simple command-line membership system for a gym/club, built to practice
object-oriented design in Python.

## What it does

- Lets you register members as **Basic** ($200) or **Premium** ($500)
- Validates input (name must not be a number, age must be 16+)
- Tracks all members and a running total count
- Lets you view all registered members from a simple text menu

## Why it's built this way

- **Inheritance**: `BasicMember` and `PremiumMember` both extend a shared
  `Member` base class, so validation logic lives in one place instead of
  being duplicated.
- **Class-level state**: `Member.names` and `Member.total_members` are
  shared across all subclasses via `classmethod`, so the system always
  has a single source of truth for "who is registered" — regardless of
  which subclass created them.
- **Fail-fast validation**: invalid names/ages raise `ValueError` in
  `__init__`, so a bad member object can never be created in the first
  place.

## Run it

```bash
python subscription_manager.py
```

## Possible next steps

- Persist members to a file/database instead of in-memory storage
- Add an "edit" or "cancel membership" option
- Add unit tests for the validation logic
