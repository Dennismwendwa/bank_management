from django.shortcuts import render, redirect
from django.urls import path
from django .contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
import datetime

from .models import Agents, Dealers, TillNumber, Company
from .models import Account, Saving_account
from .forms import AgentForm, DealersForm, CompanyForm
from .logic import create_agent_number
from .logic import generate_unique_number, generate_business_numbers
from django.contrib.auth.decorators import permission_required

def create_agents(request):

    current_time = datetime.datetime.now().time()
    target_time = datetime.time(hour=14, minute=39)

    if current_time >= target_time:
        create_agent_number()
        generate_business_numbers()

    if request.method == "POST":
        form = AgentForm(request.POST)
        sec = request.session

        #get the dealer_id from POST
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


def create_dealers(request):

    if request.method == "POST":
        form = DealersForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            id_number = form.cleaned_data["id_number"]
            contact_number = form.cleaned_data["contact_number"]
            address = form.cleaned_data["address"]

            dealer_id = generate_unique_number()

            try:
                dealer = Dealers.objects.create(first_name=first_name,
                        last_name=last_name, id_number=id_number, dealer_id=dealer_id,
                        contact_number=contact_number, address=address)
                dealer.save()
                messages.success(request, f"The dealer agent was created successfully")
                return redirect("create_dealers")
            except Exception as e:
                messages.error(request, f"Something went wrong. try again")
                return redirect("create_dealers")
        else:
            dealer_id_error = form.errors.get("id_number")
            error_message = dealer_id_error[0]
            messages.error(request, f"{error_message}")
            er = form.errors
            return redirect("create_dealers")

    form = DealersForm()

    return render(request, "savings/create_dealer.html", {
        "form": form,
        })

def display_dealers_and_own_agents(request):

    dealers = Dealers.objects.all()
    agents = Agents.objects.filter(status=True)

    context = {
            "dealers": dealers,
            "agents": agents,
            }

    return render(request, "savings/display_dealers_and_own_agents.html", context)



def company(request):

    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            contact = form.cleaned_data["contact"]
            address = form.cleaned_data["address"]
            country = form.cleaned_data["country"]
        try:

            company = Company.objects.create(name=name, email=email,
                    contact=contact, address=address, country=country
                )
            company.save()
            messages.success(request, "Your request was received seccessfully")
            return redirect("company")

        except Exception as e:
            print(e)
            messages.error(request, f"Something went wrong. try again")
            return redirect("company")

        else:
            form.errors
            messages.error(request, "Something went wrong try again")
            return redirect("company")
    else:
        
        form = CompanyForm()


    return render(request, "savings/company.html", {})


def display_companies(request):

    companies = Company.objects.filter(approved=True)

    context = {
            "companies": companies,
            }

    return render(request, "savings/display_companies.html", context)

@permission_required("accounts.change_user", raise_exception=True)
def staff_home(request):

    all_accounts = Account.objects.all()
    all_saving_acc = Saving_account.objects.all()
    
    context = {
            "all_accounts": all_accounts,
            "all_saving_acc": all_saving_acc,
            }
    
    return render(request, "savings/staffs.html", context)
