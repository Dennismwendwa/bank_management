from django.shortcuts import render, redirect
from django.urls import path
from django .contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
import datetime
from .models import Agents, Dealers
from .forms import AgentForm
from .logic import create_agent_number

def create_agents(request):

    current_time = datetime.datetime.now().time()
    target_time = datetime.time(hour=18, minute=39)

    if current_time >= target_time:
        create_agent_number()

    if request.method == "POST":
        form = AgentForm(request.POST)
        
        dealer_id = request.POST["dealer_id"]
        if Dealers.objects.filter(dealer_id=dealer_id).exists():
            if form.is_valid():
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                id_number = form.cleaned_data["id_number"]
                dealer_id = form.cleaned_data["dealer_id"]
                contact_number = form.cleaned_data["contact_number"]
                address = form.cleaned_data["address"]

                try:
                    agent = Agents.objects.create(first_name=first_name, last_name=last_name,
                            id_number=id_number, contact_number=contact_number,
                            address=address, dealer_id=dealer_id)
                    agent.save()
                    messages.success(request, f"Your request was received seccessfully")
                    return redirect("create_agents")
                except Exception as e:
                    messages.error(request, "something went wrong. try again")
                    return redirect("create_agents")
            else:
                id_number_errors = form.errors.get('id_number')
                error_message = id_number_errors[0]
                messages.error(request, f"{error_message}")
                return redirect("create_agents")
        else:
            messages.error(request, f"No Authorized dealer with that id.")
            return redirect("create_agents")
    else:
            form = AgentForm()

    return render(request, "savings/create_agents.html", {
        "form": form,
        })
