# CLAUDE.md — metUnow

## 프로젝트 정보
- **type**: development
- **purpose**: YouTube Live·SOOP·CHZZK 스트리머 방송 상태 실시간 모니터링 데스크탑 앱

## 문서·규칙
- 프로젝트 지침: `docs/` 폴더 참조
- Claude는 작업 전 `docs/` 내 관련 파일을 먼저 읽는다

## 대용량 파일
- git 비관리 산출물·재료 파일은 `~/storage/metUnow/` 에 보관
- 프로젝트 내에는 두지 않는다 (safetensors, 대용량 원본 등)

---

## Karpathy 원칙

- `raw_sources/` 는 원문 보관 전용 — Claude는 읽기만, 수정 금지
- 영어 원문 먼저 인용(블록쿼트), 번역·해석은 그 다음
- 주장은 반드시 출처 파일 명시

---

## llm-wiki 피드 규칙

**파일 경로**: `/home/mollyhyang/projects/llm-wiki/raw_sources/sessions/metUnow/YYYY-MM-DD-[slug].md`

**피드 형식**:
```yaml
---
feed_type: session_summary | requirement | memo
project: metUnow
date: YYYY-MM-DD
decision: true | false
tags: []
---
[핵심 내용]
```

### decision: true 조건

**공통**:
- 설계 결정이 확정됐을 때
- 새 개념·패턴을 처음 다뤘을 때
- 사용자가 "기억해" / "기록해"라고 명시했을 때

**type별 추가 조건**:
- development: API·아키텍처 결정, 재사용 가능한 패턴 발견

---

## 재빌드 규칙

소스 변경 후 배포가 필요한 경우 반드시 `build.sh`를 실행한다:
```bash
cd /home/mollyhyang/projects/metUnow && ./build.sh
```

`build.sh`는 다음을 순서대로 수행한다:
1. 실행 중인 AppImage 인스턴스 종료
2. PyInstaller 재빌드
3. AppDir 갱신 및 AppImage 패키징
4. 자동시작(`~/.config/autostart/`) 및 앱 런처(`~/.local/share/applications/`) 재등록

---

## Lint 트리거 조건

**임계값**: 90일
**실행 조건**: 명시적 요청 시 (`lint 해줘`)
