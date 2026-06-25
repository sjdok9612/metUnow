# 실행 흐름

## Status

- state: active
- owner: sjdok9612
- last-reviewed: 2026-05-11

---

## 1. 앱 시작 흐름

```
main.py 실행
│
├─ check_mutex()
│   ├─ 이미 실행 중 → 메시지 출력 후 종료
│   └─ 정상 → 계속
│
├─ load_config()          → config.json
├─ load_streamer_dict()   → streamers.json (없으면 빈 dict)
│
├─ QApplication 생성
├─ AppWindow 생성
│   ├─ 스트리머 목록 위젯 초기화
│   └─ QSystemTrayIcon 생성
│
├─ LiveCheckWorker(QThread) 시작
│   └─ updateLive() 루프 진입
│
└─ app.exec() → 메인 루프 진입
```

---

## 2. 라이브 체크 루프 (QThread)

```
LiveCheckWorker.run()
│
└─ while True:
    └─ 스트리머 순회
        │
        ├─ 체크 주기 미도달 → SKIP (0.5초 sleep)
        │
        └─ 체크 주기 도달
            ├─ detect_platform(live_url)  → "chzzk" | "cime" | "unknown"
            ├─ {platform}_is_live(uid) API 호출
            │
            ├─ 상태 변경 없음 → 다음 스트리머
            │
            └─ 상태 변경 감지
                ├─ streamer.is_live 갱신
                ├─ status_changed 시그널 emit(name, is_live)
                └─ 1초 sleep (API 호출 간격)
```

---

## 3. UI 갱신 흐름 (시그널/슬롯)

```
[QThread] status_changed.emit(name, is_live)
        │
        │  ← Qt 시그널/슬롯 (스레드 경계 안전)
        ↓
[메인 스레드] AppWindow.on_status_changed(name, is_live)
        ├─ 해당 스트리머 행 위젯 색상 갱신
        └─ QSystemTrayIcon.showMessage(name, "방송ON/OFF")
```

---

## 4. 화면 전환 흐름

```
홈 화면 (3×N 아이콘 그리드)
│
│  셀 렌더링:
│    assets/streamers/{key}.png 존재 → 이미지 표시 (36×36px)
│    없음 → 오시마크 텍스트 폴백
│
│  방송ON → 컬러, 상단 정렬
│  방송OFF → 흑백(그레이스케일 변환), 하단 정렬
│
└─ 아이콘 클릭
        │
        └─ 상세 화면
            ├─ 이름 + 오시마크 + 방송 상태 표시
            ├─ [방송 바로가기]  → webbrowser.open(live_url)
            ├─ [팬카페]        → webbrowser.open(fan_cafe_url)
            ├─ [트위터/X]      → webbrowser.open(twitter_url)
            └─ [뒤로가기]      → 홈 화면 복귀
```

## 5. 스트리머 편집 흐름

```
메인 윈도우 [편집] 버튼 클릭
        │
        └─ StreamerEditorDialog 열기
            │
            ├─ [추가] → 빈 폼 입력 → streamer_dict에 추가
            ├─ [수정] → 선택 항목 폼 로드 → 값 변경
            └─ [삭제] → 선택 항목 제거
                │
                └─ 확인 클릭
                    ├─ save_streamers_to_json()   → streamers.json 저장
                    └─ AppWindow 목록 새로고침
```

---

## 5. 종료 흐름

```
트레이 메뉴 [종료] 클릭
        │
        ├─ LiveCheckWorker.stop() → 루프 탈출
        ├─ QSystemTrayIcon 숨김
        ├─ release_mutex()
        └─ QApplication.quit()
```
