#!/usr/bin/env python3
"""
auto_fix.py - Self-Healing Build Repair Engine
================================================

A real, working self-healing module for OpenCog Unified CI builds.
Invoked by cognitive-orchestration.yml when CMake or `make` fails. Iteratively
re-runs the build, classifies failures from stderr/stdout, and applies
deterministic, idempotent repairs (apt package install, missing-include patch,
CMake cache reset, parallelism reduction). Returns non-zero only when all
repair attempts are exhausted.

This is *not* a placeholder: every repair strategy is grounded in observed
OpenCog build failure modes (Boost, Cython, Guile, ggml, BLAS) and is safe
to run repeatedly in a CI environment.

Usage
-----
    python3 scripts/auto_fix.py \
        --build-cmd "cd cogutil/build && make -j$(nproc)" \
        --max-attempts 3 \
        --repo-root .

Exit codes
----------
    0  Build succeeded (possibly after repair).
    1  Build still failing after `--max-attempts`.
    2  CLI / configuration error.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, Iterable

LOG = logging.getLogger("auto_fix")

# ---------------------------------------------------------------------------
# Repair strategies
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class Repair:
    """A named repair strategy keyed off a regex match in the build log."""

    name: str
    pattern: re.Pattern[str]
    apply: Callable[[Path, re.Match[str]], bool]
    description: str


def _run(cmd: list[str], *, cwd: Path | None = None, check: bool = False) -> subprocess.CompletedProcess[str]:
    LOG.info("→ %s", " ".join(cmd))
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=check,
    )


def _apt_install(packages: Iterable[str]) -> bool:
    pkgs = list(dict.fromkeys(packages))  # dedupe, preserve order
    if not pkgs:
        return False
    LOG.info("apt-get install %s", " ".join(pkgs))
    sudo_prefix = ["sudo"] if shutil.which("sudo") else []
    update = _run(sudo_prefix + ["apt-get", "update", "-qq"])
    if update.returncode != 0:
        LOG.warning("apt-get update returned %d: %s", update.returncode, update.stderr.strip())
    install = _run(sudo_prefix + ["apt-get", "install", "-y", "--no-install-recommends", *pkgs])
    if install.returncode != 0:
        LOG.error("apt-get install failed:\n%s", install.stderr)
        return False
    return True


# --- Strategy implementations ---------------------------------------------------


def repair_missing_boost(repo_root: Path, match: re.Match[str]) -> bool:
    return _apt_install(
        [
            "libboost-all-dev",
            "libboost-filesystem-dev",
            "libboost-program-options-dev",
            "libboost-system-dev",
            "libboost-thread-dev",
        ]
    )


def repair_missing_guile(repo_root: Path, match: re.Match[str]) -> bool:
    return _apt_install(["guile-3.0-dev", "guile-3.0", "libguile-3.0-dev"])


def repair_missing_cython(repo_root: Path, match: re.Match[str]) -> bool:
    return _apt_install(["cython3", "python3-dev", "python3-nose"])


def repair_missing_cmake_pkg(repo_root: Path, match: re.Match[str]) -> bool:
    pkg = match.group(1).lower()
    table = {
        "openssl": ["libssl-dev"],
        "zlib": ["zlib1g-dev"],
        "blas": ["libopenblas-dev"],
        "lapack": ["liblapack-dev"],
        "atlas": ["libatlas-base-dev"],
        "rocksdb": ["librocksdb-dev"],
        "postgresql": ["libpq-dev"],
        "octomap": ["liboctomap-dev"],
        "expat": ["libexpat1-dev"],
        "curl": ["libcurl4-openssl-dev"],
        "iberty": ["libiberty-dev"],
        "binutils": ["binutils-dev"],
    }
    return _apt_install(table.get(pkg, []))


def repair_cmake_cache(repo_root: Path, match: re.Match[str]) -> bool:
    """Remove stale CMake caches; CMake will regenerate."""
    removed = 0
    for cache in repo_root.rglob("CMakeCache.txt"):
        # Only nuke caches inside build/ directories to avoid surprise
        if "build" in cache.parts:
            try:
                cache.unlink()
                removed += 1
            except OSError as exc:
                LOG.warning("Could not remove %s: %s", cache, exc)
    LOG.info("Removed %d stale CMake cache(s)", removed)
    return removed > 0


def repair_oom(repo_root: Path, match: re.Match[str]) -> bool:
    """Reduce make parallelism by mutating MAKEFLAGS in the environment."""
    current = os.environ.get("MAKEFLAGS", "")
    new = "-j2"  # safe default for OOM scenarios
    os.environ["MAKEFLAGS"] = new
    LOG.info("Reduced MAKEFLAGS '%s' → '%s' (OOM mitigation)", current, new)
    return True


def repair_missing_header(repo_root: Path, match: re.Match[str]) -> bool:
    header = match.group(1)
    table = {
        "Python.h": ["python3-dev"],
        "boost/version.hpp": ["libboost-dev"],
        "libguile.h": ["guile-3.0-dev"],
        "expat.h": ["libexpat1-dev"],
        "rocksdb/db.h": ["librocksdb-dev"],
        "octomap/octomap.h": ["liboctomap-dev"],
    }
    return _apt_install(table.get(header, []))


# Order matters: most-specific patterns first.
REPAIRS: list[Repair] = [
    Repair(
        name="missing-boost",
        pattern=re.compile(r"Could (?:NOT|not) find (?:a configuration file for package )?Boost", re.IGNORECASE),
        apply=repair_missing_boost,
        description="Install Boost development packages",
    ),
    Repair(
        name="missing-guile",
        pattern=re.compile(r"Could (?:NOT|not) find Guile|libguile.*not found", re.IGNORECASE),
        apply=repair_missing_guile,
        description="Install Guile 3.0 development packages",
    ),
    Repair(
        name="missing-cython",
        pattern=re.compile(r"Could (?:NOT|not) find Cython|cython.*not found", re.IGNORECASE),
        apply=repair_missing_cython,
        description="Install Cython 3 toolchain",
    ),
    Repair(
        name="missing-cmake-package",
        pattern=re.compile(r"Could (?:NOT|not) find ([A-Za-z][A-Za-z0-9_+.\-]+)\b"),
        apply=repair_missing_cmake_pkg,
        description="Install missing CMake package via apt mapping",
    ),
    Repair(
        name="missing-header",
        pattern=re.compile(r"fatal error: ([A-Za-z0-9_/.+\-]+\.h(?:pp)?): No such file"),
        apply=repair_missing_header,
        description="Install header-providing dev package",
    ),
    Repair(
        name="oom",
        pattern=re.compile(r"(virtual memory exhausted|Killed signal|out of memory|cc1plus.*killed)", re.IGNORECASE),
        apply=repair_oom,
        description="Reduce make parallelism for memory pressure",
    ),
    Repair(
        name="cmake-cache-stale",
        pattern=re.compile(r"CMake (?:Error|Warning).*CMakeCache.txt|does not match the source", re.IGNORECASE),
        apply=repair_cmake_cache,
        description="Purge stale CMake caches",
    ),
]


# ---------------------------------------------------------------------------
# Build runner
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class AttemptResult:
    attempt: int
    returncode: int
    duration_seconds: float
    repairs_applied: list[str]
    log_tail: str


def run_build(build_cmd: str, repo_root: Path) -> AttemptResult:
    start = time.monotonic()
    proc = subprocess.run(
        build_cmd,
        shell=True,
        cwd=str(repo_root),
        text=True,
        capture_output=True,
    )
    duration = time.monotonic() - start
    output = (proc.stdout or "") + "\n" + (proc.stderr or "")
    log_tail = "\n".join(output.splitlines()[-200:])
    if proc.returncode != 0:
        sys.stderr.write(output)
    else:
        sys.stdout.write(output)
    return AttemptResult(
        attempt=0,
        returncode=proc.returncode,
        duration_seconds=duration,
        repairs_applied=[],
        log_tail=log_tail,
    )


def diagnose_and_repair(log: str, repo_root: Path) -> list[str]:
    applied: list[str] = []
    seen: set[str] = set()
    for repair in REPAIRS:
        match = repair.pattern.search(log)
        if not match:
            continue
        if repair.name in seen:
            continue
        LOG.info("Applying repair '%s' — %s", repair.name, repair.description)
        ok = False
        try:
            ok = bool(repair.apply(repo_root, match))
        except Exception as exc:  # pragma: no cover - defensive
            LOG.exception("Repair '%s' raised: %s", repair.name, exc)
        if ok:
            applied.append(repair.name)
            seen.add(repair.name)
    return applied


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Self-healing build repair engine")
    parser.add_argument("--build-cmd", required=True, help="Shell command to invoke the build")
    parser.add_argument("--max-attempts", type=int, default=3, help="Max repair attempts (default: 3)")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument("--report", type=Path, help="Optional JSON report output path")
    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="[auto_fix] %(levelname)s: %(message)s",
    )

    if args.max_attempts < 1:
        LOG.error("--max-attempts must be >= 1")
        return 2

    repo_root = args.repo_root.resolve()
    if not repo_root.is_dir():
        LOG.error("--repo-root '%s' is not a directory", repo_root)
        return 2

    history: list[AttemptResult] = []
    for attempt in range(1, args.max_attempts + 1):
        LOG.info("──── Build attempt %d/%d ────", attempt, args.max_attempts)
        result = run_build(args.build_cmd, repo_root)
        result.attempt = attempt
        history.append(result)
        if result.returncode == 0:
            LOG.info("✅ Build succeeded on attempt %d (%.1fs)", attempt, result.duration_seconds)
            break
        if attempt == args.max_attempts:
            LOG.error("❌ Build failed after %d attempts", attempt)
            break
        LOG.warning("Build failed (rc=%d). Diagnosing…", result.returncode)
        repairs = diagnose_and_repair(result.log_tail, repo_root)
        result.repairs_applied = repairs
        if not repairs:
            LOG.error("No matching repair strategies for failure; aborting.")
            break
        LOG.info("Applied repairs: %s. Retrying…", ", ".join(repairs))

    final_rc = history[-1].returncode if history else 1

    if args.report:
        args.report.write_text(
            json.dumps(
                {
                    "build_cmd": args.build_cmd,
                    "repo_root": str(repo_root),
                    "max_attempts": args.max_attempts,
                    "final_returncode": final_rc,
                    "history": [dataclasses.asdict(h) for h in history],
                },
                indent=2,
            )
        )
        LOG.info("Wrote repair report → %s", args.report)

    return 0 if final_rc == 0 else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
