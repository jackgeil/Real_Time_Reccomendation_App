import jwt
import time
import requests

# Path to your downloaded private key file
private_key_path = "real-time-reccomendation-app.2024-09-03.private-key.pem"

# Your GitHub App ID
app_id = "987335"

# Read the private key
with open(private_key_path, "r") as key_file:
    private_key = key_file.read()

# Generate JWT
payload = {
    'iat': int(time.time()) - 60,  # issued at time, 60 seconds in the past
    'exp': int(time.time()) + (10 * 60),  # JWT expiration time (10 minute maximum)
    'iss': app_id  # GitHub App's identifier
}

jwt_token = jwt.encode(payload, private_key, algorithm='RS256')

print("Generated JWT:", jwt_token)

# Replace with your installation ID
# First, let's fetch the installation ID
headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Accept": "application/vnd.github.v3+json"
}

# GitHub API endpoint to list installations for the authenticated app
installation_url = "https://api.github.com/app/installations"

response = requests.get(installation_url, headers=headers)
installations = response.json()

if response.status_code == 200 and installations:
    installation_id = installations[0]['id']  # Get the first installation ID
    print(f"Installation ID: {installation_id}")
else:
    print("Failed to get installation ID:", response.status_code, response.json())
    exit()

# Now, let's generate the installation access token
token_url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"

response = requests.post(token_url, headers=headers)

# Check for a successful response
if response.status_code == 201:
    access_token = response.json()['token']
    print("Installation Access Token:", access_token)
else:
    print(f"Failed to get access token: {response.status_code}")
    print(response.json())
