
import json
import sys
import mcp_wrapper

def replace_sprite_with_quad(object_name, color_r, color_g, color_b, scale_z=0.1):
    """SpriteRenderer 대신 Quad Mesh를 사용하여 오브젝트를 시각화"""

    print(f"Making {object_name} visible with Quad mesh...")

    commands = [
        # 1. SpriteRenderer 제거
        {
            "tool": "manage_gameobject",
            "params": {
                "action": "remove_component",
                "target": object_name,
                "search_method": "by_name",
                "components_to_remove": ["SpriteRenderer"]
            }
        },
        # 2. 시각적 자식 객체 생성 (Quad)
        {
            "tool": "manage_gameobject",
            "params": {
                "action": "create",
                "name": f"{object_name}Visual",
                "parent": object_name,
                "primitive_type": "Quad",
                "scale": [1.0, 1.0, scale_z]
            }
        }
    ]

    batch_args = {"commands": commands}
    mcp_wrapper.call_tool("batch_execute", batch_args)

    # 색상 설정
    print(f"Setting color for {object_name}Visual...")
    color_args = {
        "action": "set_component_property",
        "target": f"{object_name}Visual",
        "search_method": "by_name",
        "component_name": "MeshRenderer",
        "component_properties": {
            "MeshRenderer": {
                "material": {
                    "color": {
                        "r": color_r,
                        "g": color_g,
                        "b": color_b,
                        "a": 1.0
                    }
                }
            }
        }
    }

    try:
        mcp_wrapper.call_tool("manage_gameobject", color_args)
        print(f"OK: {object_name} is now visible")
    except Exception as e:
        print(f"Color setting may need manual adjustment: {e}")

def make_prefab_visible(prefab_path, object_name, color_r, color_g, color_b):
    """프리팹을 시각화"""

    print(f"\nProcessing prefab: {prefab_path}")

    # 프리팹 열기
    open_args = {"action": "open_stage", "prefab_path": prefab_path}
    mcp_wrapper.call_tool("manage_prefabs", open_args)

    # Quad로 대체
    replace_sprite_with_quad(object_name, color_r, color_g, color_b)

    # 프리팹 저장 및 닫기
    mcp_wrapper.call_tool("manage_prefabs", {"action": "save_open_stage"})
    mcp_wrapper.call_tool("manage_prefabs", {"action": "close_stage", "save_before_close": True})

    print(f"OK: {object_name} prefab updated")

if __name__ == "__main__":
    print("=" * 60)
    print("Making Game Objects Visible")
    print("=" * 60)

    # Player - 파란색
    print("\n[1/4] Player...")
    replace_sprite_with_quad("Player", 0.3, 0.6, 1.0)

    # Ground - 회색 (이미 MeshRenderer 있음, 색상만 변경)
    print("\n[2/4] Ground...")
    print("Ground already has MeshRenderer, skipping...")

    # Monster Prefab - 빨간색
    print("\n[3/4] Monster Prefab...")
    make_prefab_visible("Assets/Resources/Monster.prefab", "Monster", 1.0, 0.2, 0.2)

    # ExpGem Prefab - 노란색
    print("\n[4/4] ExpGem Prefab...")
    make_prefab_visible("Assets/Resources/ExpGem.prefab", "ExpGem", 1.0, 0.9, 0.2)

    # 씬 저장
    print("\nSaving scene...")
    mcp_wrapper.call_tool("manage_scene", {"action": "save"})

    print("\n" + "=" * 60)
    print("Done! All objects should now be visible.")
    print("=" * 60)
