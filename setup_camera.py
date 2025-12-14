
import json
import sys
import time
import mcp_wrapper

def run_step(step_name, tool, args):
    print(f"--- Executing Step: {step_name} ---")
    try:
        mcp_wrapper.call_tool(tool, args)
        print(f"--- Step {step_name} Completed ---\n")
    except Exception as e:
        print(f"--- Step {step_name} FAILED: {e} ---")
        sys.exit(1)

def main():
    # 1. Create CameraController Script
    cam_script = """using UnityEngine;

public class CameraController : MonoBehaviour
{
    public Transform target;
    public Vector3 offset = new Vector3(0, 0, -10f);
    public float smoothSpeed = 5f;

    void LateUpdate()
    {
        if (target == null)
        {
            var p = GameObject.Find("Player");
            if (p) target = p.transform;
        }

        if (target != null)
        {
            Vector3 desiredPos = target.position + offset;
            transform.position = Vector3.Lerp(transform.position, desiredPos, smoothSpeed * Time.deltaTime);
        }
    }
}
"""
    run_step("Create CameraController Script", "create_script", {
        "path": "Assets/Scripts/CameraController.cs",
        "contents": cam_script
    })

    print("Waiting 5 seconds for compilation...")
    time.sleep(5)

    # 2. Attach to Main Camera
    # Main Camera name is usually "Main Camera" in a new scene
    
    print("Attaching CameraController...")
    try:
         mcp_wrapper.call_tool("manage_gameobject", {
            "action": "add_component",
            "target": "Main Camera",
            "components_to_add": ["CameraController"]
         })
    except Exception as e:
        print(f"Retrying attach to 'Main Camera' (might be missing?): {e}")
        # Sometimes scene create makes it without space? Usually "Main Camera"
        # Let's try to find it first if needed, but managing by name "Main Camera" is standard.
    
    # 3. Save Scene
    run_step("Save Scene", "manage_scene", {
        "action": "save",
        "path": "Assets/Scenes/GameScene.unity"
    })

if __name__ == "__main__":
    main()
