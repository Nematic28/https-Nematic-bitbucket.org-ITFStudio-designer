from django.shortcuts import render_to_response
from designer.models import Catalog


def catalog(request, item_id=None):
    if item_id is None:
        this = Catalog.objects.filter(root=item_id, display=True)[0]
    else:
        this = Catalog.objects.filter(pk=item_id, display=True)[0]

    branch = Catalog.objects.filter(display=True, left__lte=this.left, right__gte=this.right).order_by('left').all()

    options = []
    # Добавляем все шаги на всех уровнях
    for node in branch:
        level = Catalog.objects.filter(display=True, root=node.root).order_by('left').all()
        for item in level:
            options.append(item)

    next_level = Catalog.objects.filter(display=True, left__gt=this.left, right__lt=this.right).order_by('left').all()
    for item in next_level:
        options.append(item)

    return render_to_response('designer/base.html', {"options": options})