# 写给妹子的简明 Django 教程

今天的课程内容比较轻松，主要就是把昨天的博客稍微加一些三方的组件。

比如评论和 rss 订阅

首先来说一下评论，这里说的评论是指我们平时看别人博客时，文章下方的那个讨论区。我所知道的比较有名的第三方评论系统有 disqus 和多说，他们都支持多帐号登录，和 sns 分享。其中多说可能更适合国内环境一些。
所以我们接下来就以往昨天的系统中加入多说评论为目的
首先，先去 http://duoshuo.com 的官网上注册一个帐号，获取一段通用代码，类似于这样的

```js
<!-- 多说评论框 start -->
	<div class="ds-thread" data-thread-key="请将此处替换成文章在你的站点中的ID" data-title="请替换成文章的标题" data-url="请替换成文章的网址"></div>
<!-- 多说评论框 end -->
<!-- 多说公共JS代码 start (一个网页只需插入一次) -->
<script type="text/javascript">
var duoshuoQuery = {short_name:"halfcrazy"};
	(function() {
		var ds = document.createElement('script');
		ds.type = 'text/javascript';ds.async = true;
		ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//static.duoshuo.com/embed.js';
		ds.charset = 'UTF-8';
		(document.getElementsByTagName('head')[0] 
		 || document.getElementsByTagName('body')[0]).appendChild(ds);
	})();
	</script>
<!-- 多说公共JS代码 end -->

```

这里 halfcrazy 是我。你的需要改成你自己的，接着将这段 js 代码贴到你的文章详情页的模板中，主要这里面几处中文说明，
请将此处替换成文章在你的站点中的 ID 这个东西是这篇文章在我们系统中的 id，我们可以直接用 post.id 来访问到。
请替换成文章的标题 这个就是换成自己的标题
请替换成文章的网址 这里需要用到昨天说过的反向路由的方法来获取到这个地址
操作完成后保存刷新即可，非常简单。


接下来说导出 rss 功能，
rss 的定义可以查看 wiki 上的说明（https://zh.wikipedia.org/wiki/RSS）， 一般会用于邮件订阅文章更新用。
直接进入主题,由于 rss 输出也是需要挂载路由的，所以我们需要中 urls.py 文件中注册这个 rss 的地址。
因为我们输出的 rss 也就是我们的文章，这里不用额外修改定义模型，只需要直接输出这个文章即可。
Django 本身为我们提供了现成的工具来帮助我们格式化文章成 rss，参照 https://docs.djangoproject.com/en/1.9/ref/contrib/syndication/  这里的说明，我们只需要定义一个类，继承于 Feed 即可。
