
import urllib.request
import json

url = "http://localhost:8080/mcp"
payload = {
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
}
headers = {
    "Content-Type": "application/json"
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.getcode()}")
        body = response.read().decode('utf-8')
        print("Response Body:")
        print(json.dumps(json.loads(body), indent=2))
except Exception as e:
    print(f"Error: {e}")
