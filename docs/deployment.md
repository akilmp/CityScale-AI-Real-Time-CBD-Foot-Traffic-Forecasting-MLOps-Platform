# Deployment Guide

This project ships Kubernetes manifests to simplify deployment.

## Ray Cluster

The Ray cluster is defined in [`k8s/ray-cluster.yaml`](../k8s/ray-cluster.yaml). It includes a single head node and an autoscaling worker group (1–5 replicas).

Apply the manifest:

```bash
kubectl apply -f k8s/ray-cluster.yaml
```

## Canary Rollout

Application updates are managed via Argo Rollouts using [`k8s/argo-rollout.yaml`](../k8s/argo-rollout.yaml). The rollout advances traffic in canary steps of 5%, 25%, and 100%.

Apply the manifest:

```bash
kubectl apply -f k8s/argo-rollout.yaml
```
