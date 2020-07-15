from django.contrib import admin

# Register your models here.
from .models import Wfh,Leave,Info,Image,WfhRequest,HolidayRequest

admin.site.register(Info)
admin.site.register(Wfh)
admin.site.register(Leave)
admin.site.register(Image)
admin.site.register(WfhRequest)
admin.site.register(HolidayRequest)