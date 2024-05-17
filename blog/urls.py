from django.urls import path
from django.views.decorators.cache import cache_page
from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='blog_detail'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/update/<int:pk>', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<int:pk>', BlogDeleteView.as_view(), name='blog_delete'),
]
