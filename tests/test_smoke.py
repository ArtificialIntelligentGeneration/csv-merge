"""Smoke test — invoke the CLI's --help and assert it exits 0."""
import subprocess
import sys


def test_help_exits_zero():
    r = subprocess.run([sys.executable, "csv_merge.py", "--help"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "csv-merge" in r.stdout.lower() or "usage" in r.stdout.lower()
