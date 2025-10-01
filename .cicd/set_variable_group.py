import sys
import requests

if len(sys.argv) < 3:
    print("Usage: python set_variable_group.py environment access_token")
    sys.exit(1)

target_env = sys.argv[1]
access_token = sys.argv[2]


# Replace with your actual IDs
workspace_id_dev = "24fbb753-b211-47f0-9acf-ad7e07029fc8"
workspace_id_test = "d8666b30-e6be-4d1e-90b8-19d40b821be9"
library_id = "000b727b-697d-439f-8593-66fbea09f8e1"

print(f"target_env is {target_env}")

if target_env == "dev":
    workspace_id = workspace_id_dev
else:
    workspace_id = workspace_id_test

print(f"workspace_id is {workspace_id}")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id_dev}/variableLibraries/{library_id}"

payload = {
    "properties": {
        "activeValueSetName": target_env
    }
}

response = requests.patch(url, headers=headers, json=payload)

print("Status:", response.status_code)
print("Response:", response.json())
