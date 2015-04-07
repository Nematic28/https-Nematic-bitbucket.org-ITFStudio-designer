from designer.models import Catalog


class DesignerForm:
    request = None

    options = []
    images = []

    checked_by_default = {}

    def __init__(self, request):
        self.request = request

    def get_checked_items_id(self):
        checked_by_default = self.checked_by_default
        result = []
        for key, item in self.request.POST.lists():
            if 'designer' in key:
                if key in checked_by_default:
                    checked_by_default.pop(key)
                result += item

        result += list(checked_by_default.values())

        return list(map(int, result))

    def load(self):
        root = list(Catalog.objects.child(None).published().ordered().all())
        self.options = self.__load_options__(root)
        self.images = self.__load_images__(self.options)

    def get_options(self):
        return self.options

    def get_images(self):
        return self.images

    def __load_images__(self, data):
        items = self.__get_checked_items__(data)
        view = {}
        for item in items:
            for image in item.images():
                if image.number in view:
                    view[image.number].append(image)
                else:
                    view[image.number] = [image]
        return view

    def __get_checked_items__(self, data):
        checked_items_id = self.get_checked_items_id()
        result = []
        for item in data:
            if item.id in checked_items_id:
                result.append(item)

        return result

    def __load_options__(self, data):
        if not data:
            return []

        result = []
        child = []
        for item in data:
            if item.default:
                self.checked_by_default[item.input_name()] = item.id
            result.append(item)

            if item.type.is_label():
                result += self.__load_options__(item.child())
            else:
                if self.__need_to_load__(item):
                    child += item.child()
        result += self.__load_options__(child)
        return result

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