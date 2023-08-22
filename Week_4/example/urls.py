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