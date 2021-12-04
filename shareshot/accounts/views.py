import json
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm,UserEditForm,ProfileEditForm
from .models import Profile

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact

@login_required
def dashboard(request):
    context={'section':dashboard}
    return render(request,'account/dashboard.html',context)
def register(request):
    if request.method=='POST':
        user_form=UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #create a new user object but avoid saving it
            new_user=user_form.save(commit=False)
            #set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            #save the object
            new_user.save()
            #create the user profile
            Profile.objects.create(user=new_user)

            context={'new_user':new_user}
            return render(request,'account/register_done.html',context)
    else:
        user_form=UserRegistrationForm()
    context={'user_form':user_form}    
    return render(request,'account/register.html',context)       

@login_required
def edit(request):
    if request.method=='POST':
        user_form=UserEditForm(instance=request.user,data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form=UserEditForm(instance=request.user)  
        profile_form=ProfileEditForm(instance=request.user.profile)  

    context={'user_form':user_form,'profile_form':profile_form}
    return render(request,'account/edit.html',context)      


@login_required
def user_list(request):
    users=User.objects.filter(is_active=True)
    context={'section':'people','users':users}
    return render(request,'account/user/list.html',context)   

def user_detail(request,username):
    user=get_object_or_404(User,username=username,is_active=True)
    context={'section':'people','user':user}
    return render(request,'account/user/detail.html',context)       


@login_required
def dashboard(request):
    users=User.objects.filter(is_active=True)
    context={'section':'dashboard','users':users}
    return render(request,'account/dashboard.html',context) 


 
    

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id=request.POST.get('id')
    action=request.POST.get('action')
    if user_id and action:
        try:
            user=User.objects.get(id=user_id)
            if action=='follow':
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})