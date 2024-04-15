#!/usr/bin/env bash
#
# Extract docstrings to docs/
# make a copy for all languages
#

# I did not find more intelligent way have API Docs for all languages
for lang in ru; do
  cp ./docs/src/en/reference.md ./docs/src/$lang/reference.md
done
