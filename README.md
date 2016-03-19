# 写给妹子的简明 Django 教程

在 写给女朋友的Django教程(1)-路由，模型，模板 中，曾经提到过 Django 有为我们提供了几种 view 来简化我们的开发。

这节我们来说一下

首先是 ListView（文档见 https://docs.djangoproject.com/en/1.9/ref/class-based-views/generic-display/#django.views.generic.list.ListView）

ListView可以认为是一个可以根据某种规则取出一组对象的视图，参照官方示例来看
```python
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
```

根据 Django 的约定， ListView 默认使用的模板是 <app name>/<model name>_list.html，这里我们可以指定template_name来使用自己写的模板，默认传入到模板中的对象列表名叫 <model name>_list 同样，我们可以通过指定 context_object_name 来自定义。这个 View 默认的行为是返回所有的指定模型的对象， 我们可以通过覆写 get_queryset 方法来指定我们想返回那些，相当于可以做一个过滤。


其次是 DetailView（文档见 https://docs.djangoproject.com/en/1.9/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView）

DetailView可以认为是一个根据主键取出某一个对象的视图，官方示例如下
```python
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
```
类似于上面说到的 ListView， DetailView 默认使用的模板是 <app name>/<model name>_detail.html， 我们同样可以自定义方法如上。传入模板的对象默认叫 object，我们可以自定义方法如上。
DetailView 有一点不同的就是，因为这个 View 是取的一个对象，它是根据路由传进来的参数进行查找的，默认是通过主键查找对应的模型中的那个对象。

然后还要修改一下的就是我们的urls.py这个文件，
```python
url(r'^$', views.IndexView.as_view(), name='index'),
url(r'^article/(?P<title>\w+)$', views.DetailView.as_view(), name='detail_post'),
```
我们之前urls这里写的是views里面的方法，现在使用来通用view之后，我们需要修改成 xxx.as_view()这样的形式
