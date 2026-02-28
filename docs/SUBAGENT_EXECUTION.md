# Subagent Execution (VSCode + PowerShell)

## 1) Worktree 상태 확인
```powershell
cd C:\CoordiPick
git -c safe.directory=C:/CoordiPick worktree list
```

## 2) VSCode 터미널 4개 열기
- Terminal A: 오케스트레이터 (`C:\CoordiPick`)
- Terminal B: admin agent (`C:\CoordiPick\backend-admin`)
- Terminal C: user agent (`C:\CoordiPick\backend-user`)
- Terminal D: frontend agent (`C:\CoordiPick\frontend`)

```powershell
# Terminal A
cd C:\CoordiPick

# Terminal B
cd C:\CoordiPick\backend-admin

# Terminal C
cd C:\CoordiPick\backend-user

# Terminal D
cd C:\CoordiPick\frontend
```

## 3) 각 세션 시작 시 첫 지시
각 터미널에서 다음 순서로 요청:
1. `Agent.md` 읽기
2. `docs/`, `api/`, `prompts/` 읽기
3. 자기 범위만 구현
4. 작업 전/후 변경 계획과 결과 요약 보고

예시:
```text
Agent.md와 docs/api/prompts를 읽고 네 범위만 작업해.
OpenAPI 계약을 절대 깨지 말고, 변경이 필요하면 먼저 제안해.
```

## 4) 오케스트레이터(메인 터미널) 체크 루프
```powershell
cd C:\CoordiPick
git -c safe.directory=C:/CoordiPick -C .\backend-admin status -sb
git -c safe.directory=C:/CoordiPick -C .\backend-user status -sb
git -c safe.directory=C:/CoordiPick -C .\frontend status -sb
```

## 5) 병합 순서 권장
1. `feat/backend-admin`
2. `feat/backend-user`
3. `feat/frontend`
