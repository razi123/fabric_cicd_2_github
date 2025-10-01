import sys
import requests

# Workspaces IDs
WORKSPACES = {
    "dev": "24fbb753-b211-47f0-9acf-ad7e07029fc8",
    "test": "d8666b30-e6be-4d1e-90b8-19d40b821be9",
    "prod": "11111111-2222-3333-4444-555555555555"  # placeholder for now
}

def get_variable_group_id(workspace_id: str, headers: dict) -> str | None:
    """Fetch the variable library ID for a given workspace."""

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/variableLibraries"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch variable libraries: {e}")
        return None

    try:
        response_data = response.json()
    except ValueError:
        print("Failed to parse JSON response.")
        return None

    variable_libraries = response_data.get("value", [])
    if not variable_libraries:
        print("No variable libraries found in workspace.")
        return None

    # Pick the first library (or filter by displayName if needed)
    return variable_libraries[0].get("id")


def update_variable_group(workspace_id: str, library_id: str, target_env: str, headers: dict):
    """Update the active variable set in a variable library."""

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/variableLibraries/{library_id}"
    payload = {"properties": {"activeValueSetName": target_env}}

    try:
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Successfully updated variable library {library_id} for env '{target_env}'")
        print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Failed to update variable library: {e}")
        if response is not None:
            print("Status:", response.status_code)
            try:
                print("Response:", response.json())
            except ValueError:
                print("Response was not JSON")


def main():
    if len(sys.argv) < 3:
        print("Usage: python set_variable_group.py <environment> <access_token>")
        sys.exit(1)

    target_env = sys.argv[1].lower()
    access_token = sys.argv[2]

    if target_env not in WORKSPACES:
        print(f"Unknown environment '{target_env}'. Valid options: {', '.join(WORKSPACES.keys())}")
        sys.exit(1)

    workspace_id = WORKSPACES[target_env]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    print(f"🔹 Target environment: {target_env}")
    print(f"🔹 Workspace ID: {workspace_id}")

    library_id = get_variable_group_id(workspace_id, headers)
    if not library_id:
        print("Could not find a variable library ID.")
        sys.exit(1)

    print(f"Variable Library ID: {library_id}")
    update_variable_group(workspace_id, library_id, target_env, headers)


if __name__ == "__main__":
    main()



# if len(sys.argv) < 3:
#     print("Usage: python set_variable_group.py environment access_token")
#     sys.exit(1)

# target_env = sys.argv[1]
# access_token = sys.argv[2]

# # Replace with your actual IDs
# workspace_id_dev = "24fbb753-b211-47f0-9acf-ad7e07029fc8"
# workspace_id_test = "d8666b30-e6be-4d1e-90b8-19d40b821be9"

# def get_variable_group_id(workspace_id):
    
#     url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/variableLibraries"

#     response = requests.get(url, headers=headers)
#     response_data = response.json()
#     variable_libraries = response_data.get("value", [])
#     if variable_libraries:
#         variable_library_id = variable_libraries[0].get("id")
#     else:
#         variable_library_id = None
#     return variable_library_id

# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/json"
# }


# if target_env == "dev":
#     workspace_id = workspace_id_dev
#     library_id = get_variable_group_id(workspace_id=workspace_id)
# elif target_env == "test":
#     workspace_id = workspace_id_test
#     library_id = get_variable_group_id(workspace_id=workspace_id)
# else:
#     pass


# print(f"target_env is {target_env}")
# print(f"workspace_id is {workspace_id}")
# print("Variable Library ID:", library_id)


# url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/variableLibraries/{library_id}"

# payload = {
#     "properties": {
#         "activeValueSetName": target_env
#     }
# }

# response = requests.patch(url, headers=headers, json=payload)

# print("Status:", response.status_code)
# print("Response:", response.json())
