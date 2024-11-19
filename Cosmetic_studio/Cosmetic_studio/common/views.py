from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, 'common/index.html')



def edit_profile(request):
    return render(request, 'user/edit_profile.html')


def delete_profile(request):
    return render(request, 'user/delete_profile.html')
