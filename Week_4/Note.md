# Chapter 4. Django REST Framework 컨셉 익히기  

***
***
***

## 4.1 Django REST Framework 시작하기  

***

### 4.1.1 Django REST Framework?  

> Django를 기반으로 REST API 서버를 만들기 위한 라이브러리  

### 4.1.2 Django REST Framework 예제 프로젝트 생성  

> **가상환경 만들기**
```bash
$ python3 -m venv myvenv
$ myvenv/Scripts/activate
```

> **myweb 프로젝트 만들기**
```bash
$ pip install django==3.2.10
$ django-admin startproject myweb .
```

### 4.1.3 Django REST Framework 설치 및 실행  

> **Django REST Framework 설치**
```bash
$ pip install djangorestframework==3.13.1
```

> **myweb/settings.py**  
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

> **example이라는 이름의 앱 만들기**
```bash
$ python manage.py startapp example
```

> **myweb/settings.py**  
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
    'example',
]
...
```

> **마이그레이션**
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

***
***

## 4.2 Django REST Framework 프로젝트 구조 살펴보기  

***

### 4.2.1 helloAPI 만들어보기  
> **example/views.py**
```python
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

@api_view(['GET'])
def HelloAPI(request):
    return Response("hello world!")
```
> 데코레이터: @표시와 함께 작성되어 있는 코드  
>   > 함수를 꾸미는 역할을 함  
>   > 해당 함수에 대한 성격(스타일)을 표시  
>   > 위 코드에는 HelloAPI함수가 GET요청을 받을 수 있는 API인 것을 표기  

***

**VS CODE 사용중 노란 밑줄 생기는 부분**
> Ctrl + Shift + P를 눌러 인터프리터를 변경하면 됨  
> 현재 위치하고 있는 가상환경의 파이썬을 인터프리터로 선택  

***

> request 객체는 사용자가 요청을 보낼 때, 무슨 데이터를 함께 보냈는지를 담고 있음  
> request.method는 요청이 어떤 타입인지(GET, POST ...)  
> request.data는 데이터를 얻기 위한 접근  
> 결과를 반환할 때는 Response 클래스를 사용  
> request와 마찬가지로 Response 또한 응답에 대한 정보를 담고 있음  
> response.data는 응답 데이터, response.status는 응답의 상태를 담음  

**상태코드**  
* HTTP_200_OK: GET 요청이 정상적으로 이뤄졌을 때, 응답에 나타나는 상태값  
    * GET 요청: 데이터를 요청하는 것  
* HTTP_201_CREATED: POST 요청이 정상적으로 이뤄졌을 때, 응답에 나타나는 상태값  
    * POST 요청: 데이터를 생성하는 것  
* HTTP_206_PARTIAL_CONTENT: PATCH 요청이 정상적으로 이뤄졌을 때, 응답에 나타내는 상태값  
    * PATCH 요청: 데이터를 일부 수정하는 것  
* HTTP_400_BAD_REQUEST: 클라이언트가 잘못된 요청을 보냈을 때, 응답에 나타내는 상태값  
* HTTP_401_UNAUTHORIZED: 인증이 필요한데 인증 관련 내용이 요청에 없을 때, 응답에 나타내는 상태값  
* HTTP_403_FORBIDDEN: 클라이언트가 접근하지 못하도록 막아놓은 곳에 요청이 왔을 때, 응답에 나타내는 상태값  
* HTTP_404_NOT_FOUND: 클라이언트가 요청을 보낸 곳이 잘못된 URL일 때(리소스가 없을 때), 응답에 나타내는 상태값  
* HTTP_500_INTERNAL_SERVER_ERROR: 서버 쪽에서 코드가 잘못되었을 때, 응답에 나타내는 상태값  

**URL: myweb/urls.py**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("example/", include("example.urls"))
]
```

**URL: example/urls.py**
```python
from django.urls import path, include
from .views import HelloAPI

urlpatterns = [
    path("hello/", HelloAPI)
]
```

### 4.2.2 Django에서 달라진 점  
> 위에서 만든 코드를 활용해 띄운 페이지 상의 데이터들은 HTTP의 헤더임  
* Pure Django
> 웹 풀스택 개발  
> 웹 페이지를 포함한 웹 서비스  
> HTML  
> templates  

* Django REST Framework  
> 백엔드 API 서버 개발  
> 여러 클라이언트에서 사용할 수 있는 API 서버  
> JSON  
> serializers.py  

**Pure Django와 Django REST Framework의 차이점을 개발 목적, 개발 결과, 응답 형태, 다른 파일의 순으로 나열했다.**  

***
***

