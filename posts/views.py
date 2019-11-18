from django.shortcuts import render
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from users.models import User


class PostListView(ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(is_active=True).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pageName'] = "The Latest Posts"
        return ctx


def post_detail(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        new_comment = Comment.objects.create(post=post, author=request.user, content=request.POST['content'])
        comments = Comment.objects.filter(post=post).order_by('-date_posted')
    else:
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post).order_by('-date_posted')

    return render(request, 'posts/post_detail.html', context={'object': post, 'comments': comments})


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    titleView = 'Create Post'
    buttonView = 'Create'
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        if self.request.user.is_staff or self.request.user.is_editor:
            form.instance.is_active = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titleView'] = self.titleView
        ctx['buttonView'] = self.buttonView
        return ctx
    


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    titleView = 'Update Post'
    buttonView = 'Update'
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titleView'] = self.titleView
        ctx['buttonView'] = self.buttonView
        return ctx

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    titleView = 'Delete Post'
    buttonView = 'Delete'
    template_name = 'posts/post_delete.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titleView'] = self.titleView
        ctx['buttonView'] = self.buttonView
        return ctx

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-date_posted')
    return render(request, 'posts/myposts.html', context={'posts':posts, 'pageName': 'My Posts'})
