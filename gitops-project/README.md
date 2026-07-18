# Plateforme GitOps individuelle

Projet complet : dépôt Git → CI (build/test/scan) → registre → Argo CD → Kubernetes (3 nœuds) → Observabilité, avec rollback via `git revert`.

## 0. Personnaliser le projet

```bash
./scripts/00-personalize.sh Marie Dupont marie-dupont gitops-platform
```

Remplace automatiquement `{{PRENOM}}`, `{{NOM}}`, `{{GITHUB_USER}}`, `{{REPO_NAME}}` dans tous les fichiers
(namespace, release Helm, dépôt Git, dashboard Grafana).

Vérifiez ensuite manuellement :
- `helm-chart/values.yaml` → `image.repository` doit pointer vers **votre** dépôt d'images
- `gitops/application.yaml` → `repoURL` doit pointer vers **votre** dépôt Git réel

## 1. Créer le dépôt Git

```bash
git init
git add .
git commit -m "init: plateforme GitOps"
git remote add origin https://github.com/<votre_user>/<votre_repo>.git
git push -u origin main
```

## 2. CI (GitHub Actions)

Le workflow `.github/workflows/ci.yml` se déclenche à chaque push sur `main` touchant `app/` ou `helm-chart/` :
1. Tests unitaires Python (`pytest`)
2. `helm lint` + `helm template` sur le chart
3. Build de l'image Docker
4. **Scan de vulnérabilités** avec Trivy (bloque le pipeline si CRITICAL/HIGH trouvé)
5. Push vers **GHCR** (`ghcr.io/<user>/<repo>`)
6. Commit automatique qui met à jour `helm-chart/values.yaml` avec le nouveau tag d'image — **c'est ce commit qu'Argo CD va détecter**

Rien à installer : GitHub Actions l'exécute automatiquement. Le seul prérequis est que le repo soit public (ou que `packages: write` soit autorisé) pour GHCR.

## 3. Créer le cluster à 3 nœuds

```bash
chmod +x scripts/*.sh
./scripts/01-create-cluster.sh
```
Crée un cluster k3d local : 1 control-plane + 2 workers. Vérifiez avec `kubectl get nodes`.

> Si votre prof exige un cluster réel multi-VM (kubeadm) ou un cloud managé (EKS/GKE/AKS), dites-le-moi et j'adapte ce script.

## 4. Installer Argo CD

```bash
./scripts/02-install-argocd.sh
```
Affiche le mot de passe admin initial et les instructions de port-forward pour l'UI.

## 5. Déployer l'application via GitOps

```bash
./scripts/03-deploy-application.sh
```
Argo CD prend alors la main : il compare en permanence l'état déclaré dans Git (`helm-chart/`) à l'état réel du cluster, et se resynchronise automatiquement (`selfHeal: true`) en cas de dérive.

## 6. Observabilité

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack \
  -f observability/prometheus-values.yaml -n monitoring --create-namespace

helm install loki grafana/loki-stack \
  -f observability/loki-values.yaml -n monitoring

helm install otel-collector open-telemetry/opentelemetry-collector \
  -f observability/otel-collector-config.yaml -n monitoring

kubectl apply -f observability/servicemonitor.yaml
```

Accès Grafana :
```bash
kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
# user: admin / mot de passe: valeur de grafana.adminPassword dans prometheus-values.yaml
```

## 7. Démonstration du rollback (Git revert)

```bash
# Simuler un mauvais déploiement
sed -i 's/tag: .*/tag: "version-cassee"/' helm-chart/values.yaml
git commit -am "bug: mauvaise version"
git push
# Argo CD synchronise -> les pods crashent (ImagePullBackOff)

# Rollback : on ne touche pas au cluster, on revert Git
git revert HEAD --no-edit
git push
# Argo CD detecte le nouveau commit et resynchronise -> retour à l'état stable
```

---

## Checklist de validation (reprend les critères du sujet)

- [ ] **Commit** : push sur `main` déclenche la CI automatiquement
- [ ] **Scan** : Trivy bloque le pipeline si une vulnérabilité CRITICAL/HIGH est détectée
- [ ] **Synchronisation GitOps** : Argo CD applique automatiquement tout changement de `helm-chart/` (`automated.selfHeal: true`)
- [ ] **Observabilité** : Prometheus scrape l'app (ServiceMonitor), Grafana affiche le dashboard personnalisé, Loki collecte les logs, OTel collecte les traces
- [ ] **Rollback par `git revert`** : testé et fonctionnel (section 7)
- [ ] **Personnalisation** : nom/prénom présents dans le namespace, la release Helm, le nom du dépôt et le titre du dashboard Grafana

## Structure du projet

```
.
├── app/                        # Application Flask (code source)
├── helm-chart/                 # Chart Helm (déploiement K8s)
├── .github/workflows/ci.yml    # Pipeline CI
├── gitops/application.yaml     # Manifest Argo CD
├── observability/              # Prometheus, Grafana, Loki, OTel
└── scripts/                    # Personnalisation + bootstrap du cluster
```
