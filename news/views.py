from .models import News, NewsComment
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'newses'
    ordering = ['-posted_on']


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'news/news_form.html'
    fields = ['headline', 'content', 'thumbnail']
    login_url = '/userdetail/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_news', args=(self.object.id,))


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = News.objects.get(pk=self.kwargs['pk'])

        is_liked = news.likes.filter(id=self.request.user.id).exists()
        is_disliked = news.dislikes.filter(id=self.request.user.id).exists()

        context['comments'] = NewsComment.objects.filter(
            news=news)
        context['user'] = self.request.user
        context['total_likes'] = news.total_likes()
        context['total_dislikes'] = news.total_dislikes()
        context['is_liked'] = is_liked
        context['is_disliked'] = is_disliked

        return context


class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    template_name = 'news/news_form.html'
    fields = ['headline', 'content', 'thumbnail']
    login_url = '/userdetail/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author


class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = '/news/'
    login_url = '/userdetail/login/'

    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author


def newsComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        newsID = request.POST.get("newsID")
        news = News.objects.get(id=newsID)
        parentID = request.POST.get("parentID")

        if parentID == "":
            comment = NewsComment(
                comment=comment,
                user=user,
                news=news
            )
        else:
            parent = NewsComment.objects.get(id=parentID)
            comment = NewsComment(
                comment=comment,
                user=user,
                news=news,
                parent=parent
            )

        comment.save()

    return redirect(f'/news/news/{newsID}/')


def likeView(request, pk):
    news = News.objects.get(pk=pk)

    if news.likes.filter(id=request.user.id).exists():
        news.likes.remove(request.user)
        is_liked = False
    else:
        news.likes.add(request.user)
        news.dislikes.remove(request.user)
        is_liked = True
        is_disliked = False

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def dislikeView(request, pk):
    news = News.objects.get(pk=pk)

    if news.dislikes.filter(id=request.user.id).exists():
        news.dislikes.remove(request.user)
        is_disliked = False
    else:
        news.dislikes.add(request.user)
        news.likes.remove(request.user)
        is_disliked = True
        is_liked = False

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
