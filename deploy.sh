#!/bin/sh
# Deploy the experiments playground to Cloudflare Pages (plain static, public).
#
# Credentials: environment, or ~/.config/cloudflare/experiments.env (falls back to aff.env):
#   export CLOUDFLARE_API_TOKEN="..."
#   export CLOUDFLARE_ACCOUNT_ID="..."
set -e
for f in "$HOME/.config/cloudflare/experiments.env" "$HOME/.config/cloudflare/aff.env"; do
  [ -f "$f" ] && . "$f" && break
done
# No token? Fine — wrangler falls back to its own OAuth login (`wrangler login`).

PROJECT="exprmnts"
cd "$(dirname "$0")"

# Stage everything except repo/tooling files, then deploy the folder as-is.
STAGE=$(mktemp -d)
cp index.html _redirects "$STAGE/"
for d in */; do
  case "$d" in .git/|node_modules/) continue;; esac
  cp -R "${d%/}" "$STAGE/"   # strip trailing slash — BSD cp would copy contents, not the dir
done

npx --yes wrangler pages deploy "$STAGE" --project-name="$PROJECT" --branch=main --commit-dirty=true
rm -rf "$STAGE"
echo "live: https://$PROJECT.pages.dev"
