#!/usr/bin/env python3
# ruff: noqa: I001
"""Compatibility entry point for ``python -m historykinetic.e6``."""

from historykinetic.e6.__main__ import main


if __name__ == "__main__":
    raise SystemExit(main())
