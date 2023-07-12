from django.contrib import admin
from .models import Account, Saving_record, Target_saving_record, Statements
from .models import Saving_account, Saving_account_statements
from .models import Agents, Dealers, TillNumber, Company, BusinessNumber
#from .models import Target_saving_record_statements

# Register your models here.

admin.site.register(Account)
admin.site.register(Statements)

admin.site.register(Saving_record)

admin.site.register(Target_saving_record)
#admin.site.register(Target_saving_record_statements)

admin.site.register(Saving_account)
admin.site.register(Saving_account_statements)

admin.site.register(Agents)
admin.site.register(Dealers)
admin.site.register(TillNumber)
admin.site.register(Company)
admin.site.register(BusinessNumber)
