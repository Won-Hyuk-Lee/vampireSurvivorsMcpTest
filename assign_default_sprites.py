
import json
import sys
import mcp_wrapper

def assign_sprite_to_renderer(object_name, sprite_name, color_r, color_g, color_b):
    """오브젝트의 SpriteRenderer에 Unity 기본 스프라이트 할당"""

    # Unity 기본 스프라이트 경로
    # Circle, Square, Triangle, Diamond, Hexagon, Knob 등
    sprite_path = f"UI/Skin/{sprite_name}"

    tool_args = {
        "action": "set_component_property",
        "target": object_name,
        "search_method": "by_name",
        "component_name": "SpriteRenderer",
        "component_properties": {
            "SpriteRenderer": {
                "sprite": sprite_path,
                "color": {
                    "r": color_r,
                    "g": color_g,
                    "b": color_b,
                    "a": 1.0
                }
            }
        }
    }

    print(f"Assigning sprite '{sprite_name}' to {object_name}...")
    try:
        mcp_wrapper.call_tool("manage_gameobject", tool_args)
        print(f"✓ Success: {object_name}")
    except Exception as e:
        print(f"✗ Failed: {object_name} - {e}")

def assign_sprites_to_prefab(prefab_path, sprite_name, color_r, color_g, color_b):
    """프리팹의 SpriteRenderer에 스프라이트 할당"""

    # 프리팹 스테이지 열기
    print(f"\nOpening prefab: {prefab_path}")

    open_args = {
        "action": "open_stage",
        "prefab_path": prefab_path
    }
    mcp_wrapper.call_tool("manage_prefabs", open_args)

    # 프리팹 루트 오브젝트 이름 추출
    prefab_name = prefab_path.split('/')[-1].replace('.prefab', '')

    # 스프라이트 할당
    assign_sprite_to_renderer(prefab_name, sprite_name, color_r, color_g, color_b)

    # 프리팹 저장 및 닫기
    save_args = {
        "action": "save_open_stage"
    }
    mcp_wrapper.call_tool("manage_prefabs", save_args)

    close_args = {
        "action": "close_stage",
        "save_before_close": True
    }
    mcp_wrapper.call_tool("manage_prefabs", close_args)

    print(f"✓ Prefab {prefab_name} updated")

if __name__ == "__main__":
    print("=" * 60)
    print("Assigning 2D Sprites to Game Objects")
    print("=" * 60)

    # Player - 파란색 원
    print("\n[1/3] Player...")
    assign_sprite_to_renderer("Player", "Knob.psd", 0.3, 0.6, 1.0)

    # Monster Prefab - 빨간색 원
    print("\n[2/3] Monster Prefab...")
    assign_sprites_to_prefab("Assets/Resources/Monster.prefab", "Knob.psd", 1.0, 0.2, 0.2)

    # ExpGem Prefab - 노란색 다이아몬드
    print("\n[3/3] ExpGem Prefab...")
    assign_sprites_to_prefab("Assets/Resources/ExpGem.prefab", "Knob.psd", 1.0, 0.9, 0.2)

    print("\n" + "=" * 60)
    print("✓ All sprites assigned successfully!")
    print("=" * 60)
