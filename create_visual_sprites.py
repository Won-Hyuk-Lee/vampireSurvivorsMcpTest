
import json
import sys
import mcp_wrapper

def create_sprite_and_assign():
    """스프라이트 에셋을 생성하고 게임 오브젝트에 할당"""

    print("Creating sprite assets...")

    # 1. Player용 스프라이트 - Circle로 생성
    commands = [
        {
            "tool": "manage_gameobject",
            "params": {
                "action": "create",
                "name": "PlayerVisual",
                "parent": "Player",
                "primitive_type": "Sphere",
                "scale": [1.0, 1.0, 0.1],
                "position": [0.0, 0.0, 0.0]
            }
        }
    ]

    # 배치 실행
    batch_args = {
        "commands": commands
    }

    print("Creating visual objects...")
    mcp_wrapper.call_tool("batch_execute", batch_args)

def delete_sprite_renderers_and_add_mesh():
    """SpriteRenderer를 제거하고 MeshRenderer로 대체"""

    print("\nRemoving SpriteRenderer from Player and adding visual mesh...")

    # Player에 자식 객체로 Cube 추가
    commands = [
        {
            "tool": "manage_gameobject",
            "params": {
                "action": "create",
                "name": "PlayerMesh",
                "parent": "Player",
                "primitive_type": "Cube",
                "scale": [1.0, 1.0, 0.2],
                "position": [0.0, 0.0, 0.0]
            }
        },
        {
            "tool": "manage_gameobject",
            "params": {
                "action": "remove_component",
                "target": "Player",
                "search_method": "by_name",
                "components_to_remove": ["SpriteRenderer"]
            }
        }
    ]

    batch_args = {
        "commands": commands
    }

    mcp_wrapper.call_tool("batch_execute", batch_args)

if __name__ == "__main__":
    print("=" * 60)
    print("Creating visual representations for game objects")
    print("=" * 60)

    delete_sprite_renderers_and_add_mesh()

    print("\nDone! Visual objects created.")
