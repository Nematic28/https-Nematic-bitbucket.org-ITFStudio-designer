__author__ = 'Vovkt'
from django.db import models


class CatalogQuerySet(models.QuerySet):
    def published(self):
        return self.filter(display=True)

    def branch(self, left, right):
        return self.filter(left__lte=left, right__gte=right)

    def child(self, catalog_id):
        return self.filter(root=catalog_id)

    def parent(self, this_id):
        return self.filter(root=this_id)

    def ordered(self):
        return self.order_by('left')


class CatalogManager(models.Manager):
    def get_queryset(self):
        return CatalogQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def branch(self, left, right):
        return self.get_queryset().branch(left, right)


    def child(self, catalog_id):
        return self.get_queryset().child(catalog_id)

    def parent(self, this_id):
        return self.get_queryset().parent(this_id)

    def ordered(self):
        return self.get_queryset().ordered()


class ImageQuerySet(models.QuerySet):
    def by_catalog_id(self, catalog_id):
        return self.filter(parent=catalog_id)

    def ordered(self):
        return self.order_by('number')


class ImageManager(models.Manager):
    def get_queryset(self):
        return ImageQuerySet(self.model, using=self._db)

    def by_catalog_id(self, catalog_id):
        return self.get_queryset().by_catalog_id(catalog_id)

    def ordered(self):
        return self.get_queryset().ordered()
