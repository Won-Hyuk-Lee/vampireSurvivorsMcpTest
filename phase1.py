
import json
import sys
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
    # 1. Create Scene
    run_step("Create Scene", "manage_scene", {
        "action": "create",
        "name": "GameScene"
    })

    # 2. Save Scene (to ensure it exists on disk)
    run_step("Save Scene", "manage_scene", {
        "action": "save",
        "path": "Assets/Scenes/GameScene.unity"
    })

    # 3. Create Player (Empty GameObject with components)
    run_step("Create Player", "manage_gameobject", {
        "action": "create",
        "name": "Player",
        "components_to_add": ["SpriteRenderer", "Rigidbody2D", "BoxCollider2D"]
    })

    # 4. Configure Rigidbody2D (Gravity Scale 0)
    # The tool definition says component_properties is a map of component_name -> map of properties
    run_step("Configure Player Rigidbody", "manage_gameobject", {
        "action": "modify",
        "name": "Player",
        "component_properties": {
            "Rigidbody2D": {
                "gravityScale": 0,
                "constraints": 4 # Freeze Rotation Z? (Constraints enum is bitmask. None=0, FreezePos=1|2|4, FreezeRot=4? No. Z is 4 in 2D? Wait. 
                # Constraints2D: None=0, FreezePosX=1, FreezePosY=2, FreezeRotation=4.
                # So 4 is FreezeRotationZ.
            }
        }
    })

    # 5. Create PlayerController Script
    script_content = """using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float moveSpeed = 5f;
    private Rigidbody2D rb;
    private Vector2 moveInput;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        moveInput.x = Input.GetAxisRaw("Horizontal");
        moveInput.y = Input.GetAxisRaw("Vertical");
        moveInput.Normalize();
    }

    void FixedUpdate()
    {
        rb.velocity = moveInput * moveSpeed;
    }
}
"""
    run_step("Create PlayerController Script", "create_script", {
        "path": "Assets/Scripts/PlayerController.cs",
        "contents": script_content
    })

    # 6. Wait for compilation? 
    # The MCP server usually handles this async, or returns immediately?
    # The instructions said: "You can poll the editor_state resource...".
    # But for simplicity, let's just try to add the component. If it fails (script not found), we might need to wait.
    # We'll try to add it. If it fails, maybe retry loop?
    # But create_script might trigger a domain reload.
    
    import time
    print("Waiting 5 seconds for compilation...")
    time.sleep(5) 

    # 7. Attach PlayerController to Player
    # We loop a few times to retry if script is not yet compiled
    max_retries = 5
    for i in range(max_retries):
        try:
            print(f"Attempt {i+1} to attach component...")
            mcp_wrapper.call_tool("manage_gameobject", {
                "action": "add_component",
                "target": "Player",
                "components_to_add": ["PlayerController"]
            })
            print("Component attached successfully")
            break
        except Exception:
            if i == max_retries - 1:
                print("Failed to attach component after retries")
                sys.exit(1)
            time.sleep(3)

    # 8. Create Ground (Quad)
    run_step("Create Ground", "manage_gameobject", {
        "action": "create",
        "name": "Ground",
        "primitive_type": "Quad",
        "scale": [50, 50, 1]
    })
    
    # 9. Save Scene Again
    run_step("Final Save", "manage_scene", {
        "action": "save",
        "path": "Assets/Scenes/GameScene.unity"
    })

if __name__ == "__main__":
    main()
