from django.contrib import admin

from core.models import driver,customer,pickup_req

# Register your models here.

admin.site.register(driver)
admin.site.register(customer)
admin.site.register(pickup_req)