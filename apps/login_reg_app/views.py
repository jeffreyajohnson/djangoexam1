from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import User

# Create your views here.
def index(request):
  return render(request, "login_reg_app/index.html")

def process(request):
    print"in process method"
    if request.method=='POST':
        print"got method=post"
        print(request.POST)
        response = User.objects.validate_registration(request.POST)
        print("response", response)
        if response[0]:
            print "Register success!!"
            request.session['goodtogo'] = True 
            request.session['alias'] = request.POST['ualias']
            request.session['id']= response[2]       
            return redirect (reverse('quotes:index'))
        else:
            request.session['goodtogo'] = False
            context = {
                'errors': response[1]
            }
            for error in response[1]:
                print"error in response:", error
            return render(request, 'login_reg_app/index.html', context)
    else:
        return render(request, 'login_reg_app/index.html')

def login(request):
    print"in login method"
    if request.method=='POST':
        print"got method=post"
        print(request.POST)
        response = User.objects.validate_login(request.POST)
        print("response", response)
        if response[0]:
            print "Login success!!"
            request.session['goodtogo'] = True 
            request.session['id']= response[2]
            request.session['alias'] = response[1]
            print"request.session['id']:", request.session['id'] 
            print"request.session['alias']:", request.session['alias'] 
            
            # context = {
            #     'first_name': response[1],
            #     'path': "logged in"
            # }
            # print("context:", context)            
            return redirect (reverse('quotes:index'))
        else:
            request.session['goodtogo'] = False
            context = {
                'errors': response[1]
            }
            for error in response[1]:
                print"error in response:", error
            return render(request, 'login_reg_app/index.html', context)
    else:
        return render(request, 'login_reg_app/index.html')



       


