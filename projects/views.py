from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404

from .models import Project
from .forms import ProjectForm


@login_required
def update_project(request, object_id=None):
    """
    Updates or creates a project and returns a view with a project form.
    """
    project = None if object_id is None else Project.all.get(id=object_id)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            if project.created_by_id is None:
                project.created_by = request.user
            project.save()
    else:
        project_form = ProjectForm()

    return render(request, 'projects/projectinfo.inc', {
        'project_form': project_form,
        'project': project,
    })


@login_required
@require_http_methods(['POST'])
def delete_project(request, object_id=None):
    """Delete a project"""
    project = get_object_or_404(Project, id=object_id)
    project.delete()
    return _get_latest(request)


def _get_latest(request, current_project=None, errors=None,
                e_project_name=None):
    """ Returns a view that displays the latest 5 projects """

    latest = Project.all.order_by('-created_at')[:5]
    return render(request, 'projects/overview.inc', {
        'project': current_project,
        'latestprojects': latest,
        'errors': errors,
        'e_project_name': e_project_name,
    })
