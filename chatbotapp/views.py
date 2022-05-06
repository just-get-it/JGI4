from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
import wolframalpha
import wikipedia
import time
from textblob import TextBlob
import threading
from chatbotapp.models import Complaint, Rating
from cartnew.models import wishlist, OrderItem


# from pathlib import Path

question = "none"
# Create your views here.
# df = Path("../../../static_mtz/")
# file1 = df / "sample.txt"






def botfunc():
    global question
    question = TextBlob(question).correct()


def check(string, sub_str):
    if (string.find(sub_str) == -1):
        return 0
    else:
        return 1


def botsearch(request):
    global question, number
    question = request.GET.get('question')
    question = question.lower()
    number = 6
    try:
        number = int(question)
    except:    
        print(question)
    
    name = "your name"
    name2 = "who are you"
    name3 = "who r u"
    name4 = "who are u"
    made = "made you"
    create = "created you"
    creator = "your creator"
    order = "orders"
    order1 = "order"
    wishlist = "wishlist"
    wishlist1 = "wishlists"
    complaint = "complaint"
    complaint1 = "complaints"
    concern = "concern"
    
    

    if(check(question, name) == 1 or check(question,name2)==1 or check(question, name3) or check(question, name4)==1):
        ans = "My name is JGI BOT and I am made by Naajid."
        print(ans)
        text_file = open("/home/ubuntu/b2b/static_mtz/sample.txt", "w")
        n = text_file.write(ans)
        time.sleep(1)
        return render(request, 'userdetail/profile.html', {'ans': ans})
        
    if(check(question, concern)==1)  :
        ans = "As of now, I can help you with your orders, complaints and wishlist"  
        print(ans)
        text_file = open("/home/ubuntu/b2b/static_mtz/sample.txt", "w")
        n = text_file.write(ans)
        time.sleep(1)
        return render(request, 'userdetail/profile.html', {'ans': ans})

    if(check(question, name) != 1):
        if(check(question, order)==1 or check(question, order1)==1):
            text_file = open("/home/ubuntu/b2b/static_mtz/sample.txt", "w")
            ans = ""
            n = text_file.write(str(ans))
            user = OrderItem.objects.first()
            ans1 = getattr(user, "product_name")
            ans2 = getattr(user, "total")
            ans3 = getattr(user, "date_placed")
            ans = "Your last order was    " + str(ans1)+ " " + "priced at" + " " + str(ans2)+ " " + "and dated   "+ str(ans3)
            n = text_file.write(str(ans))
            time.sleep(1)
            return render(request, 'userdetail/profile.html', {'ans': ans})

        if(check(question, complaint)==1 or check(question, complaint1)==1)  :
            text_file = open("/home/ubuntu/b2b/static_mtz/sample.txt", "w")
            ans = ""
            n = text_file.write(str(ans))
            user = Complaint.objects.first()
            ans1 = getattr(user, "desc")
            ans2 = getattr(user, "status")
            ans3 = getattr(user, "reply")
            ans = "Your last complaint was :   " + str(ans1)+ " " + "\n" + "Reply from us :" + str(ans3) + "\n" + ". Status :" + " " + str(ans2)
            n = text_file.write(str(ans))
            time.sleep(1)
            return render(request, 'userdetail/profile.html', {'ans': ans})

        if(check(question, wishlist)==1 or check(question, wishlist1)==1):
            text_file = open("/home/ubuntu/b2b/static_mtz/sample.txt", "w")
            ans = ""
            n = text_file.write(str(ans))
            user = wishlist.objects.first()
            ans1 = getattr(user, "product")
            ans2 = getattr(user, "customer")
            ans = "The last item you wishlisted was :   " + str(ans1)+ " " + " under customer name" + " " + str(ans2)
            n = text_file.write(str(ans))
            time.sleep(1)
            return render(request, 'userdetail/profile.html', {'ans': ans})



            
    if(check(question,made)==1 or check(question, create)==1 or check(question, creator)==1):
            ans = "I am made by Naajid."
            print(ans)
            text_file = open("/home/ubuntu/b2b/static_mtz/sample.txt", "w")
            n = text_file.write(ans)
            time.sleep(1)
            return render(request, 'userdetail/profile.html', {'ans': ans})

    if(0<=number<=5):
            ans = "Your rating has been added to the database."
            print(ans)
            Rating.objects.create(rating = number)
            text_file = open("/home/ubuntu/b2b/static_mtz/sample.txt", "w")
            n = text_file.write(ans)
            time.sleep(1)
            return render(request, 'userdetail/profile.html', {'ans': ans})






    else:
        t1 = threading.Thread(target=botfunc)
        t1.start()
        t1.join()

    try:
        client = wolframalpha.Client("6QV2GX-XQ98P6YTAQ")
        res = client.query(question)
        ans = next(res.results).text
        text_file = open("/home/ubuntu/b2b/static_mtz/sample.txt", "w")
        n = text_file.write(ans)
        text_file.close()
        print(ans)
        return render(request, 'userdetail/profile.html', {'ans': ans})
    except Exception:
        try:
            ans = "I got nothing related to your query."
            print(ans)
            text_file = open("/home/ubuntu/b2b/static_mtz/sample.txt", "w")
            n = text_file.write(ans)
            text_file.close()
            return render(request, 'userdetail/profile.html', {'ans': ans})

        except Exception:
            ans = "Error"
            return render(request, 'userdetail/profile.html', {'ans': ans})
            print("TRY RE-RUNNING THE PROGRAM")
            


def botsearch1(request):
    global question
    question = request.GET.get('question')
    print(question)
