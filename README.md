# 写给妹子的简明 Django 教程

今天的内容是熟悉 Django，学会快速用 Django 创建一个项目，并且借助 Django admin 实现一个简易的博客。
因为是讲过的内容，所以我就补充一下关键点，不重头开始了。

首先有下面这些命令需要清楚

```bash
django-admin startproject xxxx 创建项目

python manage.py startapp xxxx 创建应用

python manage.py migrate 数据库变更写入

python manage.py createsuperuser 创建超级管理员

python manage.py mkmigrations xxx 生成数据库预变更内容

python manage.py sqlmigrate xxx xxx 生成数据库预变更内容sql语句
```

然后是一些知识点

首先是路由的注册
路由分为项目的路由和应用的路由，其中应用的路由应该在项目的路由中引入，使之生效
路由匹配使用的是正则表达式，可以捕获参数，当作额外参数传递给对应的函数
为了避免写死地址，在模板里可以使用反向路由(reverse url resolution)

然后是 model 的定义
因为 django 内置了 orm，所以使用起来非常方便。就是定义 field，然后创建查询什么的很简单就不说了
这里需要提一下的是`python manage.py shell`可以进入交互模式，在这里可以用终端来操作 model(当然不限于此)

其次是试图层(view)
这里面写的是业务逻辑，也是跟其他组件(model，route)关联非常紧密的地方。第一天只讲了普通的定义函
数的方法，但是 Django 本身还内置了一些类可以用，以后有机会提。或者也可以自己看下文档。

最后是模板(templates)
因为有了模板才有了现代我们看到的网页（这么说其实不准确，在现在前后端分离的背景下，很多时候后端都是
直接通过 Ajax 输出 json 或 xml 给前台，在前端做页面的渲染展示）
模板有对应的模板语言，Django 的模板语言还蛮简单，可以看看，什么`for if else`等等，还有一个叫过滤器的东
西，可以自学看看。
模板的设计实际有一点考前端的感觉，因为模板需要尽可能的写成可复用的组件，避免重复劳动。
