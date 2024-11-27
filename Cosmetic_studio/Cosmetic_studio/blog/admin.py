from django.contrib import admin

from Cosmetic_studio.blog.models import BlogContent, Tag


class TagInline(admin.TabularInline):
    model = BlogContent.tags.through
    extra = 1


@admin.register(BlogContent)
class BlogContentAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'slug', 'main_image', 'blockquote', 'left_image', 'right_image']
    list_display = ('title', 'author', 'created_at', 'updated_at', 'get_tags')
    list_filter = ('author', 'created_at', 'updated_at', 'tags')
    search_fields = ('title', 'author__username', 'tags__name')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TagInline]
    filter_horizontal = ('tags',)

    def get_tags(self, obj):
        return ", ".join([t.name for t in obj.tags.all()])

    get_tags.short_description = 'Tags'

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object (not an edit)
            obj.author = request.user  # Set the author to the current user
        super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
