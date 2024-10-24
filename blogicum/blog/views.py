from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Category, Post
from .constants import POST_QUANTITY


def posts_filtered_publications(posts_queryset):
    posts_queryset = posts_queryset.select_related(
        'author', 'location', 'category').filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )
    return posts_queryset


def index(request):
    return render(
        request,
        'blog/index.html',
        {'post_list': posts_filtered_publications(
            Post.objects.all())[:POST_QUANTITY]},
    )


def post_detail(request, id: int):
    post = get_object_or_404(posts_filtered_publications(
        Post.objects.all()), id=id,)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )

    post_list = posts_filtered_publications(category.posts.all())

    return render(request,
                  'blog/category.html',
                  {'category': category,
                   'post_list': post_list})
