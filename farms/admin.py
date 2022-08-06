from django.contrib import admin

# Register your models here.
from .models import Farms, Function,FarmManage, ProfileChickens, Vaccination, Medician, ImageMedician, Losses, labratore, ImageLabratore



admin.site.register(Farms)
admin.site.register(FarmManage)
admin.site.register(ProfileChickens)
admin.site.register(Vaccination)
admin.site.register(Medician)
admin.site.register(ImageMedician)
admin.site.register(labratore)
admin.site.register(Losses)
admin.site.register(ImageLabratore)
admin.site.register(Function)