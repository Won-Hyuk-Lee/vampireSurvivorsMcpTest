# Vampire Survivors Unity MCP Test Plan

이 문서는 Unity MCP(Model Context Protocol) 기능을 테스트하기 위해 뱀파이어 서바이벌 핵심 로직을 단계별로 구현하는 계획을 담고 있습니다.

## Phase 1: 기초 공사 (Scene & Player & Map)
**목표**: MCP를 통해 씬을 만들고, 객체를 배치하고, 스크립트를 붙여서 움직이게 할 수 있는지 검증.
- [x] **1. 씬 생성**: 빈 씬 (`GameScene`) 생성 및 저장
- [x] **2. 플레이어 객체 생성**: `Player` GameObject 생성 (SpriteRenderer 포함)
- [x] **3. 컴포넌트 부착**: 
    - [x] `Rigidbody2D` (Gravity Scale 0 설정)
    - [x] `BoxCollider2D`
- [x] **4. 이동 구현**: 
    - [x] `PlayerController.cs` 스크립트 작성 (Input System 또는 Legacy Input 사용)
    - [ ] 스크립트를 `Player` 객체에 컴포넌트로 부착 (컴파일 대기 중)
- [x] **5. 카메라 및 맵**:
    - [x] Main Camera가 Player를 따라다니도록 설정 (`CameraController.cs` 생성 및 부착 시도 중)
    - [x] 바닥(Ground) 객체 배치 (무한 맵 테스트용 기초)

## Phase 2: 적과 스포너 (Object & Spawning)
**목표**: 동적으로 객체를 생성(Prefab)하고, 간단한 AI 로직을 심을 수 있는지 검증.
- [x] **1. 몬스터 프리팹 준비**:
    - [x] `Monster` 객체 생성
    - [x] `Rigidbody2D`, `BoxCollider2D` 부착
    - [x] 프리팹(Prefab)으로 저장
- [x] **2. 몬스터 이동**:
    - [x] `MonsterMovement.cs` 작성 (플레이어 위치로 이동)
    - [x] 몬스터 프리팹에 스크립트 부착
- [x] **3. 스포너 구현**:
    - [x] `EnemySpawner.cs` 작성 (일정 시간 간격으로 몬스터 생성)
    - [x] 씬에 `Spawner` 객체 배치 및 스크립트 연결

## Phase 3: 전투 및 루프 완성 (Combat & Exp)
**목표**: 객체 간의 상호작용(충돌, 삭제, 보상)을 구현 가능한지 검증.
- [x] **1. 기본 공격 (마늘/오라)**:
    - [x] `Weapon` 자식 객체 생성 및 반경 설정
    - [x] `WeaponAura.cs` 작성
- [x] **2. 충돌 처리**:
    - [x] `OnTriggerEnter2D`를 활용한 데미지 로직 구현
    - [x] 몬스터 체력 관리 및 사망(Destroy) 처리
- [x] **3. 경험치 시스템**:
    - [x] `ExpGem` 프리팹 생성
    - [x] 몬스터 사망 시 해당 위치에 `ExpGem` 스폰
    - [x] 플레이어가 획득 시 젬 삭제 및 로그 출력
