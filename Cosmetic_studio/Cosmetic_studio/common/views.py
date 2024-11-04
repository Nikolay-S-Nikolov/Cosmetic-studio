from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, 'common/index.html')


def login(request):
    return render(request, 'user/login.html')


def signup(request):
    return render(request, 'user/signup.html')


def signout(request):
    # logout(request)
    return render(request, 'user/signout.html')


def profile_details(request):
    return render(request, 'user/profile_details.html')


def edit_profile(request):
    return render(request, 'user/edit_profile.html')


def delete_profile(request):
    return render(request, 'user/delete_profile.html')
