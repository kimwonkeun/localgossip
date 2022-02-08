from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(gossip_table)
admin.site.register(user_table)
admin.site.register(question)
admin.site.register(answer)