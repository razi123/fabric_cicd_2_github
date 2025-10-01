import sys
import requests

if len(sys.argv) < 3:
    print("Usage: python set_variable_group.py environment access_token")
    sys.exit(1)

target_env = sys.argv[1]
access_token = sys.argv[2]

# Replace with your actual IDs
workspace_id = "24fbb753-b211-47f0-9acf-ad7e07029fc8"
library_id = "107e752c-9f02-423d-823f-7638e89ef51f"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/variableLibraries/{library_id}"

payload = {
    "properties": {
        "activeValueSetName": target_env
    }
}

response = requests.patch(url, headers=headers, json=payload)

print("Status:", response.status_code)
print("Response:", response.json())
