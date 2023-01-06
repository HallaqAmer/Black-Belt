from django.urls import path
from . import views

app_name = 'pypieapp'

urlpatterns = [
    path('', views.display_dashboard, name="home"),
    path('addpie', views.add_pypie, name="add"),
    path('pypies/list', views.display_list, name="list"),
    path('logout', views.logout_user, name="user_logout"),
    path('edit/<int:id>', views.edit_pie_page, name="edit"),
    path('editpie', views.make_edit_pie, name="editpie"),
    path('delete/<int:id>', views.delete_pie, name="delete"),
    path('show/<int:id>', views.display_pie, name="pie_info"),
    path('vote/<int:id>', views.add_vote, name="vote"),
    
]