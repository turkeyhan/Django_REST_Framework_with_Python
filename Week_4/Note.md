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

## 4.3 도서 정보 API 예제로 Django REST Framework 기초 개념 살펴보기  

***

### 4.3.1 DRF Serializer  

> * Serialize: 직렬화, Django 프로젝트에서 만든 모델로부터 뽑은 queryset(Model instance or 파이썬 데이터 객체)을 JSON으로 바꾸는 것
>   > DRF 서버가 데이터를 클라이언트에 보낼 때, API가 직렬화의 과정을 해줌    
> * Deserialize: 역직렬화, JSON 등의 문자열을 파이썬 데이터 객체로 바꾸는 것  
>   > 클라이언트가 데이터를 DRF 서버에 보낼 때, API가 역직렬화의 과정을 해줌  

**Serializer는 직렬화와 역직렬화 기능을 동시에 갖고 있음**  
**클라이언트와 서버 API 간 데이터 양식을 맞춰주는 변환기**  

> **모델: example/models.py**
```python
from django.db import models

# Create your models here.
class Book(models.Model):
    bid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    pages = models.IntegerField()
    price = models.IntegerField()
    published_date = models.DateField()
    description = models.TextField()
```

```bash
$ python manage.py makemigrations example
$ python manage.py migrate
```

> **시리얼라이저: example/serializers.py**
```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.Serializer):
    bid = serializers.IntegerField(primary_key=True)
    title = serializers.CharField(max_length=50)
    author = serializers.CharField(max_length=50)
    category = serializers.CharField(max_length=50)
    pages = serializers.IntegerField()
    price = serializers.IntegerField()
    published_date = serializers.DateField()
    description = serializers.TextField()

    def create(self, validated_data):
        return Book.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.bid = validated_data.get('bid', instance.bid)
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.category = validated_data.get('category', instance.category)
        instance.pages = validated_data.get('pages', instance.pages)
        instance.price = validated_data.get('price', instance.price)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance
```

> 모델 데이터의 어떤 속성을 JSON에 넣어줄지 선언(필드 선언)  
> create()나 update()는 POST 요청으로 들어온 데이터를 파이썬 모델 형태로 역직렬화하여 데이터베이스에 집어넣을 때, 사용함  
> 같은 내용이 반복되고 코드가 긺  
> 따라서 더 나은 대안인 serializers.ModelSerializer 사용  

> **example/serializers.py**
```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['bid', 'title', 'author', 'category', 'pages', 'price', 'published_date', 'description']
```

> 모델의 내용을 기반으로 동작하며 위에서 적은 코드와 내용은 같음  

### 4.3.2 DRF FBV, CBV, API View  

> **두 가지 유형의 뷰 개발방법**
> * Function Based View(FBV): 함수 기반 뷰  
> * Class Based View(CBV): 클래스 기반 뷰  
> 뷰 작성을 함수로 했는지 클래스로 했는지의 차이일 뿐, 기능 상 차이는 없음  

> **APIView**: 여러 가지 요청의 유형에 대해 동작할 수 있도록 도와줌  
>   > 함수형 뷰에서는 @api_view와 같이 데코레이터 형태로 사용  
**example/views.py**
```python
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

@api_view(['GET'])
def HelloAPI(request):
    return Response("hello world!")
```
  
>   > 클래스형 뷰에서는 APIView라는 클래스를 상속받는 클래스의 형태로 생성  
```python
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

class HelloAPI(APIView):
    def get(self, request):
        return Response("hello world")
```

> **함수형 뷰: example/views.py**
```python
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def HelloAPI(request):
    return Response("hello world!")

@api_view(['GET', 'POST'])
def booksAPI(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def bookAPI(request, bid):
    book = get_object_or_404(Book, bid=bid)
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)
```

> **클래스형 뷰**
```python
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import Book
from .serializers import BookSerializer

class BooksAPI(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookAPI(APIView):
    def get(self, request, bid):
        book = get_object_or_404(Book, bid=bid)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

**Saying that class-based views is always the superior solution is a mistake. Nick Coghlan**  
**클래스형 뷰의 여러 부가 기능을 보면 함수형 뷰보다 훨씬 성능이 좋을 것 같지만 절대적인 해결책은 아님**  

### 4.3.3 도서 정보 API 마무리 하기  

***
***

**함수형 뷰**  

> **URL: example/urls.py**
```python
from django.urls import path, include
from .views import HelloAPI, bookAPI, booksAPI

urlpatterns = [
    path("hello/", HelloAPI),
    path("fbv/books/", booksAPI),
    path("fbv/book/<int:bid>/", bookAPI),
]
```
> **실행 후 127.0.0.1:8000/example/fbv/books/로 접속**
```bash
$ python manage.py runserver
```

> **content란에 JSON 형식의 데이터 입력 후 POST** 
```json
{
"bid": 9788931466195,
"title": "백엔드를 위한 Django REST Framework with 파이썬",
"author": "권태형",
"category": "프로그래밍",
"pages": 248,
"price": 18000,
"published_date": "2022-05-20",
"description": "MTV 패턴으로 만드는 REST API"
}
```

> **http://127.0.0.1:8000/example/fbv/book/9788931466195/로 접속**  

***
***

**클래스형 뷰**  

> **URL: example/urls.py**
```python
from django.urls import path, include
from .views import HelloAPI, bookAPI, booksAPI, BookAPI, BooksAPI

urlpatterns = [
    path("hello/", HelloAPI),
    path("fbv/books/", booksAPI),
    path("fbv/book/<int:bid>/", bookAPI),
    path("cbv/books/", BooksAPI.as_view()),
    path("cbv/book/<int:bid>/", BookAPI.as_view()),
]
```

> **실행 후 127.0.0.1:8000/example/cbv/books/로 접속**  

> **content란에 JSON 형식의 데이터 입력 후 POST** 
```json
{
"bid": 9788931467970,
"title": "풀스택 개발이 쉬워지는 다트&플러터",
"author": "이성원",
"category": "프로그래밍",
"pages": 720,
"price": 40000,
"published_date": "2023-05-15",
"description": "시작하는 개발자를 위한 코딩 부트캠프"
}
```

> **http://127.0.0.1:8000/example/fbv/book/9788931467970/로 접속**

***
***

> **https://insomnia.rest/**  
> 위 사이트에서 API 테스트를 위한 전용 프로그램 다운로드  
> New request를 통해 http://127.0.0.1:8000/example/fbv/books/ 로 GET 요청 send  
> POST 요청으로 새로운 데이터도 생성 가능  
> Primary_key인 bid가 같을 시, 중복생성으로 데이터가 들어가지 않아서 400 오류가 뜸  

***
***

## 4.4 Django REST Framework 심화 개념 보충하기  

***

## 4.4.1 DRF의 다양한 뷰  

> **URL과 Method의 조합**  
1. 도서 전체 목록 가져오기 (GET /books/), (list)  
2. 도서 1권 정보 등록하기 (POST /books/), (create)  
3. 도서 1권 정보 가져오기 (GET /book/1), (retrieve)  
4. 도서 1권 정보 수정하기 (PUT /book/1), (update)  
5. 도서 1권 정보 삭제하기 (DELETE /book/1), (destroy)  

### 4.4.2 DRF mixins  

> **클래스형 뷰에서 시리얼라이저 중복문제**
> mixins는 APIView에서 request의 method마다 시리얼라이저 코드를 작성하는 것을 줄이기 위해 클래스 레벨에서 시리얼라이저를 등록함  
> 따라서 각 method에는 시리얼라이저 코드를 작성하는 대신 mixin에 연결해 사용  

  
> **example/views.py**
```python
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import Book
from .serializers import BookSerializer

class BooksAPIMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class BookAPIMixins(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
```

> generics와 mixins를 불러와 각각 클라스를 만들 때, 상속함  
> queryset에는 모든 데이터를 불러옴  
> serializer_class로 사용할 시리얼라이저 설정  
> 각 method에 대해 return문을 확인하면 Mixins에 해당되는 method에 알맞게 사용되어 있는 것을 알 수 있음  
  
> **update와 destroy 추가: example/views.py**  
```python
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import Book
from .serializers import BookSerializer

class BooksAPIMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class BookAPIMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

> **URL 등록: example/urls.py**
```python
from django.urls import path, include
from .views import HelloAPI, bookAPI, booksAPI, BookAPI, BooksAPI, BooksAPIMixins, BookAPIMixins

urlpatterns = [
    path("hello/", HelloAPI),
    path("fbv/books/", booksAPI),
    path("fbv/book/<int:bid>/", bookAPI),
    path("cbv/books/", BooksAPI.as_view()),
    path("cbv/book/<int:bid>/", BookAPI.as_view()),
    path("mixin/books/", BooksAPIMixins.as_view()),
    path("mixin/book/<int:bid>/", BookAPIMixins.as_view()),
]
```
> 그리고 http://127.0.0.1:8000/example/mixin/books/ 로 접속  
> 각 URL에 따른 동작 확인  
> 책 상세정보를 들어가면 PUT, DELETE 등의 버튼이 생성된 것을 확인할 수 있음(Mixins에서 제공)  

### 4.4.3 DRF generics  

> **9종류의 mixins 세트**  
1. generics.ListAPIView (전체 목록)  
2. generics.CreateAPIView (생성)  
3. generics.RetrieveAPIView (1개)  
4. generics.UpdateAPIView (1개 수정)  
5. generics.DestroyAPIView (1개 삭제)  
6. generics.ListCreateAPIView (전체 목록 + 생성)  
7. generics.RetrieveUpdateAPIView (1개 + 1개 수정)  
8. generics.RetrieveDestroyAPIView (1개 + 1개 삭제)  
9. generics.RetrieveUpdateDestroyAPIView(1개 + 1개 수정 + 1개 삭제)  

> **6번과 9번을 사용: example/views.py**
```python
...
from rest_framework import generics
...
class BooksAPIGenerics(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookAPIGenerics(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'
```

> **URL 연결: example/urls.py**
```python
from django.urls import path, include
from .views import HelloAPI, bookAPI, booksAPI, BookAPI, BooksAPI, BooksAPIMixins, BookAPIMixins, BooksAPIGenerics, BookAPIGenerics

urlpatterns = [
    path("hello/", HelloAPI),
    path("fbv/books/", booksAPI),
    path("fbv/book/<int:bid>/", bookAPI),
    path("cbv/books/", BooksAPI.as_view()),
    path("cbv/book/<int:bid>/", BookAPI.as_view()),
    path("mixin/books/", BooksAPIMixins.as_view()),
    path("mixin/book/<int:bid>/", BookAPIMixins.as_view()),
    path("generic/books/", BooksAPIGenerics.as_view()),
    path("generic/book/<int:bid>", BookAPIGenerics.as_view()),
]
```

> runserver이후에 url에 접속해서 확인했더니 잘 됨  
> **generics는 mixins를 조합하기만 해놓은 코드**  

### 4.4.4 DRF Viewset & Router  

> Viewset에서는 하나의 클래스로 하나의 모델을 전부 처리해줄 수 있어 queryset이나 serializer_class 부분이 겹치지 않음  

> **ModelViewSet: example/views.py**
```python
from rest_framework import viewsets
...
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

> ViewSet의 내부를 살펴보면 Mixin을 기반으로 작성함  

> **라우터를 사용한 URL 연결: example/urls.py**
```python
from django.urls import path, include
from rest_framework import routers
from .views import HelloAPI, bookAPI, booksAPI, BookAPI, BooksAPI, BooksAPIMixins, BookAPIMixins, BooksAPIGenerics, BookAPIGenerics, BookViewSet

router = routers.SimpleRouter()
router.register('books', BookViewSet)

# urlpatterns = [
#     path("hello/", HelloAPI),
#     path("fbv/books/", booksAPI),
#     path("fbv/book/<int:bid>/", bookAPI),
#     path("cbv/books/", BooksAPI.as_view()),
#     path("cbv/book/<int:bid>/", BookAPI.as_view()),
#     path("mixin/books/", BooksAPIMixins.as_view()),
#     path("mixin/book/<int:bid>/", BookAPIMixins.as_view()),
#     path("generic/books/", BooksAPIGenerics.as_view()),
#     path("generic/book/<int:bid>", BookAPIGenerics.as_view()),
# ]

urlpatterns = router.urls
```

> ViewSet과 Router의 사용으로 다음과 같은 장점을 얻음  
1. 하나의 클래스로 하나의 모델에 대한 내용을 전부 작성 가능 -> 중복 제거  
2. 라우터를 통해 URL을 일일이 지정하지 않아도 일정한 규칙의 URL 생성 가능  

> **위와 같은 기능들은 편리해지는 대신 자유도가 떨어지므로 프로젝트 목적에 따라 사용할지 여부를 결정하자**  

***
***
***