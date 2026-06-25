# 요구사항 및 구현목표

## Status

- state: active
- owner: sjdok9612
- last-reviewed: 2026-05-11

---

## 기능 요구사항

### FR-01 방송 상태 모니터링
- **CHZZK**, **CIME(씨미)** 두 플랫폼을 지원한다
  - YouTube / SOOP 은 지원 범위에서 제외
- 스트리머별로 방송 ON/OFF 상태를 주기적으로 폴링한다
  - 방송 OFF 상태: 60초 간격
  - 방송 ON 상태: 300초 간격
- 상태가 변경될 때만 이벤트를 발생시킨다

#### CIME API 조사 결과 (2026-05-11)

**플랫폼 기본 정보**
- 운영사: 마플코퍼레이션 / 2026년 3월 베타 출시 (신생)
- 채널 페이지 URL: `https://ci.me/@{channelHandle}`
- 개발자 포털: https://developers.ci.me/

**인증 방식**
- Client 인증: `Client-Id` / `Client-Secret` 헤더 (서버 간 호출)
- 사용자 인증: `Authorization: Bearer {accessToken}` (OAuth 2.0)

**방송 상태 확인 — 핵심 엔드포인트**
```
GET /api/openapi/v1/{channelId}/live-status
인증: 불필요 (공개 API)
응답: 라이브 여부, 제목, 시작 시간
```
→ **인증 없이 호출 가능** — `is_live()` 구현에 바로 활용 가능

**채널 정보 조회**
```
GET /api/openapi/open/v1/channels?channelIds={id1,id2,...}
인증: Client-Id / Client-Secret
응답: channelId, channelName, channelHandle, followerCount 등
최대 20개 동시 조회
```

**미확인 사항**
- 베이스 URL (추정: `https://api.ci.me`, 실측 확인 필요)
- `{channelId}` 가 channelHandle(`@hebi`)과 동일한지, 별도 ID인지 미확인
- live-status 응답 JSON 정확한 필드명 미확인 (`isLive`? `status`? 등)

**TODO (구현 전 선행 필요)**
1. 실제 베이스 URL 확인 (개발자 포털 시작하기 문서)
2. channelId 형식 확인 (channelHandle로 대체 가능한지)
3. live-status 응답 JSON 샘플 수집

### FR-02 데스크탑 알림
- 방송 ON 전환 시 데스크탑 알림을 표시한다
- 방송 OFF 전환 시 데스크탑 알림을 표시한다
- 알림 형식: `{이름}{오시마크} 방송ON / 방송OFF`

### FR-03 홈 화면 — 아이콘 그리드
- 스트리머를 **3열 × N행 그리드**로 표시한다
- 각 셀에는 아이콘 이미지만 표시한다 (텍스트 최소화)
- 방송 ON: 컬러(원본) / 방송 OFF: 흑백(그레이스케일) 표시
- 방송 중인 스트리머가 그리드 상단에 정렬된다
- 아이콘 클릭 시 해당 스트리머의 상세 화면으로 이동한다

#### 이미지 스펙
- **원본 크기**: 144 × 144 px
- **표시 크기**: 36 × 36 px (1/4)
- **저장 경로**: `assets/streamers/{key}.png`
- **이미지 없을 때 폴백**: 오시마크 텍스트를 중앙에 표시
- **흑백 처리**: Qt `QImage` 또는 `QGraphicsColorizeEffect`로 런타임 변환
  (원본 파일은 컬러 하나만 보관)

### FR-07 상세 화면 — 링크 서브버튼
- 홈 화면에서 아이콘 클릭 시 진입하는 화면이다
- 표시 요소: 스트리머 이름, 오시마크, 방송 상태
- 버튼 구현 방식: **방식 A — 고정 레이블 매핑**
  - GUI 상수로 `{extra_fields 키: 레이블}` 매핑 테이블을 정의한다
  - 해당 키가 `extra_fields`에 존재하고 값이 있는 경우에만 버튼을 생성한다
  - 버튼 순서는 매핑 테이블의 정의 순서를 따른다
  - 새 링크 종류 추가 시 매핑 테이블 한 줄 추가로 대응한다
- `live_url`은 extra_fields가 아닌 Streamer 필드이므로 항상 첫 번째 버튼으로 고정
- 뒤로가기로 홈 화면 복귀

### FR-04 스트리머 인앱 편집
- 앱 내에서 스트리머를 추가할 수 있다
- 앱 내에서 스트리머를 삭제할 수 있다
- 앱 내에서 스트리머 정보를 수정할 수 있다 (이름, live_url, uid, 오시마크)
- 편집 결과는 streamers.json에 즉시 저장된다

### FR-05 시스템 트레이
- 창 닫기 버튼은 트레이로 최소화한다 (종료 아님)
- 트레이 메뉴: [창 열기] [종료]
- 트레이 아이콘 클릭으로 창을 복원한다

### FR-06 중복 실행 방지
- 동일 프로세스가 이미 실행 중이면 신규 실행을 차단한다

---

## 비기능 요구사항

### NFR-01 환경
- OS: Linux (Ubuntu 계열)
- Python 3.12 + PyQt6 6.11

### NFR-02 성능
- 폴링 루프는 메인 스레드를 블로킹하지 않는다 (QThread 사용)
- UI 업데이트는 반드시 메인 스레드(시그널/슬롯)에서 처리한다

### NFR-03 데이터
- 스트리머 데이터: `streamers.json`
- 설정 데이터: `config.json`
- 위 두 파일은 git 추적에서 제외한다

---

## 구현목표

| 단계 | 목표 | 비고 |
|------|------|------|
| M1 | PyQt6 메인 윈도우 + 트레이 골격 | 빈 창 + 트레이 동작 확인 |
| M2 | 홈 화면 — 3×N 아이콘 그리드 | 흑백/컬러, ON 상단 정렬 |
| M3 | 상세 화면 — 링크 서브버튼 | 뒤로가기 포함 |
| M4 | 스트리머 추가/편집/삭제 UI | 다이얼로그 방식 |
| M5 | liveCheck QThread 연동 + 데스크탑 알림 | 시그널/슬롯으로 UI 갱신 |
| M6 | 전체 흐름 통합 테스트 | streamers.json 기반 실제 동작 확인 |
