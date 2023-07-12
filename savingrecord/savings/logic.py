import datetime
import uuid, random
from django.utils import timezone
from .models import Account
from .models import Agents, TillNumber, Company, BusinessNumber

current_time = datetime.datetime.now().time()
target_time = datetime.time(hour=18, minute=34)


def create_agent_number():
    agents = Agents.objects.filter(status=True, agent_number__isnull=True)
    
    
    if not agents:
        print("No agent to create account for")
	
    for agnts in agents:
		
        # setting till number from default 1111
        till_number = generate_unique_number()
        TillNumber.objects.create(agent=agnts, number=till_number)
        uniq = generate_unique_number()
        agnts.agent_number = uniq
        agnts.save()
        print("Agent number created successfull")

def generate_unique_number():
    unique_number = str(uuid.uuid4().int)[:5]
    return unique_number

def generate_business_numbers():

    companies = Company.objects.filter(approved=True, admin_review=False)
    
    if not companies:
        print("no company to create business number for")

    for company in companies:
        print(company.name)
        bus_number = str(uuid.uuid4().int)[:10]
        BusinessNumber.objects.create(company=company, buss_number=bus_number)
        company.admin_review = True
        company.save()
        print("Business number created successfully")

