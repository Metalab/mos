from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404

from .models import Project
from .forms import ProjectForm


@login_required
def update_project(request, new, object_id=None):
    """ Updates or add a project and returns a view with a project form """

    if not new:
        project = Project.all.get(id=object_id)
    else:
        project = None

    # set event_error_id to '', if an error occurs it will be the error id
    project_error_id = ''

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)

        if project_form.is_valid():
            project_data = project_form.save(commit=False)

            if new:
                project_data.created_by = request.user
                project_data.save()
                project = Project.objects.get(id=project_data.id)
            else:
                project_data.save()

        else:
            project_error_id = project.id
    else:
        project_form = ProjectForm

    return render(request, 'projects/projectinfo.inc', {
        'project_error_id': project_error_id,
        'project_form': project_form,
        'project': project,
        'new': not project.pk,
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
