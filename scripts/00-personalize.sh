#!/usr/bin/env bash
# Usage: ./scripts/00-personalize.sh Marie Dupont mon-user-github mon-repo
set -euo pipefail

if [ "$#" -lt 4 ]; then
  echo "Usage: $0 <Prenom> <Nom> <github_user> <repo_name>"
  echo "Exemple: $0 Marie Dupont marie-dupont gitops-platform"
  exit 1
fi

PRENOM_RAW="$1"
NOM_RAW="$2"
GITHUB_USER="$3"
REPO_NAME="$4"

PRENOM_LOWER=$(echo "$PRENOM_RAW" | tr '[:upper:]' '[:lower:]')
NOM_LOWER=$(echo "$NOM_RAW" | tr '[:upper:]' '[:lower:]')

echo ">> Personnalisation pour ${PRENOM_RAW} ${NOM_RAW}"

find . -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.py" \) \
  -not -path "./scripts/*" | while read -r f; do
  sed -i \
    -e "s/{{PRENOM}}/${PRENOM_RAW}/g" \
    -e "s/{{NOM}}/${NOM_RAW}/g" \
    -e "s/{{prenom}}/${PRENOM_LOWER}/g" \
    -e "s/{{nom}}/${NOM_LOWER}/g" \
    -e "s/{{GITHUB_USER}}/${GITHUB_USER}/g" \
    -e "s/{{REPO_NAME}}/${REPO_NAME}/g" \
    "$f"
done

echo ">> Termine. Fichiers personnalises :"
grep -rl "${PRENOM_RAW}" --include="*.yaml" --include="*.yml" . || true

echo ""
echo ">> Prochaine etape : verifier helm-chart/values.yaml et gitops/application.yaml,"
echo "   puis commit + push vers votre depot Git."
