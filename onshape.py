import requests
import time
import uuid
import hashlib
import hmac
import base64
import json

# === 1. Define Your API Credentials and Document Details ===
ACCESS_KEY = "jNuY9TEnPr2nwZuqfHLAS6Eh"
SECRET_KEY = "QVocU6QeUAUJMNwfd8giLDyhpMFSdzl1fW4byGG7CHSRXWEW"
document_id = "2d31f5e10fa056c96e0a75c6"
workspace_id = "8fc670243965225a2baeaa59"
element_id = "6c046a925cf8e0f222c96fba"  # Ensure this is the correct Part Studio ID

# === 2. Get User Input and Compute New Parameter Values ===
try:
    bridge_input = float(input("Enter Bridge value (mm): "))
    offset = float(input("Enter offset value (mm) for BridgeWid: "))
    lens_len_input = float(input("Enter Lens Length (mm): "))
    lens_wid_input = float(input("Enter Lens Width (mm): "))
except ValueError:
    print("Please enter valid numeric values.")
    exit(1)

BridgeWid = bridge_input + offset
LensLen = lens_len_input
LensWid = lens_wid_input

# === 3. Construct API Request for Updating Variables ===
method = "POST"
path = f"/api/variables/d/{document_id}/w/{workspace_id}/e/{element_id}"  # Use the correct Onshape variable update endpoint
query = ""

payload = {
    "variables": [
        {
            "variableId": "BridgeWid",  
            "expression": f"{BridgeWid} mm",
            "variableType": "Length"
        },
        {
            "variableId": "LensLen",
            "expression": f"{LensLen} mm",
            "variableType": "Length"
        },
        {
            "variableId": "LensWid",
            "expression": f"{LensWid} mm",
            "variableType": "Length"
        }
    ]
}

body = json.dumps(payload)

# === 4. Generate the HMAC Signature for Authentication ===
timestamp = str(int(time.time() * 1000))
nonce = str(uuid.uuid4())

message_to_sign = timestamp + nonce + method + path + query + body

signature = base64.b64encode(
    hmac.new(SECRET_KEY.encode('utf-8'),
             message_to_sign.encode('utf-8'),
             hashlib.sha256).digest()
).decode('utf-8')

# === 5. Set Up Request Headers ===
headers = {
    "Content-Type": "application/json",
    "On-Nonce": nonce,
    "On-Timestamp": timestamp,
    "On-Access-Key": ACCESS_KEY,
    "On-Signature": signature
}

# === 6. Make the API Request ===
url = "https://cad.onshape.com" + path

response = requests.post(url, headers=headers, data=body)

# === 7. Check the Response ===
if response.status_code == 200:
    print("✅ Parameters updated successfully!")
    print("Response:", response.json())
else:
    print(f"❌ Error: {response.status_code}")
    print("Details:", response.text)
