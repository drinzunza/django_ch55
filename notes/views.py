from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Note, NoteComment
from django.urls import reverse_lazy
from .forms import NoteForm


# Create your views here.
"""
Class-based views:

View         = Generic View
ListView     = get a list of records
DetailView   = get a single (detail) record
CreateView   = create a new record
DeleteView   = remove a record
UpdateView   = modify an existing record
LoginView    = LogIn

"""

class NoteListView(ListView):
    model = Note
    template_name = "notes/list.html"

    def get_queryset(self):
        return super().get_queryset()

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/create.html"
    success_url = reverse_lazy('note_list')

    def get_context_data(self, **kwargs):
        #allow us to extend/modify the context pass to the template
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Note"
        return context
    
    def form_valid(self, form):
        # before saving the record
        # set the author to be the logged in user
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    

class NoteDetailView(DetailView):
    model = Note
    template_name = "notes/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # load all the comments for each note
        note = self.object
        comments = NoteComment.objects.filter(note=note).prefetch_related("author")
        context["comments"] = comments
        return context
    

class NoteUpdate(UpdateView):
    template_name = "notes/edit.html"
    model = Note
    success_url = reverse_lazy("note_list")
    fields = ["title", "content", "image", "release_date"]


def save_comment(request):
    note_id = request.POST.get('note_id')
    text = request.POST.get('content')
    user = request.user #logged in user

    note = Note.objects.get(id=note_id)

    comment = NoteComment.objects.create(
        note=note,
        content=text,
        author = user
    )

    comment.save()

    return redirect('note_details', pk=note_id)