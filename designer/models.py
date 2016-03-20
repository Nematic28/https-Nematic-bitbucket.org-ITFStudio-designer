from django.db import models
from django.utils import timezone
from designer.scopes import CatalogManager, ImageManager
import catalog.settings
import random
import string


class Helper():
    @staticmethod
    def get_extension(filename):
        if '.' in filename:
            extension = filename.split('.')[-1]
        else:
            extension = 'png'
        return extension

    @staticmethod
    def get_random_string(length=10):
        rand = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
        return rand

    @staticmethod
    def catalog_main_image(instance, filename):
        extension = Helper.get_extension(filename)
        parent = instance.parent.id
        new_name = Helper.get_random_string()
        return '%s/%s_%s.%s' % (catalog.settings.DESIGNER_IMAGE_MAIN, str(parent), new_name, extension)

    @staticmethod
    def dop_image(instance, filename):
        extension = Helper.get_extension(filename)
        new_name = Helper.get_random_string()
        return '%s/%s.%s' % (catalog.settings.DESIGNER_IMAGE_MAIN + '/add', new_name, extension)

    @staticmethod
    def catalog_logo(instance, filename):
        extension = Helper.get_extension(filename)

        if instance.id is None:
            if Catalog.objects.all().count():
                catalog_id = Catalog.objects.order_by('-id')[0].id + 1
            else:
                catalog_id = 1
        else:
            catalog_id = instance.id

        new_name = Helper.get_random_string()
        return '%s/%s_%s.%s' % (catalog.settings.DESIGNER_IMAGE_LOGO, str(catalog_id), new_name, extension)

class Selector(models.Model):
    class Meta:
        verbose_name = 'иконка переключателя'
        verbose_name_plural = 'иконки переключателя'
    name = models.CharField('Название', max_length=255)
    icon = models.ImageField('Иконка', upload_to=Helper.dop_image, blank=True)
    def __str__(self):
        return self.name

class Color(models.Model):
    class Meta:
        verbose_name = 'цвет'
        verbose_name_plural = 'цвета'
    name = models.CharField('Название', max_length=255)
    icon = models.ImageField('Иконка', upload_to=Helper.dop_image, blank=True)
    def __str__(self):
        return self.name

class Texture(models.Model):
    class Meta:
        verbose_name = 'текстура'
        verbose_name_plural = 'текстуры'
    name = models.CharField('Название', max_length=255)
    def __str__(self):
        return self.name


class FieldType(models.Model):

    TYPE_RADIO = 'radio'
    TYPE_LABEL = 'label'
    TYPE_LINK = 'link'
    TYPE_STEP = 'step'

    class Meta:
        verbose_name = 'тип'
        verbose_name_plural = 'типы'

    name = models.CharField('Название', max_length=255, null=False)
    machine = models.CharField('Машинное имя', max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name

    def is_label(self):
        return self.machine == self.TYPE_LABEL

    def is_link(self):
        return self.machine == self.TYPE_LINK

    def is_step(self):
        return self.machine == self.TYPE_STEP
    def is_popup(self):
        return (self.machine == 'popup_header' or self.machine == 'popup_footer')

    def template(self):
        return '%s/%s/%s.%s' % ('designer', 'types', self.machine, 'html')


class Catalog(models.Model):

    class Meta:
        verbose_name = 'элемент'
        verbose_name_plural = 'элементы'

    right = models.IntegerField(default=0)
    left = models.IntegerField(default=0)
    root = models.ForeignKey('self', blank=True, null=True, help_text='Three of steps')
    type = models.ForeignKey(FieldType, verbose_name='Тип элемента', null=False,
                             help_text='Тип элемента для отображения')
    selector = models.ForeignKey(Selector, verbose_name='Иконка переключателя', null=True, blank=True,
                             help_text='Иконка переключателя из справочника')
    color = models.ForeignKey(Color, verbose_name='Цвет', null=True, blank=True,
                             help_text='Цвет для фильтрации')
    texture = models.ForeignKey(Texture, verbose_name='Текстура', null=True, blank=True,
                             help_text='Текстура для фильтрации')

    date_create = models.DateTimeField('Дата создания', auto_now_add=True)
    date_modify = models.DateTimeField('Посл. изменения', auto_now_add=True)
    name = models.CharField('Название', max_length=255)
    layer = models.IntegerField('Номер слоя', default=1000)

    default = models.BooleanField('Отображать по умолчанию',
                                  default=False,
                                  help_text='Отображать по умолчанию если не выбрано другое')
    display = models.BooleanField('Опубликовано', default=True, help_text='Отображать на сайте или нет')

    icon = models.ImageField('Иконка', upload_to=Helper.catalog_logo, blank=True)

    objects = CatalogManager()

    def __str__(self):
        return self.name

    def three_name(self):
        return "%s %s" % ('--' * self.level(), self.name)

    def images(self):
        return Image.objects.by_catalog_id(self.id).ordered().all()

    def count_images(self):
        return Image.objects.by_catalog_id(self.id).count()
    count_images.short_description = "Кол-во изображений"

    def input_name(self):
        return 'designer-%s' % self.root_id

    def form_name(self):
        return 'designer_%s' % self.id

    # Ф-и работы с деревом
    def level(self):
        return Catalog.objects.branch(self.left, self.right).count()

    def child(self):
        return Catalog.objects.child(self.id).ordered().all()

    def branch(self):
        return Catalog.objects.branch(self.left, self.right).all()

    def up(self):
        item_to_up = Catalog.objects.get(pk=self.pk)
        items_to_up = Catalog.objects.filter(left__gte=item_to_up.left, right__lte=item_to_up.right).ordered().all()
        shift_to_down = len(items_to_up) * 2

        if not Catalog.objects.filter(root=item_to_up.root, right=item_to_up.left - 1).count():
            return
        item_before = Catalog.objects.get(root=item_to_up.root, right=item_to_up.left - 1)

        if item_to_up.level() != item_before.level():
            return
        items_before = Catalog.objects.filter(left__gte=item_before.left, right__lte=item_before.right).ordered().all()
        shift_to_up = len(items_before) * 2

        for item in items_to_up:
            item.left -= shift_to_up
            item.right -= shift_to_up
            item.save()

        for item in items_before:
            item.left += shift_to_down
            item.right += shift_to_down
            item.save()

    def down(self):
        item_to_down = Catalog.objects.get(pk=self.pk)
        items_to_down = Catalog.objects.filter(left__gte=item_to_down.left, right__lte=item_to_down.right).ordered().all()
        shift_to_up = len(items_to_down) * 2

        if not Catalog.objects.filter(root=item_to_down.root, left=item_to_down.right + 1).count():
            return
        item_after = Catalog.objects.get(root=item_to_down.root, left=item_to_down.right + 1)

        if item_to_down.level() != item_after.level():
            return

        items_after = Catalog.objects.filter(left__gte=item_after.left, right__lte=item_after.right).ordered().all()
        shift_to_down = len(items_after) * 2

        for item in items_to_down:
            item.left += shift_to_down
            item.right += shift_to_down
            item.save()

        for item in items_after:
            item.left -= shift_to_up
            item.right -= shift_to_up
            item.save()

    def delete(self, using=None):
        for image in self.images():
            image.delete()

        self.icon.delete(save=False)

        if Catalog.objects.filter(pk=self.id).count():
            for child in self.child():
                child.delete()

            this = Catalog.objects.filter(pk=self.id)[0]
            super(Catalog, self).delete(using)

            Catalog.objects.select_for_update().filter(left__gte=this.left)\
                .update(left=models.F('left') - 2)
            Catalog.objects.select_for_update().filter(right__gte=this.right)\
                .update(right=models.F('right') - 2)

    def insert(self):
        if isinstance(self.root, Catalog):  # Под категория
            Catalog.objects.select_for_update().filter(left__gt=self.root.right) \
                .update(left=models.F('left') + 2)
            Catalog.objects.select_for_update().filter(right__gte=self.root.right) \
                .update(right=models.F('right') + 2)
            self.left = self.root.right
            self.right = self.root.right + 1
        else:  # Рутовая категория
            if Catalog.objects.count() > 0:  # Добавляем в конец
                obj = Catalog.objects.filter().order_by('-right')[0]
                self.left = obj.right + 1
                self.right = obj.right + 2
            else:  # По умолчанию
                self.left = 1
                self.right = 2

    def delete_icon(self):
        if not self.icon:
            this = Catalog.objects.get(pk=self.pk)
            if this and this.icon:
                this.icon.delete(save=False)

    def update(self):
        # Если поменялись данные
        if Catalog.objects.filter(pk=self.id)[0].root != self.root:
            # Данные для перемещения
            count = 2 * Catalog.objects.filter(left__gte=self.left, right__lte=self.right).count()
            if isinstance(self.root, Catalog):
                rr = self.root.right
            else:
                rr = Catalog.objects.order_by('-right')[0].right + 1

            before = True if rr < self.left else False
            if before:
                shift = rr - self.right - 1
                add = count
            else:
                shift = rr - self.left
                add = 0

            # Выделяем место
            Catalog.objects.select_for_update().filter(left__gte=rr) \
                .update(left=models.F('left') + count)
            Catalog.objects.select_for_update().filter(right__gte=rr) \
                .update(right=models.F('right') + count)

            # Перенос данных
            Catalog.objects.select_for_update() \
                .filter(left__gte=self.left + add,
                        right__lte=self.right + add) \
                .update(left=models.F('left') + shift, right=models.F('right') + shift)

            # Удаление старого пространства
            Catalog.objects.select_for_update().filter(left__gte=(self.left + count)) \
                .update(left=models.F('left') - count)
            Catalog.objects.select_for_update().filter(right__gt=self.right) \
                .update(right=models.F('right') - count)

            obj = Catalog.objects.filter(pk=self.pk)[0]
            self.left = obj.left
            self.right = obj.right

        self.delete_icon()

    def save(self, *args, **kwargs):
        # Change left and right
        if self.id is None:                         # Create
            self.insert()
        else:                                       # Update
            self.update()

        self.date_modify = timezone.now()
        super(Catalog, self).save(*args, **kwargs)


class Image(models.Model):

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    parent = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    number = models.IntegerField('Номер', help_text='Номер положения', default=1)
    file = models.ImageField('Изображение',
                             upload_to=Helper.catalog_main_image,
                             )
    objects = ImageManager()

    def __str__(self):
        return 'Разворот %s' % self.number

    def thumbnail(self):
        return u'<img src="%s" style="max-width:100px; max-height:100px" />' % self.file.url
    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True

    def layer(self):
        return self.parent.layer

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.id:
            try:
                old = Image.objects.get(pk=self.id).file
                new = self.file
                if old.url != new.url:
                    old.delete(save=False)
            except:
                pass
        super(Image, self).save(*args, **kwargs)
