# Webex Attendance Checker

셀레니움을 사용한 파이썬 기반의 웹 크롤링 자동 출석체크 프로그램

⚠️현재는 웹엑스 내의 reCAPTCHA로 인하여 정상적으로 동작하지 않습니다.

# ❓How It Works

현재 web으로 접속할 수 있는 webex 특성을 따라서, 다음과 같은 과정으로 진행됩니다.

1. 셀레니움을 통해 링크 접속 
2. 손님으로 웹 로그인 시도
3. 크롤링을 통한 사용자 목록 조회
4. 사용자 현황 조회

### 정보 입력

- 필요한 파일 목록

  ```
  1. secrets.json    --- 사용자 계정 정보
  2. members.csv     --- 이슈 스크래핑 대상자 명단
  ```

- **secrets.json**

  ```json
  {
    "nickname": "AAA_출석봇",
    "email": "AAA_bot@abc.com",
    "url" : "웹엑스_접속_URL주소"
  }
  ```

- **members.csv**

  ```text
  홍길동,(상태이상)
  가이정,
  도우니,병가
  설이현,
    :
    :
    :
  유시현,조퇴
  ```


## installation
> Windows의 경우 run.bat 파일을 실행하면 됩니다.
```bash
cd <current_directory>
python3 -m venv .venv
pip3 install -r requirements.txt
python3 ./main.py
```