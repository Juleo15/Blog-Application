from django.contrib.admin import views
from . import views
from django.urls import path
from .views import post_list, post_detail, post_create, post_vote

app_name = "post"
urlpatterns = [
    path("post/", post_list, name="post_list"),
    path("post/<int:pk>/", post_detail, name="post_detail"),
    path("post/create", post_create, name="post_create"),
    path("post/<int:pk>/vote/<str:vote_type>/", post_vote, name="post_vote"),
    path('post/<int:pk>/share/', views.post_share, name='post_share'),
    # path('user/<int:id>/', views.user_detail, name='user_detail'),
    path('', views.login, name='login'),
]