
import urllib.request
import json
import time
import threading
import sys

# MCP Client configuration
MCP_URL = "http://localhost:8080/mcp"
POST_ENDPOINT = None

def listen_sse():
    global POST_ENDPOINT
    headers = {"Accept": "text/event-stream, application/json"}
    req = urllib.request.Request(MCP_URL, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            for line in response:
                line = line.decode('utf-8').strip()
                if line.startswith("event: endpoint"):
                    # The next line should be data: ...
                    continue
                if line.startswith("data:"):
                    data_str = line[5:].strip()
                    # Expecting relative or absolute path
                    # Logic to resolve path
                    if data_str.startswith("/"):
                        base = MCP_URL.rsplit("/", 1)[0] # remove /mcp
                        if base.endswith("/"): base = base[:-1] # remove trailing slash
                        POST_ENDPOINT = base + data_str
                        # print(f"Endpoint found: {POST_ENDPOINT}")
                        return # Found endpoint, stop listening strictly for now or keep running in thread? 
                        # For this script we just need the endpoint to start interacting
                    else:
                        POST_ENDPOINT = data_str
                        return
    except Exception as e:
        print(f"SSE Error: {e}")

# Start SSE listener in a thread because it blocks
t = threading.Thread(target=listen_sse)
t.daemon = True
t.start()

# Wait for endpoint
timeout = 5
start = time.time()
while POST_ENDPOINT is None:
    if time.time() - start > timeout:
        print("Timeout waiting for SSE endpoint")
        sys.exit(1)
    time.sleep(0.1)

# print(f"Connected. Endpoint: {POST_ENDPOINT}")

# Now perform MCP Handshake
def send_rpc(method, params=None, msg_id=None):
    payload = {
        "jsonrpc": "2.0",
        "method": method
    }
    if params is not None:
        payload["params"] = params
    if msg_id is not None:
        payload["id"] = msg_id
        
    data = json.dumps(payload).encode('utf-8')
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(POST_ENDPOINT, data=data, headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

# 1. Initialize
init_params = {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "test-client", "version": "1.0"}
}
init_resp = send_rpc("initialize", init_params, 1)
# print("Initialized:", json.dumps(init_resp, indent=2))

# 2. Tools List
tools_resp = send_rpc("tools/list", None, 2)
print(json.dumps(tools_resp, indent=2))
