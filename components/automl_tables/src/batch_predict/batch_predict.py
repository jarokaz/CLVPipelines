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

"""Run Automl Tables Batch Predict."""

import logging
import time
import json

from pathlib import Path
from google.cloud import automl_v1beta1 as automl

from common import write_metadata_for_output_viewers
                    

def prediction_metadata_to_markdown_metadata(response_metadata):
    """Converts batch predict response metadat to markdown"""

    markdown_template = (
        "**Batch predict results:**  \n"
        "&nbsp;&nbsp;&nbsp;&nbsp;**Input datasource:**&nbsp;{input}  \n"
        "&nbsp;&nbsp;&nbsp;&nbsp;**Output destination:**&nbsp;{output}  \n"
    )
    markdown = markdown_template.format(
        input=response_metadata.batch_predict_details.input_config,
        output=response_metadata.batch_predict_details.output_info
    )

    markdown_metadata = {"type": "markdown", "storage": "inline", "source": markdown}

    return markdown_metadata

  
def predict(project_id, 
            region,
            model_id, 
            datasource,
            destination_prefix, 
            output_destination):
  """Runs batch predict on an AutoML tables model."""

  logging.basicConfig(level=logging.INFO)

  client = automl.PredictionServiceClient()
  # Prepare prediction query config
  model_full_id = client.model_path(
      project_id, region, model_id
  )
  if datasource.startswith("bq"):
    input_config = {"bigquery_source": {"input_uri": datasource}}
  else:
    input_uris = datasource.split(",")
    input_config = {"gcs_source": {"input_uris": input_uris}}

  if destination_prefix.startswith("bq"):
    output_config = {"bigquery_destination": {"output_uri": destination_prefix}}
  else:
    output_config = {"gcs_destination": {"output_uri_prefix": destination_prefix}}

  # Run the prediction query
  logging.info("Starting batch scoring using: {}".format(datasource))
  response = client.batch_predict(
      model_full_id, input_config, output_config)

  # Wait for completion
  # WORKAROUND to catch exception thrown by response.result()
  try:
    response.result()
  except:
    pass
  result = response.metadata

  logging.info("Batch scoring completed: {}".format(str(result)))
  write_metadata_for_output_viewers(prediction_metadata_to_markdown_metadata(result))
 
  # Save results
  if destination_prefix.startswith("bq"):
    output = result.batch_predict_details.output_info.bigquery_output_dataset
  else:
    output = result.batch_predict_details.output_info.gcs_output_directory

  Path(output_destination).parent.mkdir(parents=True, exist_ok=True)
  Path(output_destination).write_text(output)

  