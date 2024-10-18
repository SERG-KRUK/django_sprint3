from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
from datetime import datetime
from django.db.models import Q


def index(request):
    post_list = Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    )
    return render(
        request,
        "blog/index.html",
        {'post_list': post_list[:5]},
    )


def post_detail(request, id: int):
    posts = get_object_or_404(
        Post.objects.select_related(
            'category',
            'location',
            'author'
        ).exclude(
            Q(is_published=False) |
            Q(category__is_published=False) |
            Q(pub_date__gt=datetime.now())),
        id=id,
    )
    return render(request, 'blog/detail.html', {'post': posts})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = Post.objects.select_related(
        'category',
    ).filter(
        is_published=True,
        pub_date__lte=datetime.now(),
        category=category
    )
    context = {'category': category,
               'post_list': post_list}

    return render(request, "blog/category.html", context)
