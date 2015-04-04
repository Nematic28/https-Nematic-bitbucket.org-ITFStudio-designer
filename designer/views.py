from django.shortcuts import render_to_response
from django.template import RequestContext
from designer.models import Catalog, Image
from designer.models import FieldType


class DesignerForm:
    request = None

    def __init__(self, request):
        self.request = request

    def load(self):
        root = list(Catalog.objects.child(None).published().ordered().all())
        return self.__loader__(root)

    def __choice_from_form__(self, item):
        request = self.request
        list_of_elements = request.POST.getlist(item.input_name())
        if list_of_elements:
            if str(item.id) in list_of_elements:
                return True
        return False

    def __need_to_load__(self, item):

        if self.request.POST.getlist(item.input_name()):
            return self.__choice_from_form__(item)
        elif item.type.is_label():
            return True
        elif item.default:
            return True

        return False

    def __loader__(self, data):
        if not data:
            return []

        result = []
        child = []
        for item in data:
            result.append(item)

            if item.type.is_label():
                result += self.__loader__(item.child())
            else:
                if self.__need_to_load__(item):
                    child += item.child()
        result += self.__loader__(child)
        return result

    def get_checked_items(self):
        result = []
        for key, item in self.request.POST.lists():
            if 'designer' in key:
                result += item
        return list(map(int, result))


def catalog(request):
    form = DesignerForm(request)
    options = form.load()

    return render_to_response('designer/base.html', {
        "options": options,
        "checked_items": form.get_checked_items(),
        }, context_instance=RequestContext(request))