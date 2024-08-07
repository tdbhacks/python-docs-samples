#  Copyright 2024 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import google.auth

# [START batch_labels_job]
from google.cloud import batch_v1


def create_job_with_custom_job_labels(
    project_id: str,
    region: str,
    job_name: str,
    label_key1: str,
    label_value1: str,
    label_key2: str,
    label_value2: str,
) -> batch_v1.Job:
    """
    This method creates a Batch job with custom labels.
    Args:
        project_id (str): project ID or project number of the Cloud project you want to use.
        region (str): name of the region you want to use to run the job. Regions that are
            available for Batch are listed on: https://cloud.google.com/batch/docs/locations
        job_name (str): the name of the job that will be created.
        label_key1 (str): First custom label key.
        label_value1 (str): First custom label value.
        label_key2 (str): Second custom label key.
        label_value2 (str): Second custom label value.
    Returns:
        batch_v1.Job: The created Batch job object containing configuration details.
    """
    client = batch_v1.BatchServiceClient()

    runnable = batch_v1.Runnable()
    runnable.container = batch_v1.Runnable.Container()
    runnable.container.image_uri = "gcr.io/google-containers/busybox"
    runnable.container.entrypoint = "/bin/sh"
    runnable.container.commands = [
        "-c",
        "echo Hello world!",
    ]

    # Create a task specification and assign the runnable and volume to it
    task = batch_v1.TaskSpec()
    task.runnables = [runnable]

    # Specify what resources are requested by each task.
    resources = batch_v1.ComputeResource()
    resources.cpu_milli = 2000  # in milliseconds per cpu-second. This means the task requires 2 whole CPUs.
    resources.memory_mib = 16  # in MiB
    task.compute_resource = resources

    task.max_retry_count = 2
    task.max_run_duration = "3600s"

    # Create a task group and assign the task specification to it
    group = batch_v1.TaskGroup()
    group.task_count = 3
    group.task_spec = task

    # Policies are used to define on what kind of virtual machines the tasks will run on.
    # In this case, we tell the system to use "e2-standard-4" machine type.
    # Read more about machine types here: https://cloud.google.com/compute/docs/machine-types
    policy = batch_v1.AllocationPolicy.InstancePolicy()
    policy.machine_type = "e2-standard-4"
    instances = batch_v1.AllocationPolicy.InstancePolicyOrTemplate()
    instances.policy = policy
    allocation_policy = batch_v1.AllocationPolicy()
    allocation_policy.instances = [instances]

    # Create the job and assign the task group and allocation policy to it
    job = batch_v1.Job()
    job.task_groups = [group]
    job.allocation_policy = allocation_policy

    # Set the labels for the job
    job.labels = {label_key1: label_value1, label_key2: label_value2}

    # We use Cloud Logging as it's an out of the box available option
    job.logs_policy = batch_v1.LogsPolicy()
    job.logs_policy.destination = batch_v1.LogsPolicy.Destination.CLOUD_LOGGING

    # Create the job request and set the job and job ID
    create_request = batch_v1.CreateJobRequest()
    create_request.job = job
    create_request.job_id = job_name
    # The job's parent is the region in which the job will run
    create_request.parent = f"projects/{project_id}/locations/{region}"

    return client.create_job(create_request)


# [END batch_labels_job]


if __name__ == "__main__":
    PROJECT_ID = google.auth.default()[1]
    REGION = "us-central1"
    job_name = "your-job-name"
    create_job_with_custom_job_labels(
        PROJECT_ID,
        REGION,
        job_name,
        label_key1="label1",
        label_value1="value1",
        label_key2="label2",
        label_value2="value2",
    )
