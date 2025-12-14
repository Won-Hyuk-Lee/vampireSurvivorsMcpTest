
import urllib.request
import json
import sys
import os

MCP_URL = "http://localhost:8080/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

def get_session_id():
    init_payload = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05", 
            "capabilities": {},
            "clientInfo": {"name": "agent-client", "version": "1.0"}
        },
        "id": 1
    }
    data = json.dumps(init_payload).encode('utf-8')
    req = urllib.request.Request(MCP_URL, data=data, headers=HEADERS, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            sid = response.getheader('mcp-session-id')
            # Consume body
            _ = response.read()
            return sid
    except Exception as e:
        print(f"Init Error: {e}", file=sys.stderr)
        return None

def call_tool(tool_name, tool_args):
    sid = get_session_id()
    if not sid:
        print("Failed to get session ID", file=sys.stderr)
        sys.exit(1)

    # Update headers with session ID
    headers = HEADERS.copy()
    headers["mcp-session-id"] = sid
    
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": tool_args
        },
        "id": 2
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(MCP_URL, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode('utf-8')
            # Parse SSE response to extract result
            # Expected format: event: message \n data: JSON
            for line in body.splitlines():
                if line.startswith("data: "):
                    resp_json = json.loads(line[6:])
                    if "error" in resp_json:
                        print(f"Tool Error: {json.dumps(resp_json['error'])}", file=sys.stderr)
                        sys.exit(1)
                    if "result" in resp_json:
                        print(json.dumps(resp_json["result"], indent=2), flush=True)
                        return
            print(f"No result found in response: {body}", file=sys.stderr)
    except Exception as e:
        print(f"Tool Execution Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mcp_wrapper.py <tool_name> '<json_args>'")
        sys.exit(1)
    
    tool_name = sys.argv[1]
    args_str = sys.argv[2]
    try:
        args = json.loads(args_str)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON args: {e}", file=sys.stderr)
        sys.exit(1)
        
    call_tool(tool_name, args)
