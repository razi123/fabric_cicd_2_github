import requests
import subprocess
import json
import os
import sys


def get_headers(access_token: str):
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }


def az_login():
    """Logs into Azure CLI and returns access token (valid for 1 hour)."""
    try:
        subprocess.run(["az", "login", "--use-device-code"], check=True)
        token_cmd = [
            "az", "account", "get-access-token",
            "--resource", "https://api.fabric.microsoft.com"
        ]
        result = subprocess.run(token_cmd, capture_output=True, text=True, check=True)
        token_data = json.loads(result.stdout)
        return token_data.get("accessToken")
    except Exception as e:
        raise RuntimeError(f"Azure login failed: {e}")


def create_pipeline(access_token: str, payload: dict, url: str):
    response = requests.post(url, headers=get_headers(access_token), json=payload)
    return response.status_code, response.json()


def get_pipeline_details(access_token: str, pipeline_id: str, url: str):
    response = requests.get(f"{url}/{pipeline_id}", headers=get_headers(access_token))
    return response.status_code, response.json()


def list_pipelines(access_token: str, url: str):
    try:
        response = requests.get(url, headers=get_headers(access_token))
        if response.status_code == 200:
            pipelines = response.json()
            for pipeline_summary in pipelines.get("value", []):
                if pipeline_summary.get("displayName") == "Fabric Test Deployment Pipeline":
                    return 200, pipeline_summary["id"]
    except Exception as e:
        print("Error listing pipelines:", str(e))

    return 404, None

def update_dep_pipeline(access_token: str, pipeline_id):
    url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{pipeline_id}"
    try:
        response = requests.patch(url, headers=get_headers(access_token))
        if response.status_code == 200:
            pipelines = response.json()
            for pipeline_summary in pipelines.get("value", []):
                if pipeline_summary.get("displayName") == "Fabric Test Deployment Pipeline":
                    return 200, pipeline_summary["id"]
    except Exception as e:
        print("Error listing pipelines:", str(e))

    return 404, None



def assign_workspace(access_token: str, pipeline_id: str, stage_id: str, workspace_id: str):
    url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{pipeline_id}/stages/{stage_id}/assignWorkspace"
    payload = {"workspaceId": workspace_id}
    response = requests.post(url, headers=get_headers(access_token), json=payload)

    try:
        result = response.json() if response.content else {}
    except ValueError:
        result = {}

    return response.status_code, result


def save_pipeline_metadata_yaml(pipeline_data, output_file="pipeline_metadata.yaml"):
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML is required to save metadata in YAML format. Install it via 'pip install pyyaml'.")

    if not pipeline_data:
        raise ValueError("No pipeline data provided")

    extracted_metadata = {
        "pipeline_id": pipeline_data.get("id"),
        "pipeline_name": pipeline_data.get("displayName"),
        "stages": [
            {
                "stage_id": s.get("id"),
                "stage_name": s.get("displayName"),
                "order": s.get("order"),
            } for s in pipeline_data.get("stages", [])
        ]
    }

    with open(output_file, 'w') as file:
        yaml.dump(extracted_metadata, file)

    print(f"Pipeline metadata saved to {output_file}")
    return extracted_metadata


def main(access_token: str):
    # Assign workspaces (hardcoded for DEV and TEST)
    workspaceId_dev = "24fbb753-b211-47f0-9acf-ad7e07029fc8"
    workspaceId_test = "d8666b30-e6be-4d1e-90b8-19d40b821be9"

    fabric_api_url = "https://api.fabric.microsoft.com/v1/deploymentPipelines"

    payload = {
        "displayName": "Fabric Test Deployment Pipeline",
        "description": "Deployment pipeline for testing, created in DEV environment.",
        "stages": [
            {
                "displayName": "Development",
                "description": "Development stage",
                "isPublic": False
            },
            {
                "displayName": "Test",
                "description": "Testing stage",
                "isPublic": False
            }
        ]
    }

    # Check if pipeline already exists
    status, pipeline_id = list_pipelines(access_token, fabric_api_url)
    if status == 200 and pipeline_id:
        print(f"Pipeline already exists with ID: {pipeline_id}")
        update_dep_pipeline(access_token, pipeline_id=pipeline_id)
        # update_dep_pipeline_stages(access_token, fabric_api_url)
    else:
        print("Creating new pipeline...")
        status, result = create_pipeline(access_token, payload, fabric_api_url)
        if status == 201:
            pipeline_id = result.get("id")
            print(f"Created pipeline with ID: {pipeline_id}")
        else:
            print(f"Failed to create pipeline: {result}")
            sys.exit(1)

    status, pipeline_details = get_pipeline_details(access_token, pipeline_id, fabric_api_url)

    if status != 200:
        print("Failed to get pipeline details")
        sys.exit(1)

    metadata = save_pipeline_metadata_yaml(pipeline_details)

    for stage in pipeline_details.get("stages", []):
        if stage.get("displayName") == "Development":
            status, result = assign_workspace(access_token, pipeline_id, stage.get("id"), workspaceId_dev)
            print(f"Assigned DEV workspace: {status} {result}")
        elif stage.get("displayName") == "Test":
            status, result = assign_workspace(access_token, pipeline_id, stage.get("id"), workspaceId_test)
            print(f"Assigned TEST workspace: {status} {result}")


if __name__ == "__main__":
    # Pass access token from GitHub Actions
    if len(sys.argv) < 2:
        print("Usage: python deployment_pipeline.py <access_token>")
        sys.exit(1)

    token = sys.argv[1]
    main(token)
