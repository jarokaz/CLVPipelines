# Copyright 2019 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import kfp
import os
import argparse
import json
import uuid
from kfp import dsl
from kfp import gcp
from kfp import components

from helper_components import load_sales_transactions, prepare_feature_engineering_query

platform='Local'

# URIs to the specifications of the components used in the pipeline
BIGQUERY_COMPONENT_SPEC_URI = 'https://raw.githubusercontent.com/kubeflow/pipelines/3b938d664de35db9401c6d198439394a9fca95fa/components/gcp/bigquery/query/component.yaml'
#AML_IMPORT_DATASET_SPEC_URI = 'aml-import-dataset.yaml'
#AML_TRAIN_MODEL_SPEC_URI = 'aml-train-model.yaml'
#AML_RETRIEVE_METRICS_SPEC_URI = 'aml-retrieve-regression-metrics.yaml'
#AML_DEPLOY_MODEL_SPEC_URI = 'aml-deploy-model.yaml'
#AML_BATCH_PREDICT_SPEC_URI = 'aml-batch-predict.yaml'


 Create component factories
load_sales_transactions_op = kfp.components.func_to_container_op(load_sales_transactions)
prepare_feature_engineering_query_op = kfp.components.func_to_container_op(prepare_feature_engineering_query)
#batch_predict_op = kfp.components.load_component_from_file(AML_BATCH_PREDICT_SPEC_URI)
#engineer_features_op = kfp.components.load_component_from_url(BIGQUERY_COMPONENT_SPEC_URI)
engineer_features_op = component_store.load_component('bigquery/query')
batch_predict_op = component_store.load_component('aml-batch-predict')

# Define the batch predict pipeline
@kfp.dsl.pipeline(
    name='CLV Training BigQuery AutoML',
    description='CLV Training Pipeline using BigQuery for feature engineering and Automl Tables for model training'
)
def clv_batch_predict(
    project_id, 
    source_gcs_path,
    source_bq_table,
    bq_dataset_name,
    transactions_table_name,
    features_table_name,
    threshold_date,
    predict_end,
    max_monetary,
    aml_model_id,
    destination_prefix,
    dataset_location='US',
    aml_compute_region='us-central1',
    query_template_uri='gs://clv-pipelines/scripts/create_features_template.sql'
):

    # Create component factories
    load_sales_transactions_op = kfp.components.func_to_container_op(load_sales_transactions)
    prepare_feature_engineering_query_op = kfp.components.func_to_container_op(prepare_feature_engineering_query)  
    engineer_features_op = component_store.load_component('bigquery/query')
    batch_predict_op = component_store.load_component('aml-batch-predict')

    # Define the workflow
 
    # Load sales transactions 
    load_sales_transactions = load_sales_transactions_op(
        project_id=project_id,
        source_gcs_path=source_gcs_path,
        source_bq_table=source_bq_table,
        dataset_location=dataset_location,
        dataset_name=bq_dataset_name,
        table_id=transactions_table_name 
    ) 

    # Generate the feature engineering query
    prepare_feature_engineering_query = prepare_feature_engineering_query_op(
        project_id=project_id,
        source_table_id=load_sales_transactions.output,
        destination_dataset=bq_dataset_name,
        features_table_name=features_table_name,
        threshold_date=threshold_date,
        predict_end=predict_end,
        max_monetary=max_monetary,
        query_template_uri=query_template_uri
    )

    # Run the feature engineering query on BigQuery.
    engineer_features = engineer_features_op(
        query=prepare_feature_engineering_query.outputs['query'],
        project_id=project_id,
        dataset_id=prepare_feature_engineering_query.outputs['dataset_name'],
        table_id=prepare_feature_engineering_query.outputs['table_name'],
        output_gcs_path='',
        dataset_location=dataset_location,
        job_config=''
    )

    # Run the batch predict task on features in Big Query
    source_data_uri = 'bq://{}.{}.{}'.format(
        project_id,
        prepare_feature_engineering_query.outputs['dataset_name'],
        prepare_feature_engineering_query.outputs['table_name'])

    predict_batch = batch_predict_op(
        project_id=project_id,
        region=aml_compute_region,
        model_id=aml_model_id,
        datasource=source_data_uri,
        destination_prefix=destination_prefix)
    
    predict_batch.after(engineer_features)
    
    # Configure the pipeline to use GCP service account secret if running on GCP
    steps = [load_sales_transactions,
             prepare_feature_engineering_query,
             engineer_features]#,
             #predict_batch]
    for step in steps:
        if platform == 'GCP':
            step.apply(gcp.use_gcp_secret('user-gcp-sa'))



def _parse_arguments():
    """Parse command line arguments"""
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--out-folder',
        type=str,
        required=True,
        help='The output folder for a compiled pipeline')
    parser.add_argument(
        '--local-search-path',
        type=str,
        required=True,
        help='Local search path for component definitions')
    parser.add_argument(
        '--url-search-prefixes',
        type=str,
        required=True,
        help='The URL prefix to look for component definitions)
    parser.add_argument(
        '--type-check',
        type=str,
        default=False,
        help='Check types during compilation if True')
     
    return parser.parse_args()
        

if __name__ == '__main__':
    args = _parse_arguments()


    """

    # Initialize Component Store
    # local_search_paths = ['/Users/jarekk/projects/CLVPipelines/components/specs'] 
    # url_search_prefixes = ['https://raw.githubusercontent.com/kubeflow/pipelines/3b938d664de35db9401c6d198439394a9fca95fa/components/gcp/']
    component_store = kfp.components.ComponentStore(args.local_search_paths, args.url_search_prefixes)

    # Compile the pipeline
    pipeline_func = clv_batch_predict
    pipeline_filename = pipeline_func.__name__ + '.tar.gz'
    pipeline_path = os.path.join(args.out_folder, pipeline_filename)

    kfp.compiler.Compiler().compile(pipeline_func, pipeline_path, type_check=args.type_check) 

    """

    



#