from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse, get_object_or_404
from .models import Post
from .form import PostForm, PostFilterForm, CommentForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from . import isOwner


# Create your views here.


def form_example(request):
    # sent_message=request.GET.get('message')

    sent_message = None

    if request.method == 'POST':
        sent_message = request.POST.get('message')

    return render(request, 'post/form.html', context={'sent_message': sent_message})


def index(request):
    return HttpResponse("Merhaba Django")


@login_required(login_url='/users/login')
def post_create(request):
    if not request.user.is_authenticated:
        raise Http404

    post_form = PostForm()
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            created_post = post_form.save(commit=False)
            created_post.user = request.user
            created_post.save()
            print(created_post.slug)
            messages.success(request, 'Gönderi oluşturuldu')
            return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': created_post.slug}))

    return render(request, 'post/post_create.html', context={'form': post_form})


@login_required(login_url='/users/login')
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not isOwner(post, request.user):
        return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': post.slug}))

    form = PostForm(data=request.POST or None, files=request.FILES or None, instance=post)

    if form.is_valid():
        form.save(commit=True)
        messages.info(request, 'Gönderi güncellendi')
        return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': form.instance.slug}))
    return render(request, 'post/post_update.html', context={'form': form})


def post_list(request):
    page = request.GET.get('page', 1)

    q = request.GET.get('q', None)

    filter_form = PostFilterForm(request.GET or None)
    posts_list = Post.objects.all().order_by('-updated_date')

    if filter_form.is_valid():
        choice = filter_form.cleaned_data['choice']
        if choice == 'T':
            posts_list = posts_list.filter(draft=True).order_by('-updated_date')
        elif choice == 'TD':
            posts_list = posts_list.filter(draft=False).order_by('-updated_date')
    if q:
        posts_list = posts_list.filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(category__category_name__icontains=q))

    paginator = Paginator(posts_list, 3)

    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)

    return render(request, 'post/post_list.html', context={'post_list': posts_list, 'filter_form': filter_form})


@login_required(login_url='/users/login')
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        post.delete()
        return JsonResponse(data={'success':'Silindi'})

    if not isOwner(post, request.user):
        return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': post.slug}))
    post.delete()
    messages.error(request, 'Gönderi silindi')
    return HttpResponseRedirect(reverse('post_list'))


@login_required(login_url='/users/login')
def post_detail(request, slug):
    # post=Post.objects.get(pk=id)
    post = get_object_or_404(Post, slug=slug)

    comment_form = CommentForm(request.POST or None)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        comment_form = CommentForm()
        messages.success(request, 'Yorumunuz Kaydedildi')

    return render(request, 'post/post_detail.html', context={'post': post, 'form': comment_form})
