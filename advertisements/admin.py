from django.contrib import admin
from .models import Advertisement, AdvertisementImage, OtherBenefits, Complectation

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', )



@admin.register(AdvertisementImage)
class AdvertisementImageAdmin(admin.ModelAdmin):
    list_display = ('id', )



@admin.register(OtherBenefits)
class OtherBenefitsAdmin(admin.ModelAdmin):
    list_display = ('id', )



@admin.register(Complectation)
class ComplectationAdmin(admin.ModelAdmin):
    list_display = ('id', )