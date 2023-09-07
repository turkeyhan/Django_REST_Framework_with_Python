# Chapter 6. 실전 프로젝트! Django REST Framework + React.js 게시판 만들기  

***
***
***

## 6.1 Hello, 게시판 프로젝트  

***

### 6.1.1 프로젝트 소개: 게시판  

> **회원 관련 기능**  
* 회원 프로필 관리(닉네임, 관심사, 프로필 사진 등)  
* 회원가입 기능  
* 로그인 기능  
* 프로필 수정하기 기능  

> **게시글 관련 기능**  
* 게시글 생성  
* 게시글 1개 가져오기 / 게시글 목록 가져오기(가져오는 개수 제한하기)  
* 게시글 수정하기  
* 게시글 삭제하기  
* 게시글 좋아요 기능  
* 게시글 필터링(좋아요 누른 글 / 내가 작성한 글)  
* 게시글 각 기능마다 권한 설정  

> **댓글 관련 기능**  
* 댓글 생성  
* 댓글 1개 가져오기 / 댓글 목록 가져오기  
* 댓글 수정하기  
* 댓글 삭제하기  
* 게시글을 가져올 때 댓글도 가져오게 만들기  

### 6.1.2 프로젝트 세팅하기  

> **프로젝트 생성**  
```bash
python3 -m venv myvenv
```
```bash
myvenv/Scripts/activate
```
```bash
pip install django==3.1.6 djangorestframework==3.12.2
```
```bash
django-admin startproject myboard .
```

> **myboard/settings.py**  
```python
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]
...
TIME_ZONE = 'Asia/Seoul'
...
```

***
***

## 6.2 앱: 회원  

***

### 6.2.1 Django 기본 User 모델  

> Django는 User라는 기본 모델을 이미 만들어놓음  
```bash
python manage.py createsuperuser
```
> 위 명령어 또한 User 모델을 사용한 관리자임  
> settings.py에 등록되어 있는 django.contrib.auth에 models 안에 있음  
> User 모델에 접근하기 위해서는
```python
from django.contrib.auto.models import User
```
> 위와 같이 불러오면 됨  

> **User 모델의 대표적인 필드**  
* Username: ID가 들어가는 필드, 필수적, 문자열  
* first_name: 영문 이름에서 사용되는 이름 개념, 선택적, 문자열  
* last_name: 영문 이름에서 사용되는 성 개념, 선택적, 문자열  
* emaii: 이메일 주소, 선택적, 문자열  
* password: 비밀번호이며 해시값으로 저장함, 필수적, 문자열  

### 6.2.2 회원 인증 개념 이해하기  
> 인증: 서버에게 본인이 유저인지 확인받는 과정  
> **인증방식**
1. ID와 PW를 그대로 담아 보내기  
> 취약한 방법, Django의 해시 알고리즘을 모르기 때문에 비밀번호를 그대로 전달  
> Client가 전송할 때, 중간에 가로채면 그대로 비밀번호를 보여주게 됨  
2. 세션 & 쿠키  
> 세션: 서버 쪽에서 저장하는 정보  
> 쿠키: 클라이언트의 자체적인 임시 저장소  
> 로그인 후 발급되는 세션 ID를 보냄으로 인증을 대체  
> 하지만 이것 또한 세션 ID가 노출될 수 있음  
3. 토큰 & JWT  
> 세션 & 쿠키 방식과 비슷  
> 세션 & 쿠키와 다른 점은 토큰 자체에 사용자에 대한 정보가 있음  
> 토큰은 암호화 방식을 채택하여 사용  
> settings.py의 SECRET_KEY가 노출되지 않는다면 유출 가능성이 없음  

>   > 2번, 3번 방식의 해결책 중에는 토큰/세션에 대한 유효기간 설정이 있음  
>   > 하지만 이 책에서는 다루지 않음  

### 6.2.3 회원가입 구현하기  

> **회원가입, 로그인 등의 기능 모을 앱 생성**
```bash
python manage.py startapp users
```

> **myboard/settings.py**
```python
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'users',
]
...
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
...
```
> 앱 등록 및 기본 토큰 인증 방식 앱 등록  
> 프로젝트의 인증 방식으로 토큰 방식을 사용한다는 것 정의  

***
***
***

# 아래부터는 양이 많아 코드 및 간단한 설명만 첨부  

***
***
***

> **시리얼라이저: users/serializers.py**
```python
# User 모델
from django.contrib.auth.models import User
# Django의 기본 패스워드 검증 도구
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
# Token 모델
from rest_framework.authtoken.models import Token
# 이메일 중복 방지를 위한 검증 도구
from rest_framework.validators import UniqueValidator

# 회원가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        # 이메일 중복 검증
        validators = [UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only = True,
        required = True,
        # 비밀번호 검증
        validators = [validate_password],
    )
    # 비밀번호 확인 필드
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    # 추가적으로 비밀번호 일치 여부 확인
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data
    
    def create(self, validated_data):
        # CREATE 요청에 대해 create 메소드를 오버라이딩
        # 유저를 생성하고 토큰을 생성하게 함
        user = User.objects.create_user(
            username = validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user
```

> **뷰: users/views.py**
```python
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import RegisterSerializer

# CreateAPIView(generics) 사용 구현
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
```

> **URL: users/urls.py**
```python
from django.urls import path
from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view()),
]
```
> **URL: myboard/urls.py**
```python
from django.contrib import admin, include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]
```

> **마이그레이션 & 프로젝트 실행하기**
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
```bash
python manage.py runserver
```

> **Insomnia에서 JSON POST후 각각에 대한 결과확인**
```json
{
	"username": "testuser1",
	"password": "password",
	"password2": "password",
	"email": "test1@test.com"
}
```

```json
{
	"username": "testuser1",
	"password": "dkssud!!",
	"password2": "password",
	"email": "test1@test.com"
}
```

```json
{
	"username": "testuser1",
	"password": "dkssud!!",
	"password2": "dkssud!!",
	"email": "test1@test.com"
}
```

```json
{
	"username": "testuser2",
	"password": "dkssud!!",
	"password2": "dkssud!!",
	"email": "test1@test.com"
}
```

```json
{
	"username": "testuser2",
	"password": "dkssud!!",
	"password2": "dkssud!!",
	"email": "test2@test.com"
}
```

> **회원 토큰 생성 확인하기 위해 관리자 계정 생성**
```bash
python manage.py createsuperuser
```

> admin 페이지로 가서 확인해보면 token생성을 확인할 수 있음  

### 6.2.4 로그인 구현하기  

> **시리얼라이저: users/serializers.py**
```python

```