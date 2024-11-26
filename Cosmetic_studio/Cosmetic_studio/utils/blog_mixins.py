from django.utils.text import slugify


class FieldSlugMixin:
    slug_field = "name"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.slug_field)

        original_slug = self.slug
        num = 1
        model_class = self.__class__

        # Ensure the slug is unique
        while model_class.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{num}"
            num += 1

        super().save(*args, **kwargs)