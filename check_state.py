
import json
import mcp_wrapper
import time
import sys
import urllib.request

def read_resource(uri):
    sid = mcp_wrapper.get_session_id()
    if not sid: return None
    
    headers = mcp_wrapper.HEADERS.copy()
    headers["mcp-session-id"] = sid
    
    payload = {
        "jsonrpc": "2.0",
        "method": "resources/read",
        "params": {"uri": uri},
        "id": 4
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(mcp_wrapper.MCP_URL, data=data, headers=headers, method='POST')
    
    with urllib.request.urlopen(req) as response:
        body = response.read().decode('utf-8')
        for line in body.splitlines():
            if line.startswith("data: "):
                resp_json = json.loads(line[6:])
                if "result" in resp_json:
                    # Resource read result has contents list
                    contents = resp_json["result"].get("contents", [])
                    if contents:
                        return contents[0].get("text", "")
    return None

def main():
    print("--- Checking Editor State ---")
    state_json_str = read_resource("unity://editor/state")
    if state_json_str:
        try:
            state = json.loads(state_json_str)
            print(json.dumps(state, indent=2))
        except:
            print(f"Raw state: {state_json_str}")
    else:
        print("Failed to read editor state")

    print("\n--- Checking for Spawner ---")
    mcp_wrapper.call_tool("manage_gameobject", {
        "action": "find",
        "name": "Spawner"
    })

if __name__ == "__main__":
    main()
