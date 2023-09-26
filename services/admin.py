from django.contrib import admin


class Service(admin.ModelAdmin):
    empty_value_display = '-пусто-'

    list_display = (
        'pk',
        'price',
        'pet_type',
        'work_time_to',
        'about',
        'published',
        "supplier",
    )


# @admin.register(Synology)
# class SynologyAdmin(BaseAdmin):
#     model = Synology
#
#     list_display = BaseAdmin.list_display + ("task", "format", "duration",)
#     search_fields = ('task', "format", "price")
#     list_filter = ('task', "format", "price")
#
#
# @admin.register(Veterinary)
# class VeterinaryAdmin(BaseAdmin):
#     model = Veterinary
#
#     list_display = BaseAdmin.list_display + ("pet_type", "duration",)
#     search_fields = ("pet_type", "duration",)
#     list_filter = ("pet_type", "duration",)
#
#
# @admin.register(Shelter)
# class ShelterAdmin(BaseAdmin):
#     model = Shelter
#
#     list_display = BaseAdmin.list_display + ("pet_type",)
#     search_fields = ("pet_type",)
#     list_filter = ("pet_type",)
#
#
# @admin.register(Groomer)
# class GroomerAdmin(BaseAdmin):
#     model = Groomer
#
#     list_display = BaseAdmin.list_display + ("pet_type", "grooming_type", "duration",)
#     search_fields = ("pet_type", "grooming_type", "duration",)
#     list_filter = ("pet_type", "grooming_type", "duration",)
