import argparse
import requests
import os

# FUNCTIONS

def check_or_create_environment(workspace_id, env_name, headers):
    base_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}"
    envs_url = f"{base_url}/environments"
    envs_resp = requests.get(envs_url, headers=headers)

    if envs_resp.status_code != 200:
        raise Exception(f"Failed to list environments: {envs_resp.text}")

    envs = envs_resp.json().get("value", [])
    existing_env = None

    for env in envs:
        if env.get("displayName") == env_name:
            existing_env = env
            print(f"Environment exists: {env_name}")
            break

    if not existing_env:
        print(f"Creating environment: {env_name}")
        payload = {"displayName": env_name, "description": "An environment description"}
        create_resp = requests.post(envs_url, headers=headers, json=payload)
        if create_resp.status_code != 201:
            raise Exception(f"Failed to create environment: {create_resp.text}")
        existing_env = create_resp.json()

    return existing_env.get("id")


def check_whl_exists(workspace_id, env_id, headers, whl_filename):
    base_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}"
    libs_url = f"{base_url}/environments/{env_id}/libraries"
    libs_resp = requests.get(libs_url, headers=headers)

    if libs_resp.status_code != 200:
        raise Exception(f"Failed to list custom libraries: {libs_resp.text}")

    libs_data = libs_resp.json()
    wheel_files = libs_data.get("customLibraries", {}).get("wheelFiles", [])

    for whl in wheel_files:
        if whl.endswith(whl_filename):
            print(f"Wheel file exists: {whl}")
            return whl

    print("No .whl file dont exists in environment.")
    return None


def upload_whl_file(workspace_id, env_id, headers, wheel_file_path):
    print("Overwriting WHL file... uploading new version.")
    upload_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{env_id}/staging/libraries"

    with open(wheel_file_path, "rb") as whl_file:
        files = {"file": (os.path.basename(wheel_file_path), whl_file, "application/octet-stream")}
        print(f"Uploading file: {files}")

        resp = requests.post(upload_url, headers={"Authorization": headers["Authorization"]}, files=files)

    if resp.status_code in (200, 201):
        print("WHL library uploaded successfully.")
    else:
        raise Exception(f"Failed to upload WHL file: {resp.status_code} {resp.text}")


def delete_whl_file(workspace_id, env_id, headers, whl_filename):
    base_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}"
    delete_base_url = f"{base_url}/environments/{env_id}/staging/libraries"

    if whl_filename:
        print(f"Deleting existing WHL library: {whl_filename}")
        delete_url = f"{delete_base_url}?libraryToDelete={whl_filename}"
        delete_resp = requests.delete(delete_url, headers=headers)
        if delete_resp.status_code != 200:
            raise Exception(f"Failed to delete existing WHL library: {delete_resp.text}")
        print(f"Deleted existing library: {whl_filename}")



def publish_environment(workspace_id, env_id, headers):
    publish_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{env_id}/staging/publish"
    resp = requests.post(publish_url, headers=headers)
    print(resp.json())


# -------------------
# MAIN SCRIPT
# -------------------

if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Fabric deployment pipeline")
    parser.add_argument(
        "--overwrite_whl",
        type=str,
        required=False,
        help="yes/no - overwrite existing WHL file"
    )
    parser.add_argument(
        "--token",
        type=str,
        required=True,
        help="Access token for authentication"
    )

    args = parser.parse_args()
    overwrite_whl = args.overwrite_whl.lower() if args.overwrite_whl else "no"
    access_token = args.token

    workspaceId_dev = "5871c70b-6796-4e24-9444-9af3e4daa27c"
    env_name = "custom_libs_env"
    wheel_file_path = "./dist/fabric_utils-0.1.0-py3-none-any.whl"
    whl_filename = "fabric_utils-0.1.0-py3-none-any.whl"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    # Step 1: Always check/create environment
    env_id = check_or_create_environment(workspaceId_dev, env_name, headers)

    # Step 2: Always check if WHL exists
    whl_exists = check_whl_exists(workspaceId_dev, env_id, headers, whl_filename)

    # Step3: if yes then delete 
    if overwrite_whl == "yes" and whl_exists:
        delete_whl_file(workspaceId_dev, env_id, headers, whl_filename)
        publish_environment(workspaceId_dev, env_id, headers)
    

    # Step 4: Optionally upload WHL
    if overwrite_whl == "yes":
        upload_whl_file(workspaceId_dev, env_id, headers, wheel_file_path)
        publish_environment(workspaceId_dev, env_id, headers)
    else:
        print("Skipping WHL upload...")
