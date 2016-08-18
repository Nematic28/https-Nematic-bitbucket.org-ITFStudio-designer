from designer.form.designer import DesignerForm
from django.shortcuts import render


def catalog(request, element_id=None, template_name='designer/base.html'):
    form = DesignerForm(request, template_name)
    return form.load(element_id)

def new3d(request):
    return render(request, '3d/index.html')