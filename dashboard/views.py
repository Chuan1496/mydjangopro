from django.http import JsonResponse
from django.shortcuts import render, redirect
from product.models import Product
from product.models import Category
from product.models import Brand
from product.models import Supplier
from dashboard.models import stock, predict, weekPredict
from dashboard.models import purchase
import mysql.connector
import datetime
# Create your views here.
def purchaseInit(request):
    context = {}
    # Query all the data for drop down list
    cateList = Category.objects.all()
    brandList = Brand.objects.all()
    supplierList = Supplier.objects.all()
    context["cateList"] = cateList
    context["brandList"] = brandList
    context["supplierList"] = supplierList
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
        sup.SupplierName as Supplier,
        prod.cost,
        stock.quantity AS qty
    FROM
        inventory.product as prod
    INNER JOIN
        inventory.stock as stock ON prod.id = stock.ProdID
    left JOIN
        inventory.category as cate ON prod.CategoryID = cate.id
    left JOIN
        inventory.brand as brand ON prod.BrandID = brand.id
    left JOIN
        inventory.supplier as sup ON prod.SupplierID = sup.id
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
        if request.POST.get('selectedSup'):
            if query2 == "":
                query2 = " where prod.SupplierID = " + request.POST.get('selectedSup')
            else:
                query2 = query2 + " and prod.SupplierID = " + request.POST.get('selectedSup')
            context["searchSup"] = int(request.POST.get('selectedSup'))
        query = query + query2
        cursorObject.execute(query)
        context["stockList"] = cursorObject.fetchall()
        cursorObject.close()
        dataBase.close()
        return render(request, 'purchase/purchase_List.html', context)
    cursorObject.execute(query)
    context["stockList"] = cursorObject.fetchall()
    cursorObject.close()
    dataBase.close()
    return render(request, 'purchase/purchase_List.html', context)

def doPurchase(request,pk):
    context = {}
    qtyList = [x for x in range(0, 20)]
    context["qtyList"] = qtyList # Drop down list of quantity
    # Query data about the product
    prodStock = stock.objects.get(ProdID=pk)
    prodInfo = Product.objects.get(id=pk)
    context["prodStock"] = prodStock
    context["prodInfo"] = prodInfo
    if request.method == "POST":
        purchObj = purchase()
        if int(request.POST.get('inputQty')) > 0:
            purchObj.quantity = int(request.POST.get('inputQty'))
        else:
            context["status"] = "fail"
            return render(request, 'purchase/purchase.html', context)
        purchObj.ProdName = prodInfo.ProdName
        purchObj.ProdID = prodInfo.id
        purchObj.price = prodInfo.price
        purchObj.SupplierID = prodInfo.SupplierID
        purchObj.status = "P"
        purchObj.total = prodInfo.price * int(request.POST.get('inputQty'))
        purchObj.save()
        context["status"] = "success"
        return render(request, 'purchase/purchase.html', context)
    #Prediction line Chart
    prodPredict = predict.objects.filter(ProdID=pk)
    weeklyPredict = weekPredict.objects.get(ProdID=pk)
    labels = []
    data = []
    for i in prodPredict:
        labels.append(i.weekDay)
        data.append((i.quantity * weeklyPredict.quantity)/100)
    context['labels'] = labels
    context['data'] = data

    today = datetime.datetime.today()
    weekday = today.weekday()
    context['todayPred'] = data[weekday] # today's sale qty
    context['salePred'] = data[weekday+1] + data[weekday+2] # the sale qty in the next two days
    #Product's inventory and purchase Info
    purchaseList = purchase.objects.filter(ProdID=pk, status='D')
    deliverQty = 0
    if(len(purchaseList)>0):
        for i in purchaseList:
            deliverQty = deliverQty + i.quantity
    context['deliverQty'] = deliverQty
    saleResult = deliverQty + prodStock.quantity - (data[weekday+1] + data[weekday+2])
    if saleResult < 0 or weekday == 4:
        context['reccomQty'] = weeklyPredict.quantity
    else:
        context['reccomQty'] = 0
    return render(request, 'purchase/purchase.html', context)

def orderList(request):
    context = {}
    # Query all the data for drop down list
    cateList = Category.objects.all()
    supplierList = Supplier.objects.all()
    qtyList = [x for x in range(0, 20)]
    context["cateList"] = cateList
    context["supplierList"] = supplierList
    context["qtyList"] = qtyList  # Drop down list of quantity
    # Query product in cart status=P
    dataBase = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Nita87521@'
    )
    query = """
    SELECT
        pur.id,
        pur.ProdName,
        cate.CategoryName,
        brand.BrandName,
        sup.SupplierName,
        stock.quantity,
        pur.price,
        pur.quantity,
        pur.total
    FROM
        inventory.purchase as pur
    left JOIN
        inventory.stock as stock ON pur.ProdID = stock.ProdID
    left JOIN
        inventory.product as prod ON prod.id = pur.ProdID
    left JOIN
        inventory.category as cate ON prod.CategoryID = cate.id
    left JOIN
        inventory.brand as brand ON prod.BrandID = brand.id
    left JOIN
        inventory.supplier as sup ON prod.SupplierID = sup.id
    where pur.status = "P"
    """
    cursorObject = dataBase.cursor()
    if request.method == "POST":
        if request.POST.get('selectedCate'):
            query = query + " and prod.CategoryID =" + request.POST.get('selectedCate')
            context["searchCate"] = int(request.POST.get('selectedCate'))
        if request.POST.get('selectedSup'):
            query = query + " and prod.SupplierID =" + request.POST.get('selectedSup')
            context["searchSup"] = int(request.POST.get('selectedSup'))
        cursorObject.execute(query)
        context["orderList"] = cursorObject.fetchall()
        return render(request, 'purchase/order.html', context)
    cursorObject.execute(query)
    context["orderList"] = cursorObject.fetchall()
    cursorObject.close()
    dataBase.close()
    return render(request, 'purchase/order.html', context)

def doOrder(request):
    context = {}
    selectedPrice = request.POST.getlist('selectedPrice')[0]
    selectedQty = request.POST.getlist('selectedQty')[0]
    selectedId = request.POST.getlist('selectedBox')
    for i in range(len(selectedId)):
        total = int(selectedPrice.split(',')[i])*int(selectedQty.split(',')[i])
        purchase.objects.filter(id=selectedId[i], status='P').update(price=total,quantity=int(selectedQty.split(',')[i]),status='D')
    return redirect('purchaseHis')

def doDelete(request):
    selectedId = request.POST.getlist('selectedBox')
    if request.method == 'POST':
        for i in range(len(selectedId)):
            purchase.objects.filter(id=selectedId[i],status='P').delete()
    return redirect('orderList')

def purchaseHis(request):
    context = {}
    # Query all the data for drop down list
    cateList = Category.objects.all()
    supplierList = Supplier.objects.all()
    context["cateList"] = cateList
    context["supplierList"] = supplierList
    dataBase = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Nita87521@'
    )
    query = """
    SELECT
        pur.id,
        pur.purchaseDate,
        pur.ProdName,
        cate.CategoryName,
        brand.BrandName,
        sup.SupplierName,
        pur.quantity,
        pur.price,
        pur.status
    FROM
        inventory.purchase as pur
    left JOIN
        inventory.stock as stock ON pur.ProdID = stock.ProdID
    left JOIN
        inventory.product as prod ON prod.id = pur.ProdID
    left JOIN
        inventory.category as cate ON prod.CategoryID = cate.id
    left JOIN
        inventory.brand as brand ON prod.BrandID = brand.id
    left JOIN
        inventory.supplier as sup ON prod.SupplierID = sup.id
    """
    cursorObject = dataBase.cursor()
    if request.method == 'POST':
        query2 = ""
        if request.POST.get('selectedCate'):
            query2 = " where prod.CategoryID = " + request.POST.get('selectedCate')
            context["searchCate"] = int(request.POST.get('selectedCate'))
        if request.POST.get('selectedSup'):
            if query2 == "":
                query2 = " where prod.SupplierID = " + request.POST.get('selectedSup')
            else:
                query2 = query2 + " and prod.SupplierID = " + request.POST.get('selectedSup')
            context["searchSup"] = int(request.POST.get('selectedSup'))
        if request.POST.get('selectedStatus'):
            if query2 == "":
                query2 = " where pur.status = '" + request.POST.get('selectedStatus') +"'"
            else:
                query2 = query2 + " and pur.status = '" + request.POST.get('selectedStatus') +"'"
            context["searchStatus"] = request.POST.get('selectedStatus')
        query = query + query2
        cursorObject.execute(query)
        context["purchaseList"] = cursorObject.fetchall()
        cursorObject.close()
        dataBase.close()
        return render(request, 'purchase/purchaseHistory.html', context)
    cursorObject.execute(query)
    context["purchaseList"] = cursorObject.fetchall()
    cursorObject.close()
    dataBase.close()
    return render(request, 'purchase/purchaseHistory.html', context)

def editStatus(request, pk):
    if request.method == 'POST':
        dataBase = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Nita87521@'
        )
        query = """
        UPDATE inventory.stock AS s
        JOIN inventory.purchase AS p ON s.id = p.ProdID
        SET s.quantity = s.quantity + p.quantity
        where p.id = %s
        """
        cursorObject = dataBase.cursor()
        cursorObject.execute(query, [pk])
        dataBase.commit()  # Commit the changes
        cursorObject.close()
        dataBase.close()
        purchase.objects.filter(id=pk).update(status='C')
        return redirect('purchaseHis')
    return redirect('purchaseHis')

def doPredict(request, pk):



    return redirect('doPurchase')
