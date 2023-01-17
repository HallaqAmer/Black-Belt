from django.shortcuts import render,redirect
from . import models
from . models import Pypie,Vote
from login_app.models import User
from django.contrib import messages


def display_dashboard(request):
    if not "userid"  in request.session:
        return redirect('/')
    user_id=request.session["userid"]
    user_pies=models.get_user_pies(user_id)

    context = {
        "user_pies": user_pies
    }

    return render(request,"home.html",context)

def add_pypie(request):
    if not "userid"  in request.session:
        return redirect('/')
    request.session["type"] = request.POST['which_from']
    if request.method=="POST":
        errors = Pypie.objects.pypie_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/dashboard")
        else:
            user_id=request.session["userid"]
            models.create_pie(request.POST,user_id)
            return redirect("/dashboard")

def display_list(request):
    if not "userid"  in request.session:
        return redirect('/')
    pies= models.get_all_pies_ordered()
    context= {
        "pies": pies
    }

    return render(request,"pypies_list.html",context)

def edit_pie_page(request,id):

    if not "userid"  in request.session:
        return redirect('/')
    pie=Pypie.objects.get(id=id)
    request.session["pieid"]=id
    context = {
        "pie": pie,
    }
    return render(request,"pie_edit.html",context)

def make_edit_pie(request):

    if not "userid"  in request.session:
        return redirect('/')
    pie_id=str(request.session["pieid"])
    errors = Pypie.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/dashboard/edit/"+pie_id)
    else:
        models.update_pie(request.POST,pie_id)
        return redirect("/dashboard")

def delete_pie(request,id):

    if not "userid"  in request.session:
        return redirect('/')
    models.delete_pie(id)
    return redirect("/dashboard")


def display_pie(request,id):

    if not "userid"  in request.session:
        return redirect('/')
    user_id=request.session["userid"]
    logged_user=User.objects.get(id=user_id)
    pie=Pypie.objects.get(id=id)
    vote=Vote.objects.filter(user=logged_user,pie=pie)
    context = {
        "pie": pie,
        "logged_user": logged_user,
        "vote": vote,
    }
    return render(request,"pie_info.html",context)

def add_vote(request,id):

    if not "userid"  in request.session:
        return redirect('/')
    user_id=request.session["userid"]
    pie_id=id
    models.add_vote(user_id,pie_id)
    return redirect("/dashboard/pypies/list")

def remove_vote(request,id):

    if not "userid"  in request.session:
        return redirect('/')
    user_id=request.session["userid"]
    pie_id=id
    models.remove_vote(user_id,pie_id)
    return redirect("/dashboard/pypies/list")




def logout_user(request):

    if not "userid"  in request.session:
        return redirect('/')
    del request.session['userid']
    del request.session['name']
    del request.session['email']
    
    return redirect('/')
