from django.shortcuts import render
from . import util
from encyclopedia.util import get_entry
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from markdown2 import Markdown
import random


class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))
    edit = forms.BooleanField(
        initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def view(request, title):
    if get_entry(title) is not None:
        markdown = Markdown()
        entry_view = get_entry(title)
        return render(request, "encyclopedia/view.html", {
            "title": title,
            "entry_available": True,
            "get_entry": markdown.convert(entry_view),
        })
    else:
        return render(request, "encyclopedia/view.html",{
            "title": title,
            "entry_available": False,
        })

def search(request):
    value = request.GET.get('q', '')
    markdown = Markdown()
    if (get_entry(value)) is not None:
        entry_view = util.get_entry(value)
        return render(request, "encyclopedia/search.html", {
            "title": value,
            "get_entry": markdown.convert(entry_view),
        })
    else:
        substring = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                substring.append(entry)

        if substring:
            return render(request, "encyclopedia/index.html", {
                "entries": substring
            })
        else:
            return render(request, "encyclopedia/no_search_result.html", {
                "value": value
            })


def new_page(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            edit = form.cleaned_data["edit"]
            if get_entry(title) is None or edit:
                util.save_entry(title, content)
                markdown = Markdown()
                entry_view = util.get_entry(title)
                return render(request, "encyclopedia/view.html", {
                    "title": title,
                    "get_entry": markdown.convert(entry_view),
                    "entry_available": get_entry(title) != None,
                })
            else:
                return render(request, "encyclopedia/existing_page_error.html", {
                    "title": title,
                    "content": content,
                })
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": NewEntryForm()
        })


def edit(request, title):
    page = get_entry(title)
    if page is None:
        return HttpResponseRedirect(reverse("view", {
            "entry_available": False,
        }))
    else:
        initial_dict = {
            "title": title,
            "content": get_entry(title),
            "edit": True,
        }
        form = NewEntryForm(initial=initial_dict)
        return render(request, "encyclopedia/new_page.html", {
            "form": form,
        })


def random_select(request):
    entries = util.list_entries()
    rand_entry = random.choice(entries)
    markdown = Markdown()
    entry_view = util.get_entry(rand_entry)

    return render(request, "encyclopedia/view.html", {
        "title": rand_entry,
        "entry_available": True,
        "get_entry": markdown.convert(entry_view),
    })
