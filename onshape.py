import requests
import time
import uuid
import hashlib
import hmac
import base64
import json

# --- 1. API Credentials and Resource IDs ---
ACCESS_KEY = "YOUR_ACCESS_KEY"  # Replace with your actual key
SECRET_KEY = "YOUR_SECRET_KEY"  # Replace with your actual secret
document_id = "2d31f5e10fa056c96e0a75c6"
workspace_id = "8fc670243965225a2baeaa59"
# Use the element ID from the document URL if that’s the correct Part Studio:
element_id = "a377fdbdab916b853e7ea51a"  

# --- 2. Compute New Parameter Values ---
bridge_input = 20.03
offset = 5
lens_len_input = 2.587
lens_wid_input = 4.297

BridgeWid = bridge_input + offset
LensLen = lens_len_input
LensWid = lens_wid_input

# --- 3. Construct the API Request ---
method = "POST"
# If the API endpoint is versioned, you might need to include the version (e.g., /api/v6/...)
path = f"/api/variables/d/{document_id}/w/{workspace_id}/e/{element_id}"
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
# Use minified JSON to be safe:
body = json.dumps(payload, separators=(",", ":"))

# --- 4. Generate the HMAC Signature ---
timestamp = str(int(time.time() * 1000))
nonce = str(uuid.uuid4())
message_to_sign = timestamp + nonce + method + path + query + body

signature = base64.b64encode(
    hmac.new(SECRET_KEY.encode('utf-8'),
             message_to_sign.encode('utf-8'),
             hashlib.sha256).digest()
).decode('utf-8')

headers = {
    "Content-Type": "application/json",
    "On-Nonce": nonce,
    "On-Timestamp": timestamp,
    "On-Access-Key": ACCESS_KEY,
    "On-Signature": signature
}

# --- 5. Make the Request ---
url = "https://cad.onshape.com" + path
response = requests.post(url, headers=headers, data=body)

if response.status_code == 200:
    print("✅ Parameters updated successfully!")
    print("Response:", response.json())
else:
    print(f"❌ Error: {response.status_code}")
    print("Details:", response.text)
