variable "project_id" {
    description = "The GCP project ID"
}

variable "cluster_location" {
    description = "The location the GKE cluster"
}

variable "cluster_name" {
    description = "The name of the Kubernetes cluster"
}


variable "cluster_node_count" {
    description = "The cluster's node count"
    default     = 3
}

variable "kfp_sa_id" {
    description = "The ID of the Kubeflow Pipelines service account"
    default     = "kfp-sa"
}

variable "cluster_sa_id" {
    description = "The ID of the Least Priviledge GKE service account"
    default     = "gke-sa"
}

variable "bucket_name" {
    description = "The name of a GCS storage bucket that will be used as an artifact store"
}

variable "kfp_version" {
    description = "The version of Kubeflow Pipelines to install"
    default     = "0.1.27"
}
