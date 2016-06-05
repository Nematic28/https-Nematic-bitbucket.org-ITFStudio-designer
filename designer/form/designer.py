from designer.models import Catalog, Color, Texture, Selector
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import get_object_or_404


class DesignerForm:
    request = None
    template_name = None

    variables = {}

    checked_by_default = {}

    def __init__(self, request, template_name):
        self.request = request
        self.template_name = template_name

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

    def __load_steps__(self, root):
        self.variables['steps'] = Catalog.objects.child(root.root).published().ordered().all()

    def __load_root__(self, element_id):
        if element_id is None:
            item = Catalog.objects.child(element_id).published()[0]
        else:
            item = get_object_or_404(Catalog, pk=element_id, display=True)

        if item.type.is_link():
            self.template_name = 'designer/link.html'
        elif item.type.is_step():
            self.template_name = 'designer/step.html'
            self.__load_steps__(item)
        return item

    def load(self, element_id):
        item = self.__load_root__(element_id)

        child = Catalog.objects.child(element_id).published().ordered().all()
        branch = Catalog.objects.branch(item.left,item.right).ordered().all()

        for item in child:
            if item.type.is_step():
                return redirect('/designer/view/%s' % str(item.id))



        razdel = None
        for item in branch:
            if item.type.is_link():
                razdel = item


        options = self.__load_options__(child)
        images = self.__load_images__(options)
        if not images and item:
            for image in  item.images():
                if image.number in images:
                    images[image.number].append(image)
                else:
                    images[image.number] = [image]
        if razdel:
            self.variables['razdel'] = razdel
        self.variables['branch'] = branch
        self.variables['options'] = options
        self.variables['images'] = images
        items = self.get_checked_items_id()
        self.variables['checked_items'] = items
        self.variables['colors'] = self.__load_colors__(options)
        self.variables['textures'] = self.__load_textures__(options)
        self.variables['id_click'] = self.request.POST.get("id_click","")
        return self.render()

    def __load_colors__(self, data):
        color = {}
        for item in data:
            if item.color:
                if not item.color.id in color:
                    color[item.color.id] = item.color

        return color

    def __load_textures__(self, data):
        texture = {}
        for item in data:
            if item.texture:
                if not item.texture.id in texture:
                    texture[item.texture.id] = item.texture

        return texture

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

            if item.type.is_label() or item.type.is_popup():
                result += self.__load_options__(item.child().published().ordered().all())
            else:
                if self.__need_to_load__(item):
                    child += item.child().published().ordered().all()
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
        elif item.type.is_link():
            return False
        elif item.type.is_label():
            return True
        elif item.default:
            return True

        return False

    def render(self):
        return render(self.request, self.template_name, self.variables, context_instance=RequestContext(self.request))