from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task
from datetime import date


@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user)

    # -----------------------------
    # ADD TASK (with due date)
    # -----------------------------
    if request.method == "POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due_date")

        Task.objects.create(
            user=request.user,
            title=title,
            due_date=due_date if due_date else None
        )

        return redirect("home")

    # -----------------------------
    # DASHBOARD STATS
    # -----------------------------
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()

    completion_rate = 0
    if total_tasks > 0:
        completion_rate = int((completed_tasks / total_tasks) * 100)

    context = {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "completion_rate": completion_rate,
        "today": date.today(),   # for overdue check
    }

    return render(request, "home.html", context)


# -----------------------------
# DELETE TASK
# -----------------------------
@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.delete()
    return redirect("home")


# -----------------------------
# COMPLETE / TOGGLE TASK
# -----------------------------
@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect("home")


# -----------------------------
# EDIT TASK
# -----------------------------
@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.due_date = request.POST.get("due_date")
        task.save()
        return redirect("home")

    return render(request, "edit.html", {"task": task})
