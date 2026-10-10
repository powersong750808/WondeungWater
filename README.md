# 원등저수지 수위 모니터링

공식 API에서 실제 일별 관측자료를 가져와 GitHub Pages에서 보여주는 웹사이트입니다. 임의 관측값을 만들지 않습니다.

## 설정
1. GitHub에서 **공개 저장소**를 새로 만들고 이 폴더의 모든 파일을 업로드합니다 (`.github/workflows/update.yml` 포함).
2. 저장소 **Settings → Secrets and variables → Actions → New repository secret** 에서 이름 `DATA_GO_KR_KEY`로 **새로 재발급받은 Decoding 인증키**를 저장합니다. 절대 코드나 채팅에 키를 붙여 넣지 마세요.
3. **Actions → Update reservoir levels → Run workflow** 를 한 번 실행합니다. 성공하면 `data.json`이 생성됩니다.
4. **Settings → Pages → Build and deployment → Deploy from a branch → main / (root)** 선택 후 저장합니다.
5. 사이트 주소 `https://<계정>.github.io/<저장소>/`로 접속합니다. 매일 오전 10:10 KST에 자동 수집을 시도합니다(실제 실행시각은 GitHub 사정에 따라 지연 가능).

## 문제 해결
- `API 오류 04 HTTP 에러`: 공공데이터 API 원문 응답을 확인해야 합니다. 이전 웹페이지의 메시지로 인증키 오류를 확정할 수 없습니다.
- `HTTP 403`: API 접근권한/인증키 상태 확인
- `HTTP 404`: API 경로 및 제공기관 서비스 상태 확인
- `고흥 원등저수지 식별 실패`: 공식 API에서 검색 결과가 없거나 여러 건인 경우로, 결과를 확인해 검색어 또는 선택 기준 수정 필요
- `data.json` 없음: Actions 실행 실패 여부 확인
- 저수위 최신 관측일이 과거: 제공기관 일별 자료 갱신 또는 API 데이터 상태 확인

공식 가이드: `reservoircode` (저수지 코드), `reservoirlevel` (일별 수위, 저수율). **하루 1회 갱신**, 10분 실시간 자료 아님.
