#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

# Cleanup HydroLineage Kubernetes deployment

set -e

echo "🧹 HydroLineage Kubernetes Cleanup"
echo "===================================="

read -p "This will DELETE all HydroLineage resources. Continue? (yes/no) " -r
echo
if [[ ! $REPLY = "yes" ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

# Uninstall Helm release
echo "Uninstalling Helm release..."
helm uninstall hydro-lineage -n hydro-lineage || echo "Helm release not found, continuing..."

# Delete ConfigMaps and Secrets
echo "Deleting ConfigMaps and Secrets..."
kubectl delete configmap hydro-postgres-init -n hydro-lineage --ignore-not-found=true
kubectl delete secret airflow-webserver-secret -n hydro-lineage --ignore-not-found=true
kubectl delete secret airflow-connections -n hydro-lineage --ignore-not-found=true

# Ask about PVCs
echo ""
read -p "Delete persistent volumes (DATABASE DATA WILL BE LOST)? (yes/no) " -r
echo
if [[ $REPLY = "yes" ]]; then
    kubectl delete pvc -n hydro-lineage --all
    echo "✅ PVCs deleted"
fi

# Delete namespace
echo ""
read -p "Delete namespace hydro-lineage? (yes/no) " -r
echo
if [[ $REPLY = "yes" ]]; then
    kubectl delete namespace hydro-lineage
    echo "✅ Namespace deleted"
fi

echo ""
echo "✅ Cleanup complete!"
