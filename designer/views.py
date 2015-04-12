from django.shortcuts import render
from django.template import RequestContext
from designer.form.designer import DesignerForm


def catalog(request, element_id=None, template_name='designer/base.html'):
    form = DesignerForm(request, template_name)
    form.load(element_id)

    return render(request, form.get_template(), {
        "options": form.get_options(),
        "images": form.get_images(),
        "checked_items": form.get_checked_items_id(),
        }, context_instance=RequestContext(request))