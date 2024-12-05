from io import BytesIO

from django import forms
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from Cosmetic_studio.blog.forms import CreatePostForm
from Cosmetic_studio.blog.models import Tag
from PIL import Image

UserModel = get_user_model()


def generate_test_image():
    """Creates a simple in-memory test image."""
    image = BytesIO()
    img = Image.new('RGB', (100, 100), color='red')
    img.save(image, format='JPEG')
    image.seek(0)
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=image.read(),
        content_type='image/jpeg'
    )


class CreatePostFormTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='myname@gmail.com',
            password='123qwer',
        )
        self.tag1 = Tag.objects.create(name='Tag1', slug='tag-1')
        self.tag2 = Tag.objects.create(name='Tag2', slug='tag-2')

    def test__create_post_form__initializes_with_default_labels_and_widgets(self):
        form = CreatePostForm()
        self.assertEqual(form.fields['tags'].label, "Select Tags")
        self.assertIsInstance(form.fields['tags'].widget, forms.CheckboxSelectMultiple)

    def test__create_post_form__handles_empty_queryset_for_tags(self):
        Tag.objects.all().delete()

        form = CreatePostForm()

        self.assertEqual(form.fields['tags'].queryset.count(), 0)
        self.assertEqual(form.fields['tags'].label, "Select Tags")
        self.assertIsInstance(form.fields['tags'].widget, forms.CheckboxSelectMultiple)

    def test__create_post_form__allows_creation_without_slug__generates_correct_slug(self):

        mock_image = generate_test_image()

        form_data = {
            'title': 'New test title',
            'content': 'Test content short enough to reach length limit',
            'main_image': mock_image,
            'left_image': mock_image,
            'right_image': mock_image,
            'tags': [self.tag1.id, self.tag2.id],
        }
        form = CreatePostForm(data=form_data,
                              files={'main_image': mock_image, 'left_image': mock_image, 'right_image': mock_image})
        self.assertTrue(form.is_valid())
        post = form.save(commit=False)
        post.author = self.user
        post.save()
        self.assertEqual(post.slug, 'new-test-title-1')


