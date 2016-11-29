from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import Quote, Favorite 
from ..login_reg_app.models import User
from django.db.models import Count
from django.contrib import messages


# Create your views here.
def index(request):
    print "Got quote index"
    try:
        request.session['goodtogo']
    except KeyError:
        print "invalid user"  
        return redirect (reverse('login:index'))  
      
    if request.session['goodtogo']:
        print "we are goodtogo"
        u1=User.objects.get(id=request.session['id'])
        quotes = Quote.objects.all()
        favorites= Favorite.objects.filter(user=u1)
        
        context = {
            'quotes': quotes,
            'favorites': favorites
        }
        return render(request, 'quotes/index.html', context)

    else:
        print "invalid user"  
        return redirect (reverse('login:index'))  

def create(request):
    print "Got create"
    try:
        request.session['goodtogo']
    except KeyError:
        print "invalid user"  
        return redirect (reverse('login:index')) 

    if request.method == "POST" and request.session['goodtogo']:
        print "Got create post" 
        quote = request.POST['quote']
        author = request.POST['author']          
        print author
        print quote 

        if not author:
            messages.add_message(request, messages.INFO, "Need to include Author's name.")
            error=True        
        if not quote:
            messages.add_message(request, messages.INFO,"Quote cannot be blank!")
            error=True
    
        if not error: 
            u1=User.objects.get(id=request.session['id'])
            q1 = Quote(author=author, quote=quote, submitter=u1)
            q1.save()            
            return redirect (reverse('quotes:index'))
        else:
            messages.add_message(request, messages.INFO, "Please try again")
            print"we got error messages"
            return redirect (reverse('login:index')) 

def favorite(request, id):
    print "in favorite, quote id=", id
    try:
        request.session['goodtogo']
    except KeyError:
        print "invalid user"  
        return redirect (reverse('login:index')) 

    if request.session['goodtogo']:
        u1=User.objects.get(id=request.session['id'])
        q1=Quote.objects.get(id=id)
        f1= Favorite(user=u1, quote=q1)
        f1.save()
        return redirect (reverse('quotes:index'))
    else:
        print "invalid user"  
        return redirect (reverse('login:index'))      

def remove(request, id):
    print "in remove, quote id=", id
    try:
        request.session['goodtogo']
    except KeyError:
        print "invalid user"  
        return redirect (reverse('login:index')) 

    if request.session['goodtogo']:
        u1=User.objects.get(id=request.session['id'])
        q1=Quote.objects.get(id=id)
        Favorite.objects.filter(user=u1, quote=q1).delete()
        return redirect (reverse('quotes:index'))
    else:
        print "invalid user"  
        return redirect (reverse('login:index'))  



def user(request, id): 
    print "Got user"    

    try:
        request.session['goodtogo']
    except KeyError:
        print "Invalid User"  
        return redirect (reverse('login:index')) 
    print "request.session['goodtogo']", request.session['goodtogo']

    if request.session['goodtogo']: 

        # u1 = User.objects.get(id=id)
        u1 = User.objects.filter(id=id).annotate(num_postings = Count('quote'))    
        q1 = Quote.objects.filter(submitter=u1)      
        
        context = {
            'user': u1[0], 
            'quotes': q1
            }    
        return render(request, 'quotes/show_user.html', context)

    else:
        print "..invalid user"  
        return redirect (reverse('login:index'))  


def logout(request):
    request.session['goodtogo'] = False
    return redirect (reverse('login:index'))
