from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from . import models, forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = models.Post

    # Field lookups
    def get_queryset(self):
        return models.Post.objects.filter(published_date__lte = timezone.now().order_by('-published_date'))

class PostDetailView(DetailView):
    model = models.Post

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = forms.PostForm
    model = models.Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = forms.PostForm
    model = forms.Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login/'
    success_url = reverse_lazy('blog:post_list')
    model = models.Post

class DraftListView(LoginRequiredMixin, ListView):
    login_url = 'login/'
    redirect_field_name = 'blog/post_list.html'
    model = models.Post

    def get_queryset(self):
        return models.Post.objects.filter(published_date__isnull = True).order_by('create_date')

###################################################

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(models.Post, pk = pk)
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk = post.pk)
        else:
            form = forms.CommentForm()
        return render(request, 'blog/comment_form.html', {'form' : form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(models.Comment, pk = pk)
    comment.approve()
    return redirect('blog:post_detail', pk = comment.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(models.Comment, pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail', pk = post_pk)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(models.Post, pk = pk)
    post.publish()
    return redirect('blog:post_detail', pk = pk)