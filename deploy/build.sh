#!/bin/bash
#
# Submits a Cloud Build job that builds and deploys
# the pipelines and pipelines components 

SUBSTITUTIONS=\
_CLV_REPO=[CLV_REPO_NAME],\
_AUTOML_TABLES_IMAGE=automl_tables,\
_BASE_IMAGE=base_image,\
_TAG=latest,\
_TRAIN_PIPELINE=train_pipeline,\
_PREDICT_PIPELINE=predict_pipeline,\
_ARTIFACTS_FOLDER=artifacts,\
_PIPELINES_FOLDER=pipelines,\
_SAMPLE_DATASET_FOLDER=dataset,\
_BUCKET_NAME=kfp-clv-artifacts,\
_CLUSTER_NAME=kfp-clv-gke,\
_ZONE=us-central1-a

gcloud builds submit --no-source  --config cloudbuild.yaml --substitutions $SUBSTITUTIONS




