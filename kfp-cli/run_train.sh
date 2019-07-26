#!/bin/bash

python kfp-cli.py \
run_pipeline \
--experiment_name "CLV Training" \
--run-name "Training run" \
--pipeline_name clv_training \
--params '{\
"project_id": "jktest4", \
"source_gcs_path": "gs://jktest4clv/dataset/transactions.csv", \
"source_bq_table": "", \
"bq_dataset_name": "", \
"transactions_table_name": "transactions", \
"features_table_name": "features", \
"predict_end": "2011-12-12", \
"threshold_date": "2011-08-08", \
"max_monetary": 15000, \
}'