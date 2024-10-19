from django.shortcuts import get_object_or_404, render

from django.utils import timezone

from blog.models import Category, Post

from .constants import POST_QUANTITY


def posts():
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )


def index(request):
    return render(
        request,
        "blog/index.html",
        {'post_list': posts()[:POST_QUANTITY]},
    )


def post_detail(request, id: int):
    post = get_object_or_404(posts(), id=id,)
    return render(request, "blog/detail.html", {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )

    return render(request,
                  "blog/category.html",
                  {'category': category,
                   'post_list': posts().filter(category=category)})
