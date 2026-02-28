# CoordiPick Orchestration Runbook

## 1) 착수 순서
1. `docs/API_CONTRACT.md`, `docs/DB_SCHEMA.md`, `api/*.yaml` 확정
2. `backend-admin` 구현 시작
3. `backend-user` 구현 시작
4. `frontend` 구현 시작

## 2) 일일 동기화 포맷
- 각 에이전트는 아래만 보고:
  - 변경한 API endpoint
  - 변경한 schema/table
  - 리스크 1~2개
  - 다음 작업

## 3) 병합 게이트
1. OpenAPI 스펙과 실제 응답 필드 일치
2. Enum 사전 위반 없음
3. 에러 응답 envelope 일치
4. 최소 테스트 통과

## 4) 충돌 해결 원칙
1. 코드보다 스펙 먼저 수정
2. 네이밍 충돌 시 기존 클라이언트 영향이 적은 쪽을 변경
3. 브레이킹 변경은 `v1`에서 금지, 필요 시 별도 경로 추가
