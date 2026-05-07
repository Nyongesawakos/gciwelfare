from urllib import request
import threading
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models.functions import Cast
from django.contrib import messages
from django.db.models import CharField
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Q
from django.contrib.auth.models import User
import openpyxl
from openpyxl.utils import get_column_letter
from .models import user, message,Msg
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from .models import tips
from .models import room, group,update,cash_expenditure
from .forms import RoomForm, CustomUserCreationForm, MsgForm, message,MessageForm
from .forms import UpdateForm, cash_expenditureForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import F 
import datetime
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib import messages
from .models import MpesaTransaction
from.forms import MpesaForm
import json
from django.http import JsonResponse
from django_daraja.mpesa.core import MpesaClient
from django.utils import timezone
from .forms import BulkMessageForm
from .models import BulkMessage
from .utils import send_bulk_sms
from web import models
from web import models
from datetime import date
from django.utils import timezone
from django.db.models.functions import ExtractMonth, ExtractYear

MONTHLY_FEE = 2
WELFARE_START_DATE = date(2024, 10, 1)


def calculate_welfare_arrears(user):

    payments = MpesaTransaction.objects.filter(
        user=user,
        status="Success"
    )

    # total months expected since start
    today = timezone.now().date()
    diff = relativedelta(today, WELFARE_START_DATE)

    total_months = diff.years * 12 + diff.months + 1

    # total amount paid
    total_paid_amount = payments.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # convert to equivalent months paid
    paid_months = total_paid_amount // MONTHLY_FEE

    months_missing = max(total_months - int(paid_months), 0)

    amount_due = months_missing * MONTHLY_FEE

    return {
        "months_missing": months_missing,
        "amount_due": amount_due,
        "paid_months": int(paid_months)
    }
@require_http_methods(["GET", "POST"])
def cashflow(request): 
     form = cash_expenditureForm()
     s= cash_expenditure.objects.all()
     if request.method == 'POST':
         form=cash_expenditureForm(request.POST)
         if form.is_valid():
             cash=form.save(commit=False)
             cash.save()
             return redirect('cashflow')

     context ={'form': form , 's' : s }
      
     return render(request, 'web/cash_flow.html', context)
@require_http_methods(["GET", "POST"])
def insert(request):
    form=UpdateForm()
    if request.method == 'POST':
        form=UpdateForm(request.POST)
        if form.is_valid():
            update=form.save(commit=False)
            
            update.save()
            messages.success(request, 'Record added successfully')  
            return redirect('pdf')
    context ={'form': form}
    return render(request, 'web/insert.html', context)
def user_list(request):
    users = User.objects.all()
    R_messages=message.objects.all()
    User_count= users.count()
    lists =room.objects.all()
    payment=update.objects.all()
    cash= cash_expenditure.objects.all().aggregate(total=Sum('Amount'))
    payments = MpesaTransaction.objects.filter(status="Success")
    total_amount = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    
    cash_total = cash['total'] or 0
    difference = total_amount - cash_total




    
    return render(request,'web/user_list.html', {'users': users,'payments': payments,'difference': difference, 'total_amount': total_amount, 'cash': cash['total'], 'lists' : lists, 'User_count': User_count, 'R_messages': R_messages, 'payment': payment,})
@require_http_methods(["GET", "POST"])
def loginPage(request):
    page= 'login'
    if request.user.is_authenticated: 
        return redirect('root')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            User= user.objects.get(username=username)
        except:
            messages.error(request, '')
            User = authenticate(request, username=username, password=password)
            if User is not None:
                login(request, User)
                return redirect('root')
            else:
              messages.error(request, 'Wrong password or username')  
    context = {'page' : page}
    return render(request,'web/registration_login.html',context)
def logoutUser(request):
    logout(request)
    return redirect('login')
@require_http_methods(["GET", "POST"])
def registerPage(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
     form = CustomUserCreationForm(request.POST)
     if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            messages.success(request, 'success')  
            return redirect('createRoom')
     
     
      
            


    return render(request,'web/registration_login.html', { 'form' : form})
@login_required(login_url='/login')
def home(request): 
    q = request.GET.get('q') if request.GET.get('q') != None  else ''
   # tips = room.objects.filter(host=request.user) 
    tips = room.objects.filter(
        Q(group__name__icontains=q) |
        Q(Othername__icontains=q) |
        Q(lastName__icontains=q) 
        
        
                                     
                                )
    if request.user.is_authenticated:

        room_exists = room.objects.filter(host=request.user).exists()

        if not room_exists:
            return redirect("createRoom")   # url name of room form  
    
    
    topics=group.objects.all()
    contributions= update.objects.filter(user_name=request.user)
    adm = Msg.objects.all()
    users = User.objects.all()
    room_count= tips.count()
    R_messages=message.objects.all()
    context ={'tips': tips, 'contributions': contributions, 'topics': topics, 'room_count' : room_count, 'adm': adm,'users' : users, 'R_messages':R_messages}
    return render(request, 'web/home.html', context)
@require_http_methods(["GET", "POST"])
def index(request, pk):
    room_obj= room.objects.get(id=pk)
    payment= update.objects.filter(transaction_id=pk,user_name=request.user)
    #total_amount = payment.aggregate(Sum('amount'))['amount__sum'] or 0
    adm = Msg.objects.all()
    R_messages=room_obj.message_set.all().order_by('-created')

    if request.method =='POST':
        messages= message.objects.create(
            user=request.user,
            room = room_obj,
            body=request.POST.get('body')

        )
        return redirect('index', pk=index.id)
    
  
    context ={'room': room_obj, 'payment':payment,'R_messages': R_messages, 'adm':adm,}
    return render(request, 'web/index.html', context)
@require_http_methods(["GET", "POST"])
@login_required(login_url='/login')
def createRoom(request): 
    form= RoomForm()
    if request.method == 'POST':
        form=RoomForm(request.POST)
        
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('home')
     
         
        
        else:
              messages.error(request, 'You have an existing profile')
    context = {'form' : form}
    return render(request, 'web/room_form.html', context)
@require_http_methods(["GET", "POST"])
@login_required(login_url='/login')
def updateRoom(request, pk):
    update = room.objects.get(id=pk)
    form=RoomForm(instance=update)
    #if request.user != update.host:
        #return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        form=RoomForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            return redirect('home')
    context= {'update' : update, 'form' : form}
    return render(request, 'web/room_form.html', context)
@require_http_methods(["GET", "POST"])
@login_required(login_url='/login')
def deleteRoom(request, pk):
    remove=room.objects.get(id=pk)
    if request.method == 'POST':
        remove.delete()
        return redirect('members')
    return render(request, 'web/delete.html', {'obj' :remove} )
@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def pdf(request): 
    detail=room.objects.all()
    payment=update.objects.all() 
    Totals = update.objects.all().aggregate(total=Sum('transaction'))
    cash= cash_expenditure.objects.all().aggregate(total=Sum('Amount'))
    cash_total = cash['total'] or 0
    update_total = Totals['total'] or 0
    difference = update_total - cash_total

    return render(request, 'web/pdf.html',  {'payment': payment, 'detail': detail, 'difference':difference, 'cash': cash['total'] , 'Totals' : Totals['total']})
@login_required(login_url='/login')
def people(request, pk):
    detail=room.objects.get(id=pk)
    pays=update.objects.all() 
    context ={'detail':detail, 'pays': pays}
    return render(request, 'web/people.html', context)
@login_required(login_url='/login')
def Panel(request):
    payment=update.objects.all() 
    detail=room.objects.all()
    
    contributions = MpesaTransaction.objects.filter(status="Success")

    group = request.GET.get('group')

    selected_group = None

    if group:
        contributions = contributions.filter(profile__group__name__iexact=group)
        selected_group = group
    
    total_count = contributions.count()

    total_amount = sum(t.amount for t in contributions)

    return render(request, 'web/Panel.html', {
        'contributions': contributions,
        'total_amount': total_amount,
        'total_count': total_count,
        'selected_group': selected_group
    })
   
@login_required(login_url='/login')
def single(request):
    q = request.GET.get('q') if request.GET.get('q') != None  else ''
    payment=update.objects.filter(
        Q(choose__icontains=q) |
        Q(amount__icontains=q) |
         Q(choice__icontains=q) 
    )
    #single=update.objects.get  (id=pk)
    r_count=payment.count()
    context = {'payment': payment,'r_count':r_count }
    return render(request, 'web/import.html', context)
@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def members(request):
    query = request.GET.get('q')
    gci =update.objects.all()
    member=room.objects.all().order_by('-created')
    users = User.objects.all().order_by('-date_joined')
   
    if query:
        member = member.filter(
            Firstname__icontains=query
        ) | member.filter(
            Email__icontains=query
        ) | member.filter(
            HBC__icontains=query
        )
    context={'gci':gci, 'member':member, 'users':users, 'query':query}
    return render(request, 'web/members.html',  context)
@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def admi(request):
    query = request.GET.get('q')
    users = User.objects.all().order_by('-date_joined')
    if query:
        users = users.filter(
            username__icontains=query
        ) | users.filter(
            email__icontains=query
        ) 
    return render(request, 'web/admin.html', {'users': users, 'query': query})
@login_required(login_url='/login')
def Message(request):
     R_messages=message.objects.all()
     adm =Msg.objects.all()
    
     
     context={ 'R_messages': R_messages, 'adm':adm}
     return render(request, 'web/Messages.html', context)
@login_required(login_url='/login')
@require_http_methods(["GET", "POST"])
def Msge(request):
    jay = Msg.objects.all()
    form= MsgForm()
    if request.method =='POST':
        form=MsgForm(request.POST)
        if form.is_valid():
            Meso=form.save(commit=False)
            
            Meso.save()
            return redirect('Message')
    context= {'form':form, 'jay': jay}
    return render(request, 'web/update_message.html', context)
@login_required(login_url='/login')
def gci_groups(request):
     q = request.GET.get('q') if request.GET.get('q') != None  else ''
     tips = room.objects.filter(
        Q(group__name__icontains=q) |
        Q(Othername__icontains=q) |
        Q(lastName__icontains=q) 
        
        
                                     
                                )
     topics=group.objects.all()
     
     context= {'tips':tips, 'topics':topics}

     return render(request, 'web/gci_groups.html', context)
@login_required(login_url='/login')
@require_http_methods(["GET", "POST"])
def meso(request):
    jay = message.objects.all()
    form =MessageForm()
    if request.method == 'POST':
        form=MessageForm(request.POST)
        if form.is_valid():
           meso=form.save(commit=False)   
           meso.save()
           return redirect('meso')
    context={'form': form , 'jay':jay}
    return render(request, 'web/update_message.html', context)
@login_required(login_url='/login')
@require_http_methods(["GET", "POST"])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Update session hash to keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change_done')  # Redirect to a success page
        else:
            
            messages.error(request, 'Please Check passwords.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'web/reset_password.html', {'form': form})

def root(request):
    return render(request, 'web/root.html')

def about(request):
    return render(request, 'web/about.html')

def activities(request):
    return render(request, 'web/activities.html')
@login_required(login_url='/login')
def deleteRecord(request, pk):
    cancel=update.objects.get(id=pk)
    if request.method == 'POST':
        cancel.delete()
        messages.success(request, 'Record Deleted') 
        return redirect('user_list')
    
    return render(request, 'web/delete.html', {'obj' :cancel} )

def updateRecord(request, pk):
    change = update.objects.get(id=pk)
    form=UpdateForm(instance=change)
    #if request.user != change.host:
        #return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        form=UpdateForm(request.POST, instance=change)
        if form.is_valid():
            form.save()
            return redirect('pdf')
    context= {'change' : change, 'form' : form}
    return render(request, 'web/insert.html', context)



@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def expenses(request):
      
      s= cash_expenditure.objects.all()

      context ={'s' : s }

      return render(request, 'web/expenses.html', context)

def more(request, pk):
      payment= update.objects.get(id=pk)
     

      context ={'payment' : payment }

      return render(request, 'web/more.html', context)

@login_required(login_url='/login')
@csrf_exempt
def mpesa(request):
    profile = room.objects.get(host=request.user)
    timestamp = timezone.localtime().strftime('%Y%m%d%H%M%S')
    form = MpesaForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        phone_number = form.cleaned_data['phone_number']
        amount = form.cleaned_data['amount']

        # Use logged-in user name (cleaner)
        full_name = request.user.get_full_name() or request.user.username

        # Convert 07XXXXXXXX → 2547XXXXXXXX
        if phone_number.startswith("0"):
            phone_number = "254" + phone_number[1:]

        cl = MpesaClient()

        try:
            response = cl.stk_push(
                phone_number=phone_number,
                amount=amount,
                account_reference='GCI WELFARE',
                transaction_desc='Welfare Contribution',
                callback_url='https://biogenetic-supergenerous-rosann.ngrok-free.dev/mpesa/callback/'
            )

            # ✅ Save transaction linked to user
            MpesaTransaction.objects.create(
                user=request.user,  # 🔑 IMPORTANT
                profile=profile,
                full_name=full_name,
                phone_number=phone_number,
                amount=amount,
                checkout_request_id=response.checkout_request_id,
                merchant_request_id=response.merchant_request_id,
                status="Pending"  # must match model choices
            )

            messages.success(request, "STK push sent. Complete payment on your phone.")
            return redirect("home")

        except Exception as e:
            print("MPESA ERROR:", e)
            messages.error(request, "Payment request failed. Try again.")
            return redirect("mpesa")

    return render(request, "web/pay.html", {
        "form": form,
        "timestamp": timestamp
    })
@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)

    try:
        stk_callback = data['Body']['stkCallback']

        checkout_request_id = stk_callback['CheckoutRequestID']
        result_code = stk_callback['ResultCode']

        transaction = MpesaTransaction.objects.get(
            checkout_request_id=checkout_request_id
        )

        if result_code == 0:
            transaction.status = "success"
        else:
            transaction.status = "failed"

        transaction.save()

    except Exception as e:
        print("Callback Error:", e)

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def payment_list(request):
    query = request.GET.get('q')
    payments = MpesaTransaction.objects.filter(status="Success")
    

    check=MpesaTransaction.objects.all().order_by('full_name')
   
    if query:
        payments= payments.filter(
            full_name__icontains=query
        ) | payments.filter(
            phone_number__icontains=query
        ) | payments.filter(
            checkout_request_id__icontains=query
        )| payments.filter(
            created_at__date__icontains=query
        )
        


    total_amount = payments.aggregate(Sum('amount'))['amount__sum'] or 0    
        
    

   
   
    return render(request, 'web/payment.html', {'payments': payments, 'query':query, 'check': check,'total_amount': total_amount})

    #upload excel
def download_members_excel(request):
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Members"

    # Headers
    ws.append(['Username', 'Firstname', 'LastName', 'Category', 'HBC'])

    # Fetch all rooms
    members = room.objects.all()

    for m in members:
        username = m.host.username if m.host else ""  # prevent None error
        ws.append([username, m.Firstname, m.lastName, m.group.name if m.group else "", m.HBC])

    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=members.xlsx'
    wb.save(response)
    return response


def download_contributions_excel(request):
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "pdf"

    # Headers
    ws.append(['Username', 'Full name', 'Year', 'Month', 'Amount', 'Phone number', 'Transaction_id'])

    # Fetch all rooms
    pdf = update.objects.all()

    for m in pdf:
        username = m.user_name.username if m.user_name else ""  # prevent None error
        ws.append([username, m.transaction.full_name, m.choice, m.choose, m.transaction.amount, m.transaction.phone_number, m.transaction.checkout_request_id])

    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=members.xlsx'
    wb.save(response)
    return response
def upload_cash_expenditure(request):

    if request.method == "POST":
        excel_file = request.FILES.get('file')

        if not excel_file:
            return JsonResponse({"error": "No file uploaded"})

        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        headers = [str(cell.value).strip() for cell in sheet[1]]
        required = ["Expense", "Date", "Amount"]

        if headers[:3] != required:
            return JsonResponse({
        "error": f"Invalid Excel format. Found: {headers}"
    })

        count = 0

        for row in sheet.iter_rows(min_row=2, values_only=True):
            expense, date, amount = row

            if not expense or not amount:
                continue  # skip empty rows

            cash_expenditure.objects.create(
                Expense=expense,
                Date=str(date),
                Amount=amount
            )

            count += 1

        messages.success(request, f"{count} records uploaded successfully")
        return redirect("members")  # change to your page

    return redirect("members")
@login_required(login_url='/login')
@login_required
def contributions(request, pk):
    contributions = MpesaTransaction.objects.filter(
        user=request.user,
        status="Success"
    ).order_by('-created_at')

    total_paid = contributions.aggregate(Sum('amount'))['amount__sum'] or 0

    arrears = calculate_welfare_arrears(request.user)

    return render(request, 'web/contributions.html', {
        'contributions': contributions,
        'total_amount': total_paid,
        'months_missing': arrears['months_missing'],
        'amount_due': arrears['amount_due'],
        'paid_months': arrears['paid_months']
    })
#def contributions(request, pk):
  #  contributions = MpesaTransaction.objects.filter(user=request.user, status="Success").order_by('-created_at')
   # total_amount = MpesaTransaction.objects.filter(user=request.user, status="Success").aggregate(Sum('amount'))['amount__sum'] or 0  
    
    #return render(request, 'web/contributions.html', {
    #    'contributions': contributions,
        #'total_amount': total_amount
   # })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def bulk_sms_view(request):
    form = BulkMessageForm()

    if request.method == "POST":
        form = BulkMessageForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data['message']

            users = MpesaTransaction.objects.filter(status="Success")

            phone_numbers = [
                user.phone_number for user in users if user.phone_number
            ]

            if not phone_numbers:
                messages.error(request, "No valid phone numbers found.")
                return redirect('bulk_sms')

            # ✅ SEND SMS AND CAPTURE RESPONSE
            response = send_bulk_sms(phone_numbers, message)

            success_count = 0
            failed_count = 0

            # ✅ CHECK RESPONSE
            if response:
                recipients = response.get('SMSMessageData', {}).get('Recipients', [])

                for r in recipients:
                    if r.get('status') == "Success":
                        success_count += 1
                    else:
                        failed_count += 1

                messages.success(
                    request,
                    f"SMS Sent: {success_count} success, {failed_count} failed"
                )
            else:
                messages.error(request, "Failed to send SMS. Check API.")

            # ✅ SAVE LOG
            BulkMessage.objects.create(
                sender=request.user,
                message=message,
                recipients_count=len(phone_numbers)
            )

            return redirect('bulk_sms')

    context = {
        "form": form,
        "count": MpesaTransaction.objects.filter(status="Success").count()
    }


    return render(request, "web/bulk_sms.html", context)

def only_superuser(user):
    return user.is_superuser


@user_passes_test(only_superuser)
def make_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)

    user.is_staff = True
    user.is_superuser = True
    user.save()

    messages.success(request, f"{user.username} is now an admin.")
    return redirect('user_list')
def remove_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # prevent removing yourself accidentally
    if request.user.id == user.id:
        messages.error(request, "You cannot remove your own admin rights.")
        return redirect('admin')

    user.is_superuser = False
    user.is_staff = False
    user.save()

    messages.success(request, f"{user.username} is no longer an admin.")
    return redirect('admi')

    








    

    


 
    



    






