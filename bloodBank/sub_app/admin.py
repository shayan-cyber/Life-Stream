from django.contrib import admin
from . models import Bank,Chat,ChatRoom

# Register your models here.
admin.site.register(Bank)
admin.site.register(Chat)
admin.site.register(ChatRoom)