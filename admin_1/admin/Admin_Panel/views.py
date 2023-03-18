from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.views.generic import View
import psycopg2
from rest_framework.views import APIView
from rest_framework.response import Response

chartdata_X=[] 
chartdata_Y=[]

connection = psycopg2.connect(user="water__22",
                                  password="UvqtlAZhmI9uFPuIYhrzPVooe4FB0T70",
                                  host="dpg-cfmestarrk07m3tr756g-a.singapore-postgres.render.com",
                                  port="5432",
                                  database="watermeter22")
cursor = connection.cursor()
cursor.execute("select * from swm;")
record=cursor.fetchall()
for i in record:
	
    chartdata_X.append(i[0]) 
    chartdata_Y.append(i[4]) 
    
list_zipped=list(zip(chartdata_X,chartdata_Y))

# class data(View):
# 	def get(self, request, *args, **kwargs):
# 		return render(request, 'data.html')
def data(request): 
    
    context={'finalamt':'{0:10.2f}'.format(chartdata_X[-1]*10),'finalvol':'{0:10.2f}'.format(chartdata_X[-1]),"zipped":list_zipped}
    return render(request, 'data.html',context)


chartdata_X=[] 
chartdata_Y=[]
####################################################

## if you don't want to user rest_framework

# def get_data(request, *args, **kwargs):
#
# data ={
#			 "sales" : 100,
#			 "person": 10000,
#	 }
#
# return JsonResponse(data) # http response


#######################################################

## using rest_framework classes

for i in record:
	
    chartdata_X.append(i[0]) 
    chartdata_Y.append(i[4]) 
    
    # print(i)
# print(chartdata)    
class ChartData(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format = None):
		labels = chartdata_Y
                # [
			# 'Monday',
			# 'Tuesday',
			# 'Wednesday',
			# 'Thrusday',
			# 'Friday',
			# 'Saturday',
			# 'Sunday'
			# ]
		chartLabel = "my data"
		data ={
					"labels":labels,
					"chartLabel":chartLabel,
					"chartdata":chartdata_X,
        }
		return Response(data)

# Create your views here.

def home(request):
    return render(request,"home.html")

def register(request):    
    if request.method=='POST':
        name=request.POST["username"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]

        if password1==password2:        
            user=User.objects.create_user(username=name,email=email,password=password1)
            user.is_staff=True
            user.is_superuser=True
            user.save()
            messages.success(request,'Your account has been created! You are able to login')
            return redirect('Login')
        else:
            messages.warning(request,'Password Mismatching...!!!')
            return redirect('Register')        
    else:
        form=CreateUserForm()        
        return render(request,"register.html",{'form':form})
    
@login_required
def profile(request):
    return render(request,"profile.html")
    
