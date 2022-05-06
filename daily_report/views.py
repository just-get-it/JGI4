from django.shortcuts import render, redirect, HttpResponse
from .models import Employee, Tasks, Report, Fileupload, Fileuploadnext
from django.views.decorators.csrf import csrf_exempt
import random
from django.contrib import messages
from django.http import JsonResponse
from userdetail.models import detail
from channels.models import Notification


def index(request):
    unique_id = random.randint(1111, 9999)
    employees = Employee.objects.all()
    task = Tasks.objects.all()
    response = render(request, "daily_report/contact.html", {
        'emp': employees,
        'task': task
    })
    response.set_cookie("unique_id", unique_id)
    return response


def save(request):
    url = '/daily_report'
    report_object = Report()
    if request.user.is_authenticated:
        details = detail.objects.filter(email=request.user.email).first()
        report_object.report_submitter = details
    if request.POST.get("owner") != None:
        report_object.report_owner = detail.objects.get(email= request.POST.get('owner_det'))
        report_object.report_head = request.POST.get("owner")
        report_object.report_id = request.POST.get("unique")
        url = url + "/" + request.POST.get("owner") + "/" + request.POST.get("unique")
    report_object.name = request.POST["name"]
    report_object.report = request.POST["report"]
    report_object.task = request.POST["task"]
    report_object.date = request.POST["date"]
    report_object.start_time = request.POST["start_time"]
    report_object.end_time = request.POST["end_time"]
    report_object.no_of_hours = request.POST["no_of_hours"]
    report_object.team_lead = request.POST["team_lead"]
    report_object.today_progress = request.POST["today_progress"]
    report_object.todays_files_url = request.POST["file_link1"]
    report_object.concern = request.POST["concern"]
    report_object.next_plan = request.POST["next_plan"]
    report_object.next_plan_files_url = request.POST["file_link2"]
    # next_plan_files = request.FILES.getlist("upload_next")
    report_object.save()
    text = report_object.report + " report submitted by " + report_object.name
    notify = Notification(to=report_object.report_owner, type='warning', text=text, report=True)
    notify.save()
    # files = Fileupload.objects.filter(
    #     owner__name__contains="dummy",
    #     owner__no_of_hours__contains=request.COOKIES["unique_id"])
    # files2 = Fileuploadnext.objects.filter(
    #     owner__name__contains="dummy",
    #     owner__no_of_hours__contains=request.COOKIES["unique_id"])
    # for file in files:
    #     file.owner = report_object
    #     file.save()
    # for file in files2:
    #     file.owner = report_object
    #     file.save()

    to_delete = Report.objects.filter(name="dummy",
                                      no_of_hours=request.COOKIES["unique_id"])
    for dele in to_delete:
        dele.delete()

    response = redirect(url)
    response.delete_cookie("unique_id")
    messages.success(request, "You have Successfully Reported")
    return response


@csrf_exempt
def upload2(request, no):
    number = request.COOKIES["unique_id"]
    if Report.objects.filter(name="dummy", no_of_hours=number):
        dummy_report = Report.objects.get(name="dummy", no_of_hours=number)
    else:
        dummy_report = Report(name="dummy",
                              task="dummpy",
                              report="dummy",
                              date="2020-06-20",
                              start_time="17:40:00",
                              end_time="17:40:00",
                              no_of_hours=number,
                              team_lead="dummy",
                              today_progress="dummpy",
                              concern="dummy",
                              next_plan="dummy")
        dummy_report.save()
    files = request.FILES["file_input2"]
    file_object = Fileuploadnext(fileid=no, filename=files, owner=dummy_report)
    file_object.save()
    return HttpResponse("Done")


@csrf_exempt
def upload(request, no):
    number = request.COOKIES["unique_id"]
    if Report.objects.filter(name="dummy", no_of_hours=number):
        dummy_report = Report.objects.get(name="dummy", no_of_hours=number)
    else:
        dummy_report = Report(name="dummy",
                              task="dummpy",
                              report="dummy",
                              date="2020-06-20",
                              start_time="17:40:00",
                              end_time="17:40:00",
                              no_of_hours=number,
                              team_lead="dummy",
                              today_progress="dummpy",
                              concern="dummy",
                              next_plan="dummy")
        dummy_report.save()
    files = request.FILES["file_input"]
    file_object = Fileupload(fileid=no, filename=files, owner=dummy_report)
    file_object.save()
    return HttpResponse("Done")


@csrf_exempt
def delete(request):
    idfile = request.POST['id_no']
    unique_id = request.POST['unique_id']
    dummy = Fileupload.objects.get(fileid=idfile,
                                   owner__no_of_hours__contains=unique_id)
    dummy.delete()
    return HttpResponse("Done")


@csrf_exempt
def delete2(request):
    idfile = request.POST['id_no']
    unique_id = request.POST['unique_id']
    dummy = Fileuploadnext.objects.get(fileid=idfile,
                                       owner__no_of_hours__contains=unique_id)
    dummy.delete()
    return HttpResponse("Done")


def display_report(request):
    images = ['.png', '.jpeg', '.tiff', '.svg', '.ico', '.jpg']
    documents = [
        '.docx', '.ppt', 'pptx', '.html', '.doc', '.pdf', '.css', '.c', '.php',
        '.js', '.txt', '.xls', '.xlsx'
    ]
    reports = Report.objects.all().exclude(name="dummy",task="dummy")
    fileuploads = Fileupload.objects.all().exclude(
        owner__name__contains="dummy")
    return render(
        request, "daily_report/daily_report.html", {
            "reports": reports,
            "fileuploads": fileuploads,
            "images": images,
            "documents": documents
        })


def gen_uniqueid():
    captial = chr(random.randint(65, 90))
    lower = chr(random.randint(97, 122))
    # l=['@','#','$','&']
    # special=random.choice(l)
    digits = random.randint(10000, 99999)
    digit = str(digits)
    result = captial + lower + digit
    return result


def generate(request):
    belong = detail.objects.get(email=request.user)
    if belong.unique_id_for_report == '1':
        belong.unique_id_for_report = gen_uniqueid()
        belong.save()
    url = belong.name +"/"+ belong.unique_id_for_report
    return render(request,"daily_report/display_link.html",{'url':url})

# def new_link(request):
#     belong = detail.objects.get(email=request.user)
#     belong.unique_id_for_report = gen_uniqueid()
#     belong.save()
#     url = '127.0.0.1:8000/daily_report/' + belong.name +"/"+ belong.unique_id_for_report
#     return render(request,"daily_report/display_link.html",{'url':url})

# def display_report_user(request):
#     belong = detail.objects.get(email=request.user)
#     reports = Report.objects.filter(report_head= belong.name ,report_id = belong.unique_id_for_report)
#     images = ['.png', '.jpeg', '.tiff', '.svg', '.ico', '.jpg']
#     documents = [
#         '.docx', '.ppt', 'pptx', '.html', '.doc', '.pdf', '.css', '.c', '.php',
#         '.js', '.txt', '.xls', '.xlsx'
#     ]
#     fileuploads = Fileupload.objects.all().exclude(
#         owner__name__contains="dummy")
#     return render(
#         request, "daily_report/daily_report.html", {
#             "reports": reports,
#             "fileuploads": fileuploads,
#             "images": images,
#             "documents": documents
#         })
@csrf_exempt
def display_report_user(request):
    if request.user.is_authenticated:
        belong = detail.objects.get(email=request.user)
        if belong.staff or belong.vendor:
            if request.POST.get('action') == 'rate_report':
                report = Report.objects.get(pk= request.POST.get('report_id'))
                report = Report.objects.get(pk= request.POST.get('report_id'))
                new_rating = float(request.POST.get('rating'))
                if report.report_rating != None:
                    if report.report_rating != new_rating:
                        report.report_rating = new_rating
                        report.save()
                        text = "Your " + report.report + " report has been rated " + str(report.report_rating)
                        notify = Notification(to=report.report_submitter, type='primary', text=text, report=True)
                        notify.save()
                else:
                    report.report_rating = new_rating
                    report.save()
                    text = report.name + " report has been rated " + str(report.report_rating)
                    notify = Notification(to=report.report_submitter, type='primary', text=text, report=True)
                    notify.save()
                return JsonResponse({'success':True})
            # reports = Report.objects.filter(report_head= belong.name ,report_id = belong.unique_id_for_report)
            reports = Report.objects.filter(report_owner=belong).order_by('-date')
            staff = True
        else:
            reports = Report.objects.filter(report_submitter=belong).order_by('-date')
            staff = False
        return render(
            request, "daily_report/daily_report.html", {
                "reports": reports,
                "staff": staff
            })
    else:
        return redirect('login_page')

@csrf_exempt
def display_unrated_reports(request):
    if request.user.is_authenticated:
        belong = detail.objects.get(email=request.user)
        if belong.staff or belong.vendor:
            if request.POST.get('action') == 'rate_report':
                report = Report.objects.get(pk= request.POST.get('report_id'))
                new_rating = float(request.POST.get('rating'))
                if report.report_rating != None:
                    if report.report_rating != new_rating:
                        report.report_rating = new_rating
                        report.save()
                        text = report.name + " report has been rated " + str(report.report_rating)
                        notify = Notification(to=report.report_submitter, type='primary', text=text, report=True)
                        notify.save()
                else:
                    report.report_rating = new_rating
                    report.save()
                    text = report.name + " report has been rated " + str(report.report_rating)
                    notify = Notification(to=report.report_submitter, type='primary', text=text, report=True)
                    notify.save()
            staff = True
            # reports = Report.objects.filter(report_head= belong.name ,report_id = belong.unique_id_for_report, report_rating=None)
            reports = Report.objects.filter(report_owner= belong, report_rating=None).order_by('-date')
        else:
            reports = Report.objects.filter(report_submitter=belong, report_rating=None).order_by('-date')
            staff = False
        return render(
            request, "daily_report/daily_report.html", {
                "reports": reports,
                "staff": staff,
            })
    else:
        return redirect('login_page')

def form(request,slug1,slug2):
    belong = detail.objects.filter(name=slug1,unique_id_for_report=slug2)
    if len(belong) == 1 :
        unique_id = random.randint(1111, 9999)
        employees = Employee.objects.all()
        task = Tasks.objects.all()
        response = render(request, "daily_report/form.html", {
            'emp': employees,
            'task': task,
            'owner_det':belong[0],
            'owner':slug1,
            'unique':slug2
        })
        response.set_cookie("unique_id", unique_id)
        return response
    else:
        return HttpResponse("Wrong Link")