
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
    # 1. Re-create Monster (since it failed last time)
    run_step("Create Monster Object", "manage_gameobject", {
        "action": "create",
        "name": "Monster",
        "components_to_add": ["SpriteRenderer", "Rigidbody2D", "BoxCollider2D"]
    })

    run_step("Set Monster Color", "manage_gameobject", {
        "action": "modify",
        "name": "Monster",
        "component_properties": {
            "SpriteRenderer": {
                "color": [1, 0, 0, 1] 
            },
            "Rigidbody2D": {
                "gravityScale": 0
            }
        }
    })

    # 2. Attach MonsterMovement
    print("Attaching MonsterMovement...")
    created_monster = True
    try:
        mcp_wrapper.call_tool("manage_gameobject", {
            "action": "add_component",
            "target": "Monster",
            "components_to_add": ["MonsterMovement"]
        })
    except Exception as e:
        print(f"Failed to attach MonsterMovement: {e}")
        # If this fails, maybe script is still invalid? But isCompiling is false.
    
    # 3. Create Prefab (Ensure Resources folder allows this)
    # If Assets/Resources doesn't exist, create it via manage_asset
    try:
        mcp_wrapper.call_tool("manage_asset", {
            "action": "create_folder",
            "path": "Assets/Resources"
        })
    except:
        pass # Ignore if exists

    run_step("Create Monster Prefab", "manage_prefabs", {
        "action": "create_from_gameobject",
        "target": "Monster",
        "prefab_path": "Assets/Resources/Monster.prefab"
    })

    # 4. Remove Monster
    run_step("Delete Scene Monster", "manage_gameobject", {
        "action": "delete",
        "target": "Monster"
    })

    # 5. Attach EnemySpawner to Spawner
    print("Attaching EnemySpawner...")
    try:
        mcp_wrapper.call_tool("manage_gameobject", {
            "action": "add_component",
            "target": "Spawner",
            "components_to_add": ["EnemySpawner"]
        })
    except Exception as e:
        print(f"Failed to attach EnemySpawner: {e}")

    # 6. Save Scene
    run_step("Save Scene", "manage_scene", {
        "action": "save",
        "path": "Assets/Scenes/GameScene.unity"
    })

if __name__ == "__main__":
    main()
