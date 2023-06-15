from django.contrib import admin
from . models import Account, Saving_record, Target_saving_record, Statements
# Register your models here.
admin.site.register(Account)
admin.site.register(Saving_record)
admin.site.register(Target_saving_record)
admin.site.register(Statements)
