from designer.form.designer import DesignerForm
from django.shortcuts import render


def catalog(request, element_id=None, template_name='designer/base.html'):
    form = DesignerForm(request, template_name)
    return form.load(element_id)

def new3d(request):
    return render(request, 'static/3d/static/new3d/index.html')