from django import template
from django.shortcuts import render, redirect, HttpResponse
from daily_report.models import Report, Fileupload, Fileuploadnext
import random
import os.path

register = template.Library()


@register.filter
def to_and(value):
    files = Fileupload.objects.filter(owner=value)
    return files


@register.filter
def to_and2(value):
    files = Fileuploadnext.objects.filter(owner=value)
    return files


@register.filter
def remove_documents(value):
    value.name = value.name.replace("documents/", "")
    return value


@register.filter
def remove_next(value):
    value.name = value.name.replace("next/", "")
    return value


def gen_uniqueid():
    captial = chr(random.randint(65, 90))
    lower = chr(random.randint(97, 122))
    # l=['@','#','$','&']
    # special=random.choice(l)
    digits = random.randint(10000, 99999)
    digit = str(digits)
    result = captial + lower + digit
    return result


@register.filter
def unique_id(value):
    unique_id = value.name + value.report + value.task + str(value.date) + str(
        value.start_time
    ) + str(
        value.end_time
    ) + value.no_of_hours + value.team_lead + value.today_progress + value.concern + value.next_plan
    unique_id = unique_id.replace(".", "").replace("#", "").replace(
        " ", "").replace("`", "").replace("`", "").replace("!", "").replace(
            "@",
            "").replace("$", "").replace("%", "").replace("^", "").replace(
                "&", "").replace("*",
                                 "").replace("?", "").replace("(", "").replace(
                                     ")", "").replace(";", "").replace(":","").replace("'","").replace('"',"").replace("[","").replace("]","").replace("{","").replace("}","").replace("|","").replace("/","").replace("<","").replace(">","")
    return unique_id


@register.filter
def diff(value):
    extension = os.path.splitext(value.name)[1]
    if extension in [
            '.docx', '.ppt', 'pptx', '.html', '.doc', '.pdf', '.css', '.c',
            '.php', '.js', '.txt', '.xls', '.xlsx'
    ]:
        return "https://docs.google.com/gview?embedded=true&url=http://ins.justgetit.in/media/" + value.name
    # if extension in ['zip']:
    return "/media/" + value.name


@register.filter
def diff_docs(value):
    extension = os.path.splitext(value.name)[1]
    if extension in ['.docx', '.ppt']:
        return "https://docs.google.com/gview?embedded=true&url=http://ins.justgetit.in/media/next/" + value.name
    # if extension in ['zip']:
    return "/media/" + value.name


@register.filter
def id_generate(value):
    filename = value.filename
    owner = value.owner
    id_generated = unique_id(owner)
    id_generated = id_generated + str(filename).replace("documents", "")
    id_generated = id_generated.replace(".", "").replace("#", "").replace(
        " ", "").replace("`", "").replace("`", "").replace("!", "").replace(
            "@",
            "").replace("$", "").replace("%", "").replace("^", "").replace(
                "&",
                "").replace("*", "").replace("?", "").replace("(", "").replace(
                    ")",
                    "").replace(":",
                                "").replace("/",
                                            "").replace("_",
                                                        "").replace("-", "")
    return id_generated


@register.filter
def exe(value):
    extension = os.path.splitext(value.name)[1]
    return extension