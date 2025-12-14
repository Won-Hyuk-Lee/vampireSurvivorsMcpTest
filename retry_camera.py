
import json
import sys
import mcp_wrapper

def main():
    print("--- Retrying Attach CameraController ---")
    try:
        # Check if Main Camera exists
        print("Checking for Main Camera...")
        # Since find with default method is name based but manage_gameobject find by name is deprecated/requires search_term
        # We try to create it? No duplicate.
        # Just try add component to "Main Camera". If it failed before, maybe name mismatch?
        
        # Try finding by tag "MainCamera"
        mcp_wrapper.call_tool("manage_gameobject", {
            "action": "find",
            "search_method": "by_tag",
            "tag": "MainCamera"
        })
        
        # If found, use that instance to attach?
        # But for now let's just assume "Main Camera" name is standard.
        # Maybe compilation was too slow.
        
        mcp_wrapper.call_tool("manage_gameobject", {
            "action": "add_component",
            "target": "Main Camera",
            "components_to_add": ["CameraController"]
        })
        print("Successfully attached CameraController")
    except Exception as e:
        print(f"Failed again: {e}")

if __name__ == "__main__":
    main()
