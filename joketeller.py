#!/usr/bin/env python3
"""joketeller – fetch and display a random joke.

This script contacts https://v2.jokeapi.dev/ and prints a single‑line joke.
It uses only the Python standard library for maximum portability.
"""

import json
import sys
import urllib.error
import urllib.request
from typing import Any, Dict

API_URL = "https://v2.jokeapi.dev/joke/Any?type=single"


def fetch_joke() -> str:
    """Request a joke from the JokeAPI.

    Returns
    -------
    str
        The joke text.

    Raises
    ------
    RuntimeError
        If the request fails or the response cannot be parsed.
    """
    try:
        with urllib.request.urlopen(API_URL, timeout=10) as response:
            if response.status != 200:
                raise RuntimeError(f"Unexpected HTTP status: {response.status}")
            data_bytes = response.read()
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error while contacting JokeAPI: {e.reason}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}") from e

    try:
        payload: Dict[str, Any] = json.loads(data_bytes.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise RuntimeError("Failed to decode JSON response") from e

    if payload.get("error"):
        raise RuntimeError(f"JokeAPI reported an error: {payload.get('message')}")

    joke = payload.get("joke")
    if not isinstance(joke, str):
        raise RuntimeError("Unexpected response structure – missing 'joke' field")
    return joke.strip()


def main() -> None:
    try:
        joke = fetch_joke()
        print(joke)
    except RuntimeError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
