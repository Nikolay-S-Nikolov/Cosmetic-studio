from django.contrib.messages import get_messages
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages.storage.fallback import FallbackStorage
from Cosmetic_studio.blog.models import BlogContent, Comment
from Cosmetic_studio.blog.views import PostDetailView
from Cosmetic_studio.blog.forms import CommentForm

UserModel = get_user_model()


class TestPostDetailView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(
            user_name='Mo',
            email='myname@gmail.com',
            password='123qWER'
        )
        self.blog_post = BlogContent.objects.create(
            title='My Post',
            content='My content' * 10,
            author=self.user,
            slug='test-slug'
        )

    def test__post_comment__successful(self):
        request = self.factory.post(reverse(
            'post-details',
            kwargs={'slug': self.blog_post.slug}),
            {
            'content': 'My first comment'
        })
        request.user = self.user
        setattr(request, 'session', {})
        setattr(request, '_messages', FallbackStorage(request))

        view = PostDetailView.as_view()
        response = view(request, slug=self.blog_post.slug)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('post-details', kwargs={'slug': self.blog_post.slug}))
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, 'My first comment')
        self.assertEqual(Comment.objects.first().author, self.user)
        self.assertEqual(Comment.objects.first().post, self.blog_post)

        messages = list(get_messages(request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your comment has been posted successfully.')

    def test_post_comment_redirect(self):
        request = self.factory.post(reverse('post-details', kwargs={'slug': self.blog_post.slug}))

        request.user = self.user

        view = PostDetailView.as_view()
        response = view(request, slug=self.blog_post.slug)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('post-details', kwargs={'slug': self.blog_post.slug}))
