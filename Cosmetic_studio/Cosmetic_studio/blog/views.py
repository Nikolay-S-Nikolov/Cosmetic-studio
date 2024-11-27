from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from Cosmetic_studio.blog.forms import CreatePostForm
from Cosmetic_studio.blog.models import BlogContent, Tag


class CreatePostContent(views.CreateView):
    model = BlogContent
    form_class = CreatePostForm
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Create Post',
        'submit_button_text': 'Create',
    }
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse("details_post", kwargs={"pk": self.object.pk})


class PostListViews(views.ListView):
    model = BlogContent
    template_name = 'blog/posts_list.html'
    paginate_by = 2
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reversed_list'] = BlogContent.objects.order_by('?')[:4]
        context['tags_list'] = Tag.objects.order_by('name')
        return context


class PostDetailView(views.DetailView):
    model = BlogContent
    template_name = 'blog/post_details.html'


class PostListByTagView(PostListViews):
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return BlogContent.objects.filter(tags__slug=slug)
