from django.db import models
from django.utils import timezone
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
                id = Image.objects.all().order_by('-id')[0].id + 1
            else:
                id = 1
        else:
            id = instance.id
        rand = ''.join(random.choice(string.ascii_lowercase) for i in range(10))

        return '%s/%s_%s.%s' % (catalog.settings.DESIGNER_IMAGE, str(id), rand, extension)


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

    __child__ = None
    __level__ = None
    __branch__ = None
    __images__ = None
    __parents__ = None

    def __str__(self):
        return self.name

    def three_name(self):
        return "%s %s" % ('-' * self.level(), self.name)

    def images(self):
        if self.__images__ is None:
            self.__images__ = Image.objects.filter(parent=self.id).count()
        return self.__images__
    images.integer = True
    images.short_description = 'Кол-во изображений'

    # Ф-и работы с деревом
    def level(self):
        if self.__level__ is None:
            self.__level__ = Catalog.objects.filter(left__lte=self.left, right__gte=self.right).count()
        return self.__level__

    def child(self):
        if self.__child__ is None:
            self.__child__ = Catalog.objects.filter(left__gt=self.left, right__lt=self.right, root=self.id)
        return self.__child__

    def branch(self):
        if self.__branch__ is None:
            self.__branch__ = Catalog.objects.filter(left__gt=self.left, right__lt=self.right)
        return self.__branch__

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