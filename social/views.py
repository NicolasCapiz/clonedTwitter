from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import UserRegisterForm,PostForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def feed(request):
    posts = Post.objects.all()  
    context = {'posts':posts}
    return render(request,'social/feed.html',context)

@login_required
def post(request):
    #current_user obtengo el usuario que esta logueado
    #get_object_or404 se asegura de mandar un mensaje si no se encuentra el usuario
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method=='POST':
	    form = PostForm(request.POST)
	    if form.is_valid():
		    post = form.save(commit=False)
		    post.user = current_user
		    post.save()
		    messages.success(request, 'Tweet enviado')
		    return redirect('feed')
    else:
	    form = PostForm()
    return render(request, 'social/post.html', {'form' : form })


def modificarPost(request,id):
    post = Post.objects.get(id=id)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form=PostForm(request.POST,instance=post) 
        if form.is_valid():
            form.save()
            return redirect('feed')

    return render(request, 'social/modificarPost.html', {'form' : form })


def eliminarPost(request,id):
    post = Post.objects.get(id=id)
    if request.method=='POST':
        post.delete()
        return redirect('feed')
    return render(request,'social/eliminarpost.html',{'post':post})


def profile(request,username=None):
    #request.user me devuelve el usuario que estoy logueado
    current_user = request.user
    if username and username != current_user.username:
        #busca en la base de datos en el parametro username y lo compara con el username ingresado en la funcion
        user = User.objects.get(username=username)
        #en post cargamos todos los post de este usuario
        posts = user.posts.all()
    else:
        posts = current_user.posts.all()
        user = current_user
    return render(request, 'social/profile.html',{'user':user,'posts':posts})



def follow(request,username):
    #request.user = usuario logueado
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user=to_user_id)
    rel.save()
    messages.success(request, f'sigues a {username}')
    return redirect('feed')


def unfollow(request,username):
    #request.user = usuario logueado
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    #buscamos la relacion entre los dos usuarios y la eliminamos
    rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
    rel.delete()
    messages.success(request, f'Ya no sigues a @{username}')
    return redirect('feed')


def register(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST,request.FILES)
        if form.is_valid():
            #guardamos el usuario cuando se registra
            form.save()
            username = form.cleaned_data['username']
            messages.success(request,f'Usuario {username} creado')
            return redirect('feed')

    else:
        form = UserRegisterForm()
    context = {'form':form}
    
    return render(request,'social/register.html',context)






