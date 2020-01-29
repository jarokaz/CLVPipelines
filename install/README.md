## Provisioning the infrastructure

The provisioning of the insfrastructure required to run the guide's pipelines has been automated with Terraform. The Terraform configuration in the `/terraform/` folder includes the provisioning and configuration of the following infrastructure components:
- GKE cluster
- Kubeflow Pipelines
- Service Accounts used by GKE and KFP
- Container Registry
- Cloud Storage for the pipelines artifacts and sample datasets

To provision the infrastructure:

1. Select or create a GCP project
1. Make sure that the following Cloud APIs are enabled:
   - Compute Engine
   - Cloud Storage
   - Container Registry
   - Kubernetes Engine
   - BigQuery
   - AutoML 
   - Cloud Build
   - Cloud Resource Manager
1. You can enable the services using **GCP Console** or by executing the `enable_apis.sh` script in the `/install` folder.
1. Open a new session in **Cloud Shell**
1. Create a working directory and clone this repo.
1. Edit the `terraform.tfvars` file to provide your values for the configuration's parameters:

Parameter | Description
----------|------------
project_id|Project ID of the GCP project you selected for the solution
cluster_name| The name of the GKE cluster to create. 
cluster_location | The zone for the cluster. Since AutoML only support` us-central1` it is recommended to create the cluster in one of the zones in the same region
bucket_name | The name of the GCS bucket that will be used as an artifact storage. Terraform will attempt to create the bucket so make sure that the bucket under this name does not exist.


1. In Cloud Shell, in the `/install/terraform` folder execute the following commands:
```
terraform init
terraform apply
```

To clean up, execute `terraform destroy` from the `/install/terraform` folder.

To deploy the pipelines and the pipeline's artifacts follow the instructions in the [README](../deploy/README.md) in the `/deploy` folder.





