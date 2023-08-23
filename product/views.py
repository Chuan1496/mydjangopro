from django.db.models import Max
from django.shortcuts import render, redirect
from product.models import Product
from product.models import Category
from product.models import Brand
from product.models import Supplier
from .forms import ProductForm
# Create your views here.
def product_init(request):
    #Query all the data for drop down list
    cateList = Category.objects.all()
    brandList = Brand.objects.all()
    supplierList = Supplier.objects.all()
    #Query all the product List
    prodList = Product.objects.all()
    return render(request,'product/product_List.html',{"cateList":cateList,"brandList":brandList,"supplierList":supplierList,"prodList":prodList})

def doSearch(request):
    context = {}
    # Query all the data for drop down list
    context["cateList"] = Category.objects.all()
    context["brandList"] = Brand.objects.all()
    context["supplierList"] = Supplier.objects.all()
    if request.method == "POST":
        # Create a dictionary to store the arguments for the Product constructor
        searchArg = {}
        # Retrieve the search parameters from the POST request and check whether they have values
        if request.POST.get('selectedCate'):
            searchArg['CategoryID'] = int(request.POST.get('selectedCate'))
            context["searchCate"] = int(request.POST.get('selectedCate'))
        if request.POST.get('selectedBrand'):
            searchArg['BrandID'] = int(request.POST.get('selectedBrand'))
            context["searchBrand"] = int(request.POST.get('selectedBrand'))
        if request.POST.get('selectedSup'):
            searchArg['SupplierID'] = int(request.POST.get('selectedSup'))
            context["searchSup"] = int(request.POST.get('selectedSup'))
        if request.POST.get('prodName'):
            searchArg['ProdName'] = request.POST.get('prodName')
            context["searchName"] = request.POST.get('prodName')
        # Search DB using the filter() method
        context["prodList"] = Product.objects.filter(**searchArg)
    return render(request, 'product/product_List.html', context)

def newProd(request):
    # Query all the data for drop down list
    cateList = Category.objects.all()
    brandList = Brand.objects.all()
    supplierList = Supplier.objects.all()
    return render(request, 'product/newProduct.html', {"cateList":cateList,"brandList":brandList,"supplierList":supplierList})

def doSave(request):
    context = {}
    # Query all the data for drop down list
    context["cateList"] = Category.objects.all()
    context["brandList"] = Brand.objects.all()
    context["supplierList"] = Supplier.objects.all()
    if request.method == "POST":
        prodObj = Product()
        if request.POST.get('selectedCate'):
            prodObj.CategoryID = int(request.POST.get('selectedCate'))
        else:
            context["msg"] = "Category can not be empty!!"
            return render(request, 'product/newProduct.html', context)
        if request.POST.get('selectedBrand'):
            prodObj.BrandID = int(request.POST.get('selectedBrand'))
        else:
            context["msg"] = "Brand can not be empty!!"
            return render(request, 'product/newProduct.html', context)
        if request.POST.get('selectedSup'):
            prodObj.SupplierID = int(request.POST.get('selectedSup'))
        else:
            context["msg"] = "Supplier can not be empty!!"
            return render(request, 'product/newProduct.html', context)
        if request.POST.get('inputName'):
            prodObj.ProdName = request.POST.get('inputName')
        else:
            context["msg"] = "Product name can not be empty!!"
            return render(request, 'product/newProduct.html', context)
        if request.POST.get('inputCost'):
            prodObj.cost = int(request.POST.get('inputCost'))
        else:
            context["msg"] = "Cost can not be empty!!"
            return render(request, 'product/newProduct.html', context)
        if request.POST.get('inputPrice'):
            prodObj.price = int(request.POST.get('inputPrice'))
        else:
            context["msg"] = "Price can not be empty!!"
            return render(request, 'product/newProduct.html', context)
        prodObj.save()
        context["msg"] = "New product is saved!!"
    return render(request, 'product/newProduct.html', context)

def editProd(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        if request.POST.get('selectedCate'):
            item.CategoryID = int(request.POST.get('selectedCate'))
        if request.POST.get('selectedBrand'):
            item.BrandID = int(request.POST.get('selectedBrand'))
        if request.POST.get('selectedSup'):
            item.SupplierID = int(request.POST.get('selectedSup'))
        if request.POST.get('inputName'):
            item.ProdName = request.POST.get('inputName')
        if request.POST.get('inputCost'):
            item.cost = int(request.POST.get('inputCost'))
        if request.POST.get('inputPrice'):
            item.price = int(request.POST.get('inputPrice'))
        item.save()
        return redirect('productInit')
    else:
        context = {
            # Query all the data for drop down list
            'cateList': Category.objects.all(),
            'brandList': Brand.objects.all(),
            'supplierList': Supplier.objects.all(),
            'item': item,
        }
    return render(request, 'product/editProduct.html', context)

def deleteProd(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
    return redirect('productInit')