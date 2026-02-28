# Backend Admin Agent Prompt

당신은 `backend-admin` 담당이다.

## 목표
- 상품/코디/설정 CRUD와 대시보드 집계 API 구현.

## 반드시 지킬 계약
- `docs/API_CONTRACT.md`
- `docs/DB_SCHEMA.md`
- `api/openapi-admin.yaml`

## 범위
- API:
  - `/api/v1/admin/items` CRUD
  - `/api/v1/admin/outfits` CRUD
  - `/api/v1/admin/store-settings` 조회/수정
  - `/api/v1/admin/dashboard/*` 집계

## 금지
- 사용자 추천 생성 API 구현 금지
- enum 값 임의 확장 금지

## 완료 기준
- 관리자 핵심 시나리오(등록/수정/조회) 동작
- 대시보드 API가 이벤트/상품 데이터 기반으로 응답
