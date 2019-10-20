from django.db import models

# Create your models here.


from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a company genre')

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter the company market")

    def __str__(self):
        return self.name


class Company(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey('Owner', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(default='', max_length=1000, help_text='Enter a brief description of the company')
    isbn = models.CharField('ISBN', max_length=13, help_text='ID company')
    genre = models.ManyToManyField(Genre, help_text='Select genre for this company')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    numbers = models.IntegerField(help_text="Enter the company numbers")

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        return reverse('company-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


import uuid
from datetime import date
from django.contrib.auth.models import User

class CompanyInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular comapny across whole registry')
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('d', 'Maintenance'), # обслуживание
        ('o', 'On loan'), # в кредит
        ('a', 'Available'), # доступный
        ('r', 'Reserved'), # зарезервированный
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Company availability')

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'company withdrew from the contract'),)

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.company.title)


class Owner(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('owner-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)
