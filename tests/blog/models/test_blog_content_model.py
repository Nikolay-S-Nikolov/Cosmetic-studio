from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from Cosmetic_studio.blog.models import BlogContent, Tag

UserModel = get_user_model()


class BlogContentModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='myname@gmail.com',
            password='123qWER',
        )
        self.tag = Tag.objects.create(name='New Tag', slug='new-tag')

    def test__create_blog__valid_content(self):
        blog_content = BlogContent.objects.create(
            title="My Blog Post",
            main_image="image/main_image.jpg",
            left_image="image/left_image.jpg",
            right_image="image/right_image.jpg",
            content="This is a test blog." * 10,
            slug="my-blog-post",
            author=self.user,
            published=True
        )
        blog_content.tags.add(self.tag)

        self.assertEqual(blog_content.title, "My Blog Post")
        self.assertEqual(blog_content.slug, "my-blog-post")
        self.assertEqual(blog_content.main_image, "image/main_image.jpg")
        self.assertEqual(blog_content.left_image, "image/left_image.jpg")
        self.assertEqual(blog_content.right_image, "image/right_image.jpg")
        self.assertEqual(blog_content.content, "This is a test blog." * 10)
        self.assertEqual(blog_content.author, self.user)
        self.assertTrue(blog_content.published)
        self.assertEqual(blog_content.tags.count(), 1)
        self.assertEqual(blog_content.tags.first(), self.tag)
        self.assertIsNotNone(blog_content.created_at)
        self.assertIsNotNone(blog_content.updated_at)

    def test__blog_content__title_min_length__raise_validation_error(self):
        with self.assertRaises(ValidationError):
            blog = BlogContent(
                title="Ab",
                main_image="image/main_image.jpg",
                left_image="image/left_image.jpg",
                right_image="image/right_image.jpg",
                content="This is a test blog." * 10,
                author=self.user
            )
            blog.full_clean()

    def test__blog_content__limit_values(self):
        invalid_title_min = 'T' * (BlogContent.MIN_TITLE_LENGTH - 1)
        valid_max_limit_title = 'T' * BlogContent.MAX_TITLE_LENGTH
        invalid_title_max = 'T' * (BlogContent.MAX_TITLE_LENGTH + 1)

        valid_content = 'C' * BlogContent.MIN_CONTENT_LENGTH
        invalid_content_min = 'C' * (BlogContent.MIN_CONTENT_LENGTH - 1)
        invalid_content_max = 'C' * (BlogContent.MAX_CONTENT_LENGTH + 1)

        valid_blockquote = 'B' * BlogContent.MAX_BLOCKQUOTE_LENGTH
        invalid_blockquote_max = 'B' * (BlogContent.MAX_BLOCKQUOTE_LENGTH + 1)

        blog_content = BlogContent.objects.create(
            title=valid_max_limit_title,
            content=valid_content,
            blockquote=valid_blockquote,
            main_image="image/main_image.jpg",
            left_image="image/left_image.jpg",
            right_image="image/right_image.jpg",
            author=self.user,
            slug="my-blog-post",
        )
        blog_content.tags.add(self.tag)
        blog_content.full_clean()

        with self.assertRaises(ValidationError):
            blog_content.title = invalid_title_min
            blog_content.full_clean()

        with self.assertRaises(ValidationError):
            blog_content.title = invalid_title_max
            blog_content.full_clean()

        with self.assertRaises(ValidationError):
            blog_content.content = invalid_content_min
            blog_content.full_clean()

        with self.assertRaises(ValidationError):
            blog_content.content = invalid_content_max
            blog_content.full_clean()

        with self.assertRaises(ValidationError):
            blog_content.blockquote = invalid_blockquote_max
            blog_content.full_clean()

    def test__blog_content__creation__without_images__raises_validation_error(self):
        blog_content = BlogContent.objects.create(
            title="Sample Blog Post",
            content="This is a sample content with sufficient length.",
            author=self.user,
            slug="sample-slug",
            published=True,
        )
        with self.assertRaises(ValidationError):
            blog_content.full_clean()

    def test__blog_content__str_method__return_name(self):
        blog_content = BlogContent.objects.create(
            title="Sample Blog Post",
            content="This is a sample content with sufficient length.",
            main_image="image/main_image.jpg",
            left_image="image/left_image.jpg",
            right_image="image/right_image.jpg",
            author=self.user,
            slug="my-blog-post",
        )
        self.assertEqual(str(blog_content), "Sample Blog Post")