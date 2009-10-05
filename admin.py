#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db import models
from nopsa.demoapp.models import *
from nopsa.demoapp.widgets import jQCalendarWidget
import datetime

class WorkerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('',),
            'fields': (('surname', 'forename'), 'active', 'hourly_salary', 'comment')
        }),
    )
    
    list_display = ('surname', 'forename', 'active',)
    list_filter = ('active',)
    search_fields = ('surname', 'forename',)

class Customer_groupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('',),
            'fields': ('name', 'active', 'comment')
        }),
    )

    list_display = ('name', 'active',)
    list_filter = ('active',)
    search_fields = ('name',)    

class CustomerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'customer_group', 'billing_address', 'delivery_address', 'email', 'default_delivery_term', 'default_payment_term', 'active', 'comment')
        }),
    )

    list_display = ('name', 'customer_group', 'active',)
    list_filter = ('customer_group', 'active',)
    search_fields = ('name',)

class Product_groupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('',),
            'fields': ('name', 'active', 'comment')
        }),
    )

    list_display = ('name', 'active',)
    list_filter = ('active',)
    search_fields = ('name',)    

class Delivery_termAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('',),
            'fields': ('name', 'active', 'comment')
        }),
    )

    list_display = ('name', 'active',)
    list_filter = ('active',)

class Payment_termAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('',),
            'fields': ('name', 'active', 'comment')
        }),
    )

    list_display = ('name', 'active',)
    list_filter = ('active',)

class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('',),
            'fields': ('name', 'product_group', 'active', 'comment')
        }),
    )

    list_display = ('name', 'product_group', 'active',)
    list_filter = ('product_group', 'active',)
    search_fields = ('name',)    

class ShiftAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('',),
            'fields': ('name', 'start_time', 'end_time', 'active', 'comment')
        }),
    )

    list_display = ('name', 'start_time', 'end_time', 'active',)
    list_filter = ('active',)

class Salary_classAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('',),
            'fields': ('name', 'salary_multiplier', 'active', 'comment')
        }),
    )

    list_display = ('name', 'active',)
    list_filter = ('active',)

class Work_phaseAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('',),
            'fields': ('name', 'work_phase_type', 'active', 'comment')
        }),
    )

    list_display = ('name', 'work_phase_type', 'active',)
    list_filter = ('work_phase_type', 'active',)

class Sales_order_lineInline(admin.TabularInline):
    model = Sales_order_line
    exclude = ['price', 'source', 'active', ]
    verbose_name = 'myyntitilausrivi'
    verbose_name_plural = 'Myyntitilausrivit'
    max_num = 10
    extra = 10

class Sales_orderAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('customer', 'delivery_date_requested', 'delivery_date_actual', ('delivery_status', 'invoice_status'), 'comment',)
        }),
    )

    list_display = ('id', 'customer', 'order_date', 'delivery_status', 'delivery_date_requested', 'delivery_date_actual',)
    list_filter = ('delivery_status', 'delivery_date_requested', 'order_date', )
    search_fields = ('customer__name',)
    save_on_top = True
    inlines = [Sales_order_lineInline,]
    
    formfield_overrides = {
      models.DateField: {'widget': jQCalendarWidget},
    }

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.price = instance.quantity * instance.unit_price
            instance.save()
        formset.save_m2m()

    def send_order(self, request, queryset):
        rows_updated = queryset.update(delivery_status='FD', delivery_date_actual=datetime.date.today())
        self.message_user(request, '%s rivi(ä) päivitettiin.' %rows_updated)
    send_order.short_description = "Merkitse tilaukset toimitetuksi"

    actions = [send_order]
        
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Customer_group, Customer_groupAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Product_group, Product_groupAdmin)
admin.site.register(Delivery_term, Delivery_termAdmin)
admin.site.register(Payment_term, Payment_termAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Salary_class, Salary_classAdmin)
admin.site.register(Work_phase, Work_phaseAdmin)
admin.site.register(Sales_order, Sales_orderAdmin)