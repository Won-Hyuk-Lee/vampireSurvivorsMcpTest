
import json
import sys
import time
import mcp_wrapper

def run_step(step_name, tool, args, expected_error_substr=None):
    print(f"--- Executing Step: {step_name} ---")
    try:
        # mcp_wrapper.call_tool prints to stdout
        # We might miss errors if we don't capture properly, but for now we rely on exceptions
        mcp_wrapper.call_tool(tool, args)
        print(f"--- Step {step_name} Completed ---\n")
    except SystemExit:
        # mcp_wrapper exits on error
        if expected_error_substr:
            print(f"(Expected error occurring, continuing...)")
            pass
        else:
            raise
    except Exception as e:
        print(f"--- Step {step_name} FAILED: {e} ---")
        sys.exit(1)

def main():
    # 1. Scripts Creation
    
    # MonsterMovement.cs
    # Simple logic: Find Player, Move towards it.
    monster_script = """using UnityEngine;

public class MonsterMovement : MonoBehaviour
{
    public float speed = 2f;
    private Transform player;
    private Rigidbody2D rb;

    void Start()
    {
        // Modern Unity finding (Unity 2023+ prefers FindFirstObjectByType)
        // Check API compatibility, use classic FindObjectOfType for now for safety or try/catch
        player = GameObject.Find("Player")?.transform;
        rb = GetComponent<Rigidbody2D>();
    }

    void FixedUpdate()
    {
        if (player != null && rb != null)
        {
            Vector2 direction = (player.position - transform.position).normalized;
            rb.velocity = direction * speed;
        }
        else if (player == null)
        {
             // Try to find player again if lost (e.g. player died and respawned, or scene reload)
             var p = GameObject.Find("Player");
             if (p) player = p.transform;
             rb.velocity = Vector2.zero;
        }
    }
}
"""
    run_step("Create MonsterMovement Script", "create_script", {
        "path": "Assets/Scripts/MonsterMovement.cs",
        "contents": monster_script
    })

    # EnemySpawner.cs
    # Spawns monster prefab every N seconds at random position
    # Uses Resources.Load for simplicity in assigning prefab reference via code
    spawner_script = """using UnityEngine;
using System.Collections;

public class EnemySpawner : MonoBehaviour
{
    public GameObject monsterPrefab;
    public float spawnInterval = 3f;
    public float spawnRadius = 10f;

    void Start()
    {
        if (monsterPrefab == null)
        {
            // Fallback load from Resources if not assigned
            monsterPrefab = Resources.Load<GameObject>("Monster");
        }
        StartCoroutine(SpawnRoutine());
    }

    IEnumerator SpawnRoutine()
    {
        while (true)
        {
            yield return new WaitForSeconds(spawnInterval);
            SpawnMonster();
        }
    }

    void SpawnMonster()
    {
        if (monsterPrefab == null) return;

        Vector2 randomPos = Random.insideUnitCircle.normalized * spawnRadius;
        // Assume spawner is at (0,0) or add to spawner's pos
        Vector3 spawnPos = transform.position + (Vector3)randomPos;
        
        Instantiate(monsterPrefab, spawnPos, Quaternion.identity);
    }
}
"""
    run_step("Create EnemySpawner Script", "create_script", {
        "path": "Assets/Scripts/EnemySpawner.cs",
        "contents": spawner_script
    })

    print("Waiting 5 seconds for compilation...")
    time.sleep(5)

    # 2. Create Resources Folder
    run_step("Create Resources Folder", "manage_asset", {
        "action": "create_folder",
        "path": "Assets/Resources"
    })

    # 3. Create Monster GameObject
    run_step("Create Monster Object", "manage_gameobject", {
        "action": "create",
        "name": "Monster",
        "components_to_add": ["SpriteRenderer", "Rigidbody2D", "BoxCollider2D"]
    })

    # 4. Config Monster
    # Set Sprite color to Red (to distinguish)
    run_step("Set Monster Color", "manage_gameobject", {
        "action": "modify",
        "name": "Monster",
        "component_properties": {
            "SpriteRenderer": {
                "color": [1, 0, 0, 1] # RGBA
            },
            "Rigidbody2D": {
                "gravityScale": 0
            }
        }
    })

    # 5. Attach MonsterMovement
    # Retry logic needed?
    print("Attaching MonsterMovement...")
    for i in range(5):
        try:
             # We assume manage_gameobject throws/returns error if fails
             # Using mcp_wrapper directly inside try block of run_step won't work perfectly with retry
             # So we call mcp_wrapper.call_tool manually here
             mcp_wrapper.call_tool("manage_gameobject", {
                "action": "add_component",
                "target": "Monster",
                "components_to_add": ["MonsterMovement"]
             })
             print("Attached MonsterMovement")
             break
        except Exception:
            time.sleep(2)
            if i == 4: print("Warning: Could not attach MonsterMovement (compilation lag?)")

    # 6. Create Prefab
    # We save it to Assets/Resources/Monster.prefab
    run_step("Create Monster Prefab", "manage_prefabs", {
        "action": "create_from_gameobject",
        "target": "Monster", # hierarchy name
        "prefab_path": "Assets/Resources/Monster.prefab"
    })

    # 7. Delete Monster from Scene (cleanup)
    run_step("Delete Scene Monster", "manage_gameobject", {
        "action": "delete",
        "target": "Monster"
    })

    # 8. Create Spawner Object
    run_step("Create Spawner Object", "manage_gameobject", {
        "action": "create",
        "name": "Spawner"
    })

    # 9. Attach EnemySpawner
    print("Attaching EnemySpawner...")
    for i in range(5):
        try:
             mcp_wrapper.call_tool("manage_gameobject", {
                "action": "add_component",
                "target": "Spawner",
                "components_to_add": ["EnemySpawner"]
             })
             print("Attached EnemySpawner")
             break
        except Exception:
            time.sleep(2)
    
    # 10. Save Scene
    run_step("Save Scene", "manage_scene", {
        "action": "save",
        "path": "Assets/Scenes/GameScene.unity"
    })

if __name__ == "__main__":
    main()
