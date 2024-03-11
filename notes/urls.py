"""Notes URL Configuration."""
from django.urls import path
from .views import SectionsView, BySectionView, NoteDetails, SearchResultsView, AddNote

from notes.views import home, search_view, ok_page, edit_note, vote

app_name = "notes"
urlpatterns = [
    path('', home, name="home"),
    path('sections/', SectionsView.as_view(), name="sections"),
    path('sections/<section_name>/', BySectionView.as_view(), name="by_section"),
    path('<int:note_id>/', NoteDetails.as_view(), name="details"),
    path('<int:id>/edit/', edit_note, name="edit_note"),
    path('search/', search_view, name="search_view"),
    path('add/', AddNote.as_view(), name="add_note"),
    path('add/ok', ok_page, name="ok_page"),
    path('<int:id>/vote/', vote, name="vote"),
    path('<str:search_term>/', SearchResultsView.as_view(), name="search"),
]

