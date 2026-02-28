# CoordiPick Architecture (MVP + Recommendation Upgrade Path)

## 1) 서비스 경계
- `frontend` (Flutter): 사용자/관리자 UI, 상태관리, API 호출
- `backend-user` (FastAPI): 추천 생성/조회, 이벤트 수집
- `backend-admin` (FastAPI): 상품/코디/설정 CRUD, 대시보드 집계
- `postgresql` (shared): 단일 DB, 스키마 분리(`core`, `admin`, `analytics`)

## 2) 데이터 흐름
1. 사용자 앱이 `POST /api/v1/recommendations/generate` 호출
2. `backend-user`가 아이템 후보 필터링 + 조합 + 점수화 후 카드 6개 반환
3. 사용자 상세 조회/클릭 시 이벤트를 `POST /api/v1/events`로 적재
4. `backend-admin`은 집계 API로 TOP3, TPO 비율, 재고부족을 제공

## 3) 추천 엔진 파이프라인
1. Candidate: 성별/TPO/온도/재고 기반 후보 필터
2. Scoring: TPO/온도/mood/가격대/재고 점수 가중합
3. Compose: slot(top/bottom/shoes/outer) 조합 생성
4. Re-rank: 다양성 패널티 적용 후 상위 6개 선택
5. Explain: reason tags 생성 (예: `date_match`, `temp_fit`)

## 4) 고도화 포인트
- `analytics.events` 기반으로 가중치 자동 튜닝
- `features` 저장 후 learning-to-rank 모델 교체 가능
- 룰 기반과 AI 생성(`generation_source`)을 병행 운영

## 5) 브랜치/워크트리 운영
- `feat/backend-user`
- `feat/backend-admin`
- `feat/frontend`
- 오케스트레이터는 OpenAPI/ERD/Enum 계약을 먼저 고정하고 병합 순서를 관리
