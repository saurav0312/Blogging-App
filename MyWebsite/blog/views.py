from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from .forms import PostForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer


def home(request):
    context={
        'posts':Post.objects.all(),
        'title':'Home'
    }
    return render(request,'blog/home.html',context)


def like_post(request):
    post=get_object_or_404(Post,id=request.POST.get('post_id'))
    if post.liked_by.filter(id=request.user.id).exists():
        post.like -= 1
        post.liked_by.remove(request.user)
    else:
        post.like += 1
        post.liked_by.add(request.user)
    post.save()
    context = {
        'posts': Post.objects.all().order_by('-date_posted'),
        'title': 'Home'
    }
    return render(request, 'blog/home.html', context)

    #return HttpResponseRedirect(post.get_absolute_url())


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    #paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','image','content']
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','image','content']
    #success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request,'blog/about.html',{'title':'About'})



#/posts/
class PostList(APIView):

    def get(self,request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)


    def post(self):
        pass






def post_new(request):
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect('post-detail',pk=post.pk)
    else:
        form=PostForm()
    return render(request,'blog/post_create.html',{'form':form})


def post_edit(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=PostForm(request.POST,instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect('post-detail',pk=post.pk)
    else:
        form=PostForm(instance=post)
    return render(request,'blog/post_create.html',{'form':form})



