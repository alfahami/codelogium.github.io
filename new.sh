#!/usr/bin/env bash
# Start a new piece of content from templates/, or prepare one for publishing.
#   ./new.sh article <section> "Title"    e.g. ./new.sh article java "Java Streams"
#   ./new.sh blog "Title"                 e.g. ./new.sh blog "My Claude Certification"
#   ./new.sh project <group> "Title"      e.g. ./new.sh project java "Banking App"
#   ./new.sh img <file> <assets-dir>      e.g. ./new.sh img ~/Downloads/shot.png projects/banking-app
#   ./new.sh photo <file> <assets-dir>    e.g. ./new.sh photo ~/Downloads/cover.jpg posts
#   ./new.sh readtime <page.md>           e.g. ./new.sh readtime docs/java/java-streams.md
set -euo pipefail
cd "$(dirname "$0")"

usage() { sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }

kind="${1:-}"
case "$kind" in
  article) [ $# -eq 3 ] || usage; dir="docs/$2"; title="$3"; template="templates/article.md" ;;
  blog)    [ $# -eq 2 ] || usage; dir="docs/blog/posts"; title="$2"; template="templates/blog-post.md" ;;
  project) [ $# -eq 3 ] || usage; dir="docs/projects/$2"; title="$3"; template="templates/project.md" ;;
  img|photo|readtime) exec python3 templates/tools.py "$@" ;;
  *) usage ;;
esac

slug=$(printf '%s' "$title" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')
file="$dir/$slug.md"
[ -e "$file" ] && { echo "Already exists: $file"; exit 1; }

mkdir -p "$dir"
escaped=$(printf '%s' "$title" | sed 's/[&/\]/\\&/g')
sed -e "s/TITLE/$escaped/g" -e "s/DATE/$(date +%Y-%m-%d)/" "$template" > "$file"

echo "Created $file"
echo
echo "Next:"
echo "  1. Fill in the front matter (description, categories, tags, icon) and write."
case "$kind" in
  article) where="$dir/index.md (and docs/languages/index.md for a language)"; label="Read article" ;;
  project) where="docs/projects/index.md and docs/projects/$2/index.md"; label="View project" ;;
esac
if [ "$kind" = blog ]; then
  echo "  2. Nothing else: the blog page lists it automatically."
else
  echo "  2. Paste this card into the grid in $where,"
  echo "     with the same icon and a one-line description:"
  echo
  echo "-   :lucide-file-text:{ .lg .middle } __${title}__"
  echo
  echo "    ---"
  echo
  echo "    One line on what it covers."
  echo
  echo "    ---"
  echo
  echo "    [$label :lucide-arrow-right:]($slug/)"
  echo
fi
[ "$kind" = blog ] || echo "  3. When done writing: ./new.sh readtime $file"
echo "  Preview: venv/bin/zensical serve"
