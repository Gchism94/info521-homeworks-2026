#!/bin/sh
# make_template_repo.sh <hw>
#
# Stamps one assignment from this source-of-truth workspace into a standalone, publishable
# GitHub Classroom *template repo* under build/<hw>/ (its own fresh git repo). Local only —
# it does NOT create remotes or push (that's the instructor's step; see README).
#
# What it assembles into build/<hw>/:
#   - the STUDENT-FACING release (solutions stripped) via the assignment's make_release
#   - .github/workflows/classroom.yml   (the autograder workflow)
#   - .gitignore, LICENSE                (from shared/ and repo root)
#   - for Typst assignments: shared common.typ + equations.typ bundled at repo root
#
# KNOWN ADJUSTMENT (Typst): assignment Makefiles import shared assets via `--root ../../`
# (correct in the monorepo). In a standalone repo the shared .typ files are bundled at the
# repo root, so the Makefile's `--root ../../` must become `--root .`. This script bundles
# the assets and WARNS; fix the Makefile `--root` as part of the per-assignment overhaul.
set -e

HW="$1"
[ -z "$HW" ] && { echo "usage: $0 <hw>   e.g. $0 hw3"; exit 1; }

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/assignments/$HW"
OUT="$ROOT/build/$HW"
[ -d "$SRC" ] || { echo "no such assignment: $SRC"; exit 1; }

echo ">> building student release for $HW"
( cd "$SRC" && sh ./make_release )

echo ">> assembling template repo at $OUT"
rm -rf "$OUT"; mkdir -p "$OUT/.github/workflows"
cp -r "$SRC/release/." "$OUT/"
cp "$ROOT/shared/classroom.yml" "$OUT/.github/workflows/classroom.yml"
cp "$ROOT/shared/gitignore" "$OUT/.gitignore"
cp "$ROOT/LICENSE" "$OUT/LICENSE"

# Bundle shared Typst assets for standalone builds
if [ -f "$SRC/hw.typ" ]; then
    cp "$ROOT/shared/common.typ" "$OUT/common.typ"
    cp "$ROOT/shared/equations.typ" "$OUT/equations.typ"
    echo "!! Typst assignment: bundled common.typ/equations.typ at repo root."
    echo "!! Adjust the Makefile '--root ../../' to '--root .' for standalone builds."
fi

echo ">> git init + initial commit"
( cd "$OUT" && git init -q && git add -A && git commit -qm "Template repo for $HW (generated)" )

cat <<EOF

Done: $OUT  (fresh git repo, student-facing)

Next (your steps — replace the org):
  gh repo create info521-sp26/$HW --public --source=$OUT --remote=origin --push
  # then point GitHub Classroom at info521-sp26/$HW as the assignment template
EOF
