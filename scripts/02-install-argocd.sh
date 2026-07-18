#!/usr/bin/env bash
set -euo pipefail

echo ">> Creation du namespace argocd"
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

echo ">> Installation d'Argo CD"
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo ">> Attente que les pods Argo CD soient prets (peut prendre 1-2 min)"
kubectl wait --for=condition=Available deployment --all -n argocd --timeout=180s

echo ">> Mot de passe admin initial :"
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
echo ""
echo ">> Pour acceder a l'UI : kubectl port-forward svc/argocd-server -n argocd 8081:443"
echo ">> Puis ouvrir https://localhost:8081 (user: admin)"
