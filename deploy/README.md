# Deployment auf Kubernetes (Helm)

```bash
# 1. Zugangsdaten als Secret anlegen (nicht in Git!)
kubectl create secret generic iq-quiz-zugang \
  --from-literal=DATABASE_URL='postgresql://...' \
  --from-literal=ADMIN_TOKEN='langes-zufaelliges-token'

# 2. Chart prüfen und installieren
helm lint deploy/helm/iq-quiz --set existingSecret=iq-quiz-zugang
helm upgrade --install iq deploy/helm/iq-quiz --set existingSecret=iq-quiz-zugang

# 3. Testen
kubectl port-forward svc/iq-iq-quiz 8000:80
curl localhost:8000/health
```

**Was das Chart macht:**
- Deployment mit 2 Replikas (geht, weil laufende Spiele in der Datenbank liegen)
- Readiness- und Liveness-Probe auf `/health`
- Läuft als Nicht-root-Benutzer, ohne Linux-Capabilities
- Prometheus-Annotations für `/metrics`
- Optional: Ingress (mit TLS) und Autoscaling (HPA)

Das Docker-Image wird von der CI nach `ghcr.io/enesdoudouzi-sys/iq-quiz-backend` hochgeladen.
Mit ArgoCD kann dieses Chart direkt aus dem Git-Repository deployt werden (GitOps).
