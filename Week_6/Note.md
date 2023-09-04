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