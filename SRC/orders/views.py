from django.shortcuts import redirect, render

# Create your views here.

def add_to_cart(request):
    return redirect('products')
from django.shortcuts import render , redirect
from django.contrib import  messages
from products.models import Product
from orders.models import Order
from orders.models import OrderDetails
from django.utils import timezone


# Create your views here.

def add_to_cart(request):
    if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        pro_id= request.GET['pro_id']
        qty= request.GET['qty']
        order= Order.objects.all().filter(user= request.user, is_finished=False)

        if not Product.objects.all().filter(id=pro_id).exists():
            return redirect('products')
        pro = Product.objects.get(id=pro_id)
            


        if order :
            # messages.success(request, 'You have order befor old order')
            old_order= Order.objects.get(user= request.user, is_finished=False)
            if OrderDetails.objects.all().filter(order= old_order,product= pro).exists():
                orderdetails=OrderDetails.objects.get(order= old_order,product= pro)
                orderdetails.quantity += int(qty)
                orderdetails.save()
            else:
                if pro.PrdDescountPrice > 0:                           
                    orderdetails= OrderDetails.objects.create(product= pro, order= old_order, price= pro.PrdDescountPrice, quantity= qty )
                else:                         
                    orderdetails= OrderDetails.objects.create(product= pro, order= old_order, price= pro.PrdPrice, quantity= qty )
            messages.success(request, 'Yor add another item to cart')


        else:
            # messages.success(request, 'success order New order')
            if pro.PrdDescountPrice > 0:
                new_oreder= Order()
                new_oreder.user = request.user
                new_oreder.order_date = timezone.now()
                new_oreder.is_finished = False
                new_oreder.save()
                orderdetails= OrderDetails.objects.create(product= pro, order= new_oreder, price= pro.PrdDescountPrice, quantity= qty)
            else:
                new_oreder= Order()
                new_oreder.user = request.user
                new_oreder.order_date = timezone.now()
                new_oreder.is_finished = False
                new_oreder.save()
                orderdetails= OrderDetails.objects.create(product= pro, order= new_oreder, price= pro.PrdPrice, quantity= qty)
            messages.success(request, 'Yor add a new item to cart')

        
        return redirect('/products/'+ request.GET['pro_id'])
        
    else:
        messages.info(request, ' You must be lognin first')
        return redirect('signin')


def cart(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user= request.user,is_finished=False):
            order= Order.objects.get(user= request.user,is_finished=False)
            orderdetails= OrderDetails.objects.all().filter(order= order)
            total = 0
            for sub in orderdetails:
                total += sub.price * sub.quantity
            
            context={
                'order':order, 
                'orderdetails':orderdetails, 
                'total':total,
            }    

    
    return render(request, 'orders/cart.html', context)


def remove_from_cart(request, orderdetails_id):
    if  request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id==request.user.id:
            orderdetails.delete()
    return redirect('cart')



def add_qty(request, orderdetails_id):
    if  request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        orderdetails.quantity +=1
        orderdetails.save()
    return redirect('cart')

def sub_qty(request, orderdetails_id):
    if  request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.quantity > 1:
            orderdetails.quantity -=1
            orderdetails.save()
    return redirect('cart')


def payment(request, ):
    return render(request, 'orders/payment.html')