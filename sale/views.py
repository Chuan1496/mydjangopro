# Create your views here.
from django.shortcuts import render, redirect
import mysql.connector

from dashboard.models import stock
from product.models import Category, Brand, Product
from sale.models import sale, Customer
import datetime

# Create your views here.
def customer_init(request):
    context = {}
    if request.method == "POST":
        # Create a dictionary to store the arguments for the Product constructor
        searchArg = {}
        # Retrieve the search parameters from the POST request and check whether they have values
        if request.POST.get('custName'):
            searchArg['CustName'] = request.POST.get('custName')
            context["searchName"] = request.POST.get('custName')
        if request.POST.get('custBirth'):
            searchArg['birthday'] = datetime.datetime.strptime(request.POST.get('custBirth'), '%Y-%m-%d').date()
            context["searchBirth"] = request.POST.get('custBirth')
        if request.POST.get('custPhone'):
            searchArg['phone'] = request.POST.get('custPhone')
            context["searchPhone"] = request.POST.get('custPhone')
        # Search DB using the filter() method
        context["custList"] = Customer.objects.filter(**searchArg)
    else:
        # Query all the customer List
        context["custList"] = Customer.objects.all()
    return render(request, 'customer/customer_List.html', context)

def newCust(request):
    context = {}
    # Query all the data for drop down list
    if request.method == "POST":
        custObj = Customer()
        if request.POST.get('inputName'):
            custObj.CustName = request.POST.get('inputName')
        else:
            context["msg"] = "Customer name can not be empty!!"
            return render(request, 'customer/newCustomer.html', context)
        if request.POST.get('inputBirth'):
            custObj.birthday = datetime.datetime.strptime(request.POST.get('inputBirth'), '%Y-%m-%d').date()
        else:
            context["msg"] = "Birthday can not be empty!!"
            return render(request, 'customer/newCustomer.html', context)
        if request.POST.get('inputPhone'):
            custObj.phone = request.POST.get('inputPhone')
        else:
            context["msg"] = "Phone number can not be empty!!"
            return render(request, 'customer/newCustomer.html', context)
        if request.POST.get('inputEmail'):
            custObj.email = request.POST.get('inputEmail')
        custObj.save()
        context["msg"] = "New customer is saved!!"

    return render(request, 'customer/newCustomer.html', context)

def editCust(request, pk):
    item = Customer.objects.get(id=pk)
    if request.method == 'POST':
        if request.POST.get('inputName'):
            item.CustName = request.POST.get('inputName')
        if request.POST.get('inputBirth'):
            item.birthday = datetime.datetime.strptime(request.POST.get('inputBirth'), '%Y-%m-%d').date()
        if request.POST.get('inputPhone'):
            item.phone = request.POST.get('inputPhone')
        if request.POST.get('inputEmail'):
            item.email = request.POST.get('inputEmail')
        item.save()
        return redirect('customer_init')
    return render(request, 'customer/editCustomer.html', {'item': item})


def deleteCust(request, pk):
    item = Customer.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
    return redirect('customer_init')


def saleInit(request):
    context = {}
    # Query all the data for drop down list
    cateList = Category.objects.all()
    brandList = Brand.objects.all()
    context["cateList"] = cateList
    context["brandList"] = brandList
    # Query all the product List
    dataBase = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Nita87521@'
    )
    query = """
    SELECT
        prod.id,
        prod.ProdName,
        cate.CategoryName as Category,
        brand.BrandName as Brand,
        prod.price,
        stock.quantity AS qty
    FROM
        inventory.product as prod
    INNER JOIN
        inventory.stock as stock ON prod.id = stock.ProdID
    left JOIN
        inventory.category as cate ON prod.CategoryID = cate.id
    left JOIN
        inventory.brand as brand ON prod.BrandID = brand.id
    """
    cursorObject = dataBase.cursor()
    if request.method == "POST":
        query2 = ""
        if request.POST.get('selectedCate'):
            query2 = " where prod.CategoryID = " + request.POST.get('selectedCate')
            context["searchCate"] = int(request.POST.get('selectedCate'))
        if request.POST.get('selectedBrand'):
            if query2 == "":
                query2 = " where prod.BrandID = " + request.POST.get('selectedBrand')
            else:
                query2 = query2 + " and prod.BrandID = " + request.POST.get('selectedBrand')
            context["searchBrand"] = int(request.POST.get('selectedBrand'))
        query = query + query2
        cursorObject.execute(query)
        queryList = cursorObject.fetchall()
        productList = []
        for i in queryList:
            tuple1 = (i[0], i[1], i[2], i[3], i[4], [x for x in range(0, i[5] + 1)])
            productList.append(tuple1)
        context["productList"] = productList
        cursorObject.close()
        dataBase.close()
        return render(request, 'sale/sale.html', context)
    cursorObject.execute(query)
    queryList = cursorObject.fetchall()
    productList = []
    for i in queryList:
        tuple1 = (i[0], i[1], i[2], i[3], i[4], [x for x in range(0, i[5]+1)])
        productList.append(tuple1)
    context["productList"] = productList
    cursorObject.close()
    dataBase.close()
    return render(request, 'sale/sale.html', context)

def doSale(request):
    if request.method == "POST":
        selectedQty = request.POST.getlist('selectedQty')[0]
        selectedId = request.POST.getlist('selectedBox')
        for i in range(len(selectedId)):
            productinfo = Product.objects.get(id=int(selectedId[i]))
            saleObj = sale()
            saleObj.ProdName = productinfo.ProdName
            saleObj.ProdID = productinfo.id
            saleObj.price = productinfo.price
            saleObj.quantity = int(selectedQty.split(',')[i])
            saleObj.total = productinfo.price * int(selectedQty.split(',')[i])
            saleObj.status = "C"
            if request.POST.get('custId'):
                saleObj.CustID = int(request.POST.get('custId'))
                saleObj.CustName = request.POST.get('custName')
            saleObj.save()
            prodStock = stock.objects.get(ProdID=int(selectedId[i]))
            prodStock.quantity = prodStock.quantity - int(selectedQty.split(',')[i])
            prodStock.save()
        return redirect('saleHis')

def searchCust(request):
    context = {}
    if request.method == "POST":
        searchArg = {}
        if request.POST.get('custName'):
            searchArg['CustName'] = request.POST.get('custName')
        if request.POST.get('custBirth'):
            searchArg['birthday'] = datetime.datetime.strptime(request.POST.get('custBirth'), '%Y-%m-%d').date()
        if request.POST.get('custPhone'):
            searchArg['phone'] = request.POST.get('custPhone')
        # Search DB using the filter() method
        context["custList"] = Customer.objects.filter(**searchArg)
        return render(request, 'customer/searchCustomer.html', context)
    return render(request, 'customer/searchCustomer.html', context)

def saleHis(request):
    context = {}
    # Query all the data for drop down list
    cateList = Category.objects.all()
    brandList = Brand.objects.all()
    context["cateList"] = cateList
    context["brandList"] = brandList
    # Query all the product List
    dataBase = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Nita87521@'
    )
    query = """
    SELECT
        sale.id,
        sale.CustName,
        sale.ProdName,
        cate.CategoryName,
        brand.BrandName,
        sale.price,
        sale.quantity,
        sale.total,
        sale.saleDate
    FROM
        inventory.sale as sale
    left JOIN
        inventory.product as prod ON prod.id = sale.ProdID
    left JOIN
        inventory.category as cate ON prod.CategoryID = cate.id
    left JOIN
        inventory.brand as brand ON prod.BrandID = brand.id
    left JOIN
        inventory.customer as cust ON sale.CustID = cust.id    
    """
    cursorObject = dataBase.cursor()
    if request.method == "POST":
        query2 = ""
        if request.POST.get('selectedCate'):
            query2 = " where prod.CategoryID = " + request.POST.get('selectedCate')
            context["searchCate"] = int(request.POST.get('selectedCate'))
        if request.POST.get('selectedBrand'):
            if query2 == "":
                query2 = " where prod.BrandID = " + request.POST.get('selectedBrand')
            else:
                query2 = query2 + " and prod.BrandID = " + request.POST.get('selectedBrand')
            context["searchBrand"] = int(request.POST.get('selectedBrand'))
        if request.POST.get('custName'):
            if query2 == "":
                query2 = " where sale.CustName = '" + request.POST.get('custName') + "'"
            else:
                query2 = query2 + " and sale.CustName = " + request.POST.get('custName') + "'"
            context["searchCustName"] = request.POST.get('custName')
        if request.POST.get('custPhone'):
            if query2 == "":
                query2 = " where cust.phone = '" + request.POST.get('custPhone') + "'"
            else:
                query2 = query2 + " and cust.phone = '" + request.POST.get('custPhone') + "'"
            context["searchPhone"] = request.POST.get('custPhone')
        if request.POST.get('saleDate'):
            if query2 == "":
                query2 = " WHERE sale.saleDate = DATE '" + request.POST.get('saleDate') + "'"
            else:
                query2 = query2 + " and sale.saleDate = DATE '" + request.POST.get('saleDate') + "'"
        query = query + query2
        cursorObject.execute(query)
        context["saleList"] = cursorObject.fetchall()
        cursorObject.close()
        dataBase.close()
        return render(request, 'sale/saleHistory.html', context)
    cursorObject.execute(query)
    context["saleList"] = cursorObject.fetchall()
    cursorObject.close()
    dataBase.close()
    return render(request, 'sale/saleHistory.html', context)








