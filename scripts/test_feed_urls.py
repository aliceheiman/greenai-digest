#!/usr/bin/env python3
"""Test all RSS feed URLs to verify they are accessible."""

import urllib.request
import urllib.error
from time import sleep
import sys
import os

# Add parent directory to path to import feed_sources
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.collectors.feed_sources import get_all_feeds


def test_feed_url(url, name):
    """Test a single RSS feed URL."""
    try:
        # Use a complete browser User-Agent to avoid 403 errors from sites like The Lancet
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode("utf-8", errors="ignore")[:500]
            # Accept both standard RSS/Atom (<?xml) and RDF feeds (<rdf:RDF)
            if response.status == 200 and ("<?xml" in content or "<rdf:RDF" in content):
                return True, response.status, None
            else:
                return False, response.status, "No XML/RDF content found"
    except urllib.error.HTTPError as e:
        return False, e.code, f"HTTP Error: {e.reason}"
    except urllib.error.URLError as e:
        return False, 0, f"URL Error: {e.reason}"
    except Exception as e:
        return False, 0, str(e)


def main():
    """Test all RSS feeds from feed_sources.py"""
    feeds = get_all_feeds()

    print(f"Testing {len(feeds)} RSS feeds...\n")

    working = []
    broken = []

    for url, name, always_include in feeds:
        print(f"Testing: {name}...", end=" ")
        success, status, error = test_feed_url(url, name)

        if success:
            working.append((name, url))
            print(f"✓ OK (Status: {status})")
        else:
            broken.append((name, url, status, error))
            print(f"✗ FAILED")
            if error:
                print(f"  Error: {error}")

        sleep(0.5)  # Be polite to servers

    # Summary
    print("\n" + "=" * 70)
    print(f"SUMMARY")
    print("=" * 70)
    print(
        f"Working feeds: {len(working)}/{len(feeds)} ({len(working)/len(feeds)*100:.1f}%)"
    )
    print(f"Broken feeds:  {len(broken)}/{len(feeds)}")

    if broken:
        print("\n" + "=" * 70)
        print("BROKEN FEEDS - Need to be fixed or removed:")
        print("=" * 70)
        for name, url, status, error in broken:
            print(f"\n• {name}")
            print(f"  URL: {url}")
            print(f"  Status: {status if status else 'N/A'}")
            print(f"  Error: {error}")

    if working:
        print("\n" + "=" * 70)
        print(f"✓ {len(working)} feeds are working correctly")
        print("=" * 70)

    return 0 if not broken else 1


if __name__ == "__main__":
    exit(main())
