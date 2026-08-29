#!/usr/bin/env bash
# Push the 300 product photographs to GitHub in chunks.
#
# A single 115 MB push was rejected with HTTP 408 — GitHub timed out closing
# the connection after the whole pack had been written. Committing and pushing
# the images in groups keeps each request small enough to complete, and each
# chunk that lands stays landed.
set -u
cd "$(dirname "$0")/.." || exit 1

CHUNKS=("ACC" "DRM" "GEAR GTR OUD" "PA" "STR VLN WND")
NAMES=("accordions" "percussion" "guitars, gear and ouds" "audio and studio" "strings, violins and wind")

fail=0
for i in "${!CHUNKS[@]}"; do
  paths=()
  for p in ${CHUNKS[$i]}; do paths+=("import/images/${p}-"*.jpg); done

  git add -- "${paths[@]}" 2>/dev/null
  if git diff --cached --quiet; then
    echo "[$((i+1))/${#CHUNKS[@]}] ${NAMES[$i]} — already committed, skipping"
  else
    n=$(git diff --cached --name-only | wc -l)
    git -c user.name="Divercitieslb" -c user.email="divercitieslb@gmail.com" \
        commit -q -m "Product photographs: ${NAMES[$i]} (${n} images)"
    echo "[$((i+1))/${#CHUNKS[@]}] ${NAMES[$i]} — committed ${n} images"
  fi

  for attempt in 1 2 3; do
    if git push -q origin build:refs/heads/main 2>&1 | grep -v "^remote:"; then :; fi
    if [ "$(git rev-parse HEAD)" = "$(git ls-remote origin refs/heads/main | cut -f1)" ]; then
      echo "    pushed ok"
      break
    fi
    echo "    push attempt ${attempt} did not land, retrying..."
    sleep 3
    if [ "$attempt" = 3 ]; then fail=1; echo "    FAILED after 3 attempts"; fi
  done
done

echo
echo "local HEAD : $(git rev-parse HEAD)"
echo "remote main: $(git ls-remote origin refs/heads/main | cut -f1)"
echo "images tracked: $(git ls-files import/images | wc -l)"
exit $fail
