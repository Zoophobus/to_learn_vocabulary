from django.urls import path,include
from . import views

urlpatterns = [
        path('',views.index,name='index'),
        path('add/',views.add,name='add'),
#        path('add_two/',views.add_two,name='add_two'),
        path('options/',views.options,name='options'),
        path('start_learning/',views.Learn.as_view,name='learn'),
        path('test/',views.Test.as_view,name='test'),
        path('delete/',views.delete,name='delete'),
        path('group/',views.group,name='group'),
        ]
