from django.shortcuts import render_to_response
from django.template import RequestContext
from designer.models import Catalog, Image


def catalog(request, this_id=None):
    if this_id is None:
        this = Catalog.objects.parent(this_id).published()[0]
    else:
        this = Catalog.objects.published().get(pk=this_id)

    branch = Catalog.objects.branch(this.left, this.right).published().ordered().all()

    options = []
    images = []
    # Добавляем все шаги на всех уровнях
    for node in branch:
        if node.images():
            images.append(node.images()[0])

        level = Catalog.objects.parent(node.root).published().ordered().all()
        for item in level:
            options.append(item)

    next_level = Catalog.objects.child(this.id).published().ordered().all()
    for item in next_level:
        options.append(item)

    return render_to_response('designer/base.html', {
        "options": options,
        "images": images,
        }, context_instance=RequestContext(request))