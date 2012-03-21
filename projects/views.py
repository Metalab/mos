from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from mos.projects.models import Project
from mos.projects.forms import ProjectForm


@login_required
def update_project(request, new, object_id=None):
    """ Updates or add a project and returns a view with a project form """

    if not request.POST or not request.user.is_authenticated():
        return

    if not new:
        project = Project.all.get(id=object_id)
    else:
        project = Project()

    project_error_id = '' # set event_error_id to '', if an error
                          # occurs it will be the error id

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

    return render_to_response('projects/projectinfo_nf.inc',
            {'project_error_id': project_error_id,
             'project_form': project_form,
             'project': project,
             'new': not project.pk,
             }, context_instance=RequestContext(request))


@login_required
def delete_project(request, object_id=None):
    """ Deletes the project with object_id """
    if not request.POST or not object_id \
            or not request.user.is_authenticated():
        return

    project = Project.all.get(id=object_id)

    project.delete()
    project.save()

    return _get_latest(request)


def _get_latest(request, current_project=None, errors=None,
                e_project_name=None):
    """ Returns a view that displays the latest 5 projects """

    latest = Project.all.order_by('-created_at')[:5]
    return render_to_response('projects/overview.inc',
                              {'project': current_project,
                               'latestprojects': latest,
                               'errors': errors,
                               'e_project_name': e_project_name,
                               }, context_instance=RequestContext(request))
