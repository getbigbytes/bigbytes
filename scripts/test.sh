#!/bin/bash
set -e

git diff --name-only master...HEAD --diff-filter=d | \
  grep -v '^bigbytes/server/frontend_dist/' | \
  grep -v '^bigbytes/server/frontend_dist_base_path_template/' | \
  grep -E '\.(js|jsx|ts|tsx)$' | \
  xargs prettier --config bigbytes/frontend/.prettierrc --write

git diff --name-only master...HEAD --diff-filter=d | \
  grep -v '^bigbytes/server/frontend_dist/' | \
  grep -v '^bigbytes/server/frontend_dist_base_path_template/' | \
  grep -E '\.(js|jsx|ts|tsx)$' | \
  xargs eslint_d --quiet --config bigbytes/frontend/.eslintrc.js --fix --ext .js,.jsx,.ts,.tsx

HOST='' PORT='' PROJECT='' docker compose run --rm app sh -c './scripts/clean.sh' 2>/dev/null
HOST='' PORT='' PROJECT='' docker compose run --rm app yarn install_and_test 2>/dev/null

git diff --name-only master...HEAD --diff-filter=d | \
  grep -v '^bigbytes/server/frontend_dist/' | \
  grep -v '^bigbytes/server/frontend_dist_base_path_template/' | \
  grep -E '\.(py)$' | \
  xargs poetry run pre-commit run --show-diff-on-failure --files
