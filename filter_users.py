"""Small, beginner-friendly user filtering tool.

This script is organized into small functions to make it easy to read
and test.

It follows simple best practices suitable for a junior developer:
clear function responsibilities, docstrings, simple input validation,
and a `main()` entry point.
"""

from typing import Any, Dict, List, Optional
import json
import sys


DEFAULT_USERS_FILE = "users.json"


def load_users(file_path: str = DEFAULT_USERS_FILE) -> List[Dict[str, Any]]:
    """Load and return list of users from given JSON file.

    Raises FileNotFoundError or json.JSONDecodeError on failure.
    """

    with open(file_path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def filter_users_by_name(
    users: List[Dict[str, Any]],
    name: str,
) -> List[Dict[str, Any]]:
    """Return users whose `name` matches the provided name.

    Comparison is case-insensitive.
    """

    name_lower = name.lower()
    return [u for u in users if str(u.get("name", "")).lower() == name_lower]


def filter_users_by_age(users: List[Dict[str, Any]], age: int) -> List[Dict[str, Any]]:
    """Return users whose `age` equals the provided age.

    Only integer ages are matched.
    """

    return [
        u
        for u in users
        if isinstance(u.get("age"), int) and u["age"] == age
    ]


def filter_users_by_email(
    users: List[Dict[str, Any]],
    email: str,
) -> List[Dict[str, Any]]:
    """Return users whose `email` matches the provided email.

    Comparison is case-insensitive.
    """

    email_lower = email.lower()
    return [u for u in users if str(u.get("email", "")).lower() == email_lower]


def print_users(users: List[Dict[str, Any]]) -> None:
    """Print users one per line in a readable format."""

    if not users:
        print("No users found.")
        return

    for user in users:
        # Simple, readable print for beginners
        line = (
            f"id: {user.get('id')}, "
            f"name: {user.get('name')}, "
            f"age: {user.get('age')}, "
            f"email: {user.get('email')}"
        )
        print(line)


def get_choice() -> Optional[str]:
    """Prompt the user for a filter choice and return it, or None on cancel."""

    choices = ("name", "age", "email")
    try:
        prompt = (
            "What would you like to filter by? "
            "(Enter 'name', 'age', or 'email'): "
        )
        choice = input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nInput cancelled.")
        return None

    if choice not in choices:
        print("Invalid choice. Please enter 'name', 'age', or 'email'.")
        return None
    return choice


def get_value_for_choice(choice: str) -> Optional[str]:
    """Get the filtering value from the user for the provided choice."""

    try:
        if choice == "name":
            return input("Enter a name to filter users: ").strip()
        if choice == "age":
            return input("Enter an age to filter users: ").strip()
        return input("Enter an email to filter users: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nInput cancelled.")
        return None


def main() -> None:
    """Main interactive flow: load data, prompt user, apply filter, print results."""

    try:
        users = load_users()
    except FileNotFoundError:
        print(f"Users file not found: {DEFAULT_USERS_FILE}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Users file is not valid JSON: {DEFAULT_USERS_FILE}")
        sys.exit(1)

    choice = get_choice()
    if not choice:
        return

    value = get_value_for_choice(choice)
    if value is None or value == "":
        print("No value provided; exiting.")
        return

    if choice == "name":
        results = filter_users_by_name(users, value)
    elif choice == "age":
        try:
            age = int(value)
        except ValueError:
            print("Please enter a valid integer for age.")
            return
        results = filter_users_by_age(users, age)
    else:
        results = filter_users_by_email(users, value)

    print_users(results)


if __name__ == "__main__":
    main()
