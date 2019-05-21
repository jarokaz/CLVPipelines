This repository maintains code samples for the tutorial **Operationalizing Customer Lifetime Value model training and deployment with Kubeflow Pipelines**. The tutorial is the fifth part of the series [Predicting Customer Lifetime Value with AI Platform](https://cloud.google.com/solutions/machine-learning/clv-prediction-with-offline-training-intro).
The fifth part focuses on demonstrating how to operationalize model training, deployment, and inference using Kubeflow Pipelines on Google Kubernetes Engine.

The repository includes two subfolders: `pipelines` and `components`.

The `pipelines` folder contains the example pipelines that demonstrate how to utilize pre-built and custom **Kubeflow Pipelines Components** to orchestrate data preparation, model training, model deployment and inference. Refer to README files associated with each pipeline for more details.

The `component` folder contains an example implementation of a custom Kubeflow Pipeline Component. This component is a wrapper around **AutoML Tables API**.

To run the code samples you need to set up a Google Cloud Platform (GCP)  with the following GCP services enabled:
- Google Kubernetes Engine (GKE)
- BigQuery
- Dataproc
- Cloud Storage
- AutoML Tables (beta)

Refer to this [how-to-guide](https://cloud.google.com/apis/docs/enable-disable-apis) to enable the required services.

## Configuring Kubeflow Pipelines
You are going to use [Cloud Shell](https://cloud.google.com/shell/) to install and configure Kubeflow Pipelines on GKE.

### Install Google Kubernetes Engine (GKE)
Create a single-zone **Standard** cluster. Make sure to replace the placeholders with your zone and cluster name.
```
CLUSTERNAME=[your cluster name]
ZONE=[your zone]
gcloud beta container clusters create $CLUSTERNAME \
  --cluster-version '1.12.7-gke.10' --enable-autoupgrade \
  --zone $ZONE \
  --scopes cloud-platform \
  --enable-cloud-logging \
  --enable-cloud-monitoring 
```

Bind your account as a cluster admin.
```
kubectl create clusterrolebinding ml-pipeline-admin-binding --clusterrole=cluster-admin --user=$(gcloud config get-value account)
```

### Install Kubeflow pipelines
Install version 1.20 of KFP.
```
PIPELINE_VERSION=4eeeb6e22432ece32c7d0efbd8307c15bfa9b6d3
kubectl apply -f https://raw.githubusercontent.com/kubeflow/pipelines/$PIPELINE_VERSION/manifests/namespaced-install.yaml
```
### Connect to Kubeflow Pipelines UI

To connect to KFP UI use Cloud Shell to forward a port to KFP UI service. 
```
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```
After port forwarding has been established, use Cloud Shell web preview to open KFP UI on port 8080.


## Configuring AI Platform Notebook
During the tutorial, you use an AI Platform Notebook instance as primary interface. 

### Provision an AI Platform Notebook instance
1. Create a new notebook instance with default options following the [how-to-guide](https://cloud.google.com/ml-engine/docs/notebooks/create-new). Use a **Python** instance type.
2. Follow the instructions in [how-to-guide](https://cloud.google.com/ml-engine/docs/notebooks/create-new) to connect to **JupyterLab** on your notebook instance.
3. Create a new terminal from the **Launcher** tab of **JupyterLab** interface.
4. In the terminal, use **git** to clone the tutorial's github repository.
```
git clone https://github.com/jarokaz/CLVPipelines
```

### Install and configure Kubeflow Pipelines SDK
Before running the tutorial's Jupyter notebooks you need to install Kubeflow Pipelines SDK into the Python 3 kernel of you AI Platform notebook instance and configure access to the Pipelines service on your GKE cluster.

Open a new terminal in **JupyterLab**. Run the following command to install SDK version 0.1.20.
```
SDK_VERSION=0.1.20
python3 -m pip install https://storage.googleapis.com/ml-pipeline/release/$SDK_VERSION/kfp.tar.gz --upgrade
```

### Configure port forwarding to the Pipeline service 
Get the credentials to your GKE cluster.
```
ZONE=[your zone]
CLUSTERNAME=[your cluster name]
gcloud container clusters get-credentials $CLUSTERNAME --zone $ZONE
```
Configure port forwarding.
```
kubectl port-forward -n kubeflow svc/ml-pipeline 8082:8888
```

Make sure that the terminal window stays open and the command is running while you walk through the tutorial's notebooks.




## Starting the tutorial
The tutorial's notebooks are located in the `pipelines` folder. Follow the instructions in the notebooks to walk through the tutorial's scenarios.




