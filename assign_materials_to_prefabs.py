
import json
import sys
import mcp_wrapper

def assign_material_to_prefab_sprite(prefab_path, material_path):
    """프리팹의 SpriteRenderer에 머티리얼 할당"""

    # 프리팹 파일 이름 추출
    prefab_name = prefab_path.split('/')[-1].replace('.prefab', '')

    print(f"Processing {prefab_name} prefab...")

    # 프리팹 열기
    open_args = {
        "action": "open_stage",
        "prefab_path": prefab_path
    }
    result = mcp_wrapper.call_tool("manage_prefabs", open_args)
    print(f"Opened prefab stage: {result}")

    # 프리팹 루트의 계층구조 가져오기
    hierarchy_args = {
        "action": "get_prefab_hierarchy",
        "prefab_path": prefab_path
    }
    hierarchy = mcp_wrapper.call_tool("manage_prefabs", hierarchy_args)
    print(f"Hierarchy: {hierarchy}")

    # 머티리얼 할당 (by_instance_id 사용)
    try:
        # 먼저 prefab_path로 직접 시도
        material_args = {
            "action": "assign_material_to_renderer",
            "prefab_path": prefab_path,
            "material_path": material_path
        }
        result = mcp_wrapper.call_tool("manage_material", material_args)
        print(f"Material assignment result: {result}")
    except Exception as e:
        print(f"Failed to assign material: {e}")

    # 프리팹 저장 및 닫기
    save_args = {
        "action": "save_open_stage"
    }
    mcp_wrapper.call_tool("manage_prefabs", save_args)
    print("Saved prefab")

    close_args = {
        "action": "close_stage",
        "save_before_close": True
    }
    mcp_wrapper.call_tool("manage_prefabs", close_args)
    print(f"{prefab_name} prefab processing complete\n")

if __name__ == "__main__":
    print("=" * 60)
    print("Assigning Materials to Prefabs")
    print("=" * 60 + "\n")

    # Monster Prefab - 빨간색
    print("[1/2] Monster Prefab...")
    assign_material_to_prefab_sprite("Assets/Resources/Monster.prefab", "Assets/Materials/MonsterMat.mat")

    # ExpGem Prefab - 노란색
    print("[2/2] ExpGem Prefab...")
    assign_material_to_prefab_sprite("Assets/Resources/ExpGem.prefab", "Assets/Materials/ExpGemMat.mat")

    # 씬 저장
    print("Saving scene...")
    mcp_wrapper.call_tool("manage_scene", {"action": "save"})

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
