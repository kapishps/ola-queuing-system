from django.shortcuts import render

from core.forms import userinput
from core.models import customer,driver,pickup_req

# Create your views here.



def driver_view(request):
    pass

def customer_view(request):
    input_id = userinput(request.POST or None)
    if request.POST and input_id.is_valid():
        cust_id = input_id.cleaned_data['q']
        rider = customer.objects.filter(customer_id=cust_id)
        print(len(rider))
    return render(request, "customer.html", {'form': userinput})

def dashboard_view(request):
    pass

def create_req(request):
    pass

def pick_req(request):
    pass