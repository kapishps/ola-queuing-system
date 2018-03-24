from django.shortcuts import render

from core.forms import userinput
from core.models import customer,driver,pickup_req

import datetime
from django.utils import timezone

# Create your views here.


def driver_view(request):
    ids = ['1','2','3','4','5']
    if request.GET.get('id') in ids:
        context = {}
        context['driver_id'] = request.GET.get('id')
        curr_driver = driver.objects.get(pk=request.GET.get('id'))

        # print(curr_driver)
        waiting = pickup_req.objects.filter(status='W')
        context['Waiting'] = []
        for i in waiting:
            d = {
                'req_id' : i.req_id,
                'customer_id': i.customer.customer_id,
                'time_elapsed' : int((timezone.now() - i.created_at).total_seconds()/60)
            }
            context['Waiting'].append(d)


        ongoing = pickup_req.objects.filter(status='O',driver=curr_driver)
        context['Ongoing'] = []
        for i in ongoing:
            d ={
                'req_id': i.req_id,
                'customer_id': i.customer.customer_id,
                'requested': int((timezone.now() - i.created_at).total_seconds() / 60),
                'pickedup': int((timezone.now() - i.accepted_at).total_seconds() / 60)
            }
            if d['pickedup'] >= 5:
                i.status = 'C'
                i.save()
            else:
                context['Ongoing'].append(d)


        completed = pickup_req.objects.filter(status='C',driver=curr_driver)
        context['Complete'] = []
        for i in completed:
            d = {
                'req_id': i.req_id,
                'customer_id': i.customer.customer_id,
                'requested': int((timezone.now() - i.created_at).total_seconds() / 60),
                'pickedup': int((timezone.now() - i.accepted_at).total_seconds() / 60),
                'completed': int((timezone.now() - i.accepted_at).total_seconds() / 60) - 5
            }
            context['Complete'].append(d)



        return render(request, context=context, template_name="driver.html")

    return render(request, "driver.html", {'message': 'Driver Not Found'})



def customer_view(request):
    input_id = userinput(request.POST or None)
    if request.POST and input_id.is_valid():
        cust_id = input_id.cleaned_data['q']
        # print(cust_id)
        rider = customer.objects.filter(customer_id=cust_id)
        if rider.count() == 0:
            rider = customer()
            rider.customer_id = cust_id
            rider.save()
        else:
            rider = rider[:1].get()

        new_ride = pickup_req(customer=rider,status='W')
        new_ride.save()

        return render(request, "customer.html", {'form': userinput, 'message': 'Pick up Request Placed Successfully'})

    return render(request, "customer.html", {'form': userinput})

def dashboard_view(request):
    pass

def create_req(request):
    pass

def pick_req(request):
    pass