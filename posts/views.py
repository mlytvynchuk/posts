from django.shortcuts import render
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Post
from users.models import User
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
# Create your views here.

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


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    titleView = 'Create Post'
    buttonView = 'Create'
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        if self.request.user.is_staff:
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
