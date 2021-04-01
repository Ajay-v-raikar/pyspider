from django.shortcuts import render
import csv
from csv import writer
from datetime import datetime
from datetime import timedelta

def get_product_list():
    res=[]
    with open('products.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            res+=[row]
    return res

def search_name(user):
    with open('user.csv', 'rt') as file:
        reader = csv.reader(file,delimiter=",")
        for row in reader:
            if user==row[2]:
                return row[0] 
def user_exist(user):
    with open('user.csv', 'rt') as file:
        reader = csv.reader(file,delimiter=",")
        for row in reader:
            if user==row[2]:
                return True
    return False
def get_username():
    file=open('username.txt','r')
    return file.read()

def get_cartlist():
    res=[]
    with open('cart_details.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            res+=[row]
    res1={}
    for i in res:
        if i[0] not in res1:
            res1[i[0]]=int(i[1])
        else:
            res1[i[0]]+=int(i[1])
    list_cart=[[i,  str(res1[i])] for i in res1]
    return list_cart

def signup(request):    
    return render(request,'signup_page.html')

def login(request):
    return render(request,'user_login.html')

def main(request):
    if 'SIGN' in request.POST:
        return render(request,'signup_page.html')
    cart_list=get_cartlist()
    count=len(cart_list)
    if 'log' in request.POST:
        username=request.POST.get("loginUser")
        password=request.POST.get("loginpassword")
        res=[]
        with open('user.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                res+=[row]
        for i in res:
            if i[2]==username:
                if i[3]==password:
                    print(1)
                    file=open('username.txt','w')
                    file.write(i[0].capitalize())
                    file.close()
                    return render(request,'main.html',{'count':count,'name':get_username()})
                print(2)
                return render(request,'user_login.html',{'message':"Wrong Password...!"})   
        print(3)
        return render(request,'user_login.html',{'message':"Account not Exist...!"})
    
    if 'sign' in request.POST:
        signup_details=[request.POST.get("name").upper(),request.POST.get("email").upper(),
                request.POST.get("username"),request.POST.get("password"),
                request.POST.get("date"),request.POST.get("gender"),
                request.POST.get("phone")]
        if user_exist(request.POST.get("username")):
            return render(request,'signup_page.html',{'message':"Username Already Exist...!"})
        file=open('username.txt','w')
        file.write(request.POST.get("name").capitalize())
        with open('user.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(signup_details)
    if request == "POST":
        writer_object=open('cart_details.csv', 'w')
        return render(request,'main.html',{'count':count,'name':get_username(),'message':"Placed your order successfully...."})
    return render(request,'main.html',{'count':count,'name':get_username()})
def homeapplience(request):
    cart_list=get_cartlist()
    count=len(cart_list)
    product_list=get_product_list()
    res1=[]
    if request.method=='POST' and 'home' in request.POST:
        product_list=product_list[:23]
    if request.method=='POST' and 'fash' in request.POST:
        product_list=product_list[24:44]
    if request.method=='POST' and 'book' in request.POST:
        product_list=product_list[44:64]
    if request.method=='POST' and 'electric' in request.POST:
        product_list=product_list[64:84]
    else:
        product_list=product_list
    for row in product_list:
        res1+=[{'pid':row[0],'pname':row[1].capitalize(),'price':int(row[2]),'rate':(round(float(row[3]))*100)//5,'seller':row[4],'path':row[5]}]
    name=request.POST.get("name")
    print(res1)
    return render(request,'homeapplience.html',{'res':res1,'name':name,'count':count,'name':get_username()})

def cart(request):
    cart_list=get_cartlist()
    count=len(cart_list)
    name=request.POST.get("name")
    if request.method=='POST' and 'remove' in request.POST:
        cart_list=get_cartlist()
        res0=[]
        value=request.POST.get("id")
        for i in cart_list:
            if i[0]!=value:
                res0+=[i]
        res=res0
        writer_object=open('cart_details.csv', 'w')
        for i in res:
            List=i[0]
            sep=","
            list2=i[1]+"\n"
            writer_object=open('cart_details.csv', 'a')
            writer_object.write(List)
            writer_object.write(sep)
            writer_object.write(list2)
            writer_object.close()
        res=[]
        with open('cart_details.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                res+=[row]

        res0=[]
        res=[]
        with open('cart_details.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                res+=[row]
        product_list=get_product_list()
        res2=[]
        for i in res:
            for j in product_list:
                if i[0] == j[0]:
                    res2+=[j+[i[1]]]
                    print(res2)
        res3=[]
        for row in res2:
            res3+=[{'pid':row[0],'pname':row[1].capitalize(),'price':int(row[2]),'rate':(round(float(row[3]))*100)//5,'seller':row[4],'path':row[5],'no':row[7],'sub':int(row[7])*int(row[2])}]
        bill=0
        for i in res3:
            bill+=(i['sub'])
        cart_list=get_cartlist()
        count=len(cart_list)
        return render(request,'cart.html',{'res':res3,'bill':bill,'name':name,'count':count,'name':get_username()})

    elif request.method=='POST' and 'search' in request.POST:
        var=request.POST.get("sele").lower()
        product_list=get_product_list()
        res1=[]
        res2=[]
        
        var2=request.POST.get("cat")
        if request.method=='POST' and  var2=='home' :
            product_list=product_list[:23]
        if request.method=='POST' and  var2=='fash': 
            product_list=product_list[24:44]
        if request.method=='POST' and  var2=='book' :
            product_list=product_list[44:64]
        if request.method=='POST' and  var2=='electric': 
            product_list=product_list[64:84]
        else:
            product_list=product_list
        for i in product_list:
            if var in i[1].lower():
                res1+=[i]
        for row in res1:
            res2+=[{'pid':row[0],'pname':row[1],'price':int(row[2]),'rate':(round(float(row[3]))*100)//5,'seller':row[4],'path':row[5]}]
        
        return render(request,'homeapplience.html',{'res':res2,'count':count,'name':get_username()})
    elif request.method=='POST' and 'logout' in request.POST:
        return render(request,'signup_page.html')
    else:
        res=get_cartlist()
        
        product_list=get_product_list()
        res2=[]
        for i in res:
            for j in product_list:
                if len(i)>0:
                    if i[0] == j[0]:
                        res2+=[j+[i[1]]]
        res3=[]
        for row in res2:
            res3+=[{'pid':row[0],'pname':row[1],'price':int(row[2]),'rate':(round(float(row[3]))*100)//5,'seller':row[4],'path':row[5],'no':row[7],'sub':int(row[7])*int(row[2])}]
        bill=0
        for i in res3:
            bill+=(i['sub'])
        return render(request,'cart.html',{'res':res3,'bill':bill,'count':count,'name':get_username()})
def checkout(request):
    return render(request,'checkout.html')

def product(request,var1,massage=None):
    cart_list=get_cartlist()
    count=len(cart_list)
    pid=request.POST.get('val')
    product_list=get_product_list()
    res1=[]
    for row in product_list:
        if row[0]==str(var1):
            res1={'pid':row[0],'pname':row[1],'price':int(row[2]),'rate':(round(float(row[3]))*100)//5,'seller':row[4],'path':row[5]}
    return render(request, 'product.html',{'pro':res1,'count':count,'name':get_username(),'massage':massage})

def addcart(request):
    List=request.POST.get("val")
    sep=","
    list2=request.POST.get("numbers")+"\n"
    writer_object=open('cart_details.csv', 'a')
    writer_object.write(str(List))
    writer_object.write(sep)
    writer_object.write(list2)
    writer_object.close()
    
    product_list=get_product_list()
    res1=set()
    for row in product_list:
        if row[0]==List:
            res1={'pid':row[0],'pname':row[1],'price':int(row[2]),'rate':(round(float(row[3]))*100)//5,'seller':row[4],'path':row[5]}
    cart_list=get_cartlist()
    count=len(cart_list)
    return render(request, 'product.html',{'pro':res1,'count':count,'name':get_username(),'massage':"Added to Cart"})
def checkout(request):
    cart_list=get_cartlist()
    count=len(cart_list)
    cart_list = get_cartlist()
    product_list=get_product_list()
    res2=[]
    for i in cart_list:
        for j in product_list:
            if i[0] == j[0]:
                res2+=[j+[i[1]]]
    res3=[]
    for row in res2:
        res3+=[{'pid':row[0],'pname':row[1],'price':int(row[2]),'rate':(round(float(row[3]))*100)//5,'seller':row[4].split(","),'path':row[5],'no':row[7],'sub':int(row[7])*int(row[2])}]
    bill=0
    for i in res3:
        bill+=(i['sub'])
    if bill<=1000:
        dc=50
    if 1001<=bill<=5000:
        dc=100
    if 5000<=bill<=10000:
        dc=200
    else:
        dc=300
    state=(bill*0.06)
    central=(bill*0.06)
    grand=bill+(state+central+dc)
    from datetime import datetime
    from datetime import timedelta

    date_now = (datetime.now() + timedelta(days=6) ).strftime('%Y-%m-%d %A')

    date=date_now
    return render(request,'checkout.html',{'res':res3,'bill':round(bill,2),'state':round(state,2),'central':round(central,2),'grand':round(grand,2),'dc':round(dc,2),'date':date,'count':count,'name':get_username()})