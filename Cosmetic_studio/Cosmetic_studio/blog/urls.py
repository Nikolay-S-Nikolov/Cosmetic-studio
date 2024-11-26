from django.urls import path, include

from Cosmetic_studio.blog.views import CreatePostContent, blog, PostDetailView

urlpatterns = (
    path('', blog, name='blog'),
    path('create/', CreatePostContent.as_view(), name='create_post'),
    path('<int:pk>/', include([
        path('details/', PostDetailView.as_view(), name='details_post'),
    ])),

)
