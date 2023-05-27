from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse
from django.contrib import messages
from markdown2 import Markdown
import random

from . import util

markdowner = Markdown()
# title_entries = []
searches = []

class SearchForm(forms.Form):
    search = forms.CharField(label="")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].widget.attrs['class'] = 'search'
        self.fields['search'].widget.attrs['placeholder'] = 'Search Encyclopedia'
        self.fields['search'].widget.attrs['name'] = 'q'
        
class CreateForm(forms.Form):
    create_title = forms.CharField(label="Create New Title:", widget=forms.TextInput(attrs={'class': "new-title", 'placeholder': 'Title'}))
    create_area = forms.CharField(label="Create New Form", widget=forms.Textarea(attrs={'class':'textarea', 'placeholder': 'Create New Entry Page'}))


def index(request):
    form = SearchForm()
    data = util.list_entries()
    if "create_title" not in request.session:
        request.session["create_title"] = data

    return render(request, "encyclopedia/index.html", {
        # "entries": request.session["create_title"],
        "entries": data,
        "form": form
    })
    
def title(request, title):
    if title not in util.list_entries():
        raise Http404
    pre_titles = util.get_entry(title)
    titles = markdowner.convert(pre_titles)

    return render(request, "encyclopedia/title.html", {
        "titles": titles,
        "title": title,
        "form": SearchForm()
    })
        
def search(request):
    form = SearchForm(request.POST)
    titles = util.get_entry(form)
    
    if request.method == "POST":
        
        if form.is_valid():
            searched = form.cleaned_data['search']
            searches.append(searched)
            
            if titles:
                return HttpResponseRedirect(reverse("title", args=[searched] ))
            else:
                title_list = util.list_entries()
                title_entries = [title_input for title_input in title_list if searched in title_list]
                
                # for title_input in title_list:
                #     if searched.lower() in title_list.lower() or title_list.lower() in searched.lower():
                #         title_entries.append[title_input]
                                  
                return render(request, "encyclopedia/search.html", {
                    "title_entries": title_entries,
                    "form": SearchForm(),
                    "title": searches
                })
    else:
        return HttpResponseRedirect(reverse("index"))
    
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["create_title"]
            area = form.cleaned_data["create_area"]
            
            if title.lower() in [i.lower() for i in util.list_entries()]:
                messages.warning(request, f"The page {title} already exists. Please choose a different title")
                return render(request, "encyclopedia/new.html", {
                "create_form": form
            })
                
            else:
                # marked_area = markdowner.convert(area)
                created = util.save_entry(title, area)
                listed = util.list_entries()
                listed.append(created)

            return HttpResponseRedirect(reverse("title", args=[title]))
        else:
            return render(request, "encyclopedia/new.html", {
                "create_form": form
            })
    
    else: 
        return render(request, "encyclopedia/new.html", {
            "create_form": CreateForm(),
            "form": SearchForm()
        })
        
def update(request, title):
    if request.method == "POST":
        form = CreateForm(request.POST)

        if form.is_valid():
            update_title = form.cleaned_data["create_title"]
            update_area = form.cleaned_data["create_area"]
            
            util.save_entry(update_title, update_area)
            
            return HttpResponseRedirect(reverse("title",args=[title]))
    else:
        entry = util.get_entry(title)

        return render(request, "encyclopedia/update.html", {
            "update_form": CreateForm({"create_title": title, "create_area": entry }),
            "form": SearchForm(),
            "title": title
        })

def random_page(request):
    pages = util.list_entries()
    found = random.choice(pages)
    return redirect("title", found)
    