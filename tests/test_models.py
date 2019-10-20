from django.test import TestCase

# Create your tests here.

from catalog.models import Owner


class OwnerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Owner.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        owner = Owner.objects.get(id=1)
        field_label = owner._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_last_name_label(self):
        owner = Owner.objects.get(id=1)
        field_label = owner._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')

    def test_date_of_birth_label(self):
        owner = Owner.objects.get(id=1)
        field_label = owner._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'date of birth')

    def test_date_of_death_label(self):
        owner = Owner.objects.get(id=1)
        field_label = owner._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'died')

    def test_first_name_max_length(self):
        owner = Owner.objects.get(id=1)
        max_length = owner._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_last_name_max_length(self):
        owner = Owner.objects.get(id=1)
        max_length = owner._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        owner = Owner.objects.get(id=1)
        expected_object_name = '{0}, {1}'.format(owner.last_name, owner.first_name)

        self.assertEquals(expected_object_name, str(owner))

    def test_get_absolute_url(self):
        owner = Owner.objects.get(id=1)
        self.assertEquals(owner.get_absolute_url(), '/catalog/owner/1')
