from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse

from core.forms import userinput
from core.models import customer,driver,pickup_req

import datetime,json
from django.utils import timezone

# Create your views here.

def home(request):
    return render(request, "index.html")


def driver_view(request,id):
    ids = [1,2,3,4,5]
    if id in ids:
        context = {}
        context['driver_id'] = id
        curr_driver = driver.objects.get(pk=id)

        context['refresh_url'] = curr_driver.get_absolute_url()

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
        # print(ongoing)
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
        # print(completed)
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

    return render(request, "driver.html", {'error': 'Driver Not Found'})



def customer_view(request):
    return render(request, "customer.html", {'form': userinput})


def create_req(request):
    input_id = userinput(request.POST or None)
    resp = {}
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

        new_ride = pickup_req(customer=rider, status='W')
        new_ride.save()

        resp['status'] = 'success'
        return HttpResponse(json.dumps(resp), content_type='application/json')

    resp['status'] = 'error'
    return HttpResponse(json.dumps(resp), content_type='application/json')



def dashboard_view(request):
    reqs = pickup_req.objects.all()
    objects = []
    for i in reqs:
        d = {
            'req_id': i.req_id,
            'customer_id': i.customer.customer_id,
            'time_elapsed': str(int((timezone.now() - i.created_at).total_seconds() / 60)) + ' mins ' + str(int((timezone.now() - i.created_at).total_seconds() % 60)) + ' seconds'
        }

        if i.driver:
            d['driver_id'] = i.driver.driver_id
            if i.status == 'O' and int((timezone.now() - i.accepted_at).total_seconds() / 60) >=5:
                i.status = 'C'
        else:
            d['driver_id'] = 'None'

        if i.status == 'W':
            d['status'] = 'Waiting'
        elif i.status == 'O':
            d['status'] ='Ongoing'
        else:
            d['status'] = 'Completed'
        objects.append(d)

    return render(request, "dashboard.html", {'reqs': objects})



def pick_req(request):
    req_id = request.POST['req_id']
    driver_id = request.POST['driver_id']

    req = pickup_req.objects.get(pk=req_id)
    curr_driver = driver.objects.get(pk=driver_id)

    ongoing = pickup_req.objects.filter(status='O', driver=curr_driver)

    if ongoing.count() == 0 and req.status == 'W':
        req.driver = curr_driver
        req.status = 'O'
        req.accepted_at = timezone.now()
        req.save()


    return HttpResponseRedirect(curr_driver.get_absolute_url())