from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import render

from blog.models import BlogPost


def index(request):
    posts = BlogPost.objects.all()
    return render(request, 'index.html', {'posts': posts})


def article(request, title):
    post = BlogPost.objects.get(title=title)
    return render(request, 'detail.html', {'post': post})


class LatestEntriesFeed(Feed):
    title = "Feeds"
    link = "/feed/"
    description = "Show lastest posts"

    def items(self):
        return BlogPost.objects.order_by('-timestamp')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return reverse('blog:detail_post', args=[item.title])
