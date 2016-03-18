from django.shortcuts import render

from blog.models import BlogPost


def index(request):
    posts = BlogPost.objects.all()
    return render(request, 'index.html', {'posts': posts})


def article(request, title):
    post = BlogPost.objects.get(title=title)
    return render(request, 'detail.html', {'post': post})
