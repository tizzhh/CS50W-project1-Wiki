from audioop import reverse
from html import entities
import re, os.path, random
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    entry = util.get_entry(name)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "name": name
    })

def search(request):
    # https://stackoverflow.com/questions/53920004/add-q-searchterm-in-django-url
    name = request.GET.get('q')
    entry = util.get_entry(name)
    if entry == None:
        match = []
        entries = util.list_entries()
        for entry in entries:
            if name.lower() in entry.lower():
                match.append(entry)
        return render(request, "encyclopedia/search_results.html", {
            "entries": match
        })
    '''entries = util.list_entries()
    for entry in entries:
        if name in entry:
            name = entry'''
    return HttpResponseRedirect(f"../wiki/{name}")

    '''entry = util.get_entry(name)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "name": name.capitalize()
    })'''

def newpage(request):
    return render(request, "encyclopedia/newpage.html")

def checkentry(request):
    title = request.GET.get('title')
    entry = request.GET.get('entry')
    # https://www.pythontutorial.net/python-basics/python-check-if-file-exists/
    if os.path.exists(f"entries/{title}.md"):
        return render(request, "encyclopedia/newpage.html", {
            "check": True
        })
    with open(f"entries/{title}.md", "w") as file:
        file.write(entry)
    return HttpResponseRedirect(f"../wiki/{title}")

def editpage(request, name):
    return render(request, "encyclopedia/edit_page.html", {
        "name": name,
        "entry": util.get_entry(name)
    })

def saveentry(request):
    title = request.GET.get('title')
    entry = request.GET.get('entry')
    with open(f"entries/{title}.md", "w") as file:
        file.write(entry)
    return HttpResponseRedirect(f"../wiki/{title}")

def randompage(request):
    entries = util.list_entries()
    return HttpResponseRedirect(f"../wiki/{random.choice(entries)}")