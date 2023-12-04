from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .models import User, Sighting
import bcrypt
from time import localtime, strftime
from datetime import datetime

def root(request):
    
    return render(request, 'index.html')


def user_processing(request):
    if request.POST['which_form'] == 'Register':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0 :
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hash_pass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            User.objects.create(first_name = request.POST['first_name'],last_name = request.POST['last_name'],email_address = request.POST['email_address'],password = hash_pass)
            request.session['login_id'] = User.objects.last().id
            messages.success(request, "User created Successfully")
            return redirect('/dashboard')


    elif request.POST['which_form'] == 'login':
        if not User.objects.filter(email_address = request.POST['email_address']):
            messages.error(request, "Account doesnt exist")
            return redirect('/')
        
        else:
            if bcrypt.checkpw(request.POST['password'].encode(), User.objects.get(email_address = request.POST['email_address']).password.encode()):
                request.session['login_id'] = User.objects.get(email_address = request.POST['email_address']).id
                return redirect('/dashboard')

            else:
                messages.error(request, "password is not correct")
                return redirect('/')

def user_dashboard(request):
    content = {
        'current_user' : User.objects.get(id = request.session['login_id']),
        'sightings' : Sighting.objects.all().order_by('-date'),
        }

    return render(request,'dashboard.html',content)

def new_sighting(request):
        content = {
            'current_user' : User.objects.get(id = request.session['login_id'])
        }
        return render(request, 'new.html',content)
    
def add_sighting(request):
    errors = Sighting.objects.basic_validator(request.POST)
    if len(errors) > 0 :
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/sightings/new')
    else:
        location = request.POST['location']
        date = request.POST['date']
        number = request.POST['number']
        desc = request.POST['desc']
        my_user = User.objects.get(id = request.session['login_id'])
        new_sighting = Sighting.objects.create(location = location, date = date, number = number, desc = desc, my_user = my_user)
        content = {
            'sightings' : Sighting.objects.all(),
            'current_user' : my_user
        }
        return redirect('/dashboard')

def details(request,id):
    my_user = User.objects.get(id = request.session['login_id'])
    sighting = Sighting.objects.get(id = id)
    content = {
        'sighting' : sighting,
        'current_user' : my_user
    }
    return render(request,'view.html',content)

def edit_form(request, id):
    sighting = Sighting.objects.get(id = id)
    my_user = User.objects.get(id = request.session['login_id'])
    content = {
        'sighting' : sighting,
        'current_user' : my_user
    }
    return render(request, 'edit.html',content)

def edit_process(request, id):
    description = Sighting.objects.get(id = id).desc
    errors = Sighting.objects.basic_validator(request.POST)
    if len(errors) > 0 :
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/sightings/edit/{id}')
    else:
        sighting = Sighting.objects.get(id = id)
        sighting.location = request.POST['location']
        sighting.date = request.POST['date']
        sighting.number = request.POST['number']
        if request.POST['desc'] == '':
            sighting.desc = description
        else:
            sighting.desc = request.POST['desc']

        sighting.save()

        return redirect(f'/sightings/{id}')
    
def logout(request):
    request.session.flush()
    return redirect('/')

def add_skeptic(request,id):
    user = User.objects.get(id = request.session['login_id'])
    sighting = Sighting.objects.get(id = id)
    if request.POST['which_form'] == 'add':
        sighting.skeptic.add(user)

    elif request.POST['which_form'] == 'remove':
        sighting.skeptic.remove(user)
    return redirect(f'/sightings/{id}')

def delete(request, id):
    sighting = Sighting.objects.get(id = id)
    if sighting.my_user == User.objects.get(id = request.session['login_id']):
        sighting.delete()
    return redirect('/dashboard')
