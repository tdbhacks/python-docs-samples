# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START generativeaionvertexai_sdk_embedding]
import re

from google.cloud.aiplatform import initializer as aiplatform_init
from vertexai.language_models import TextEmbeddingModel


def tune_embedding_model(
    api_endpoint: str,
    base_model_name: str = "text-embedding-004",
    task_type: str = "DEFAULT",
    corpus_path: str = "gs://cloud-samples-data/ai-platform/embedding/goog-10k-2024/r11/corpus.jsonl",
    queries_path: str = "gs://cloud-samples-data/ai-platform/embedding/goog-10k-2024/r11/queries.jsonl",
    train_label_path: str = "gs://cloud-samples-data/ai-platform/embedding/goog-10k-2024/r11/train.tsv",
    test_label_path: str = "gs://cloud-samples-data/ai-platform/embedding/goog-10k-2024/r11/test.tsv",
    batch_size: int = 128,
    train_steps: int = 1000,
    output_dimensionality: int = 768,
    learning_rate_multiplier: float = 1.0,
):  # noqa: ANN201
    match = re.search(r"^(\w+-\w+)", api_endpoint)
    location = match.group(1) if match else "us-central1"
    base_model = TextEmbeddingModel.from_pretrained(base_model_name)
    tuning_job = base_model.tune_model(
        task_type=task_type,
        corpus_data=corpus_path,
        queries_data=queries_path,
        training_data=train_label_path,
        test_data=test_label_path,
        batch_size=batch_size,
        train_steps=train_steps,
        tuned_model_location=location,
        output_dimensionality=output_dimensionality,
        learning_rate_multiplier=learning_rate_multiplier,
    )
    return tuning_job


# [END generativeaionvertexai_sdk_embedding]
if __name__ == "__main__":
    tune_embedding_model(aiplatform_init.global_config.api_endpoint)
