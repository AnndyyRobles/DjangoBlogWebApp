from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .email_form import EmailPostForm
from .comment_form import CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity

# class PostListViews(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'
def post_search(request):
    form = SearchForm()
    query = None
    results =[]
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query, 'spanish')


            results = Post.published.annotate(similarity = TrigramSimilarity('title', query),).filter(similarity__gt = 0.1).order_by('-similarity')
    return render(request, 'blog/post/search.html', {'form' : form, 'query' : query, 'results' : results})

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # set amount of objects per page to 3
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)

    except PageNotAnInteger:
        posts = paginator.page(1)

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    

    return render(request,
        'blog/post/list.html', {'posts': posts, 'tag' : tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status = Post.Status.PUBLISHED, slug = post, publish__year = year, publish__month = month, publish__day = day)
    #comments that are active in this post
    comments = post.comments.filter(active = True)
    form =  CommentForm()

    #List od similar to comment
    post_tags_ids = post.tags.values_list('id', flat = True)
    similar_posts = Post.published.filter(tags__in = post_tags_ids).exclude(id = post.id)
    similar_posts= similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post' : post, 'comments' : comments, 'form' : form, 'similar_posts' : similar_posts})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment=None
    #a comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html',{'post' : post, 'form' : form, "comment" : comment})
