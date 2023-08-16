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

# 3.3 Todo 상세 조회 기능 만들기  

***

## 3.3.1 Todo 상세 조회 기능 컨셉  

> Todo를 선택했을 때, 조회할 수 있는 기능
> Todo를 선택하면 Todo의 제목과 설명을 나타냄  

## 3.3.2 Todo 상세 조회 템플릿 만들기  

**템플릿: todo/templates/todo/todo_detail.html**
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
            <h1>TODO 상세보기</h1>
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">{{ todo.title }}</h5>
                                <p class="card-text">{{ todo.description }}</p>
                                <a href="{% url 'todo_list' %}" class="btn btn-primary">목록으로</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
```

> Bootstrap을 사용해 스타일을 적용  
> Todo 제목과 설명을 보여줌  
> 목록으로 다시 돌아갈 수 있는 버튼까지 만듦  

## 3.3.3 Todo 상세 조회 뷰 만들기  

**뷰: todo/views.py**
```python
from django.shortcuts import render, redirect
from .models import Todo

# Create your views here.
def todo_list(request):
    todos = Todo.objects.filter(complete=False)
    return render(request, 'todo/todo_list.html', {'todos': todos})

def todo_detail(request, pk):
    todo = Todo.objects.get(id=pk)
    return render(request, 'todo/todo_detail.html', {'todo': todo})
```
> Todo의 pk인 id를 기반으로 Todo 객체를 찾아 todo_detail.html로 전달  

**todo/templates/todo/todo_list.html**
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
                    <a href="{% url 'todo_detail' pk=todo.pk %}">{{ todo.title }}</a>
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

> todo_list.html의 버튼에 링크를 넣음  

## 3.3.4 Todo 상세 조회 URL 연결하기  

**URL: todo/urls.py**
```python
from django.urls import path
from . import views
# Register your models here.

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('<int:pk>/', views.todo_detail, name='todo_detail'),
]
```
> url을 /pk/로 설정해 선택한 Todo를 연결할 수 있도록 설정  

***
***
***

# 3.4 Todo 생성 기능 만들기  

***

## 3.4.1 Todo 생성 기능 컨셉  

> Todo 생성은 제목, 설명, 중요도를 입력해야 하기 때문에 입력 폼이 필요함  
> todo/forms.py를 활용할 예정  

## 3.4.2 Todo 생성 템플릿 만들기  

**todo/forms.py**
```python
from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'description', 'important')
```

> 폼을 활용해 템플릿 작성  
> 위 폼을 form.as_p의 형태로 작성하면 태그 꼴로 템플릿에 폼이 생성  

**todo/templates/todo/todo_post.html**
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
            <h1>TODO 추가하기</h1>
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-body">
                               <form method="POST">
                                {% csrf_token %} {{ form.as_p }}
                                <button type="submit" class="btn btn-primary">등록</button>
                               </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
```

## 3.4.3 Todo 생성 뷰 만들기  

**뷰: todo/views.py**
```python
from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm

# Create your views here.
def todo_list(request):
    todos = Todo.objects.filter(complete=False)
    return render(request, 'todo/todo_list.html', {'todos': todos})

def todo_detail(request, pk):
    todo = Todo.objects.get(id=pk)
    return render(request, 'todo/todo_detail.html', {'todo': todo})

def todo_post(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todo/todo_post.html', {'form': form})    
```
> POST요청이 들어왔는지 확인하고 폼도 검증함  
> GET요청이거나 폼이 유효하지 않으면 폼 템플릿 페이지를 보여줌  

**todo/templates/todo/todo_list.html**
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
                <a href="{% url 'todo_post' %}"><i class="bi-plus"></i>Add Todo</a>
                <a href="" class="btn btn-primary" style="float:right">완료한 TODO 목록</a>
            </p>
            <ul class="list-group">
                {% for todo in todos %}
                <li class="list-group-item">
                    <a href="{% url 'todo_detail' pk=todo.pk %}">{{ todo.title }}</a>
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

> todo_list.html의 버튼에 링크 추가  

## 3.4.4 Todo 생성 URL 연결하기  

**URL: todo/urls.py**
```python
from django.urls import path
from . import views
# Register your models here.

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('<int:pk>/', views.todo_detail, name='todo_detail'),
    path('post/', views.todo_post, name='todo_post'),
]
```
> url을 post/로 지정해 url 연결  

***
***
***

# 3.5 Todo 수정 기능 만들기  

***

## 3.5.1 Todo 수정 기능 컨셉  
> 생성 기능과 거의 동일  
> 차이점은 폼에 이미 데이터가 입력되어 있다는 것  

## 3.5.2 Todo 수정 뷰 만들기  

**뷰: todo/views.py**
```python
def todo_edit(request, pk):
    todo = Todo.objects.get(id = pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/todo_post.html', {'form': form})
```
> 기존 Todo 데이터를 form에 전달하고 수정한 것 템플릿으로 전달  
> objects.get()을 통해 id로 구분하여 기존 값 받아옴  
> instance를 통해 폼에 객체를 전달  

**todo/templates/todo/todo_list.html**
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
                <a href="{% url 'todo_post' %}"><i class="bi-plus"></i>Add Todo</a>
                <a href="" class="btn btn-primary" style="float:right">완료한 TODO 목록</a>
            </p>
            <ul class="list-group">
                {% for todo in todos %}
                <li class="list-group-item">
                    <a href="{% url 'todo_detail' pk=todo.pk %}">{{ todo.title }}</a>
                    {% if todo.important %}
                        <span class="badge badge-danger">!</span>
                    {% endif %}
                    <div style="float:right">
                        <a href="" class="btn btn-danger">완료</a>
                        <a href="{% url 'todo_edit' pk=todo.pk %}" class="btn btn-outline-primary">수정하기</a>
                    </div>
                </li>
                {% endfor %}
            </ul>
        </div>
    </body>
</html>
```
> 수정 버튼에 링크 추가  

## 3.5.3 Todo 수정 URL 연결하기  

**todo/urls.py**
```python
from django.urls import path
from . import views
# Register your models here.

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('<int:pk>/', views.todo_detail, name='todo_detail'),
    path('post/', views.todo_post, name='todo_post'),
    path('<int:pk>/edit/', views.todo_edit, name='todo_edit'),
]
```
> /edit/형태로 url 연결  

***
***
***

# 3.6 Todo 완료 기능 만들기  

***

## 3.6.1 Todo 완료 기능 컨셉  

> 완료 버튼을 눌렀을 때, Todo의 complete를 True로 설정해 주는 기능  
> 완료 Todo 조회 기능은 완료된 Todo만 필터링해 보여주는 기능  

## 3.6.2 Todo 완료 템플릿 만들기  

**템플릿: todo/templates/todo/done_list.html**
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
            <h1>DONE 목록</h1>
            <p>
                <a href="{% url 'todo_list' %}" class="btn btn-primary">홈으로</a>
            </p>
            <ul class="list-group">
                {% for done in dones %}
                <li class="list-group-item">
                    <a href="{% url 'todo_detail' pk=done.pk %}">{{ done.title }}</a>
                    {% if done.important %}
                        <span class="badge badge-danger">!</span>
                    {% endif %}
                </li>
                {% endfor %}
            </ul>
        </div>
    </body>
</html>
```

**todo/templates/todo/todo_list.html**
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
                <a href="{% url 'todo_post' %}"><i class="bi-plus"></i>Add Todo</a>
                <a href="{% url 'done_list' %}" class="btn btn-primary" style="float:right">완료한 TODO 목록</a>
            </p>
            <ul class="list-group">
                {% for todo in todos %}
                <li class="list-group-item">
                    <a href="{% url 'todo_detail' pk=todo.pk %}">{{ todo.title }}</a>
                    {% if todo.important %}
                        <span class="badge badge-danger">!</span>
                    {% endif %}
                    <div style="float:right">
                        <a href="" class="btn btn-danger">완료</a>
                        <a href="{% url 'todo_edit' pk=todo.pk %}" class="btn btn-outline-primary">수정하기</a>
                    </div>
                </li>
                {% endfor %}
            </ul>
        </div>
    </body>
</html>
```

> todo_list.html의 버튼에 링크 추가  

## 3.6.3 Todo 완료 뷰 만들기  

> 완료된 목록을 보여주는 기능  
> Todo를 완료로 바꿔주는 기능  

**todo/views.py**
```python
from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm

# Create your views here.
def todo_list(request):
    todos = Todo.objects.filter(complete=False)
    return render(request, 'todo/todo_list.html', {'todos': todos})

def todo_detail(request, pk):
    todo = Todo.objects.get(id=pk)
    return render(request, 'todo/todo_detail.html', {'todo': todo})

def todo_post(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todo/todo_post.html', {'form': form})    

def todo_edit(request, pk):
    todo = Todo.objects.get(id = pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/todo_post.html', {'form': form})

def done_list(request):
    dones = Todo.objects.filter(complete=True)
    return render(request, 'todo/done_list.html', {'dones': dones})

def todo_done(request, pk):
    todo = Todo.objects.get(id=pk)
    todo.complete = True
    todo.save()
    return redirect('todo_list')
```

**todo/templates/todo/todo_list.html**
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
                <a href="{% url 'todo_post' %}"><i class="bi-plus"></i>Add Todo</a>
                <a href="{% url 'done_list' %}" class="btn btn-primary" style="float:right">완료한 TODO 목록</a>
            </p>
            <ul class="list-group">
                {% for todo in todos %}
                <li class="list-group-item">
                    <a href="{% url 'todo_detail' pk=todo.pk %}">{{ todo.title }}</a>
                    {% if todo.important %}
                        <span class="badge badge-danger">!</span>
                    {% endif %}
                    <div style="float:right">
                        <a href="{% url 'todo_done' pk=todo.pk %}" class="btn btn-danger">완료</a>
                        <a href="{% url 'todo_edit' pk=todo.pk %}" class="btn btn-outline-primary">수정하기</a>
                    </div>
                </li>
                {% endfor %}
            </ul>
        </div>
    </body>
</html>
```

## 3.6.4 Todo 완료 URL 연결하기  

**todo/urls.py**
```python
from django.urls import path
from . import views
# Register your models here.

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('<int:pk>/', views.todo_detail, name='todo_detail'),
    path('post/', views.todo_post, name='todo_post'),
    path('<int:pk>/edit/', views.todo_edit, name='todo_edit'),
    path('done/', views.done_list, name='done_list'),
    path('done/<int:pk>', views.todo_done, name='todo_done'),
]
```

***
***
***

**책에.. views.py 마지막 부분이 잘못나왔고.. 그냥 중간에 코드가 잘못나온게 좀 많다**  
**무작정 따라하기보다 잘 보면서 맞는지 확인하고 이해하며 보기**