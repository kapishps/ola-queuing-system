from django.db import models

# Create your models here.



class customer(models.Model):
    pass


class driver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)


class pickup_req(models.Model):
    req_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    customer = models.ForeignKey(to=customer,on_delete=models.DO_NOTHING,)
    driver = models.ForeignKey(to=driver,on_delete=models.DO_NOTHING,)

    STATUS_TYPES = (
        ('W', 'Waiting'),
        ('O', 'Ongoing'),
        ('C', 'Complete')
    )
    status = models.CharField(
        max_length=1,
        default='W',
        choices=STATUS_TYPES
    )



