***
***
***
# 3.1 Todo 목록 웹 서비스 시작하기   

***

## 3.1.1 프로젝트 기능 정리하기  
> CRUD: Create, Read, Update, Delete의 약자이며 Todo 목록 서비스에 포함됨  
  
## 3.1.2 프로젝트 생성하기  
**가상환경 종료하기**
```bash
$ deactivate
```  

**가상환경 세팅**
```bash
$ python3 -m venv myvenv
$ myvenv/Scripts/activate
```

**장고 설치**
```bash
$ pip install django~=3.2.10
```

**장고 프로젝트 생성**
```bash
$ django-admin startproject mytodo .
```

**todo 앱 생성**
```bash
$ python manage.py startapp todo
```

## 3.1.3 Todo 프로젝트 설정하기  

**Todo_list/mytodo/settings.py**
```python
...
ALLOWED_HOSTS = ['127.0.0.1']
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todo',
]
TIME_ZONE = 'Asia/Seoul'
...
```

**관리자 계정 생성**
```bash
$ python manage.py createsuperuser
```

## 3.1.4 Todo 모델 생성하기  

* title: Todo의 제목  
* description: Todo에 대한 설명  
* created: Todo의 생성 일자  
* complete: Todo의 완료 여부  
* important: Todo의 중요 여부  

**Todo_list/todo/models.py**
```python
from django.db import models

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    important = models.BooleanField(default=False)

    def __str__(self):
        return self.title
```
> auto_now_add속성을 통해 생성일이 자동으로 추가되도록 설정  
> 이후 id인 pk를 통해 Todo 데이터를 구분할 예정  

**모델 마이그레이션**
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

**Todo_list/todo/admin.py**
```python
from django.contrib import admin
from .models import Todo
# Register your models here.

admin.site.register(Todo)
```
> 관리자 페이지에서 확인할 수 있게 Todo 모델 등록  

**Todo_list/mytodo/urls.py**
```python
from django.contrib import admin
from django.urls import path, include
# Register your models here.

urlpatterns = [
    path('admin/', admin.site.urls)
]
```
> 관리자 페이지에 접속하기 위한 url추가  

***
***
***

# 3.2 Todo 전체 조회 기능 만들기  

***

## 3.2.1 Todo 전체 조회 기능 컨셉  

> 첫 페이지 화면은 완료되지 않은 Todo만 보여주는 전체 조회 기능  

## 3.2.2 Bootstrap으로 좀 더 멋진 템플릿 만들기  

> Bootstrap: CSS Framework, 미리 스타일이 정의되어 있음, 사용법이 간단하고 정갈한 결과물이 만들어짐  

## 3.2.3 Todo 전체 조회 템플릿 만들기  

**템플릿: Todo_list/todo/templates/todo/todo_list.html**
```html
<html>
    <head>
        <title>TODO 목록 앱</title>
        <link
        rel = "stylesheet"
        href = "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
        />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.1/font/boot-strap-icons.css">
    </head>
    <body>
        <div class="container">
            <h1>TODO 목록 앱</h1>
            <p>
                <a href=""><i class="bi-plus"></i>Add Todo</a>
                <a href="" class="btn btn-primary" style="float:right">완료한 TODO 목록</a>
            </p>
            <ul class="list-group">
                {% for todo in todos %}
                <li class="list-group-item">
                    <a href="">{{ todo.title }}</a>
                    {% if todo.important %}
                        <span class="badge badge-danger">!</span>
                    {% endif %}
                    <div style="float:right">
                        <a href="" class="btn btn-danger">완료</a>
                        <a href="" class="btn btn-outline-primary">수정하기</a>
                    </div>
                </li>
                {% endfor %}
            </ul>
        </div>
    </body>
</html>
```
> head안에 link태그가 있고 여기서 Bootstrap을 불러옴  
>   > Bootstrap 홈페이지에서 css 파일들을 받아와 프로젝트 폴더에 집어넣는 방식도 있음  
>   > 하지만 간단하게 하려면 웹 링크 방식으로 연결시키는 것이 좋음  

> 각 태그마다 class를 작성  
>   > class 이름은 Bootstrap이 미리 정의해놓은 값  
>   > Bootstrap의 공식 문서에서 확인할 수 있음  

> todos를 넘겨받아 반복문으로 각 todo의 제목, 중요도, 완료, 수정 기능 표현  
> 위에는 Todo 추가 링크와 완료 Todo 목록 링크 있음  

## 3.2.4 Todo 전체 조회 뷰 만들기  

**뷰: Todo_list/todo/views.py**
```python
from django.shortcuts import render, redirect
from .models import Todo

# Create your views here.
def todo_list(request):
    todos = Todo.objects.filter(complete=False)
    return render(request, 'todo/todo_list.html', {'todos': todos})
```
> complete=False 옵션으로 완료되지 않은 Todo만 전달  
> 필터링은 Todo.objects.filter로 처리  

## 3.2.5 Todo 전체 조회 URL 연결하기  

**URL 연결: Todo_list/todo/urls.py**
```python
from django.urls import path
from . import views
# Register your models here.

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
]
```
> 주소에 todo_list 뷰를 연결  

**mytodo/urls.py와 todo/urls.py 연결**
**mytodo/urls.py**
```python
from django.contrib import admin
from django.urls import path, include
# Register your models here.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', include('todo.urls')),
]
```

***
***
***

