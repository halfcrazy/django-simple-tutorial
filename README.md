# 写给妹子的简明 Django 教程
2016.3.19的课

今天的内容是表单以及注册登录。
先前我们写博文是通过 Django 的 admin 后台直接创建 model 来实现的。
这次我们来自己实现一个用户的注册登录，以及博文的发布编辑删除功能。
这样，只有我们站点所有者自己登录之后才能操作文章，未登录用户就只可以浏览。


我们还是先来实现一套注册登录系统。非常爽的是 Django 本身为我们提供来一套组件来做这件事。
首先因为注册登录实际是有三部分组成，1）注册 2）登录 3）登出
所以我们还是需要先挂载三个基础路由来接受请求。

=================================下面是一堆的科普====================================

先说几个概念，首先是 http method，平时接触最多是 get 和 post 这两种。
我们通过浏览器打开的网页，比如说在浏览器中输入 www.baidu.com 那么浏览器首先发起的会是一个 get 请求.
打开火狐的开发者工具，点击网络，然后打开 www.baidu.com 你就会看到一系列的请求，忽略资源文件的那些，那么最开始就是一条 get / 请求。
get 请求可以通过 ?a1=xx&a2=xx 这种形式来传递参数，也就是说提交的数据会暴露在url里面，同时，使用 get 方法能传递的参数大小是有限制的，大概是2kb。


现在登录百度，注意看下面开发者工具里面的网络，你会发现，现在的请求变成了post，相比之前的get，post传递数据并不会暴露在url里面，而是会在请求的header中，点击params可以看到。
￼
和 http method 类似的还有 http status code
我列举几个常见的解释一下
200 请求成功
404 请求资源不存在
302 临时跳转
301 永久跳转
500 服务器内部错误
所有的http请求都会返回一个状态码

科普完毕，下面我们先来看一下，如何获取请求中传递过来的参数

在 写给女朋友的Django教程(1)-路由，模型，模板 中， 我们自定义的view方法，接受的第一个参数都是 request， 例如
```python
def index(request):
    posts = BlogPost.objects.all()
    return render(request, 'index.html', {'posts': posts})
```
request这个东西实际就是请求对象，我们可以通过访问它来取到这个请求相关的信息，我们来看下 request 里面都有什么东西
https://docs.djangoproject.com/en/1.9/ref/request-response/

还是有不少东西的，我们现在比较在意的有 request.method， request.GET，request.POST 这三个，其中method表示这是个什么样的请求是 GET 请求，还是 POST 请求，还是其他什么请求。 然后  request.GET 里面会是一个 querystring 的字典。request.POST也是类似，稍有区别的是，通过 POST 请求上传文件的时候，文件可能会在 request.FILES 里面。

请求说完了，再说一下响应。
之前在 写给女朋友的Django教程(1)-路由，模型，模板 中，我们的响应就是 HttpResponse 或者是 直接 render ...
其实我们返回时，还可以指定 header 中的内容，比如 status code， content-type等。


说到注册登录，还需要科普一个东西，那就是 cookie 和 session。
因为http请求是无状态的，所以为了辨别请求，就需要我们给请求加上标识，可以让后端服务器识别出来这个请求属于谁。
有两种常见的做法，
第一种是把身份标识放在url里面，相当于一个token，形如 www.baidu.com/?token=123
这样服务器就可以根据某种规则，使用这个token进行反查，找到对应的信息。
第二种是把身份标识放在header里面，通过header中的cookie字段来记录,cookie传递时的格式形如Cookie:a=1;b=2;c=3这样。Cookie设置时可以指定domain path 还要 expires。当客户端发起请求时，只有domain和path完全匹配了，这个请求才会带上本地的cookie发给服务端。

接下来科普最后一个东西，表单form
在html语言里面form长这个样
```html
<form action="http://xxxx/login" method="POST">
    <input name="username" type="text">
    <input name="password" type="password">
    <input type="submit" value="登录">
</form>
```
我们关注一下这个里面都有些什么，首先是form标签，它需要指定一个action，也就是表单的提交地址，这里是http://xxxx/login。然后是method，也就是提交的方法，这里是POST。在form里面还有3个input标签，前两个type为text和password的是会有两个输入框，最后那个submit是用来提交表单的按钮，不可以省掉。

=====================================科普完毕=============================================

必须要吐槽了，这节课太难备了。。。牵涉太多，你之前有没有听说过这些。。。如果之前什么都不知道的话，看完我的科普，很可能还是会蒙蔽，最好自己能再网上搜搜看了解一下。

那么切入正题，我们先来写两个视图，分别用来测试读取我们前台传过来的get和post的参数
```python
def test_get(request):
    print(request.GET)
    return HttpResponse(123)


def test_post(request):
    print(request.POST)
    return HttpResponse(123)
```

这里演示一下是可以取到的

现在我们来构想一个场景，用户要注册了，前端显示给他一个 用户名，密码的输入框，一个确认按钮。用户此时可以在输入框里随便写东西，但是我们后台却有做限制，比如密码需要6位以上，当然这个可以在前端通过js来限制一次，但是对于用户的模拟提交却是可以到达后端的，所以我们不论前端做不做限制，后端都需要有这么一个验证机制。
在我们接触现成的表单工具之前，我们大概会在业务逻辑里做这个验证，或者写一个中间层来验证。但是我们用来 Django 之后，就完全没必要自己来写这部分，而是可以直接借助 Django 提供给我们的表单工具来写表单。

暂时先跳过注册登录，我们先来写一个文章发布编辑的表单把,
之前我们定义文章模型的时候，它有三个字段，标题，内容，时间戳，其中时间戳这个字段为文章的创建时间，我们在model里面有设置默认值，所以这里可以省略。
那么我们的表单就至少需要有标题和正文这两个输入框。
我们可以写出如下所示的 form

```python
from django import forms


class PostForm(forms.Form):
    title = forms.CharField(label='标题',
                            max_length=200)
    body = forms.CharField(label='正文',
                           widget=forms.Textarea)

```

定义了 form 怎么使用呢，我理解的 form 可以做两件事。1）用来验证表单的数据 2）用来生成前端界面


验证数据应该是在view的业务逻辑中
```python
def new_article(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_post = BlogPost(title=cd['title'], body=cd['body'])
            new_post.save()
            return redirect('/')
        return redirect(reverse('blog:new_post'))
    else:
        form = PostForm()
        return render(request, 'post/new.html', {'form': form})
```

这里还有一种更好的办法，直接使用 Django 的 ModelForm
```python
class PostForm(forms.ModelForm):
    title = forms.CharField(label='标题',
                            max_length=200)
    body = forms.CharField(label='正文',
                           widget=forms.Textarea)

    class Meta:
        model = BlogPost
        fields = ('title', 'body')
```
解释一下，这里的 Meta 相当于做了一次 Form 和 Model 的绑定。

使用了 ModelForm 之后，view也可以重新写一下
```python
def new_article(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return redirect(reverse('blog:new_post'))
    else:
        form = PostForm()
        return render(request, 'post/new.html', {'form': form})
```

前端界面应该是在template的模板中
```html
{% extends "base.html" %}

{% block content %}
    <form action="" method="post">
        {% csrf_token %}
        {{ form.as_p  }}
        <input type="submit" value="创建">
    </form>
{% endblock %}
```

这里还有一种更方便的做法，直接使用 Django 的 FormView，这个 view 做的事就是我们上面view中写的那些。它的写法是
```python
class NewArticle(FormView):
    template_name = 'post/new.html'
    form_class = PostForm
    success_url = '/'
```
如果为说还有一种更方便的你信不信，不要打我
```python
class NewArticle(CreateView):
    model = BlogPost
    fields = ['title', 'body']
    template_name = 'post/new.html'
```

还记得我们之前访问我们的某一篇文章是怎么进入的么？我们是通过路由捕捉到文章的标题来找到具体的文章的，当时那里埋了一个小坑，我们没有在model层限制文章的标题唯一，所以我们这里来对model稍作修改，把 `title = models.CharField(max_length=200)` 改成 `title = models.CharField(max_length=200, unique=True)` 保存并做一次数据库迁移。需要注意的是因为是新增加了约束，所以迁移之前请务必确保数据库中原本内容不存在冲突。否则迁移会失败。
现在文章的创建就做好了，接下来做一个文章的编辑界面，文章的编辑界面跟文章的创建界面很像，只是编辑的时候内容都是写好了的。
编辑文章当然首先需要找到这篇文章，那么我们就根据具体单页应用的来修改一下。
路由就叫 `^/article/xxxxx/edit$`
```python
class UpdateArticle(UpdateView):
    model = BlogPost
    fields = ['title', 'body']
    template_name = 'post/edit.html'

    def get_object(self):
        return BlogPost.objects.get(title=self.kwargs.get('title'))
```

删除的话，暂时不用写界面，就直接给一个路由访问到就删除就好了。。
当然实际产品中肯定不能这么搞，如果随便访问一个地址就能删除那就太恐怖了。一般都会限制一下作者，或者管理员才可以删除。
我们接下来就做一下用户的注册登录，为了省事。我就不新建model了，直接用django的admin model。
这里要用到 django 的 `from django.contrib.auth.forms import AuthenticationForm, UserCreationForm`
后面就直接看代码吧
