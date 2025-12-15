
import json
import sys
import mcp_wrapper

def create_sprite_asset(asset_name, path):
    """스프라이트 에셋 생성"""

    # Texture2D를 생성하고 스프라이트로 변환
    tool_args = {
        "action": "create",
        "path": path,
        "asset_type": "Sprite",
        "properties": {
            "name": asset_name,
            "pixelsPerUnit": 100.0,
            "pivot": {"x": 0.5, "y": 0.5}
        }
    }

    print(f"Creating sprite asset: {asset_name}")
    try:
        mcp_wrapper.call_tool("manage_asset", tool_args)
        print(f"Success: {asset_name} created at {path}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    print("Creating sprite assets...")

    # Player 스프라이트
    create_sprite_asset("PlayerSprite", "Assets/Sprites/PlayerSprite.png")

    # Monster 스프라이트
    create_sprite_asset("MonsterSprite", "Assets/Sprites/MonsterSprite.png")

    # ExpGem 스프라이트
    create_sprite_asset("ExpGemSprite", "Assets/Sprites/ExpGemSprite.png")

    print("Done!")
