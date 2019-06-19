# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Commom utilities and helper functions."""

import json

from google.cloud import automl_v1beta1 as automl


def get_latest_evaluation_metrics(model_full_id):
  """Retrieves the latest evaluation metrics for an AutoML Tables model."""

  client = automl.AutoMlClient()
  evaluations = list(client.list_model_evaluations(model_full_id))

  create_seconds = 0
  evaluation_metrics = None
  for evaluation in evaluations:
    if evaluation.create_time.seconds > create_seconds:
      if evaluation.regression_evaluation_metrics.ListFields():
        evaluation_metrics = evaluation.regression_evaluation_metrics
        create_seconds = evaluation.create_time.seconds
      elif evaluation.classification_evaluation_metrics.ListFields():
        evaluation_metrics = evaluation.classification_evaluation_metrics
        create_seconds = evaluation.create_time.seconds

  return evaluation_metrics


def write_metadata_for_output_viewers(*argv):
  """Writes items to be rendered by KFP UI as artificats."""

  output_metadata = {'version': 1, 'outputs': argv}
  with open('/mlpipeline-ui-metadata.json', 'w') as f:
    json.dump(output_metadata, f)

"""
def write_metrics(*metrics):
  """Writes pipeline metrics."""

  metrics_metadata = {'metrics': metrics}
  with open('/mlpipeline-metrics.json', 'w') as f:
    json.dump(metrics_metadata, f)

"""