#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Re-check every quote in rows.yaml against the page it came from.

Exit codes
  0  every quote was found
  1  at least one quote is gone from a page that loaded
  2  no quote was missing, but at least one page could not be read (e.g. HTTP 403)

A quote that disappears is the signal: the vendor moved, renamed or dropped a
control and the row needs a fresh quote from the page.
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
)
TAG = re.compile(r"(?is)<(script|style)\b.*?</\1>")
HTML = re.compile(r"(?s)<[^>]+>")
SPACE = re.compile(r"\s+")


def normalise(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u00a0", " ")
    return SPACE.sub(" ", text).strip().casefold()


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=45) as response:
        body = response.read().decode("utf-8", "ignore")
    body = TAG.sub(" ", body)
    body = HTML.sub(" ", body)
    return normalise(body)


def main() -> int:
    data = yaml.safe_load((ROOT / "rows.yaml").read_text(encoding="utf-8"))
    sources = data.get("sources", {})
    pages: dict[str, str | None] = {}
    missing: list[str] = []
    unreadable: list[str] = []

    for row in data["rows"]:
        name = row["source"]
        url = sources[name]
        if name not in pages:
            try:
                pages[name] = fetch_text(url)
                print(f"read    {name}: {url}")
            except urllib.error.HTTPError as error:
                pages[name] = None
                unreadable.append(f"{name} (HTTP {error.code}): {url}")
                print(f"unread  {name}: HTTP {error.code} {url}")
            except Exception as error:  # noqa: BLE001 - any failure means unverified
                pages[name] = None
                unreadable.append(f"{name}: {error}")
                print(f"unread  {name}: {error}")

        text = pages.get(name)
        if text is None:
            continue
        if normalise(row["quote"]) in text:
            print(f"ok      {row['control']}")
        else:
            missing.append(f"{row['control']} -> {url}")
            print(f"MISSING {row['control']} -> {url}")

    print()
    if missing:
        print(f"{len(missing)} quote(s) no longer on the page they came from:")
        for line in missing:
            print(f"  - {line}")
        print("Copy the new sentence from the page into rows.yaml, with the URL and today's date.")
        return 1
    if unreadable:
        print("Every readable page still carries its quote. These pages could not be read:")
        for line in unreadable:
            print(f"  - {line}")
        print("Open them in a browser and update their rows by hand.")
        return 2
    print(f"All {len(data['rows'])} quotes confirmed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
