from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from decimal import Decimal, InvalidOperation
import decimal

from django.utils import timezone
import datetime

from savings.models import Account
from savings.classes import not_negative, register_history


@permission_required("accounts.change_user")
def edit_user_data(request, user_id):

    user = get_object_or_404(User, id=user_id)

    current_account = Account.objects.filter(user=user).first()


    return render(request, "userdata/edit_user_data.html", {})


def admin_deposit_simba(request):

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
        

        transaction_type = "deposit"
        transaction_date = timezone.now()
        account_type = "Simba"

        d_account.account_balance += deposit_amount
        
        d_account.last_transaction_date = transaction_date
        d_account.total_deposit += deposit_amount
        d_account.total_trans_amount += deposit_amount
        d_account.save()
        register_history(account, deposit_amount, transaction_type, transaction_date, account_type)

        messages.success(request, f"deposit of {deposit_amount} was successfull.")
        return redirect("userdata:admin_deposit_simba")


    return render(request, "userdata/admin_deposit_simba.html", {})


def admin_widthdraw(request):

    if request.method == "POST":
        withdraw_amount = request.POST["withdraw_amount"]
        account = request.POST["account"]
        user_id = request.POST["user_id"]

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
            register_history(account, withdraw_amount, transaction_type, transaction_date, account_type)
            messages.success(request, f"withdraw of {withdraw_amount} was successfull.")
            return redirect("userdata:admin_widthdraw")

        else:
            messages.error(request, f"Insufficient funds")
            return redirect("userdata:admin_widthdraw")

    return render(request, "userdata/admin_withdraw_simba.html", {})
