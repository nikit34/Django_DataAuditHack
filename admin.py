from django.contrib import admin

# Register your models here.

from .models import Company, Owner, CompanyInstance, Genre, Language


# admin.site.register(Company)
# admin.site.register(CompanyInstance)
admin.site.register(Genre)
admin.site.register(Language)
# admin.site.register(Owner)


class CompanysInline(admin.TabularInline):
    model = Company


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [CompanysInline]


class CompanysInstanceInline(admin.TabularInline):
    model = CompanyInstance


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'display_genre')
    inlines = [CompanysInstanceInline]


admin.site.register(Company, CompanyAdmin)


@admin.register(CompanyInstance)
class CompanyInstanceAdmin(admin.ModelAdmin):
    list_display = ('company', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('company', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
