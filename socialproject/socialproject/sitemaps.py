from django.contrib.sitemaps import Sitemap
from posts.models import Post
from django.urls import reverse

class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    # def location(self,obj):
    #     return '/blog/%s' % (obj.pk)

class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return ['home', 'about', 'contact']

    def location(self, item):
        return reverse(item)
