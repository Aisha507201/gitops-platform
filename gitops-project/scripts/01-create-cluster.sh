#!/usr/bin/env bash
# Cree un cluster Kubernetes local a 3 noeuds : 1 control-plane + 2 workers
# Prerequis : k3d (https://k3d.io) et kubectl installes localement
set -euo pipefail

CLUSTER_NAME="${1:-gitops-cluster}"

echo ">> Creation du cluster ${CLUSTER_NAME} (1 control-plane + 2 workers)"
k3d cluster create "${CLUSTER_NAME}" \
  --servers 1 \
  --agents 2 \
  --port "8080:80@loadbalancer" \
  --wait

echo ">> Verification des noeuds :"
kubectl get nodes -o wide

echo ">> Cluster pret."
