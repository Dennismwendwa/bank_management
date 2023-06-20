from django.contrib import admin
from . models import Account, Saving_record, Target_saving_record, Statements
from . models import Saving_account, Saving_account_statements

# Register your models here.

admin.site.register(Account)
admin.site.register(Saving_record)
admin.site.register(Target_saving_record)
admin.site.register(Statements)

admin.site.register(Saving_account)
admin.site.register(Saving_account_statements)
