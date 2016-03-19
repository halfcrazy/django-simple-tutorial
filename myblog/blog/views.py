from django.views import generic
from django.http import Http404

from blog.models import BlogPost


class IndexView(generic.ListView):
    model = BlogPost
    template_name = 'index.html'

    def get_queryset(self):
        return BlogPost.objects.order_by('-timestamp')


class DetailView(generic.DetailView):
    model = BlogPost
    template_name = 'detail.html'

    def get_object(self, **kwargs):
        title = self.kwargs.get('title')
        try:
            article = BlogPost.objects.get(title=title)
        except BlogPost.DoesNotExist:
            raise Http404("Article does not exist")
        return article
