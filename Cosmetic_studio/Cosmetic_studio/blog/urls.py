from django.urls import path, include

from Cosmetic_studio.blog.views import CreatePostContent, PostListViews, PostDetailView, PostListByTagView

urlpatterns = (
    path('', PostListViews.as_view(), name='posts-list'),
    path('create/', CreatePostContent.as_view(), name='post-create'),
    path('<slug:slug>/', include([
        path('', PostListByTagView.as_view(), name='post-by-tag'),
        path('details/', PostDetailView.as_view(), name='post-details'),
    ])),

)
