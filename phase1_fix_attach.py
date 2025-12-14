
import time
import sys
import json
import urllib.request
import mcp_wrapper

def main():
    print("Attempting to attach PlayerController...")
    
    max_retries = 10
    tool_name = "manage_gameobject"
    
    for i in range(max_retries):
        print(f"Attempt {i+1}/{max_retries}...")
        
        # We need to capture the output of mcp_wrapper to check for success: false
        # Since mcp_wrapper prints to stdout, we can't easily capture it without modifying it 
        # or redirecting stdout.
        # But we can import it and modify the call_tool function or just duplicate logic.
        
        # Let's use the mcp_wrapper's logic but customized here.
        sid = mcp_wrapper.get_session_id()
        headers = mcp_wrapper.HEADERS.copy()
        headers["mcp-session-id"] = sid
        
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": {
                    "action": "add_component",
                    "target": "Player",
                    "components_to_add": ["PlayerController"]
                }
            },
            "id": i+100
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(mcp_wrapper.MCP_URL, data=data, headers=headers, method='POST')
        
        # import urllib.request was here
        
        try:
            with urllib.request.urlopen(req) as response:
                body = response.read().decode('utf-8')
                for line in body.splitlines():
                    if line.startswith("data: "):
                        resp_json = json.loads(line[6:])
                        if "result" in resp_json:
                            # Check if the text content contains "success":false
                            content = resp_json["result"].get("content", [])
                            text_content = ""
                            for c in content:
                                if c.get("type") == "text":
                                    text_content += c.get("text", "")
                            
                            # The tool returns a JSON string inside the text field!
                            # We need to parse that inner JSON.
                            try:
                                inner_json = json.loads(text_content)
                                if inner_json.get("success") == True:
                                    print("SUCCESS: Component attached!")
                                    return
                                else:
                                    print(f"Failed: {inner_json.get('error')}")
                            except:
                                print(f"Could not parse tool result: {text_content}")
        except Exception as e:
            print(f"Error executing tool: {e}")
        
        time.sleep(5)
    
    print("Failed to attach component after all retries.")
    sys.exit(1)

if __name__ == "__main__":
    main()
