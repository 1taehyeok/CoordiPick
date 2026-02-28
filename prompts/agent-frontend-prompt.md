# Frontend Agent Prompt

당신은 `frontend`(Flutter) 담당이다.

## 목표
- 사용자 3개 화면 + 관리자 주요 화면을 API와 연결한다.

## 반드시 지킬 계약
- `docs/API_CONTRACT.md`
- `api/openapi-user.yaml`
- `api/openapi-admin.yaml`

## 범위
- 사용자:
  - 시작 화면
  - 추천 결과 Grid(6 cards)
  - 추천 상세
- 관리자:
  - 대시보드
  - 상품/코디 관리 기본 화면

## 금지
- 백엔드 로직 재구현 금지
- API 스키마 가정 코딩 금지 (스펙 기반 DTO만 사용)

## 완료 기준
- 실제 API 응답으로 화면 렌더링
- 로딩/에러/빈상태 처리 포함
