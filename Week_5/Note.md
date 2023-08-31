# Chapter 5. 연습 프로젝트 : Todo 목록 API 만들기  

***
***
***

## 5.1 Todo 목록 API 시작하기   

***

### 5.1.1 Django 기반 Todo 목록 웹 서비스 복습  

> Todo의 목록 및 상세 조회, 수정, 완료  
> Todo를 프론트 영역과 분리, API 형태로 개발  

### 5.1.2 프로젝트 생성하기  

> **가상 환경 세팅**
```bash
python3 --version
python3 -m venv myvenv
myvenv/Scripts/activate
```

> **장고 설치**
```bash
pip install django~=3.2.10 djangorestframework~=3.13.1
```

> **장고 프로젝트 생성**
```bash
django-admin startproject mytodo .
```

> **todo 앱 생성**
```bash
python manage.py startapp todo
```

### 5.1.3 Todo 프로젝트 설정하기  

> **mytodo/settings,py**
```python
...
ALLOWED_HOSTS = ['127.0.0.1']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'todo',
]
...
TIME_ZONE = 'Asia/Seoul'
...
```

> **관리자 계정 생성**
```bash
python manage.py createsuperuser
```

### 5.1.4 Todo 모델 생성하기  

> **todo/models.py**
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

***
***

## 5.2 Todo 전체 조회 API 만들기  

***

### 5.2.1 Todo 전체 조회 시리얼라이저 만들기  

> 시리얼라이저는 데이터를 원하는 형태로 보내고 받기 위한 양식  
> 보내고 받는 형태에 따라 다른 시리얼라이저 필요  
> 그 중 첫번째 시리얼라이저는 전체 조회용 시리얼라이저  

> **todo/serializers.py**
```python
from rest_framework import serializers
from .models import Todo

class TodoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'complete', 'important')
```

### 5.2.2 Todo 전체 조회 뷰 만들기  

> APIView를 통한 뷰 만들기  
> **todo/views.py**
```python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSimpleSerializer

class TodosAPIView(APIView):
    def get(self, request):
        todos = Todo.objects.filter(complete=False)
        serializer = TodoSimpleSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

> GET 방식으로 요청 처리  
> complete가 False인 Todo들을 필터링  
> 시리얼라이저를 통해 보낼 수 있는 형태로 변환  
> Response 객체 형태로 전달  

### 5.2.3 Todo 전체 조회 URL 연결하기  

> **todo/urls.py**
```python
from django.urls import path
from .views import TodosAPIView

urlpatterns = [
    path('todo/', TodosAPIView.as_view()),
]
```

> **mytodo/urls.py**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
]
```

### 5.2.4 Todo 전체 조회 API 테스트하기  

> 테스트 안할래요!  
> **모델 등록**
```bash
python manage.py makemigrations
python manage.py migrate
```

***
***

## 5.3 Todo 상세 조회 API 만들기  

***

## 5.3.1 상세 조회용 Todo 시리얼라이저 만들기  

> 필드는 Todo 모델의 모든 필드  
> **todo/serializers.py**
```python
from rest_framework import serializers
from .models import Todo

class TodoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'complete', 'important')

class TodoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'created', 'complete', 'important')     
```

### 5.3.2 Todo 상세 조회 뷰 만들기  

> GET 방식으로 통신  
> 전체 조회와는 주소가 다르기에 클래스 구분  
> **todo/views.py**
```python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSimpleSerializer, TodoDetailSerializer
from rest_framework.generics import get_object_or_404

class TodosAPIView(APIView):
    def get(self, request):
        todos = Todo.objects.filter(complete=False)
        serializer = TodoSimpleSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TodoAPIView(APIView):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

### 5.3.3 Todo 상세 조회 URL 연결하기  

> **todo/urls.py**
```python
from django.urls import path
from .views import TodosAPIView, TodoAPIView

urlpatterns = [
    path('todo/', TodosAPIView.as_view()),
    path('todo/<int:pk>/', TodoAPIView.as_view()),
]
```

### 5.3.4 Todo 상세 조회 API 테스트하기  
> PASS

***
***

## 5.4 Todo 생성 API 만들기  

***

### 5.4.1 생성용 Todo 시리얼라이저 만들기  

> 생성에 필요한 입력 값은 title, description, important  
> 나머지는 자동 생성  
> **todo/serializers.py**
```python
from rest_framework import serializers
from .models import Todo

class TodoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'complete', 'important')

class TodoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'created', 'complete', 'important')

class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('title', 'description', 'important')
```

### 5.4.2 Todo 생성 뷰 만들기  

> Todo 생성은 /todo URL에서 동작  
> 따라서 Todo 생성 뷰는 TodosAPIView 클래스 내에 포함 가능  
> Todo 생성은 POST 방식  
> **todo/views.py**
```python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSimpleSerializer, TodoDetailSerializer, TodoCreateSerializer
from rest_framework.generics import get_object_or_404

class TodosAPIView(APIView):
    def get(self, request):
        todos = Todo.objects.filter(complete=False)
        serializer = TodoSimpleSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TodoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TodoAPIView(APIView):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

### 5.4.3 Todo 생성 URL 연결하기  

> 별도의 작업은 필요 없음  

### 5.4.4 Todo 생성 API 테스트하기  

> PASS  

***
***

## 5.5 Todo 수정 API 만들기  

***

### 5.5.1 Todo 수정 뷰 만들기  

> Todo 생성과 비슷  
> 따라서 TodoCreateSerializer 활용  
> Todo 수정은 특정 Todo에 대해 이뤄지므로 TodoAPIView 클래스에 포함  
> **todo/views.py**
```python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSimpleSerializer, TodoDetailSerializer, TodoCreateSerializer
from rest_framework.generics import get_object_or_404

class TodosAPIView(APIView):
    def get(self, request):
        todos = Todo.objects.filter(complete=False)
        serializer = TodoSimpleSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TodoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TodoAPIView(APIView):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoCreateSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

> PUT 메소드 형태로 작성  

### 5.5.2 Todo 수정 URL 연결하기  

> 이미 URL에 연결되어 필요없음  

### 5.5.3 Todo 수정 API 테스트하기  

> PASS  

***
***

## 5.6 Todo 완료 API 만들기  

***

### 5.6.1 Todo 완료 뷰 만들기  

> 별도의 클래스에 작성  
> 완료 목록 조회용 API, 특정 Todo 완료 API 필요  
> **todo/views.py**
```python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSimpleSerializer, TodoDetailSerializer, TodoCreateSerializer
from rest_framework.generics import get_object_or_404

class TodosAPIView(APIView):
    def get(self, request):
        todos = Todo.objects.filter(complete=False)
        serializer = TodoSimpleSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TodoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TodoAPIView(APIView):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoCreateSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoneTodosAPIView(APIView):
    def get(selt, request):
        dones = Todo.objects.filter(complete=True)
        serializer = TodoSimpleSerializer(dones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

### 5.6.2 Todo 완료 조회 뷰 만들기  

> **todo/views.py**
```python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSimpleSerializer, TodoDetailSerializer, TodoCreateSerializer
from rest_framework.generics import get_object_or_404

class TodosAPIView(APIView):
    def get(self, request):
        todos = Todo.objects.filter(complete=False)
        serializer = TodoSimpleSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TodoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TodoAPIView(APIView):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoCreateSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoneTodosAPIView(APIView):
    def get(self, request):
        dones = Todo.objects.filter(complete=True)
        serializer = TodoSimpleSerializer(dones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DoneTodoAPIView(APIView):
    def get(self, request, pk):
        done = get_object_or_404(Todo, id=pk)
        done.complete = True
        done.save()
        serializer = TodoDetailSerializer(done)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

> get 메소드  
> Todo를 찾아 complete를 True로 설정  

### 5.6.3 Todo 완료 URL 연결하기  

> **todo/urls.py**
```python
from django.urls import path
from .views import TodosAPIView, TodoAPIView, DoneTodoAPIView, DoneTodosAPIView

urlpatterns = [
    path('todo/', TodosAPIView.as_view()),
    path('todo/<int:pk>/', TodoAPIView.as_view()),
    path('done/', DoneTodosAPIView.as_view()),
    path('done/<int:pk>/', DoneTodoAPIView.as_view()),
]
```

### 5.6.4 Todo 완료 API 테스트하기  
> PASS

***
***

## 모든 테스트 진행하기  

> Insomnia로 전체 조회, 세부 조회, 수정, 완료 조회, 완료 세부 조회까지 다 테스트 완료  

***
***
***