# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import helpers
from django.shortcuts import render
from django.utils.text import mark_safe, capfirst
from django.utils.html import escape
from django import forms
from django import template
from .models import Catalog, Image, FieldType
# Register your models here.

admin.AdminSite.site_title = 'Панель администратора'
admin.AdminSite.site_header = 'Панель администратора'


class CatalogImagesInline(admin.TabularInline):
    model = Image
    extra = 1
    max_num = 3
    readonly_fields = ('thumbnail',)


class CatalogChoiceRootField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return "%s %s" % ('-' * obj.level(), obj.name)


class CatalogAdminForm(forms.ModelForm):
    root = CatalogChoiceRootField(queryset=Catalog.objects.all().order_by('left'),
                                  required=False,
                                  help_text='Three of category')

    def clean_root(self):
        root = self.cleaned_data['root']
        obj = self.instance
        if isinstance(root, Catalog):
            if root.left >= obj.left and root.right <= obj.right:
                raise forms.ValidationError('Choice other')
        return root


class CatalogAdmin(admin.ModelAdmin):

    form = CatalogAdminForm

    fieldsets = [
        ('Основное',    {'fields': ['name', 'root', 'type']}),
        ('Информация',  {'fields': [('date_modify', 'date_create')]}),
        ('Настройки',   {'fields': ['default', 'display', 'layer']}),
    ]

    list_display = ('three_name', 'count_images', 'date_create', 'date_modify', 'display')
    list_filter = ('date_create', 'date_modify', 'display')
    readonly_fields = ('date_create', 'date_modify')
    ordering = ('left',)

    actions = ['delete_list', 'hide_list', 'show_list']
    inlines = [CatalogImagesInline]

    save_as = True

    def delete_list(self, request, queryset):
        opts = self.model._meta

        deletable_objects = []
        for obj in queryset:
            deletable_objects.append([mark_safe(u'%s: <a href="%s/">%s</a>' % (escape(capfirst(opts.verbose_name)), obj.pk, escape(obj))), []])

        if request.POST.get('post'):
            n = queryset.count()
            if n:
                for obj in queryset:
                    obj_display = obj
                    obj.delete()

                self.message_user(request, ("Successfully deleted %(count)d %(items)s.") % {
                    "count": n, "items": 1
                })
            # Return None to display the change list page again.
            return None
        context = {
            "title": "Вы уверены?",
            "deletable_objects": deletable_objects,
            'queryset': queryset,
            "opts": opts,
            'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
        }
        return render(request, 'admin/test.html', context, context_instance=template.RequestContext(request))
    delete_list.short_description = 'Удалить выбранные'

    def hide_list(self, request, queryset):
        for obj in queryset:
            if obj.display is True:
                obj.display = False
                obj.save()
    hide_list.short_description = 'Скрыть выбранные'

    def show_list(self, request, queryset):
        for obj in queryset:
            if obj.display is False:
                obj.display = True
                obj.save()
    show_list.short_description = 'Опубликовать выбранные'

    def get_actions(self, request):
        actions = super(CatalogAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        obj.delete()


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(FieldType)