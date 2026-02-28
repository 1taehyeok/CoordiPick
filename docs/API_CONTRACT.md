# API Contract Rules (Shared)

## Base
- Base URL: `/api/v1`
- Content-Type: `application/json`
- Auth:
  - user API: optional anonymous session token
  - admin API: bearer JWT required

## Response Envelope
- Success:
```json
{
  "success": true,
  "data": {},
  "meta": {}
}
```
- Error:
```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "validation failed",
    "details": {}
  }
}
```

## Enum Dictionary (MVP)
- `gender`: `male | female | unisex`
- `tpo`: `commute | date | friends | travel | daily | special`
- `slot`: `top | bottom | outer | shoes | acc`
- `event_type`: `impression | click | detail_view`
- `generation_source`: `rule | ai | admin`

## Status Code Rules
- `200` 조회/성공
- `201` 생성
- `400` 입력 오류
- `401` 인증 필요
- `403` 권한 없음
- `404` 없음
- `409` 충돌
- `422` 비즈니스 규칙 위반
- `500` 서버 오류
