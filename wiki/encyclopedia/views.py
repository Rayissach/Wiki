from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

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
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['create_area'].widget.attrs['class'] = 'new_title'
    #     self.fields['create_area'].widget.attrs['placeholder'] = 'Create New Entry Page'
    #     self.fields['create_title'].widget.attrs['placeholder'] = 'Title'
    #     self.fields['create_title'].widget.attrs['class'] = 'textarea', 'modtext'


def index(request):
    form = SearchForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": form
    })
    
def title(request, title):
    return render(request, "encyclopedia/title.html", {
        "titles": util.get_entry(title)
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
    # form = CreateForm(request.POST)
    
    # if request.method == "POST":
    #     if form.is_valid():
    #         print("Hello World")
            
    # else: 
    return render(request, "encyclopedia/new.html", {
        "create_form": CreateForm(),
        "form": SearchForm()
    })
        