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
    
if __name__=="__main__":
    main()
        