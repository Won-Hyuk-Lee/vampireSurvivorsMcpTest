
import json
import sys
import mcp_wrapper

def assign_sprite_to_object(object_name, color_r, color_g, color_b):
    """오브젝트에 기본 스프라이트를 할당하고 색상 설정"""

    # Unity 내장 스프라이트 사용 (Circle)
    tool_args = {
        "action": "set_component_property",
        "target": object_name,
        "search_method": "by_name",
        "component_name": "SpriteRenderer",
        "component_properties": {
            "SpriteRenderer": {
                "color": {
                    "r": color_r,
                    "g": color_g,
                    "b": color_b,
                    "a": 1.0
                }
            }
        }
    }

    print(f"Setting color for {object_name}...")
    mcp_wrapper.call_tool("manage_gameobject", tool_args)

def create_sprite_material():
    """스프라이트용 기본 머티리얼 생성"""
    print("Creating sprite materials...")

    # Player 스프라이트를 Primitive Quad로 대체
    # Player를 Quad primitive로 다시 생성

if __name__ == "__main__":
    print("Assigning sprites to game objects...")

    # Player - 파란색
    assign_sprite_to_object("Player", 0.2, 0.5, 1.0)

    print("\nNote: Sprites need to be assigned manually in Unity Editor or")
    print("we need to create primitive objects with MeshRenderer instead.")
    print("\nAlternative: Use GameObject primitives (Cube/Sphere) for visibility.")
