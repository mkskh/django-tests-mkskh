"""Todo views."""
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render

from todo.models import todos

def details(request, todo_id):
        """Show a single todo matching the todo_id."""
        todo = todos[todo_id - 1]
        previous = todo_id - 1 if todo_id > 1 else None
        next = todo_id + 1 if todo_id < len(todos) else None

        response = {
                "todo": todo,
                "previous": previous,
                "next": next,
                }

        return render(request, "todo/details.html", response)