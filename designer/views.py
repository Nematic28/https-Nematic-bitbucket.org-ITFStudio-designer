from django.shortcuts import render_to_response
from django.template import RequestContext
from designer.form.designer import DesignerForm


def catalog(request):
    form = DesignerForm(request)
    form.load()

    return render_to_response('designer/base.html', {
        "options": form.get_options(),
        "images": form.get_images(),
        "checked_items": form.get_checked_items_id(),
        }, context_instance=RequestContext(request))