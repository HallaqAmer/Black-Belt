from django.db import models
from login_app.models import User
from django.db.models import Count


class PypieManager(models.Manager):
    def pypie_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if not postData['name']:
            errors["name"] = "This field is required"
        if not postData['filling']:
            errors["filling"] = "This field is required"
        if not postData['crust']:
            errors["crust"] = "This field is required"
        return errors
    def edit_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if not postData['name']:
            errors["name_edit"] = "All Fields are required"
        if not postData['filling']:
            errors["filling_edit"] = "All Fields are required"
        if not postData['crust']:
            errors["crust_edit"] = "All Fields are required"
        return errors

class Pypie(models.Model):
    name=models.CharField(max_length=255)
    filling=models.CharField(max_length=255)
    crust=models.CharField(max_length=255)
    added_by=models.ForeignKey(User, related_name='added_pies', on_delete=models.CASCADE)
    liked_by=models.ManyToManyField(User,related_name="liked_pies")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = PypieManager()

class Vote(models.Model):
    pie=models.ForeignKey(Pypie, related_name='voted_pies',on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User, related_name='voted_users',on_delete=models.CASCADE,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
def create_pie(postData,id):

    name=postData["name"]
    filling=postData["filling"]
    crust=postData["crust"]
    user=User.objects.get(id=id)
    new_pie=Pypie.objects.create(name=name,filling=filling,crust=crust,added_by=user)
    return new_pie

def get_user_pies(id):

    user=User.objects.get(id=id)
    user_pies=user.added_pies.all()
    return user_pies

def get_all_pies_ordered():
    
    pies=Pypie.objects.annotate(likes=Count('liked_by')).order_by('-likes')

    return pies

def add_vote(user_id,pie_id):

    user=User.objects.get(id=user_id)
    pie=Pypie.objects.get(id=pie_id)
    pie.liked_by.add(user)
    new_vote=Vote.objects.create(pie=pie,user=user)
    return new_vote


def remove_vote(user_id,pie_id):

    user=User.objects.get(id=user_id)
    pie=Pypie.objects.get(id=pie_id)
    if user in pie.liked_by.all():
        pie.liked_by.remove(user)


def delete_pie(id):
    pie=Pypie.objects.get(id=id)
    pie.delete()

def update_pie(postData,pie_id):

    pie=Pypie.objects.get(id=pie_id)
    pie.name=postData["name"]
    pie.filling=postData["filling"]
    pie.crust=postData["crust"]
    pie.save()
    return pie

def get_all_votes():
    votes=Vote.objects.all()
    return votes