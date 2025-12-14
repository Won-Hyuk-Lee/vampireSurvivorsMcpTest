
import json
import sys
import time
import mcp_wrapper

def run_step(step_name, tool, args, ignore_error=False):
    print(f"--- Executing Step: {step_name} ---")
    try:
        mcp_wrapper.call_tool(tool, args)
        print(f"--- Step {step_name} Completed ---\n")
    except Exception as e:
        print(f"--- Step {step_name} FAILED: {e} ---")
        if not ignore_error:
            sys.exit(1)

def main():
    # 1. Add Tags
    tags = ["Monster", "Gem"]
    for tag in tags:
        run_step(f"Add Tag {tag}", "manage_editor", {
            "action": "add_tag",
            "tag_name": tag
        }, ignore_error=True) # Ignore if exists

    # 2. Create Scripts
    
    # EnemyHealth.cs
    enemy_health_script = """using UnityEngine;

public class EnemyHealth : MonoBehaviour
{
    public float hp = 10f;
    public GameObject gemPrefab;

    void Start()
    {
        if (gemPrefab == null) gemPrefab = Resources.Load<GameObject>("ExpGem");
    }

    public void TakeDamage(float amount)
    {
        hp -= amount;
        if (hp <= 0) Die();
    }

    void Die()
    {
        if (gemPrefab != null)
        {
            Instantiate(gemPrefab, transform.position, Quaternion.identity);
        }
        Destroy(gameObject);
    }
}
"""
    run_step("Create EnemyHealth Script", "create_script", {
        "path": "Assets/Scripts/EnemyHealth.cs",
        "contents": enemy_health_script
    })

    # WeaponAura.cs
    weapon_script = """using UnityEngine;

public class WeaponAura : MonoBehaviour
{
    public float dps = 5f;

    void OnTriggerStay2D(Collider2D other)
    {
        // Simple DPS check
        if (other.CompareTag("Monster"))
        {
            var health = other.GetComponent<EnemyHealth>();
            if (health != null)
            {
                health.TakeDamage(dps * Time.deltaTime);
            }
        }
    }
}
"""
    run_step("Create WeaponAura Script", "create_script", {
        "path": "Assets/Scripts/WeaponAura.cs",
        "contents": weapon_script
    })

    # ExpGem.cs
    # Using OnTriggerEnter to detect Player
    gem_script = """using UnityEngine;

public class ExpGem : MonoBehaviour
{
    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.name == "Player" || other.CompareTag("Player"))
        {
            Debug.Log("EXP GEM COLLECTED!");
            Destroy(gameObject);
        }
    }
}
"""
    run_step("Create ExpGem Script", "create_script", {
        "path": "Assets/Scripts/ExpGem.cs",
        "contents": gem_script
    })

    print("Waiting 5 seconds for compilation...")
    time.sleep(5)

    # 3. Create ExpGem Prefab
    run_step("Create ExpGem Object", "manage_gameobject", {
        "action": "create",
        "name": "ExpGem",
        "tag": "Gem",
        "components_to_add": ["SpriteRenderer", "CircleCollider2D"]
    })

    run_step("Config ExpGem", "manage_gameobject", {
        "action": "modify",
        "name": "ExpGem",
        "component_properties": {
            "SpriteRenderer": {
                "color": [0, 1, 0, 1] # Green
            },
            "CircleCollider2D": {
                "isTrigger": True,
                "radius": 0.5
            },
            "Transform": {
                "scale": [0.5, 0.5, 1]
            }
        }
    })

    print("Attaching ExpGem Script...")
    try:
        mcp_wrapper.call_tool("manage_gameobject", {
            "action": "add_component",
            "target": "ExpGem",
            "components_to_add": ["ExpGem"]
        })
    except:
        print("Retrying attachment...")
        time.sleep(2)
        mcp_wrapper.call_tool("manage_gameobject", {
            "action": "add_component",
            "target": "ExpGem",
            "components_to_add": ["ExpGem"]
        })

    run_step("Save ExpGem Prefab", "manage_prefabs", {
        "action": "create_from_gameobject",
        "target": "ExpGem",
        "prefab_path": "Assets/Resources/ExpGem.prefab"
    })

    run_step("Delete Scene ExpGem", "manage_gameobject", {
        "action": "delete",
        "target": "ExpGem"
    })

    # 4. Update Monster Prefab (Add EnemyHealth & Tag)
    # We will instantiate the existing monster prefab, modify it, and overwrite.
    # But wait, how do we load prefab into scene easily if we don't know uuid? 
    # We can use manage_scene -> create to make a clean slate or just Instantiate via Spawner? No.
    # We can use `manage_asset` to get info? 
    # Actually, simpler: create a new Monster object, configure everything, save as prefab (overwrite).
    # Since we know the config from phase 2, we can just redo it + new stuff.
    
    run_step("Create Temp Monster", "manage_gameobject", {
        "action": "create",
        "name": "TempMonster",
        "tag": "Monster",
        "components_to_add": ["SpriteRenderer", "Rigidbody2D", "BoxCollider2D", "MonsterMovement"]
    })
    
    run_step("Config Temp Monster", "manage_gameobject", {
        "action": "modify",
        "name": "TempMonster",
        "component_properties": {
            "SpriteRenderer": { "color": [1, 0, 0, 1] },
            "Rigidbody2D": { "gravityScale": 0 }
        }
    })
    
    # Attach EnemyHealth
    print("Attaching EnemyHealth to Monster...")
    try:
         mcp_wrapper.call_tool("manage_gameobject", {
            "action": "add_component",
            "target": "TempMonster",
            "components_to_add": ["EnemyHealth"]
         })
    except:
        pass

    run_step("Overwrite Monster Prefab", "manage_prefabs", {
        "action": "create_from_gameobject",
        "target": "TempMonster",
        "prefab_path": "Assets/Resources/Monster.prefab",
        "allow_overwrite": True
    })

    run_step("Delete Temp Monster", "manage_gameobject", {
        "action": "delete",
        "target": "TempMonster"
    })

    # 5. Setup Weapon Aura on Player
    # Find Player first
    run_step("Create Aura Object", "manage_gameobject", {
        "action": "create",
        "name": "WeaponAura",
        "parent": "Player",
        "components_to_add": ["CircleCollider2D", "WeaponAura"] # Assuming scripts compiled
    })

    run_step("Config Aura", "manage_gameobject", {
        "action": "modify",
        "name": "WeaponAura",
        "component_properties": {
            "CircleCollider2D": {
                "isTrigger": True,
                "radius": 3.0
            },
            # "WeaponAura": { "dps": 10 } # Can we set script fields? manage_gameobject allows setting component properties via reflection if supported
        }
    })
    
    # 6. Save Scene
    run_step("Save Scene", "manage_scene", {
        "action": "save",
        "path": "Assets/Scenes/GameScene.unity"
    })

if __name__ == "__main__":
    main()
