#!/usr/bin/env python3
"""Offline CI entry point for the legacy written raw-recovery campaign."""

from recovery_campaign import validate


if __name__ == "__main__":
    raise SystemExit(0 if validate() else 1)
