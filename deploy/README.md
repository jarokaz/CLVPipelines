

## Building and deploying the pipelines

Building and deploying of the pipelines and components have been automated using [GCP Cloud Build](https://cloud.google.com/cloud-build/docs/).  The build process goes through the following steps:
1. Create a docker image to support custom build steps
1. Build the base image for the lightweigh Python helper components. The name of the image is provided as a build parameter.
1. Build the image that hosts AutoML Tables components. The name of the image is provided as a build parameter.
1. Update the YAML specifications of the AutoML Tables components with the names of the created images in the previous step
1. Update the settings that control the pipelines' compilation. The values for these settings are provided as build parameters.
1. Compile the pipelines. 
1. Deploy the compiled pipelines to a GCS location. The path to the location is provided as a build parameter.
1. Deploy the artifacts used by the pipelines to a GCS location. The path to the location is provided as a build parameter.
1. Deploy the component images to the Container Registry of your project. 
1. Copy the sample dataset to a GCS location. The path to the location is provided as a build parameter.
1. Deploy compiled pipelines to the KFP GKE cluster. The cluster name and location are provided as build parameters.


### Build parameters
You can use the `gcloud builds submit` command's `--substitutions` option to set the parameters of the build.

Parameter | Description 
-----------|-------------
_BASE_IMAGE | The name of the base image for Lightweight Python compoments. Specify the image name only. The image will be pushed to `gcr.io/[YOUR_PROJECT_ID]/[_BASE_IMAGE]`
_AUTOML_TABLES_IMAGE | The name of the image that hosts AutoML Tables components
_TAG | The tag to apply when building images. Both images will be tagged with the same tag.
_TRAIN_PIPELINE | The name for the compiled training pipeline. The compiled pipeline is saved as `[_TRAIN_PIPELINE].tar.gz`
_PREDICT_PIPELINE | The name for the compiled batch predict pipeline. The compiled pipeline will be saved as `[_PREDICT_PIPELINE].tar.gz` |
_BUCKET_NAME | The name of a GCP bucket in your project to store compiled pipelines and other artifacts used by the pipelines. 
_PIPELINES_FOLDER | The name of the folder in _BUCKET_NAME to store the compiled pipelines
_ARTIFACTS_FOLDER | The name of the folder in _BUCKET_NAME to store artificats used by the pipelines at running time. 
_SAMPLE_DATASET_FOLDER | The name of the folder in _BUCKET_NAME to store the sample dataset used by the pipelines.
_CLUSTER_NAME | The name of a KFP GKE cluster.
_ZONE | The location of a KFP GKE cluster.


The `/cloud-build/build.sh` demonstrates how to use `gcloud builds submit` to start the build process. 


To build and deploy the solution:
1. Open [Cloud Shell](https://cloud.google.com/shell/docs/) in your project.
2. Clone this repo.
3. Update `build.sh` with your argument values.
4. Execute `build.sh`.


### Folder structure

This folder contains Cloud Build artifacts:
- `cloudbuild.yaml` - a Cloud Build config file
- `build.sh` - a bash script template that uses `gcloud builds submit` to configure and start the build
- `kfp-builder/Dockerfile` - Dockerfile for an image used by the build's custom steps.

