from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 디렉토리 루트에다가 myapi.db 파일을 만들고 해당 주소로 데이터베이스를 접속한다.
SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

# create_engine : 커넥션 풀(데이터베이스에 접속하는 세션수를 제어하고 세션 접속에 소요되는 시간을 줄이고자 한 용도)을 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# 데이터베이스에 접속하기 위한 클래스
# Tip) autocommit을 True로 주면 commit 명령어 없이 DB저장이 가능하지만 롤백불가능
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 여기서 declarative_base()을 받아간 Base는 데이터베이스 모델을 구성할 때 사용되는 클래스
Base = declarative_base()


# 정리
# 1. 어디 데이터베이스에 접근할건지 루트를 알려준다.
# 2. create_engine을 이용하여 커넥션 풀을 생성한다.
# 3. 세션을 열어서 데이터베이스에 접속한다.
# 4. declarative_base를 이용하여 데이터베이스 모델을 구성할 수 있도록 만들어준다.