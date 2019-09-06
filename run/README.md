## Running the solution's pipelines

There are two ways of triggering a KFP pipeline run:
- Using the Kubeflow Pipelines UI
- Using the KFP SDK

### Running the pipelines using Kubeflow Pipelines UI

If you provisioned the lightweight Kubeflow Pipelines deployment, the KFP UI is available at the URL that can be retrieved using the following command:

`echo "https://"$(kubectl describe configmap inverse-proxy-config -n kubeflow | grep "googleusercontent.com")`

Use the procedure described in [Pipelines Quickstart](https://www.kubeflow.org/docs/pipelines/pipelines-quickstart/) to create experiments and submit pipeline runs.

The compiled training pipeline has been stored by Cloud Build in the following GCS location:

`gs://[_BUCKET_NAME][_PIPELINES_FOLDER]/[_TRAIN_PIPELINE].tar.gz`

The compiled batch predict pipeline is in

`gs://[_BUCKET_NAME][_PIPELINES_FOLDER]/[_PREDICT_PIPELINE].tar.gz`

In addition both pipelines have been uploaded to Kubeflow Pipelines.

The sample training and testing datasets can be found in:

`gs://[_BUCKET_NAME][_SAMPLE_DATASET]`

The runtime parameters required by the pipelines are described in detail in [`/pipelines/README.md`](/pipelines/README.md)

Most of the parameters have reasonable default values that don't have to be modified during the intial runs.

### Running the pipelines using KFP SDK


This folder contains a sample Python script demonstrating how to use `kfp.Client()` API from the KFP SDK to configure experiments, upload pipelines, and submit pipeline runs programmatically.

The `kfp-cli.py` script implements a CLI wrapper around `kfp.Client()`. The `run_train.sh` and `run_batch_predict.sh` are example bash scripts that utilize `kpf-cli.py` to submit pipeline runs.

To submit a run using `kfp-cli.py`

```
python kfp-cli.py \
run_pipeline \ 
--experiment_name [EXPERIMENT_NAME] \
--run_name [RUN_NAME] \
--pipeline_name [PIPELINE_NAME] \
--params [DICTIONARY_OF_PIPELINE_ARGUMENTS]
```

**ARGUMENTS**


`--experiment_name`

The name of experiment. If the experiment under this name does not exist it is created.

`--run_name`

The name of the run.

`--pipeline_name`

The name of the pipeline to execute. The pipeline must have been uploaded to the KFP cluster.

`--params`

A dictionary literal with the pipeline's runtime arguments.


Inspect `run_train.sh` and `run_batch_predict.sh` to see the examples of using `kfp-cli.py`. Note that the example argument values WILL NOT work in your environment.

Make sure that you have configured the credentials to access your GKE cluster.
```
gcloud container clusters get-credentials [YOUR_CLUSTER_NAME] --zone [CLUSTER_ZONE]
```

#### Installing Kubeflow Pipelines SDK

To use `kfp.Client()` you need a Python 3.5+ environment with KFP SDK installed. It is highly recommended to install KFP SDK into a dedicated Python or Conda environment.

The code in this tutorial was tested with the 0.1.27 version of KFP SDK. 

```
SDK_VERSION=0.1.27
pip install https://storage.googleapis.com/ml-pipeline/release/$SDK_VERSION/kfp.tar.gz --upgrade
```

To use `kfp-cli.py` utility you also need [Python Fire package](https://google.github.io/python-fire/guide/). 
```
pip install fire
```




