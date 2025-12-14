
import json
import sys
import mcp_wrapper
import urllib.request

def main():
    print("--- Listing Resources ---")
    sid = mcp_wrapper.get_session_id()
    if not sid:
        print("Failed to get session ID")
        return

    headers = mcp_wrapper.HEADERS.copy()
    headers["mcp-session-id"] = sid
    
    payload = {
        "jsonrpc": "2.0",
        "method": "resources/list",
        "params": {},
        "id": 3
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(mcp_wrapper.MCP_URL, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode('utf-8')
            for line in body.splitlines():
                if line.startswith("data: "):
                    resp_json = json.loads(line[6:])
                    if "result" in resp_json:
                        print(json.dumps(resp_json["result"], indent=2))
                        return
            print(f"No result found: {body}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
