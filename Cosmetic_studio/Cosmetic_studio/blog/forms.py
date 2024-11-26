from django import forms

from Cosmetic_studio.blog.models import BlogContent, Tag


class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].label = "Select Tags"

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = BlogContent
        fields = ['title', 'content', 'slug', 'main_image', 'blockquote', 'left_image', 'right_image', 'tags']
