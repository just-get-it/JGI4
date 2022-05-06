from django.shortcuts import render, redirect 
from django.http import HttpResponseRedirect
from blogs.models import *
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
# Create your views here.

def archbase(request):
    return render(request, 'archplan/home.html')

def about(request):
    return render(request, 'archplan/about.html')

def services(request):
    return render(request, 'archplan/services.html')

def projects(request):
    return render(request, 'archplan/projects.html')

def gallery(request):
    return render(request, 'archplan/gallery.html')

def contact(request):
    return render(request, 'archplan/contact.html')

def blog(request):
    posts = Post.objects.all()
    return render(request, 'archplan/blog.html', {'posts':posts})

def blog_detail(request, slug):
    post = Post.objects.get(slug=slug)
    return render (request, 'archplan/blog_detail.html', {'post':post})

# Copied from blogs/views.py

class PostListView(ListView):
    model = Post
    template_name = 'archplan/blog.html'
    context_object_name = 'posts'
    ordering = ['-posted_on']

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blogs/post_form.html'
    fields = ['title', 'content', 'thumbnail']
    login_url = '/userdetail/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        print(form.instance.author)
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'archplan/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['pk'])

        is_liked = post.likes.filter(id=self.request.user.id).exists()
        is_disliked = post.dislikes.filter(id=self.request.user.id).exists()
        # is_disliked = False

        context['comments'] = BlogComment.objects.filter(
            post=post)
        context['user'] = self.request.user
        context['total_likes'] = post.total_likes()
        context['total_dislikes'] = post.total_dislikes()
        context['is_liked'] = is_liked
        context['is_disliked'] = is_disliked

        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blogs/post_form.html'
    fields = ['title', 'content', 'thumbnail']
    login_url = '/userdetail/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'archplan/blog_delete.html'
    success_url = '/archplan/'
    login_url = '/userdetail/login/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postID = request.POST.get("postID")
        post = Post.objects.get(id=postID)
        parentID = request.POST.get("parentID")

        if parentID == "":
            comment = BlogComment(
                comment=comment,
                user=user,
                post=post
            )
        else:
            parent = BlogComment.objects.get(id=parentID)
            comment = BlogComment(
                comment=comment,
                user=user,
                post=post,
                parent=parent
            )

        comment.save()

    return redirect(f'/archplan/blog/{postID}/')


def likeView(request, pk):
    post = Post.objects.get(pk=pk)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        post.dislikes.remove(request.user)
        is_liked = True
        is_disliked = False

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def dislikeView(request, pk):
    post = Post.objects.get(pk=pk)

    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        is_disliked = False
    else:
        post.dislikes.add(request.user)
        post.likes.remove(request.user)
        is_disliked = True
        is_liked = False

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))