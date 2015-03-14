from django.shortcuts import render_to_response
from designer.models import Catalog
from django.http import Http404


# def index(request, this_id=None):
#     if this_id is None:
#         this = None
#         parents = None
#     else:
#         try:
#             this = Catalog.objects.get(pk=this_id)
#             parents = this.parents()
#         except:
#             raise Http404('Data not found')
#
#     return render_to_response('designer/index.html', {
#         'this': this,
#         'data': Catalog.objects.filter(root=this_id, display=True),
#         'request': this_id,
#         'parents': parents,
#     })


def catalog(request):

    result = Catalog.objects.filter(root=None, display=True).order_by('left').all()
    for item in result:
        if item.type.machine == 'radio':
            item.checked = True
    return render_to_response('designer/base.html', {"options": result})