from django.shortcuts import  get_object_or_404, render
from .models import Product

# Create your views here.

def products(request):
    pro = Product.objects.all()
    cs =None

    if 'cs' in request.GET:
        cs = request.GET['cs']
        if not cs:
            cs= 'off'

    if 'searchname' in request.GET:
        name = request.GET['searchname']
        if name :
            if cs =='on':                
                pro = pro.filter(PrdName__contains=name)
            else:
                pro = pro.filter(PrdName__icontains=name)
    
    if 'searchdesc' in request.GET:
        desc= request.GET['searchdesc']
        if desc:
            if cs =='on':                
                pro = pro.filter(PrdDesc__contains=desc)
            else:
                pro = pro.filter(PrdDesc__icontains=desc)

    if 'searchpricefrom' in request.GET and 'searchpriceto' in request.GET:
        pricefrom = request.GET['searchpricefrom']
        priceto= request.GET['searchpriceto']
        if pricefrom and priceto:
            if pricefrom.isdigit() and priceto.isdigit():
                pro= pro.filter(PrdDescountPrice__range= (pricefrom, priceto))
            else:
                pro= pro.filter(PrdPrice__range= (pricefrom, priceto))


    context = {
        'products': pro
    }
    return render(request, 'products/products.html', context)

def product(request, id):
    context = {
        'pro':get_object_or_404(Product, pk=id)
    }
    return render(request, 'products/product.html', context)

def search(request):
    return render(request, 'products/search.html')