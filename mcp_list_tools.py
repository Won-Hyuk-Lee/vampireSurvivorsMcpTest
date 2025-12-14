
import urllib.request
import json

url = "http://localhost:8080/mcp"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

# 1. Initialize
init_payload = {
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05", 
        "capabilities": {},
        "clientInfo": {"name": "test-client", "version": "1.0"}
    },
    "id": 1
}

init_data = json.dumps(init_payload).encode('utf-8')
init_req = urllib.request.Request(url, data=init_data, headers=headers, method='POST')

session_id = None
try:
    with urllib.request.urlopen(init_req) as response:
        # Check headers for session ID
        session_id = response.getheader('mcp-session-id')
        print(f"Session ID: {session_id}")
        # Consume body to close stream properly (though we don't strictly need to)
        _ = response.read()
except Exception as e:
    print(f"Init Error: {e}")
    exit(1)

if not session_id:
    print("No session ID found")
    exit(1)

# 2. List Tools
list_payload = {
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 2
}

list_data = json.dumps(list_payload).encode('utf-8')
# Headers for subsequent requests?
headers["mcp-session-id"] = session_id

list_req = urllib.request.Request(url, data=list_data, headers=headers, method='POST')

try:
    with urllib.request.urlopen(list_req) as response:
        print(f"Tools List Status: {response.getcode()}")
        body = response.read().decode('utf-8')
        # Parse SSE
        all_tools = []
        for line in body.splitlines():
            if line.startswith("data: "):
                data_json = json.loads(line[6:])
                all_tools.append(data_json)
        
        with open("tools.json", "w") as f:
            json.dump(all_tools, f, indent=2)
        print("Tools saved to tools.json")
except Exception as e:
    print(f"Tools List Error: {e}")
