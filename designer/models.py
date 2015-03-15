from django.db import models
from django.utils import timezone
from designer.scopes import CatalogManager, ImageManager
import catalog.settings
import random
import string


class Helper():
    @staticmethod
    def new_image_name(instance, filename):
        if '.' in filename:
            extension = filename.split('.')[-1]
        else:
            extension = 'png'
        if instance.id is None:
            if Image.objects.all().count():
                image_id = Image.objects.all().order_by('-id')[0].id + 1
            else:
                image_id = 1
        else:
            image_id = instance.id
        rand = ''.join(random.choice(string.ascii_lowercase) for i in range(10))

        return '%s/%s_%s.%s' % (catalog.settings.DESIGNER_IMAGE, str(image_id), rand, extension)


class FieldType(models.Model):

    name = models.CharField('Название', max_length=255, null=False)
    machine = models.CharField('Машинное имя', max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name

    def template(self):
        return '%s/%s/%s.%s' % ('designer', 'type', self.machine, 'html')


class Catalog(models.Model):

    class Meta:
        verbose_name = 'элемент'
        verbose_name_plural = 'элементы'

    right = models.IntegerField(default=0)
    left = models.IntegerField(default=0)
    root = models.ForeignKey('self', blank=True, null=True, help_text='Three of steps')
    type = models.ForeignKey(FieldType, verbose_name='Тип элемента', null=False,
                             help_text='Тип элемента для отображения')

    date_create = models.DateTimeField('Дата создания', auto_now_add=True)
    date_modify = models.DateTimeField('Посл. изменения', auto_now_add=True)
    name = models.CharField('Название', max_length=255)
    layer = models.IntegerField('Номер слоя', default=1000)

    default = models.BooleanField('Отображать по умолчанию',
                                  default=False,
                                  help_text='Отображать по умолчанию если не выбрано другое')
    display = models.BooleanField('Опубликовано', default=True, help_text='Отображать на сайте или нет')

    objects = CatalogManager()

    def __str__(self):
        return self.name

    def three_name(self):
        return "%s %s" % ('-' * self.level(), self.name)

    def images(self):
        return Image.objects.by_catalog_id(self.id).ordered().all()

    def count_images(self):
        return Image.objects.by_catalog_id(self.id).count()
    count_images.short_description = "Кол-во изображений"

    # Ф-и работы с деревом
    def level(self):
        return Catalog.objects.branch(self.left, self.right).count()

    def child(self):
        return Catalog.objects.child(self.id).all()

    def branch(self):
        return Catalog.objects.branch(self.left, self.right).all()

    def delete(self, using=None):
        if Catalog.objects.filter(pk=self.id).count():
            this = Catalog.objects.filter(pk=self.id)[0]
            self.left = this.left
            self.right = this.right
            count = Catalog.objects.filter(left__gte=self.left, right__lte=self.right).count()
            Catalog.objects.filter(left__gte=self.left, right__lte=self.right).delete()
            Catalog.objects.select_for_update().filter(left__gte=self.left)\
                .update(left=models.F('left') - 2 * count)
            Catalog.objects.select_for_update().filter(right__gte=self.right)\
                .update(right=models.F('right') - 2 * count)

    def save(self, *args, **kwargs):
        # Change left and right
        if self.id is None:                         # Create
            if isinstance(self.root, Catalog):      # Под категория
                Catalog.objects.select_for_update().filter(left__gt=self.root.right)\
                    .update(left=models.F('left') + 2)
                Catalog.objects.select_for_update().filter(right__gte=self.root.right)\
                    .update(right=models.F('right') + 2)
                self.left = self.root.right
                self.right = self.root.right + 1
            else:                                   # Рутовая категория
                if Catalog.objects.count() > 0:     # Добавляем в конец
                    obj = Catalog.objects.filter().order_by('-right')[0]
                    self.left = obj.right + 1
                    self.right = obj.right + 2
                else:                               # По умолчанию
                    self.left = 1
                    self.right = 2
        else:                                       # Update
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
                Catalog.objects.select_for_update().filter(left__gte=rr)\
                    .update(left=models.F('left') + count)
                Catalog.objects.select_for_update().filter(right__gte=rr)\
                    .update(right=models.F('right') + count)

                # Перенос данных
                Catalog.objects.select_for_update()\
                    .filter(left__gte=self.left + add,
                            right__lte=self.right + add)\
                    .update(left=models.F('left') + shift, right=models.F('right') + shift)

                # Удаление старого пространства
                Catalog.objects.select_for_update().filter(left__gte=(self.left + count))\
                    .update(left=models.F('left') - count)
                Catalog.objects.select_for_update().filter(right__gt=self.right)\
                    .update(right=models.F('right') - count)

                obj = Catalog.objects.filter(pk=self.pk)[0]
                self.left = obj.left
                self.right = obj.right

        self.date_modify = timezone.now()
        super(Catalog, self).save(*args, **kwargs)


class Image(models.Model):

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    parent = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    number = models.IntegerField('Номер', help_text='Номер положения', default=1)
    file = models.ImageField('Изображение',
                             upload_to=Helper.new_image_name,
                             )
    objects = ImageManager()

    def thumbnail(self):
        return u'<img src="/%s" style="max-width:100px; max-height:100px" />' % self.file.url
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
