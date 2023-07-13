from savings.models import *
from accounts.models import *
from accounts.models import User
import datetime
from django.utils import timezone

from packs.quotes import money_quotes
from savings.classes import get_transaction_history, get_account_details
from savings.classes import get_calender, get_transaction_percentage
from savings.models import Saving_account


def common_variables(request):
	
		
	user = User.objects.get(username=request.user.username)
	acc_detail = get_account_details(user)
	statemest = get_transaction_history(user)
	statement2 = get_transaction_history(user)[:10]
	quote = money_quotes()
	acc_saving = Saving_account.objects.filter(user=user)

	month_name, year, calendar, current_day = get_calender()
	percent_acc, percent_withdral, percent_deposit, percent_transfer, percent_paybill = get_transaction_percentage(user)
		

		
	return {
	"user": user,
	"acc_detail": acc_detail,
	"statemest": statemest,
	"statement2": statement2,
	"quote": quote,
	"acc_saving": acc_saving,

	"percent_acc": percent_acc,
	"percent_withdral": percent_withdral,
	"percent_deposit": percent_deposit,
	"percent_transfer": percent_transfer,
	"percent_paybill": percent_paybill,

	"month_name": month_name,
	"year": year,
	"calendar": calendar,
	"current_day": current_day,
	}
