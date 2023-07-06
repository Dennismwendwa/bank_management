from .models import Account
from .classes import register_history, not_negative
from django.utils import timezone
from decimal import Decimal, InvalidOperation



def pay_bills(amount_to_pay, account_number, account_to_pay_to, user):
    
    current_datetime = timezone.now()
    transaction_type = "paybills"
    account_type = "Simba"

    try:
        amount_to_pay = Decimal(amount_to_pay)
    except InvalidOperation:
        return "wrong_type"

    status = not_negative(amount_to_pay)
    if status == "negative":
        return "negative"

    try:
        accounts = Account.objects.filter(user=user)
        account = accounts.get(account_number=account_number)
        print(account)
        account_to = Account.objects.get(account_number=account_to_pay_to)
    except Account.DoesNotExist:
        return "no_account"

    if amount_to_pay > account.account_balance:
        return "less_amount"
    print()
    print("account balance", account.account_balance)
    print(type(amount_to_pay))
    print("amount to pay", amount_to_pay)
    print("account yo pay to", account_to.account_balance)

    account.account_balance -= amount_to_pay
    account.total_paybil += amount_to_pay
    account.total_trans_amount += amount_to_pay

    account_to.account_balance += amount_to_pay
    account.save()
    account_to.save()

    register_history(account_number, amount_to_pay, transaction_type, current_datetime, account_type)

    return "success"
