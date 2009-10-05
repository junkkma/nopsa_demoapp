#!/usr/bin/python
#!encoding=utf-8

from django.db import models
import datetime

# Create your models here.
class CF_all(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=10, default="APP")
    active = models.BooleanField(default=True, verbose_name="Aktiivinen", help_text="Jos tämä kohta on rastittu, niin objekti näytetään uusien tietojen syötössä")
    
    class Meta:
        abstract = True

class CF_comment(CF_all):
    comment = models.TextField(blank=True, verbose_name="Kommentti")
    
    class Meta:
        abstract = True

class Worker(CF_comment):
    forename = models.CharField(max_length=20, verbose_name="Etunimi")
    surname = models.CharField(max_length=30, verbose_name="Sukunimi")
    hourly_salary = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Tuntipalkka", default=0, help_text="Tuntipalkka euroissa, käytä desimaalierottimena pistettä. Esimerkki: 17.50")
    
    def __unicode__(self):
        return u'%s %s' % (self.surname, self.forename)
    
    class Meta:
        verbose_name = "työntekijä"
        verbose_name_plural = "Työntekijät"
        ordering = ['surname', 'forename']

class Customer_group(CF_comment):
    name = models.CharField(max_length=100, verbose_name="Nimi")

    def __unicode__(self):
        return self.name	

    class Meta:
        verbose_name = "asiakasryhmä"
        verbose_name_plural = "Asiakasryhmät"
        ordering = ['name']

class Delivery_term(CF_comment):
    name = models.CharField(max_length=100, verbose_name="Nimi")
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "toimitusehto"
        verbose_name_plural = "Toimitusehdot"
        ordering = ['name']

class Payment_term(CF_comment):
    name = models.CharField(max_length=100, verbose_name="Nimi")
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "maksuehto"
        verbose_name_plural = "Maksuehdot"
        ordering = ['name']

class Customer(CF_comment):
    name = models.CharField(max_length=100, verbose_name="Nimi")
    customer_group = models.ForeignKey(Customer_group, verbose_name="Asiakasryhmä", default="Oletus")
    billing_address = models.TextField(verbose_name="Laskutusosoite", blank=True)
    delivery_address = models.TextField(verbose_name="Toimitusosoite", blank=True)
    email = models.EmailField(verbose_name="Sähköposti", blank=True)
    default_delivery_term = models.ForeignKey(Delivery_term, verbose_name="Oletustoimitusehto", blank=True, null=True)
    default_payment_term = models.ForeignKey(Payment_term, verbose_name="Oletusmaksuehto", blank=True, null=True)

    def __unicode__(self):
        return self.name	

    class Meta:
        verbose_name = "asiakas"
        verbose_name_plural = "Asiakkaat"
        ordering = ['name']
    
class Product_group(CF_comment):
    name = models.CharField(max_length=100, verbose_name="Nimi")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "tuoteryhmä"
        verbose_name_plural = "Tuoteryhmät"
        ordering = ['name']

class Product(CF_comment):
    name = models.CharField(max_length=100, verbose_name="Nimi")
    product_group = models.ForeignKey(Product_group, default="Oletus", verbose_name="Tuoteryhmä")
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "tuote"
        verbose_name_plural = "Tuotteet"
        ordering = ['name']

class Shift(CF_comment):
    name = models.CharField(max_length=100, verbose_name="Nimi")
    start_time = models.TimeField(verbose_name = "Alkaa")
    end_time = models.TimeField(verbose_name = "Loppuu")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "vuoro"
        verbose_name_plural = "Vuorot"
        ordering = ['name']

class Salary_class(CF_comment):
    name = models.CharField(max_length=100, verbose_name = "Palkaluokka")
    salary_multiplier = models.DecimalField(max_digits=6, decimal_places = 3, default = 1, verbose_name = "Palkkakerroin")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "palkkaluokka"
        verbose_name_plural = "Palkkaluokat"
        ordering = ['name']

class Sales_order(CF_comment):
    DELIVERY_STATUS_CHOICES = (
        ('ND', 'Toimittamatta'),
        ('PD', 'Osittain toimitettu'),
        ('FD', 'Toimitettu')
    )    
    INVOICE_STATUS_CHOICES = (
        ('NI', 'Laskuttamatta'),
        ('PI', 'Osittain laskutettu'),
        ('FI', 'Laskutettu')
    )
    customer = models.ForeignKey(Customer, verbose_name="Asiakas")
    delivery_address = models.TextField(verbose_name="Toimitusosoite", blank=True)
    payment_address = models.TextField(verbose_name="Laskutusosoite", blank=True)
    payment_term = models.ForeignKey(Payment_term, verbose_name="Maksuehto", blank=True, null=True)
    delivery_term = models.ForeignKey(Delivery_term, verbose_name="Toimitusehto", blank=True, null=True)
    order_date = models.DateField(verbose_name="Tilauspäivämäärä", default=datetime.date.today())
    delivery_date_requested = models.DateField(verbose_name="Pyydetty toimituspäivämäärä", blank=True, null=True)
    delivery_date_actual = models.DateField(verbose_name="Todellinen toimituspäivämäärä", blank=True, null=True)
    delivery_status = models.CharField(verbose_name="Toimitustilanne",max_length=20, choices=DELIVERY_STATUS_CHOICES, default='ND')
    invoice_status = models.CharField(verbose_name="Laskutustilanne",max_length=20, choices=INVOICE_STATUS_CHOICES, default='ND')

    class Meta:
        verbose_name = "myyntitilaus"
        verbose_name_plural = "Myyntitilaukset"
        ordering = ['-order_date', 'customer']
        
class Sales_order_line(models.Model):
    sales_order = models.ForeignKey(Sales_order)
    product = models.ForeignKey(Product, verbose_name="Tuote")
    quantity = models.IntegerField(verbose_name="Määrä")
    unit_price = models.DecimalField(verbose_name="Yksikköhinta", decimal_places=2, max_digits=10)
    price = models.DecimalField(verbose_name="Hinta", decimal_places=2, max_digits=15)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
class Work_phase(CF_comment):
    WORK_PHASE_TYPE_CHOICES = (
        ('Direct', 'Välitön'),
        ('Indirect', 'Välillinen')
    )
    name = models.CharField(max_length=100, verbose_name="Nimi")
    work_phase_type = models.CharField(max_length=30, choices=WORK_PHASE_TYPE_CHOICES, verbose_name="Työvaiheen laji")
    
    class Meta:
        verbose_name = "työvaihe"
        verbose_name_plural = "Työvaiheet"
        ordering = ['name']
    
class Work_entry(CF_comment):
    worker = models.ForeignKey(Worker)
    start = models.DateTimeField()
    end = models.DateTimeField()
    shift = models.ForeignKey(Shift)
    work_phase = models.ForeignKey(Work_phase)
    salary_class = models.ForeignKey(Salary_class)
    sales_order_line = models.ForeignKey(Sales_order_line, blank=True, null=True)
    hours = models.DecimalField(max_digits=6, decimal_places=2)
    
