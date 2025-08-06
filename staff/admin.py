from django.contrib import admin
from .models import ClientVisit, OnlineClassInquiry, OfficeVisit, CollegeVisit


@admin.register(ClientVisit)
class ClientVisitAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'purpose', 'date', 'user')
    list_filter = ('date', 'user')
    search_fields = ('name', 'contact_number', 'purpose')
    ordering = ('-date',)
    date_hierarchy = 'date'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_verbose_name(self):
        return "Client Visit"


@admin.register(OnlineClassInquiry)
class OnlineClassInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'purpose', 'date', 'user')
    list_filter = ('date', 'user')
    search_fields = ('name', 'contact', 'purpose')
    ordering = ('-date',)
    date_hierarchy = 'date'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_verbose_name(self):
        return "Online Class Inquiry"


@admin.register(OfficeVisit)
class OfficeVisitAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'email', 'address', 'purpose', 'date', 'user')
    list_filter = ('date', 'user')
    search_fields = ('name', 'contact', 'email', 'address', 'purpose')
    ordering = ('-date',)
    date_hierarchy = 'date'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_verbose_name(self):
        return "Office Visit"


@admin.register(CollegeVisit)
class CollegeVisitAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'person_name', 'purpose', 'date', 'user')
    list_filter = ('date', 'user')
    search_fields = ('name', 'contact', 'person_name', 'purpose')
    ordering = ('-date',)
    date_hierarchy = 'date'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_verbose_name(self):
        return "School/College Visit"