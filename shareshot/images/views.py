
from django.core import paginator
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .forms import ImageCreateForm
from common.decorators import ajax_required

from django.shortcuts import get_object_or_404
from .models import Image
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import redis
from django.conf import settings

from django.http import JsonResponse
from django.views.decorators.http import require_POST

#connect to redis
redi=redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)


@login_required
def image_create(request):

    if request.method=='POST':
        #form is sent
        form=ImageCreateForm(data=request.POST)
        if form.is_valid():
            #form data is valid
            cd=form.cleaned_data
            new_item=form.save(commit=False)

            #assign the image to user
            new_item.user=request.user
            new_item.save()
            messages.success(request,'Image added successfully')

            #redirect to new created item detail view
            return redirect(new_item.get_absolute_url())

    else:
            #build form with data provided via Bookmark GET
        form=ImageCreateForm(data=request.GET)
    context={'section':'images','form':form}
    return render(request,'images/image/create.html',context)   



def image_detail(request,id,slug):
    image=get_object_or_404(Image,id=id,slug=slug)
    #INCREMENT TOTAL IMAGE VIEWS BY 
    total_views=redi.incr('image:{}:views'.format(image.id))
    context={'section':'images','image':image,'total_views':total_views}
    return render(request,'images/image/detail.html',context)  

        
@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id  =request.POST.get('id')
    action    =request.POST.get('action')
    if image_id and action:
        try:
            image  =Image.objects.get(id=image_id)
            if action=='like':
                image.users_like.add(request.user)
                
            else:
                image.users_like.remove(request.user)

            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})   


@login_required
def image_list(request):
    images=Image.objects.all()
    paginator=Paginator(images,30)
    page=request.GET.get('page')

    try:
        images=paginator.page(page)

    except PageNotAnInteger:
        #if page is not an integer deliver there first page
        images=paginator.page(1)

    except EmptyPage:
        if request.is_ajax():
            #if the request is AJAX and the page is out of the range
            # return an empty page
            return HttpResponse('')


            #if page is out of range deliver last page of results
            images=paginator.page(paginator.num_pages)


    if request.is_ajax():
        context={'section':'images','images':images}
        return render(request,'images/image/list_ajax.html',context)

    context={'section':'images','images':images}
    return render(request,'images/image/list.html',context)                    




 

