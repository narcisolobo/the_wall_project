from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

import bcrypt

from .models import User, Message, Comment

def index(request):
    request.session['logged'] = False
    all_users = User.objects.all().values()
    context = {
        'users':all_users
    }
    return render(request, 'the_wall/index.html', context)

def process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pword = request.POST['password']
        hashed = bcrypt.hashpw(pword.encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first-name'], last_name=request.POST['last-name'], email=request.POST['email'], pwhash=hashed.decode())
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        request.session['logged'] = True
        messages.success(request, 'Successfully registered!')
        return redirect('/success')

def success(request):
    if request.session['logged'] == False:
        return redirect('/')
    elif request.session['logged'] == True:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user':user,
            }
        return render(request, 'the_wall/success.html', context)

def login(request):
    errors = User.objects.password_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        request.session['logged'] = True
        user = User.objects.get(email=request.POST['login-email'])
        request.session['user_id'] = user.id
        messages.success(request, 'Successfully logged in!')
        return redirect('/success')

def wall(request):
    all_messages = Message.objects.all()
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'all_messages':all_messages,
        'user':user,
    }
    return render(request, 'the_wall/wall.html', context)

def process_message(request):
    user = User.objects.get(id=request.session['user_id'])
    Message.objects.create(message_body=request.POST['message_from_form'], posted_by=user)
    return redirect('/wall')

def process_comment(request):
    user = User.objects.get(id=request.session['user_id'])
    message_parent = Message.objects.get(id=request.POST['message-parent-id'])
    Comment.objects.create(comment_body=request.POST['comment_from_form'], posted_by=user, message_parent=message_parent)
    return redirect('/wall')

def logout(request):
    request.session.clear()
    return redirect('/')