from django.urls import reverse_lazy
from django.utils.text import slugify
from Cosmetic_studio.utils.user_mixins import AuthorOrAdminMixin


class FieldSlugMixin:
    slug_field = "name"

    def save(self, *args, **kwargs):
        if not self.pk:
            num = 1
            if not self.slug:
                self.slug = slugify(self.slug_field-{num})

            original_slug = self.slug

            model_class = self.__class__

            # Ensure the slug is unique
            while model_class.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{num}"
                num += 1

        super().save(*args, **kwargs)


class CommentAuthorOrAdminMixin(AuthorOrAdminMixin):
    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'slug': self.object.post.slug})
