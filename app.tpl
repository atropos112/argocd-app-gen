apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  annotations:
    atropos.auto.genenerated: "true"
  name: _APP_NAME
  namespace: platform
spec:
  ignoreDifferences: []
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
  destination:
    namespace: _NAMESPACE
    server: https://kubernetes.default.svc
  project: default
  source:
    path: _PATH
    repoURL: REPO_URL
    targetRevision: HEAD
