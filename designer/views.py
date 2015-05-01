from designer.form.designer import DesignerForm


def catalog(request, element_id=None, template_name='designer/base.html'):
    form = DesignerForm(request, template_name)
    return form.load(element_id)