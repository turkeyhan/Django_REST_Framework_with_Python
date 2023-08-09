# Chapter 2. Django 기본 컨셉 익히기   
      
***  
***  
***  

## 2.1 Django 시작하기  

### 2.1.1 Django란  
> Django: 파이썬 기반의 웹 풀스택 프레임워크  
>   > 자유도가 낮음 -> 건드릴 수 있는 부분이 적음 -> 몇 개 건드리지 않아도 웹 어플리케이션 완성 가능  
> 개발 패턴: 만들어야 하는 개발 요소들에 대한 규격화된 양식  
>   > Django의 경우 MTV 패턴이라는 것이 존재  

### 2.1.2 개발 환경 세팅  
> VS Code 설치, terminal에서 python3 입력  

### 2.1.3 프로젝트 시작하기  
> 가상환경: 가상의 환경을 만들어 설정하고 그 위에서 프로젝트를 진행  
>   > 가상환경을 쓰는 이유? -> 프로젝트마다 필요한 패키지 버전이 다르기 때문 -> 의존성 관리  

**terminal(윈도우 기준)**  
* Python 버전 확인  
```bash
$ python3 --version
```
* 가상 환경 myvenv 생성  
```bash
$ python3 -m venv myvenv
```
* myvenv를 실행(활성화)  
```bash
$ myvenv\Scripts\activate
```
*보안 오류 뜰 시, Powershell을 관리자 권한으로 실행 후 `Set-ExecutionPolicy RemoteSigned` 입력하고 Y 입력*
* Django 설치  
```bash
$ pip install django~=3.2.10
```
* 현재 위치에 myweb이라는 Django 프로젝트 만들기  
```bash
$ django-admin startproject myweb .
```
* photo라는 앱 추가  
```bash
$ python manage.py startapp photo
```
* 프로젝트 실행  
```bash
$ python manage.py runserver
```

***

## 2.2 Django 프로젝트 구조 살펴보기  

### 2.2.1 Django 프로젝트와 앱  
> * 프로젝트: 어떤 하나의 큰 서비스  
> * 앱: 프로젝트 내 기능과 같은 요소들을 일정한 기준으로 나눠 놓은 단위  
>   > 앱을 설계하는 것이 중요  

### 2.2.2 Django 프로젝트 설정 마무리하기  
* 앱 추가 및 시간대 한국으로 설정
**myweb/settings.py 열기**  
**photo앱 추가 및 시간대를 한국으로 설정**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'photo',
]
TIME_ZONE = 'Asia/Seoul'
```

### 2.2.3 Django 프로젝트 구성요소 살펴보기  
* manage.py: Django 프로젝트 내 Django와 관련된 여러 명령어를 써야할 때, 사용하는 파일  
> django.core.management 모듈로부터 execute_from_command_line 함수를 가져와 명령어 처리  
**Example**
```bash
$ python manage.py runserver
$ python manage.py migrate
```
* settings.py: 프로젝트의 설정 파일  
    * 디버깅 모드에 대한 옵션: True면 디버깅 모드가 됨 -> Error가 웹 페이지에 그대로 노출 / 배포시에는 끄고 배포
    ```python
    DEBUG = True
    ```
    * 허용할 호스트 주소에 대한 내용: Django 프로젝트가 돌아가는 환경에 접속할 수 있는 주소
    **default: 127.0.0.1**
    ```python
    ALLOWED_HOSTS = []
    ```
    * 설치된 앱들을 등록하는 옵션: Django 프로젝트에서 만든 앱들을 여기에 선언해야 등록이 됨  
    ```python
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'photo',
    ]
    ```
* urls.py: 프로젝트의 url 주소를 등록해놓는 파일  
**path()를 통해 원하는 주소 등록**
```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

### 2.2.4 Django 앱 구조로 알아보는 MTV 패턴  
* MTV 패턴: 직관적이고 간단한 구조, Model, Template, View의 약자  
    * Model: 앱의 데이터와 관련된 부분  
    * Template: 사용자에게 보이는 부분  
    * View: Model의 데이터를 Template로 전달, Template에서 발생하는 이벤트 처리  

***

## 2.3 Django Model 알아보기  

### 2.3.1 Migration 에러 수정하기  
```bash
$ python manage.py migrate
```
  
### 2.3.2 어드민 페이지 들어가보기  
* **아래 명령어 입력 후 http://127.0.0.1:8000/admin 들어가기**
```bash
$ python manage.py runserver
```
* **관리자 계정 새로 만들기**
```bash
$ python manage.py createsuperuser
```
**그리고 admin 페이지 들어가서 로그인 하면 관리자 페이지가 나옴**

### 2.3.3 모델이란  
> 모델: 앱의 데이터와 관련된 부분, 개체를 모델링한 결과물  
>   > Example) 사람, 사용자  
> 모델링: 현실에 있는 개체의 특징들을 뽑아 이를 구성 요소로 하는 것  
>   > 구성 요소, 속성의 Example) 이름, 나이  
> 마이그레이션(Migration): **모델을 데이터베이스에 적용시키는 과정**(테이블을 만드는 과정)  

### 2.3.4 Django 모델 만들기  

**photo/models.py**
```python
from django.db import models

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    image = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
```
> models.Model을 상속받음  
> 각 속성들을 models를 사용해 정의  

**쓸만한 필드 종류**
1. CharField: 문자열(길이제한 필요)  
2. IntegerField: 정수  
3. TextField: 문자열(길이제한 필요 없음)  
4. DateField: 날짜  
5. DateTimeField: 날짜 + 시간  
6. FileField: 파일  
7. ImageField: 이미지 파일  
8. ForeignKey: 외래 키(관계)  
9. OneToOneField: 1대1 관계  
10. ManyToManyField: 다대다 관계  
  
### 2.3.5 Django 모델 적용시키기  
  
* 마이그레이션(Migration): 모델을 데이터베이스에 적용시키는 과정  
    * makemigrations: 모델 변경 내용을 기록해 파일로 만들어주는 과정, photo/migrations 폴더 내에 생기는 파일들이 결과물임  
    * migrate: makemigrations에서 생성된 파일을 실제로 실행시켜 실제 데이터베이스에 반영  
**makemigrations - 모델 변경 내용을 파일(photo/migrations/0001_initial.py)로 생성**
```bash
$ python manage.py makemigrations
```
  
**migrate - 생성된 0001_initial.py 파일의 내용 DB에 적용**
```bash
$ python manage.py migrate
```  
  
### 2.3.6 Django 모델 어드민 페이지 적용  

**photo/admin.py**
```python
from django.contrib import admin
from .models import Photo

# Register your models here.
admin.site.register(Photo)
```
> Photo 클래스를 import를 통해 불러오고 Photo 모델을 등록  
  
***

## 2.4 Django Template 알아보기  
  
### 2.4.1 Django Template이란  
  
> 템플릿(Template): 사용자에게 보이는 부분(프론트)  

### 2.4.2 Django Template의 특징  

> HTML 작성과 99% 비슷  
> 아주 작은 차이: 템플릿 태그(Template Tag)  
>   > 템플릿 태그(Template Tag): HTML이 파이썬 코드(Django Project)로부터 데이터를 바로 넘겨받아 손쉽게 처리할 수 있는 도구  
>   >   > {}으로 감싸는 형태
>   >   > 데이터를 넣을 수 있고 for, if와 같은 구문도 사용가능  

