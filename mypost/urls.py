
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('post.urls')),
    # 공지글 urls 연결

    
    # url 만들고 나서 
    #ModuleNotFoundError: No module named 'cal' 오류가 계속 뜨네요 ㅜㅜ
]
