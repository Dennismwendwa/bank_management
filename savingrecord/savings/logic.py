import datetime
import uuid, random
from django.utils import timezone
from .models import Account
from .models import Agents

current_time = datetime.datetime.now().time()
target_time = datetime.time(hour=18, minute=34)


def create_agent_number():
    agents = Agents.objects.filter(status=True, agent_number__isnull=True)
    
    if not agents:
        print("No agent to create account for")

    def generate_unique_number():
        unique_number = str(uuid.uuid4().int)[:5]
        return unique_number

    for agnts in agents:

        uniq = generate_unique_number()
        agnts.agent_number = uniq
        agnts.save()
        print("Agent number created successfull")
