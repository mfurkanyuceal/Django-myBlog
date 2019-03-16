from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from .forms import *
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from post.models import Post


# Create your views here.


def user_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('post_list'))

    form = RegisterForm(request.POST or None)

    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        isCompetent = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

        if isCompetent:
            login(request, new_user)
            return HttpResponseRedirect(reverse('post_list'))

    return render(request, 'user/register.html', context={'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('post_list'))

    next = request.GET.get('next', None)
    form = LoginForm(request.POST or None)
    if form.is_valid():
        next = request.POST.get('next', None)
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            if next != 'None':
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse('post_list'))
        else:
            error_message = 'Kullanıcı adı veya parola hatalı!'
            return render(request, 'user/login.html',
                          context={'form': form, 'next': next, 'error_message': error_message})
    return render(request, 'user/login.html', context={'form': form, 'next': next})


@login_required(login_url='/users/login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


@login_required(login_url='/users/login')
def user_edit_profile(request):
    data = {
        'sex': request.user.userprofile.sex,
        'biography': request.user.userprofile.biography,
        'birth_date': request.user.userprofile.birth_date,
        'phone': request.user.userprofile.phone
    }

    user_profile_form = UserProfileForm(request.POST or None, instance=request.user, initial=data)

    if request.method == "POST":
        if user_profile_form.is_valid():
            user_profile_form.save(commit=True)

            biography = user_profile_form.cleaned_data['biography']
            phone = user_profile_form.cleaned_data['phone']
            birth_date = user_profile_form.cleaned_data['birth_date']
            sex = user_profile_form.cleaned_data['sex']

            request.user.userprofile.sex = sex
            request.user.userprofile.biography = biography
            request.user.userprofile.birth_date = birth_date
            request.user.userprofile.phone = phone
            request.user.userprofile.save()

        messages.success(request, 'Kullanıcı bilgileriniz güncellendi')
        return HttpResponseRedirect(reverse('post_list'))

    return render(request, 'user/user_edit_profile.html', context={'form': user_profile_form})


@login_required(login_url='/users/login')
def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    post_list = Post.objects.filter(user=user)
    return render(request, 'user/user_profile.html', context={'post_list': post_list})


@login_required(login_url='/users/login')
def user_change_password(request):
    form = UserPasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Parolanız güncellendi!')
        else:
            messages.error(request, 'Lütfen alanları doğru doldurunuz!')

    return render(request, 'user/change_password.html', context={'form': form})


def user_upload_photo(request):
    if request.method == 'POST':
        form = UserProfilePhotoForm(instance=request.user.userprofile, data=request.POST, files=request.FILES)
        if form.is_valid():
            userprofile = form.save(commit=True)
            data = {'is_valid': True, 'image_url': userprofile.profile_photo.url,
                    'success': 'Profil Fotoğrafı Güncellendi'}
            return JsonResponse(data=data)
        else:
            return JsonResponse(data={'is_valid': False})
    else:
        return HttpResponseRedirect(reverse('user/user_edit_profile.html'))
