
import json
import sys
import mcp_wrapper

def main():
    print("--- Verifying Scene State ---")
    
    # Get Hierarchy
    try:
        # We need to capture output properly.
        # Calling mcp_wrapper.call_tool prints result to stdout.
        # We can just run it and see the output.
        mcp_wrapper.call_tool("manage_scene", {"action": "get_hierarchy"})
        
        # Check Player components specifically?
        # manage_gameobject action=find? or get_components?
        # manage_gameobject does not have "get_components" action directly, wait.
        # Checking tools.json...
        # manage_gameobject action enum: ..., "get_components", ...
        # Yes it does!
        
        print("\n--- Player Components ---")
        mcp_wrapper.call_tool("manage_gameobject", {
            "action": "get_components",
            "target": "Player"
        })
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
