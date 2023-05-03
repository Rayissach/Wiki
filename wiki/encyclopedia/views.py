from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        self.fields['search'].widget.attrs['class'] = 'search'
        self.fields['search'].widget.attrs['placeholder'] = 'Search Encyclopedia'
        self.fields['search'].widget.attrs['name'] = 'q'


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
            # searched = form.cleaned_data['search']
            # searched.append['search']
            if form == titles:
                return HttpResponseRedirect("/wiki/")
        elif form.contains(titles):
                return render(request, "encyclopedia/search.html", {
                    "entries": titles
                })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": titles,
                "form": form
            })
            
        
        # if form.is_valid():
        #     searched = form.cleaned_data['search']
        #     searched.append['search']
        #     return HttpResponseRedirect("/title.html")
    else:
        return render(request, "encyclopedia/index.html", {
            "form": form,
            "queried": util.get_entry()
        })
        