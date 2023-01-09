# 뭐먹냥(What-cat-eat)
고양이 사료 선호도 기록 서비스입니다. 고양이가 선호하는 사료들을 기록하고 알러지가 있다면 알러지 내용도 기록할 수 있습니다. 또한 커뮤니티 공간을 통해 집사들간 소통도 가능합니다.

## 목차
- [프로젝트 실행 방법](#프로젝트-실행-방법)
- [테스트 코드 동작 방법](#테스트-코드-동작-방법)
- [사용기술](#사용기술)

## 프로젝트 실행 방법
1. homebrew 설치
```
$ xcode-select --install
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
2. 파이썬 설치하기
(python 3.10.6버전)
```
$ brew install python3.10.6
$ python3 --version
```
3. 가상환경 설치 및 진입
```
$ python3 -m venv env
$ source env/bin/activate
```
4. 필요 라이브러리 설치
- fastapi
- uvicorn : ASGI web server
- SQLAlchemy : Python용 ORM
- alembic : 데이터베이스 마이그레이션 도구
- bcrypt : 패스워드 암호화
- flake8 : 코드 Lint용 도구
- black : 코드 Lint용 도구
- pytest : 테스트 코드 작성용
- httpx : 테스트 코드 작성용
```
$ pip install -r requrements.txt
```
5. DB 초기화 및 alembic 세팅
```
$ alembic init migrations
$ alembic revision --autogenerate
$ alembic upgrade head
```
6. 서버 실행하기(FastAPI)
```
$ uvicorn main:app --reload
```
## 테스트 코드 동작 방법
1. pytest 설치
```
$ pip install pytest
```
2. 실행
```
python -m pytest tests
```
## Docker 실행 방법
1. docker 이미지 만들기
```
docker build -t myimage .
```
2. 컨테이너 만들기
```
docker run -d --name mycontainer -p 80:80 myimage
```
## 사용 기술
1. FastAPI
2. Python3.10