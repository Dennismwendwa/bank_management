from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from accounts.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from decimal import Decimal, InvalidOperation
import decimal
from django.utils import timezone
import datetime

from savings.models import Account, Company, BusinessNumber, TillNumber
from savings.models import Agents
from savings.classes import not_negative, register_history
from savings.logic import generate_business_numbers, create_agent_number
from .forms import EditBusinessNumberForm, EditCompanyForm, EditAgentsForm
from .models import write_to_file, write_to_csv, write_to_bus_file

def forbidden_view(request, exception):

    return render(request, 'userdata/forbidden.html', status=404)

def page_not_found(request, exception):

    return render(request, "userdata/error_404.html")

def bad_request_view(request, exception):

    return render(request, "userdata/error_400.html")

def server_error(request):

    return render(request, "userdata/error_500.html")

def permission_denied(request, exception):

    return render(request, "userdata/error_403.html")

#@login_required
@permission_required("accounts.change_user", raise_exception=True)
def edit_user_data(request, user_id):

    user = get_object_or_404(User, id=user_id)

    current_account = Account.objects.filter(user=user).first()


    return render(request, "userdata/edit_user_data.html", {})


@permission_required("accounts.change_user", raise_exception=True)
def admin_deposit_simba(request):
    
    admin = request.user
    if request.method == "POST":
        deposit_amount = request.POST["deposit_amount"]
        account = request.POST["account"]
        user_id = request.POST["user_id"]
        
        try:
            deposit_amount = Decimal(deposit_amount)
        except InvalidOperation:
            messages.error(request, "Enter amount in numbers. e.g 1000, 2000, 1234.")
            return redirect("userdata:admin_deposit_simba")

        status = not_negative(deposit_amount)
        if status == "negative":
            messages.error(request, f"Amount can not be zero or less than one")
            return redirect("userdata:admin_deposit_simba")

        try:
            d_account = Account.objects.get(account_number=account)

        except Account.DoesNotExist:
            messages.error(request, f"Wrong account number")
            return redirect("userdata:admin_deposit_simba")
        else:
        
            transaction_type = "deposit"
            transaction_date = timezone.now()
            account_type = "Simba"

            d_account.account_balance += deposit_amount
        
            d_account.last_transaction_date = transaction_date
            d_account.total_deposit += deposit_amount
            d_account.total_trans_amount += deposit_amount
            d_account.save()
            data = f"{transaction_date}: {admin} deposited {deposit_amount} in account {account}\n"
            write_to_file(data)
            

            register_history(account, deposit_amount, transaction_type, transaction_date, account_type)

            messages.success(request, f"deposit of {deposit_amount} was successfull.")
            return redirect("userdata:admin_deposit_simba")
    

    print("last line")
    return render(request, "userdata/admin_deposit_simba.html", {})


@permission_required("accounts.change_user", raise_exception=True)
def admin_widthdraw(request):

    if request.method == "POST":
        withdraw_amount = request.POST["withdraw_amount"]
        account = request.POST["account"]
        user_id = request.POST["user_id"]
        admin = request.user
        try:
            withdraw_amount = Decimal(withdraw_amount)
        except InvalidOperation:
            messages.error(request, "Enter amount in numbers. e.g 1000, 2000, 1234.")
            return redirect("userdata:admin_deposit_simba")

        status = not_negative(withdraw_amount)
        if status == "negative":
            messages.error(request, f"Amount can not be zero or less than one")
            return redirect("userdata:admin_widthdraw")
        elif status == "wrong_type":
            messages.error(request, "Enter amount in numbers. e.g 1000, 2000, 1234.")
            return redirect("userdata:admin_widthdraw")
        try:
            w_account = Account.objects.get(account_number=account)

        except Account.DoestNotExist:
            messages.error(request, f"Wrong account number")
            return redirect("userdata:admin_widthdraw")
        
        transaction_type = "withdraw"
        transaction_date = timezone.now()
        account_type = "Simba"

        withdraw_amount = int(withdraw_amount)
        if (w_account.account_balance - 500) >= withdraw_amount:
            
            w_account.account_balance -= withdraw_amount
            
            w_account.last_transaction_date = timezone.now()
            w_account.total_withdraw += withdraw_amount
            w_account.total_trans_amount += withdraw_amount
            w_account.save()
            data = f"{transaction_date}: {admin} withdrow {withdraw_amount} from account {account}\n"
            write_to_file(data)
            register_history(account, withdraw_amount, transaction_type, transaction_date, account_type)
            messages.success(request, f"withdraw of {withdraw_amount} was successfull.")
            return redirect("userdata:admin_widthdraw")

        else:
            messages.error(request, f"Insufficient funds")
            return redirect("userdata:admin_widthdraw")

    return render(request, "userdata/admin_withdraw_simba.html", {})


@permission_required("accounts.change_user", raise_exception=True)
def business_number_approval(request):

    bus_num = Company.objects.filter(business_numbers__isnull=True).first()
    all_com = Company.objects.all()
    tran_date = timezone.now()
    if bus_num is not None:

        if request.method == "POST":
            c_form = EditCompanyForm(request.POST, instance=bus_num)

            if c_form.is_valid():
                company = c_form.save(commit=False)
                business_number = generate_business_numbers()

                BusinessNumber.objects.create(buss_number=business_number,
                        company=company)
                company.save()

            messages.success(request, f"Successfully saved.")
            data = f"{tran_date}: {admin} updated {bus_num.name} details\n"
            write_to_bus_file(data)
            return redirect("userdata:business_number_approval")

        else:
            c_form = EditCompanyForm(instance=bus_num)

        context = {
                "c_form": c_form,
                }
        
        return render(request, "userdata/business_number_approval.html", context)
    
    else:
        context = {
                "all_com": all_com,
                }
        return render(request, "userdata/business_number_approval.html", context)
        #return HttpResponse("No company found without a business number.")

@permission_required("savings.change_till_number", raise_exception=True)
def till_number_approval(request):

    till_num = Agents.objects.filter(agent_number__isnull=True, status=False).first()
    all_agents = Agents.objects.filter(status=True)
    tran_date = timezone.now()
    admin = request.user
    if till_num is not None:
        if request.method == "POST":
            till_form = EditAgentsForm(request.POST, instance=till_num)
            
            if till_form.is_valid():
                agent = till_form.save(commit=False)
                till_number, agent_number = create_agent_number()
                agent.agent_number = agent_number
                #agent.image = request.FILES['image']
                TillNumber.objects.create(number=till_number, agent=till_num)
                agent.save()
                data = f"{tran_date}: {admin} updated {till_num.first_name} details\n"
                write_to_bus_file(data)
            messages.success(request, f"Successfully saved.")
            return redirect("userdata:till_number_approval")
        else:
            till_form = EditAgentsForm(instance=till_num)

        context = {
                "till_form": till_form,
                }
        return render(request, "userdata/till_number_approval.html", context)
    else:

        context = {
                "all_agents": all_agents,
                }
        return render(request, "userdata/till_number_approval.html", context)
