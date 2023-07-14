from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required

from django.utils import timezone
import datetime

from savings.models import Account

@permission_required("accounts.change_user")
def edit_user_data(request, user_id):

    user = get_object_or_404(User, id=user_id)

    current_account = Account.objects.filter(user=user).first()


    return render(request, "userdata/edit_user_data.html", {})
