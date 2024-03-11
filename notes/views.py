"""Views for the notes app."""
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView
from .forms import SearchForm, NoteForm, EditNoteForm

from notes.models import NoteStore
from user.models import UserProfile


store = NoteStore()
notes = store.get()

def redirect_to_note_detail(request, note_id):
    """Redirect to the note details view."""
    return redirect(reverse("notes:details", args=[note_id]))


def home(request):
    """Home for my notes app."""
    template = get_template('notes/notes_page.html')
    context = {
        'sections_url': reverse('notes:sections'),
        'first_note_url': reverse('notes:details', args=[1]),
        'add_note_url': reverse('notes:add_note'),
    }
    rendered_template = template.render(context, request)
    return HttpResponse(rendered_template)


class SectionsView(View):

    def get(self, request):
        """Show the list of note sections."""
        template = get_template('notes/sections.html')
        context = {
            'web_framework': reverse("notes:by_section", args=["Web Frameworks"]),
            'set_up_dj': reverse("notes:by_section", args=["Setting up Django"]),
            'url_map': reverse("notes:by_section", args=["URL Mapping"]),
            'back_home': reverse("notes:home")
        }
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template)


class BySectionView(View):

    def get(self, request, section_name):
        """Show the notes of a section."""
        template = get_template('notes/by_section.html')
        notes_for_section = self._get_note_items_by_section(section_name)
        context = {
            'section_name': section_name,
            'notes': notes_for_section,
            'back_sections': reverse("notes:sections"),
        }
        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template)


    def _get_note_items_by_section(self, section_name):
        """Return the notes of a section as list items."""
        store = NoteStore()
        notes = store.get()
        return [f"{note['text']}" for note in notes
                if note["section"] == section_name]


class NoteDetails(TemplateView):
    """Note details."""

    template_name = "notes/details.html"

    def get_context_data(self, note_id):
        """Return the note data."""
        store = NoteStore()
        notes = store.get()
        if self.request.user.is_authenticated:
            current_user = self.request.user
            user_profile = UserProfile.objects.get(user=current_user)
        else:
            user_profile = None
        return {
            "id": note_id,
            "num_notes": len(notes),
            "note": notes[note_id - 1],
            'next_note': note_id + 1 if note_id < len(notes) else None,
            'previous_note': note_id - 1 if note_id > 1 else None,
            'user_profile': user_profile,
        }


class SearchResultsView(TemplateView):
    """Execute the search and show results."""

    template_name = "notes/search.html"

    def get_context_data(self, search_term):
        """Return the term and list of notes."""
        result = [(note['section'], note['text']) for note in notes if search_term.lower() in note['text'].lower()]
        return {
            "term": search_term,
            "result": result,
        }


def search_view(request):
    form = SearchForm()
    store = NoteStore()
    notes = store.get()
    result = []

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            section = form.cleaned_data['section']
            
            for note in notes:
                if section == 'All Categories' or not section: 
                    if search_term.lower() in note['text'].lower():
                        result.append((note['section'], note['text']))
                elif section:
                    if note['section'] == section:
                        if search_term.lower() in note['text'].lower():
                            result.append((note['section'], note['text']))
            
            return render(request, "notes/search.html", {"form": form, "term": search_term, "section": section, 'result': result})
        
    elif request.method == "GET":
        form = SearchForm()
        # search_term = request.GET.get('search_term', None)
        # section = request.GET.get('section', None)

    return render(request, "notes/search.html", {"form": form})


def ok_page(request):
    return render(request, "notes/ok.html")


class AddNote(View):

    def post(self, request):
        form = NoteForm(request.POST)
        if form.is_valid():
            section = form.cleaned_data['section']
            text = form.cleaned_data['text']
            store = NoteStore()
            notes = store.get()
            notes.append({'section': section, 'text': text})
            store.save(notes)
            return redirect('notes:ok_page')
        
    def get(self, request):
        form = NoteForm()
        return render(request, 'notes/add_note.html', {"form": form})


def edit_note(request, id):
    store = NoteStore()
    notes = store.get()
    note = notes[id - 1]
    
    if request.method == 'GET':
        form = EditNoteForm(initial={'text':note['text']})
        return render(request, 'notes/edit_note.html', {'form': form})
    
    elif request.method == 'POST':
        form = EditNoteForm(request.POST)
        if form.is_valid():
            note['text'] = form.cleaned_data['text']
            store.save(notes)
            return redirect('notes:details', id)


def vote(request, id):

    if request.method == "GET":
        store = NoteStore()
        notes = store.get()
        notes[id - 1]["voted"] += 1
        store.save(notes)

        current_user = request.user
        user_profile = UserProfile.objects.get(user=current_user) 
        user_profile.voted = True
        user_profile.save()

        context = {
        "id": id,
        "num_notes": len(notes),
        "note": notes[id - 1],
        'next_note': id + 1 if id < len(notes) else None,
        'previous_note': id - 1 if id > 1 else None,
        'user_profile': user_profile
        }
        return render(request, 'notes/details.html', context)
