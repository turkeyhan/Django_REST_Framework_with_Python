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

***  

## 2.5 Django View, URL 알아보기  
  
### 2.5.1 Django View란  
  
> 뷰(View): 템플릿과 모델 사이를 이어주는 다리  
>   > * 함수형 뷰  
>   > * 클래스형 뷰  
  
### 2.5.2 Django URL이란  

> URL(Uniform Resource Locator): 라우팅의 역할과 동시에 서버로 해당 주소에 할당된 리소스를 요청  

***

## 2.6 서비스 기능 하나씩 구현하기  
  
### 2.6.1 사진 목록 화면 만들기  
  
**템플릿: photo/templates/photo/photo_list.html**  
```html
<html>
    <head>
        <title>Photo App</title>
    </head>
    <body>
        <h1><a href="">사진 목록 페이지</a></h1>
        <section>
            <div>
                <h2>
                    <a href="">화난 준우</a>
                </h2>
                <img
                    src="https://w7.pngwing.com/pngs/92/998/png-transparent-anger-scalable-graphics-angry-face-pics-love-smiley-anger.png"
                    alt="화난준우"
                    width="300"
                />
                <p>화난 준우, 1000원</p>
            </div>
            
            <div>
                <h2>
                    <a href="">화난 준우 2</a>
                </h2>
                <img
                    src="https://png.pngtree.com/png-vector/20190114/ourlarge/pngtree-vector-angry-emoticon-icon-png-image_313017.jpg"
                    alt="화난준우"
                    width="300" 
                />
                <p>화난 준우, 1000원</p>
            </div>
        </section>
    </body>
</html>
```

**뷰: photo/views.py**
```python
from django.shortcuts import render

# Create your views here.
def photo_list(request):
    return render(request, 'templates/photo/photo_list.html', {})
```
> templates를 경로에 포함시키면 오류가 발생함
> templates는 default로 포함된다고 생각  
> 따라서 아래와 같이 수정  
**photo/views.py**
```python
from django.shortcuts import render

# Create your views here.
def photo_list(request):
    return render(request, 'photo/photo_list.html', {})
```


**URL**
* photo/urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.photo_list, name='photo_list'),
]
```
* myweb/urls.py  
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('photo.urls')),
]
```
  
**템플릿 태그: photo/templates/photo/photo_list.html**
```html
<html>
    <head>
        <title>Photo App</title>
    </head>
    <body>
        <h1><a href="">사진 목록 페이지</a></h1>
        <section>
            {% for photo in photos %}
            <div>
                <h2>
                    <a href="">{{ photo.title }}</a>
                </h2>
                <img src="{{ photo.image }}" alt="{{ photo.title }}" width="300" />
                <p>{{ photo.author }}, {{ photo.price }}원</p>
            </div>
            {% endfor %}
        </section>
    </body>
</html>
```

**뷰 수정: photo/views.py**
```python
from django.shortcuts import render
from .models import Photo
# Create your views here.
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/photo_list.html', {'photos': photos})
```
> 뷰 마지막 인자의 {}을 활용해 템플릿으로 데이터 보내기 가능  
> 그전에 모델에서 데이터를 꺼내와야 함 -> Django의 ORM(Object Relational Mapping)기능 사용  
> Photo.objects.all()을 통해 Photo 모델 데이터를 가져옴  
> 해당 데이터를 {}에 넣어서 템플릿으로 전달   
> 템플릿은 해당 데이터를 템플릿 태그와 함께 활용  

***
***
***
# 개인적 수정
> Image를 굳이 src로 받아야 하는가?
> 파일로 올릴 수 있게 수정  


**모델 수정: photo/models.py**
```python
from django.db import models

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    image = models.ImageField(upload_to='static/images')
    description = models.TextField()
    price = models.IntegerField()
```
> image부분을 ImageField로 수정하고 upload 경로를 지정  

**세팅 수정: myweb/settings.py**
```python
import os
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')] # 개발단계
# STATIC_ROOT = os.path.join(BASE_DIR,'static') # 배포단계
```

> photo폴더 안에 static/images폴더 생성  
> 그리고 서버실행  

***
***
***

## 2.6.2 사진 게시물 보기 화면 만들기  

* 템플릿  
**photo/templates/photo/photo_detail.html**
```html
<html>
    <head>
        <title>Photo App</title>
    </head>
    <body>
        <h1>{{ photo.title }}</h1>
        <section>
            <div>
                <img src="{{ photo.image.url }}" alt="{{ photo.title }}" width="300" />
                <p>{{ photo.description }}</p>
                <p>{{ photo.author }}, {{ photo.price }}원</p>
            </div>
        </section>
    </body>
</html>
```

* 뷰
**photo/views.py**
```python
from django.shortcuts import render, get_object_or_404
from .models import Photo

# Create your views here.
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/photo_list.html', {'photos': photos})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo/photo_detail.html', {'photo': photo})
```
> get_object_or_404()는 모델로부터 데이터를 찾아보고 없다면 404 에러를 반환  
> pk(모델의 데이터를 구분하는 Django의 기본 ID값)로 데이터를 찾음  
> 찾은 photo data를 photo_detail.html에 전달  

* URL  
**photo/urls.py**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.photo_list, name='photo_list'),
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),
]
```
> pk로 데이터를 유일하게 구분해 URL을 추가  

**photo/templates/photo/photo_list.html**
```html
<html>
    <head>
        <title>Photo App</title>
    </head>
    <body>
        <h1><a href="">사진 목록 페이지</a></h1>
        <section>
            {% for photo in photos %}
            <div>
                <h2>
                    <a href="{% url 'photo_detail' pk=photo.pk %}">{{ photo.title }}</a>
                </h2>
                <img src="{{ photo.image.url }}" alt="{{ photo.title }}" width="300" />
                <p>{{ photo.author }}, {{ photo.price }}원</p>
            </div>
            {% endfor %}
        </section>
    </body>
</html>
```
> 메인화면에서 세부화면으로 이동할 수 있게 photo_detail.html의 URL에 대한 뷰를 설정  

## 2.6.3 사진 게시물 작성 기능 만들기  

* 템플릿  
**photo/templates/photo/photo_post.html**
```html
<html>
    <head>
        <title>Photo App</title>
    </head>
    <body>
        <h1><a href="/">홈으로 돌아가기</a></h1>
        
        <section>
            <h2>New Photo</h2>
            <form method="POST">
                {% csrf_token %} {{ form.as_p }}
                <button type="submit">완료!</button>
            </form>
        </section>
    </body>
</html>
```
> form은 사용자가 데이터를 입력한 것을 서버로 보내도록 도와주는 역할  
> csrf_token은 보안 토큰: 사용자의 세션에 있는 토큰과 요청으로 돌아온 토큰이 일치하는지 확인하는 것  
> form.as_p는 우리가 만들 form을 태그 형식으로 만들어주겠다는 것  

* 폼  
**photo/forms.py**
```python
from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = (
            'title',
            'author',
            'image',
            'description',
            'price',
        )
```
> django의 기본 ModelForm을 상속받아 fields의 필드 값들을 입력으로 받는 폼을 만듦  

* 뷰
**photo/views.py**
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Photo
from .forms import PhotoForm

# Create your views here.
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/photo_list.html', {'photos': photos})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo/photo_detail.html', {'photo': photo})

def photo_post(request):
    if request.method == "POST":
        form = PhotoForm(request.POST)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm()
    return render(request, 'photo/photo_post.html', {'form': form})
```

> redirect: 다시 다른 페이지로 이동시켜주는 함수  
> 조건문으로 들어온 요청이 POST인지 확인(일반적으로 웹 브라우저에서 페이지로 접속하는 요청은 GET요청임)  
> 요청으로 들어온 폼 데이터를 form이라는 변수에 받아와 폼에 맞춰 잘 작성된 데이터인지 검사(Django에서 제공하는 기능)  
> valid하다면 photo라는 변수에 form에서 받은 데이터를 받아 photo.save()로 저장  
> 그리고 해당 게시글의 세부 페이지로 이동  
> POST요청이 아니라면 해당 페이지에 처음 접속일테니 form을 제공  
> form이 valid하지 않거나 POST요청이 아닐 때, render로 가게 되어 빈 폼 페이지를 보여줌  

* URL  
**photo/urls.py**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.photo_list, name='photo_list'),
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),
    path('photo/new/', views.photo_post, name='photo_post'),
]
```

**photo/templates/photo/photo_list.html**
```html
<html>
    <head>
        <title>Photo App</title>
    </head>
    <body>
        <h1><a href="">사진 목록 페이지</a></h1>
        <h3><a href="{% url 'photo_post' %}">New Photo</a></h3>
        <section>
            {% for photo in photos %}
            <div>
                <h2>
                    <a href="{% url 'photo_detail' pk=photo.pk %}">{{ photo.title }}</a>
                </h2>
                <img src="{{ photo.image.url }}" alt="{{ photo.title }}" width="300" />
                <p>{{ photo.author }}, {{ photo.price }}원</p>
            </div>
            {% endfor %}
        </section>
    </body>
</html>
```

**위와 같이 했더니! 사진 업로드가 안되고 오류가 떠버림!**

***
***
***

## 책은 생각보다 불친절하다, 구글링을 통해 내 방식대로 해봤다

**photo/models.py**
```python
from django.db import models

# Create your models here.
class Photo(models.Model):
    title = models.CharField(blank = True, max_length=50)
    author = models.CharField(blank = True, max_length=50)
    image = models.ImageField(blank = True, null = True, upload_to='static/images')
    description = models.TextField(blank = True)
    price = models.IntegerField(blank = True)
```
> 공란도 입력받을 수 있게 blank=True속성을 줌  
> ImageField에서 문제가 발생한 것 같음  

**photo/views.py**
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Photo
from .forms import PhotoForm

# Create your views here.
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/photo_list.html', {'photos': photos})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo/photo_detail.html', {'photo': photo})

def photo_post(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = Photo(
                title=request.POST['title'],
                author=request.POST['author'],
                image=request.FILES['image'],
                description=request.POST['description'],
                price=request.POST['price']
                )
            photo.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm()
    return render(request, 'photo/photo_post.html', {'form': form})
```

> 가장 중요한 부분..
> photo_post 함수에서 request.POST와 request.FILES를 통해 데이터를 받아옴  
> request.POST에는 title, author, description, price가 있음  
> request.FILES에는 image가 있음  
> 데이터베이스에 photo.save()를 통해 저장하고 redirect  


**photo/templates/photo/photo_post.html**
```html
<html>
    <head>
        <title>Photo App</title>
    </head>
    <body>
        <h1><a href="/">홈으로 돌아가기</a></h1>
        
        <section>
            <div>
                <h2>New Photo</h2>
                <form method="POST" enctype="multipart/form-data">
                    {% csrf_token %} {{ form.as_p }}
                    <button type="submit">완료!</button>
                </form>
            </div>
        </section>
    </body>
</html>
```
> 파일이 포함된 form을 제출한다는 multipart/form-data로 인코딩 타입 명시  


**위의 과정을 통해 오류를 해결함!**
***
***
***

## 2.6.4 사진 게시물 수정 기능 만들기  

* 템플릿
> 작성 기능과 템플릿이 동일해 기존 photo_post.html 이용  

* 뷰  
**photo/views.py**
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Photo
from .forms import PhotoForm

# Create your views here.
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/photo_list.html', {'photos': photos})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo/photo_detail.html', {'photo': photo})

def photo_post(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = Photo(
                title=request.POST['title'],
                author=request.POST['author'],
                image=request.FILES['image'],
                description=request.POST['description'],
                price=request.POST['price']
                )
            photo.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm()
    return render(request, 'photo/photo_post.html', {'form': form})
    
def photo_edit(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            photo = Photo(
                title=request.POST['title'],
                author=request.POST['author'],
                image=request.FILES['image'],
                description=request.POST['description'],
                price=request.POST['price']
            )
            photo.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm(instance=photo)
    return render(request, 'photo/photo_post.html', {'form': form})
```

> 먼저 수정할 대상을 pk로 찾아옴  
> 작성 때와 다른 것은 동일하고 PhotoForm의 instance를 photo로 설정해 수정 대상이 될 데이터를 설정함  
> GET 요청이 들어와도 photo데이터를 폼에 담아 photo_post.html에 넘겨 기존 데이터를 수정  

* URL
**photo/urls.py**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.photo_list, name='photo_list'),
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),
    path('photo/new/', views.photo_post, name='photo_post'),
    path('photo/<int:pk>/edit/', views.photo_edit, name='photo_edit'),
]
```

> pk를 URL에 넣어 구분  

**photo/templates/photo/photo_detail.html**
```html
<html>
    <head>
        <title>Photo App</title>
    </head>
    <body>
        <h1>{{ photo.title }}</h1>
        <h3><a href="{% url 'photo_edit' pk=photo.pk %}">Edit Photo</a></h3>
        <section>
            <div>
                <img src="{{ photo.image.url }}" alt="{{ photo.title }}" width="300" />
                <p>{{ photo.description }}</p>
                <p>{{ photo.author }}, {{ photo.price }}원</p>
            </div>
        </section>
    </body>
</html>
```

> 수정하는 링크를 photo_detail 페이지에 추가  

## 2.6.5 예시 마무리 하기  

> 끝

***
***
***

> 인줄 알았지만... 역시나 수정이 안되고 추가가 되버리는 문제...  

## 구글링을 통한.. static/images 경로에 있는 사진 삭제와 추가 기능 추가  

**photo/views.py**
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Photo
from .forms import PhotoForm
import os
# Create your views here.
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/photo_list.html', {'photos': photos})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo/photo_detail.html', {'photo': photo})

def photo_post(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = Photo(
                title=request.POST['title'],
                author=request.POST['author'],
                image=request.FILES['image'],
                description=request.POST['description'],
                price=request.POST['price']
                )
            photo.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm()
    return render(request, 'photo/photo_post.html', {'form': form})
    
def photo_edit(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        old_img = photo.image.path
        if form.is_valid():
            # 기존 이미지 파일 삭제
            if os.path.exists(old_img):
                os.remove(old_img)
            # 새로운 이미지 파일 등록
            form.save()
            return redirect('photo_detail', pk=photo.pk)
    else:
        form = PhotoForm(instance=photo)
    return render(request, 'photo/photo_post.html', {'form': form})
```

> import os를 해서 경로를 찾을 수 있게 해줌  
> photo_edit 부분에 기존 객체를 받고 이미지 경로 변수에 저장  
> os.path.exists에 인자로 기존 객체의 이미지 경로를 넘겨주고 경로가 실제로 존재하는지 확인  
> 존재한다면 os.remove로 삭제  
> PhotoForm에 맞게 받아온 form을 그대로 데이터베이스에 저장  
> 나머지는 똑같음  
>   > 사실 왜 되지? 하는 부분이 조금 있었지만 일단 되기에 패스.. 시간을 너무 많이 써버림  


**진짜 끝**

***
***
***
