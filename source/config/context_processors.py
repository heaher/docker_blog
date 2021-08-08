from blog.models import Category, Tag,Post
from django.db.models import Count, Q

def common(request):
    context = {
        'post': Post.objects.all(),
        'categories': Category.objects.annotate(
            num_posts=Count('post')),
        'tags': Tag.objects.annotate(
            num_posts=Count('post')),
    }
    return context