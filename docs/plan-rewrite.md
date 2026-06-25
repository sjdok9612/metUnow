# metUnow 리라이트 계획

## Status

- state: active
- owner: sjdok9612
- last-reviewed: 2026-05-11

---

## 목표

기존 Windows 전용 Tkinter 앱을 Linux 환경에 맞게 재구성.
기능은 최소화하고, 스트리머 관리를 앱 내에서 할 수 있도록 개선.

---

## 유지 / 제거 / 재구현 범위

### 유지 (기존 코드 재활용)
- `api/chzzk_api.py` — CHZZK 방송 상태 조회
- `api/liveCheck.py` — 상태 폴링 + 알림 트리거
- `tool/Streamers.py` — 스트리머 데이터 모델 + JSON 저장
- `tool/config.py` — 설정 로드
- `tool/mutex.py` — 중복 실행 방지

### 신규 작성
- `api/cime_api.py` — CIME 방송 상태 조회 (API 조사 후 구현)

### 제거
- `api/soop_api.py` — 지원 범위 제외
- `api/youtube_api.py` — 지원 범위 제외
- `tool/downloader.py` — 자동 다운로드 기능 전체 제거
- `gui/notif.py` — PyQt6 내장 알림으로 대체
- `gui/tray_icon.py` (pystray) — QSystemTrayIcon으로 대체

### 재구현 (PyQt6)
- `gui/app_window.py` — 메인 윈도우
- `gui/streamer_window.py` — 스트리머 행 위젯
- 신규: `gui/streamer_editor.py` — 스트리머 추가/편집/삭제 UI

---

## GUI 프레임워크

| 항목 | 기존 | 변경 |
|------|------|------|
| 기본 GUI | Tkinter | PyQt6 |
| 시스템 트레이 | pystray | QSystemTrayIcon (내장) |
| 데스크탑 알림 | notifypy | QSystemTrayIcon.showMessage() |
| 아이콘 이미지 | Pillow | Qt 내장 또는 QPixmap |

---

## 구현 순서

- [x] 1. 프로젝트 셋업 (requirements.txt, venv)
- [x] 2. `api/` + `tool/` 코드 이식 및 동작 확인
- [x] 3. PyQt6 메인 윈도우 + 트레이 아이콘 기본 골격
- [x] 4. 스트리머 목록 표시 (이미지/오시마크 5×N 그리드, 방송ON/OFF 컬러/흑백)
- [x] 5. 스트리머 추가/편집/삭제 UI (StreamerEditorDialog, LinkRow)
- [x] 6. liveCheck 연동 + 데스크탑 알림 (LiveCheckWorker QThread, tray.showMessage)
- [ ] 7. 전체 흐름 통합 테스트

---

## 결정 사항

- 방송 ON 클릭 시 브라우저로 채널 열기 → **유지**
- 링크 버튼 종류 → **나중에 결정** (일단 방송 링크만 구현 후 추가)

## 미결 사항

- 트레이 아이콘 이미지 (기존 파란 원 유지 or 새 디자인)
