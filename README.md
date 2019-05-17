This repository maintains code samples for the tutorial **Operationalizing Customer Lifetime Value model training and deployment with Kubeflow pipelines**. The tutorial is the fifth part of a series that discusses how you can develop and deploy customer lifetime value (CLV) prediction models by using AI Platform on Google Cloud Platform (GCP).


## Setting up the tutorial's environment
This tutorial uses the following services of Google Cloud Platform:
- Google Kubernets Engine (GKE)
- AI Platform Notebooks
- BigQuery
- Dataproc
- Cloud Storage
- AutoML Tables (beta)

Before you begin the environment setup [enable the corresponding APIs](https://cloud.google.com/apis/docs/enable-disable-apis) for your GCP project.

## Installing AI Platform Notebook
Create a new notebook instance with default options following the [how-to-guide](https://cloud.google.com/ml-engine/docs/notebooks/create-new). Use a **Python** instance type.

## Installing Google Kubernetes Engine (GKE)
Create a single-zone **Standard** cluster using [Cloud Shell](https://cloud.google.com/shell/) Replace the placeholders with your zone and cluster name.
```
CLUSTERNAME=[your cluster name]
ZONE=[your zone]
gcloud config set compute/zone $ZONE
gcloud beta container clusters create $CLUSTERNAME \
  --cluster-version 1.11.8-gke.6 --enable-autoupgrade \
  --zone $ZONE \
  --scopes cloud-platform \
  --enable-cloud-logging \
  --enable-cloud-monitoring 
```

```
kubectl create clusterrolebinding ml-pipeline-admin-binding --clusterrole=cluster-admin --user=$(gcloud config get-value account)
```

## Install Kubeflow pipelines
```
#!/bin/bash
PIPELINE_VERSION=0.1.7
kubectl create -f https://storage.googleapis.com/ml-pipeline/release/$PIPELINE_VERSION/bootstrapper.yaml
```
## Monitor installation
```
#!/bin/bash
jobname=$(kubectl get job | tail -1 | awk '{print $1}')
kubectl wait --for=condition=complete --timeout=5m $jobname
```

## Connect to ambassador proxy
```
export NAMESPACE=kubeflow
kubectl port-forward -n ${NAMESPACE} $(kubectl get pods -n ${NAMESPACE} --selector=service=ambassador -o jsonpath='{.items[0].metadata.name}') 8085:80
```

## Install Kubeflow pipelines SDK
```
pip install https://storage.googleapis.com/ml-pipeline/release/$PIPELINE_VERSION/kfp.tar.gz --upgrade
```
