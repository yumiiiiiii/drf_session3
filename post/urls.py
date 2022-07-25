from django.urls import path

from .views import PostsAPIView, PostAPIView
from .views import CalAPIView, CalsAPIView
from .views import *

app_name='post'

urlpatterns = [

    path('post/', PostsAPIView.as_view()),
    # 공지글 전체조회 url
    path('post/<int:pk>/', PostAPIView.as_view()),
    # 공지글 세부조회 url

    path('cal/', CalsAPIView.as_view()),
    # 일정 전체조회 url
    path('cal/<int:pk>/', CalAPIView.as_view()),
    # 일정 세부조회 url

    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),

    path('todo/',TodoView.as_view()),
    path('todo/<int:pk>',TodoDetailView.as_view()),


    path('todocomments/', TodoCommentView.as_view()),
    path('todocomments/<int:pk>/', TodoCommentDetailView.as_view()),

]