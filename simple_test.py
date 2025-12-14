
import json
import sys
import mcp_wrapper

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python simple_test.py <tool_name> '<json_args>'")
        sys.exit(1)
    
    tool_name = sys.argv[1]
    args_str = sys.argv[2]
    try:
        args = json.loads(args_str)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON args: {e}", file=sys.stderr)
        sys.exit(1)
        
    mcp_wrapper.call_tool(tool_name, args)
