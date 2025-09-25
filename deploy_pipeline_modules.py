import requests
import subprocess
import json
import os

def get_headers(access_token: str):
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

def az_login():
    """Logs into Azure CLI and returns access token (valid for 1 hour)."""
    try:
        subprocess.run(["az", "login"], check=True)
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
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            pipelines = response.json()
            for pipeline_summary in pipelines.get("value", []):
                pipeline_id = pipeline_summary["id"]
                print("Pipeline ID:", pipeline_id)
                print("Pipeline Name:", pipeline_summary.get("displayName"))

                # Get full details for this pipeline
                details_response = requests.get(f"{url}/{pipeline_id}", headers=get_headers(access_token))
                if details_response.status_code == 200:
                    pipeline_details = details_response.json()
                    print("Stages:")
                    for stage in pipeline_details.get("stages", []):
                        print(f"  - Stage ID: {stage['id']}")
                        print(f"    Name: {stage['displayName']}")
                        print(f"    Order: {stage['order']}")
                        print(f"    Is Public: {stage['isPublic']}")
                else:
                    print(f"Failed to fetch pipeline details for {pipeline_id}")

                print("---")
        else:
            print("Failed to list pipelines")
            print(response.text)


    except Exception as e:
        print("Error:", str(e))

    return response.status_code   #, response.json()

def delete_pipeline(access_token: str, pipeline_id: str):
    url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{pipeline_id}"
    response = requests.delete(url, headers=get_headers(access_token))
    return response.status_code, response.text

def assign_workspace(access_token: str, pipeline_id: str, stage_id: str, workspace_id: str):
    url = f"https://api.fabric.microsoft.com/v1/deploymentPipelines/{pipeline_id}/stages/{stage_id}/assignWorkspace"
    payload = {"workspaceId": workspace_id}
    response = requests.post(url, headers=get_headers(access_token), json=payload)
    return response.status_code, response.json()

def main():
    fabric_api_url = "https://api.fabric.microsoft.com/v1/deploymentPipelines"

    payload = {
        "displayName": "my deployment pipeline 2",  # you write the pipeline name if new otherwsise fine 
        "description": "A pipeline to automate deployments across dev and test stages.",
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

    access_token = az_login()   # for now user login esle spn toekn 

    status, result = create_pipeline(access_token, payload, fabric_api_url)
    print(f"Create pipeline status: {status}\n{json.dumps(result, indent=2)}")

    if status == 201:
        pipeline_id = result.get("id")
        status, details = get_pipeline_details(access_token, pipeline_id, fabric_api_url)
        print(f"Pipeline details status: {status}\n{json.dumps(details, indent=2)}")
    elif status == 409:
        print("Pipeline already exists. Fetching existing pipelines...")

    # list the pipelines 
    status = list_pipelines(access_token, fabric_api_url)
    # print(f"List pipelines status: {status}\n{json.dumps(pipelines, indent=2)}")




if __name__ == "__main__":
    main()
