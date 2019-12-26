from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json

# Create your views here.
def index(request):
    allProds=[]
    catProds=Product.objects.values('category','id')
    cats={item['category'] for item in catProds}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n = len(prod)
        nslides = (n // 4) + ceil((n / 4) - (n // 4))
        allProds.append([prod,range(1,nslides),nslides])
    params={'allProds':allProds}

    return render(request, "store/index.html", params)


def about(request):
    return render(request, "store/about.html")


def contact(request):
    if request.method=="POST":
        print(request)
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('description','')
        contact = Contact(name=name,email=email,phone=phone, desc = desc)
        contact.save()

        contacted = True
        return render(request, "store/contact.html",{"contacted":contacted})

    return render(request, "store/contact.html")


def tracker(request):
    if request.method=="POST":
        order_id = request.POST.get("orderId",'')
        email = request.POST.get('email','')
        try:
            order = Orders.objects.filter(order_id=order_id,email=email)
            if (len(order)>0):
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc, 'time':item.timestamp})
                    response = json.dumps([updates,order[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("{}")
        except Exception as e:
            return HttpResponse("{}")
    return render(request, "store/tracker.html")


def search(request):
    return render(request, "store/search.html")


def productView(request, myid):
    #fetch the product by id
    product = Product.objects.filter(id=myid)
    print(product)

    return render(request, "store/productView.html",{'product':product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get("itemsJson",'')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address1 = request.POST.get('address1','')
        address2 = request.POST.get('address2','') 
        address = address1 +" "+ address2        
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')

        order = Orders(items_json= items_json,name=name,email=email,address = address, city= city,state=state,zip_code=zip_code,phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc = "The order has been placed")
        update.save()
        order_id = order.order_id
        thank = True
        return render(request, "store/checkout.html",{'thank':thank,'order_id':order_id})

    return render(request, "store/checkout.html")
