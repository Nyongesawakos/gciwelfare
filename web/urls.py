from django.urls import path
from . import views 
from .views import change_password
from django.views.generic import TemplateView

urlpatterns = [    
path('login/', views.loginPage, name= 'login'),
path('user_list/', views.user_list, name= 'user_list'),
path('cashflow/', views.cashflow, name='cashflow'),
path('insert/', views.insert, name= 'insert'),
path('logout/', views.logoutUser, name= 'logout'),
path('register/', views.registerPage, name= 'register'),
path('', views.root, name='root'),
path('index/<str:pk>/', views.index, name='index'),
path('createRoom/', views.createRoom, name='createRoom'),
path('updateRoom/<str:pk>/', views.updateRoom, name='updateRoom'),
path('deleteRoom/<str:pk>/', views.deleteRoom, name='deleteRoom'),
path('cashflow/', views.cashflow, name='cashflow'),  
path('pdf/', views.pdf, name='pdf'),
path('detail/<str:pk>/', views.people, name='detail'),
path('Panel/', views.Panel, name='Panel'),
path('single/', views.single, name='single'),
path('members/', views.members, name='members'),
path('download-members-excel/', views.download_members_excel, name='download_members_excel'),
path('download-contributions-excel/',views.download_contributions_excel, name='download_contributions_excel'),
path('Message/', views.Message, name='Message'),
path('Msge/', views.Msge, name='Msge'),
path('gci/', views.gci_groups, name='gci'),
path('meso/', views.meso, name='meso'),
path('password/change/', change_password, name='password_change'),
path('password/change/done/', TemplateView.as_view(template_name='web/password_change_done.html'), name='password_change_done'),
#path('accounts/', include('django.contrib.auth.urls')),
path('home/', views.home, name='home'),
path('about/', views.about, name='about'),
path('activities/', views.activities, name='activities'),
path('deleteRecord/<str:pk>/', views.deleteRecord, name='deleteRecord'),
path('updateRecord/<str:pk>/', views.updateRecord, name='updateRecord'),
 path('expenses/', views.expenses, name='expenses'),
 path('more/<str:pk>/', views.more, name='more'),
 path('mpesa/', views.mpesa, name='mpesa'),
path("mpesa/callback/", views.mpesa_callback, name="mpesa_callback"),
path('payments/', views.payment_list, name='payment_list'),
path('contributions/<str:pk>/', views.contributions, name='contributions'),
path('make-admin/<int:user_id>/', views.make_admin, name='make_admin'),
path('remove-admin/<int:user_id>/', views.remove_admin, name='remove_admin'),
path('bulk-sms/', views.bulk_sms_view, name='bulk_sms'),
path('admi/', views.admi, name='admi'),
path('manual-transaction/', views.manual_transaction, name='manual_transaction'),
 




]