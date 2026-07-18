#!/usr/bin/env bash
set -euo pipefail

echo ">> Application du manifest Argo CD (gitops/application.yaml)"
kubectl apply -f gitops/application.yaml

echo ">> Statut de la synchronisation :"
kubectl get application -n argocd

echo ">> Pour suivre en direct : kubectl get application -n argocd -w"
