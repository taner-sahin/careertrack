from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Note
from .forms import NoteForm
from django.shortcuts import redirect


@login_required
def note_list(request):
    notes = Note.objects.filter(
        user=request.user,
    )

    context = {
        "notes": notes,
    }

    return render(
        request,
        "notes/note_list.html",
        context,
    )
    
@login_required
def note_detail(request, slug):
    note = get_object_or_404(
        Note,
        slug=slug,
        user=request.user,
    )

    context = {
        "note": note,
    }

    return render(
        request,
        "notes/note_detail.html",
        context,
    )
    
@login_required
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            return redirect("notes:note_list")

    else:
        form = NoteForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "notes/note_form.html",
        context,
    )
    
@login_required
def note_update(request, slug):
    note = get_object_or_404(
        Note,
        slug=slug,
        user=request.user,
    )

    if request.method == "POST":
        form = NoteForm(
            request.POST,
            instance=note,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "notes:note_detail",
                slug=note.slug,
            )

    else:
        form = NoteForm(
            instance=note,
        )

    context = {
        "form": form,
        "note": note,
    }

    return render(
        request,
        "notes/note_form.html",
        context,
    )
    
@login_required
def note_delete(request, slug):
    note = get_object_or_404(
        Note,
        slug=slug,
        user=request.user,
    )

    if request.method == "POST":
        note.delete()

        return redirect(
            "notes:note_list"
        )

    context = {
        "note": note,
    }

    return render(
        request,
        "notes/note_confirm_delete.html",
        context,
    )