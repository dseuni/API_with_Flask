# mysql은 사용할 수 있으니 pass (*참고: 책에서는 sqlalchemy사용)
# - 인증
# - 사용자 비밀번호 암호화 : 단방향 해시함수 (보안강화) -> salting|key stretching
# - Access Token: JWT(JSON Web Tokens)

# 단방향 해시함수
import hashlib
m = hashlib.sha256()
m.update(b"test_password")
print(m.hexdigest())


# key stretching & salting : pip install bcrypt
import bcrypt
password = bcrypt.hashpw(b"test_password", bcrypt.gensalt())
print(password)
print(bcrypt.hashpw(b"test_password", bcrypt.gensalt()).hex())
print(bcrypt.checkpw('test_password'.encode('UTF-8'), password))


# JWT: 단순 데이터 전송 기능 이외의 검증 기능이 있음
# header, payload, signature로 구성됨, signature만 복호화가능한 암호, 나머지는 인코딩
# pip install PyJWT
import jwt
data_to_encode = {'some': 'payload'}  # payload부분
encryption_secret = 'secrete'  # signature 암호화용
algorithm = 'HS256'
encoded = jwt.encode(data_to_encode, encryption_secret, algorithm=algorithm)
print(encoded)
print(jwt.decode(encoded, encryption_secret, algorithms=[algorithm]))


# decorator 함수: 어떠한 함수를 다른 함수가 실행되기 전에 자동으로 먼저 실행될 수 있도록 해주는 문법
# ex) @app.route()
from functools import wraps

def test_decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Decorated Function")
        return f(*args, **kwargs)

    return decorated_function

@test_decorator
def func():
    print("Calling func function")

func()


# pip install flask-cors
# : API URL 도메인 주소와 Front-end URL 도메인 주소가 달라서 생기는 CORS문제 해결