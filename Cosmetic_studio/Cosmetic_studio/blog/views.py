from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from Cosmetic_studio.blog.forms import CreatePostForm
from Cosmetic_studio.blog.models import BlogContent


def blog(request):
    return render(request, 'blog/blog.html')


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


# class PostListViews(views.ListView):
#     model = BlogContent
#     template_name = 'blog/post_details.html'
#     paginate_by = 4
#     ordering = ['-created_at']
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['last_post'] = BlogContent.objects.last()
#         return context


class PostDetailView(views.DetailView):
    model = BlogContent
    template_name = 'blog/post_details.html'
