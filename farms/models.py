from django.db import models
import os
from django.core.validators import RegexValidator
from jalali_date import date2jalali
# Create your models here.
class Farms(models.Model):
    unitـtype = models.CharField(max_length=200, verbose_name='نوع واحد')
    name_type = models.CharField(max_length=200, verbose_name='نام واحد')
    image = models.ImageField(upload_to = 'media', verbose_name='تصویر مزرعه')
    Capacity = models.PositiveBigIntegerField(verbose_name='ظرفیت')
    Typeـofـfood = models.CharField(max_length=200, verbose_name='نوع دانخوری')
    Type_of_water = models.CharField(max_length=200, verbose_name='نوع آب خوری') 
    ventilation_system = models.CharField(max_length=200, verbose_name='سیستم تهویه')
    address = models.CharField(max_length=500, verbose_name=' آدرس مزرعه')
    active = models.BooleanField(default=True, verbose_name='مزرعه در حال فعالیت؟؟')
    date_start = models.DateField()

    def m2j(self):
        return date2jalali(self.date_start)

    class Meta:
        verbose_name = 'مزرعه'
        verbose_name_plural = 'مزرعه ها'

    def __str__(self):
        return f'نام:{self.name_type}'

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Farms, self).delete()

    def save(self, *args, **kwargs):
        try:
            this = Farms.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()
        except: 
            pass

        super(Farms, self).save(*args, **kwargs)

class FarmManage(models.Model):
    CHOICE_PLACE = (
        ('O','مالک'),
        ('T','مستاجر'),
        ('I','سرمایه گذار'),
    )
    phone_regex = RegexValidator(regex=r'^\d{9,15}$', message="+989120000000 فرمت صحیح وارد نمودن تلفن")

    which_farm = models.ForeignKey(Farms, on_delete=models.CASCADE, verbose_name='انتخاب مزرعه', related_name='farms_farmmanage')
    individualـposition = models.CharField(max_length=1, choices=CHOICE_PLACE, verbose_name='جایگاه فرد')
    name = models.CharField(max_length=300, verbose_name='نام')
    phone_number = models.CharField(validators=[phone_regex], max_length=17,verbose_name='تلفن')
    address = models.CharField(max_length=500, verbose_name='آدرس')

    class Meta:
        verbose_name = 'مدیر مزرعه'
        verbose_name_plural = 'مدیران مزرعه'

    def __str__(self):
        return f'مزرعه:{self.which_farm}-جایگاه:{self.individualـposition}-نام:{self.name}-تلفن:{self.phone_number}'


class ProfileChickens(models.Model):
    which_farm = models.OneToOneField(Farms,on_delete=models.CASCADE, related_name='farm_chicken', verbose_name='انتخاب مزرعه')
    origin = models.CharField(max_length=100, verbose_name='مبدا')
    number = models.PositiveBigIntegerField(verbose_name='تعداد')
    breeds = models.CharField(max_length=50, verbose_name='نژاد')
    age_into_farm = models.PositiveIntegerField(verbose_name='سن ورود به مزرعه')
    time_into_farm = models.DateField(verbose_name='زمان ورود به مزرعه')

    class Meta:
        verbose_name = 'مشخصات جوجه در هر مزرعه'
        verbose_name_plural = 'مشخصات جوجه ها در هر مزرعه'
   
    def m2j(self):
        return date2jalali(self.time_into_farm)

    def __str__(self):
        return f'مزرعه:{self.which_farm}-نژاد:{self.origin}-تعداد:{self.number}'
    

class Vaccination(models.Model):
    which_farm = models.ForeignKey(Farms,on_delete=models.CASCADE, related_name='farm_vaccination', verbose_name='انتخاب فارم')
    typeـvaccine = models.CharField(max_length=100, verbose_name='نوع واکسن')
    ageـprescription = models.PositiveIntegerField(verbose_name='سن تجویز')
    doing = models.BooleanField(default=False, verbose_name='تزریق شده؟؟')
    informationـRurry = models.TextField(verbose_name='اطلاعات ضروری')
    prescriptionـmethod = models.TextField(verbose_name='روش تجویز')
    date_injection = models.DateField(verbose_name='تاریخ تزریق')

    class Meta:
        verbose_name = 'برنامه واکسیناسیون'
        verbose_name_plural = 'برنامه واکسیناسیون'

    def m2j(self):
        return date2jalali(self.date_injection)

    def __str__(self):
        return f'مزرعه:{self.which_farm}-نوع واکسن:{self.typeـvaccine}-سن:{self.ageـprescription}'
    

class Manufacturing(models.Model):
    which_farm = models.ForeignKey(Farms,on_delete=models.CASCADE, related_name='farm_manufacturing', verbose_name='انتخاب فارم')
    Broken = models.PositiveBigIntegerField(verbose_name='شکسته')
    normal = models.PositiveBigIntegerField(verbose_name='طبیعی') 
    eggـyolk = models.PositiveBigIntegerField(verbose_name='2-زرده') 
    date = models.DateField(verbose_name='تاریخ تولید')

    class Meta:
        verbose_name = 'تولید روزانه هر فارم'
        verbose_name_plural = 'تولید روزانه هر فارم'

    def m2j(self):
        return date2jalali(self.date)

    def __str__(self):
        return f'مزرعه:{self.which_farm}-تاریخ:{self.date}'


class Losses(models.Model):
    which_farm = models.ForeignKey(Farms, on_delete=models.CASCADE, related_name='losses_farm', verbose_name='انتخاب مزرعه')
    hit_back = models.PositiveBigIntegerField(verbose_name=' تعداد پس زده')
    hit_description = models.TextField(verbose_name='توضیحات پس زده')
    sickness = models.PositiveBigIntegerField(verbose_name='تعداد بیماری')
    sicknes_description = models.TextField(verbose_name='توضیحات بیماری')
    suffocation = models.PositiveBigIntegerField(verbose_name='تعداد  خفگی')
    suffocation_description = models.TextField(verbose_name='توضیحات  خفگی')
    physics = models.PositiveBigIntegerField(verbose_name='تعداد فیزیکی')
    physics_description = models.TextField(verbose_name='توضیحات فیزیکی')
    date = models.DateField(verbose_name='تاریخ تلفات')

    class Meta:
        verbose_name = 'تلفات'
        verbose_name_plural = 'تلفات'

    def m2j(self):
        return date2jalali(self.date)

    def __str__(self):
        return f'مزرعه:{self.which_farm}-تاریخ{self.date}'
    

class MakBery(models.Model):
    which_farm = models.ForeignKey(Farms, on_delete=models.CASCADE, related_name='makbery_farm', verbose_name='انتخاب مزرعه')
    description = models.TextField(verbose_name='توضیحات')
    date_start = models.DateField(verbose_name='تاریخ شروع')
    date_end = models.DateField(verbose_name='تاریخ اتمام')
    
    def m2j_start(self):
        return date2jalali(self.date_start)

    def m2j_end(self):
        return date2jalali(self.date_end)

    class Meta:
        verbose_name = 'مک بری'
        verbose_name_plural = 'مک بری'

    def __str__(self):
        return f'مزرعه{self.which_farm}-از:{self.date_start}تا:{self.date_end}'
    
class labratore(models.Model):
    which_farm = models.ForeignKey(Farms, on_delete=models.CASCADE, related_name='labratore_farm', verbose_name='انتخاب مزرعه')
    descriptor = models.TextField(verbose_name='توضیح نتایج آزمایشگاهی')
    date = models.DateField(verbose_name='تاریخ آزمایش')

    def m2j(self):
        return date2jalali(self.date)

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''

    def __str__(self):
        return f'مزرعه:{self.which_farm}-تاریخ:{self.date}'

def path_save_image_labratore(instance, filename):
    path_save = os.path.join('labratore', instance.labratore.which_famr.name,str(instance.labratore.m2j()), filename)
    return path_save

class ImageLabratore(models.Model):
    labratore = models.ForeignKey(labratore, on_delete=models.CASCADE, related_name='image_labratore', verbose_name='انتخاب آزمایشگاه')
    image = models.ImageField(upload_to=path_save_image_labratore, verbose_name='تصویر آزمایشگاه')

    class Meta:
        verbose_name = 'تصاویر آزمایشگاه'
        verbose_name_plural = 'تصاویر آزمایشگاه'

    def __str__(self):
        return f'{self.labratore}'

class Medician(models.Model):
    which_farm = models.ForeignKey(Farms, on_delete=models.CASCADE, related_name='medician_farm', verbose_name='انتخاب مزرعه')
    is_sickness = models.BooleanField(default=False, verbose_name='بیماری مشاهده شد؟؟')
    section_sickness = models.TextField(verbose_name='مشخضات بیماری')
    treatmentـinstructions = models.TextField(verbose_name='دستورالعمل درمانی')
    date = models.DateField(verbose_name='تاریخ بازدید')

    def m2j(self):
        return date2jalali(self.date)

    class Meta:
        verbose_name = 'بهداشت و سلامت'
        verbose_name_plural = 'بهداشت و سلامت'

    def __str__(self):
        return f'مزرعه:{self.which_farm}-تاریخ:{self.date}'


def path_save_image_medician(instance, filename):
    path_save = os.path.join('medician', instance.which_medician.which_farm.name_type,str(instance.which_medician.m2j()), filename)
    return path_save 
    
class ImageMedician(models.Model):
    which_medician = models.ForeignKey(Medician, on_delete=models.CASCADE, related_name='image_medician', verbose_name='انتحاب بازدید بهداشتی')
    image = models.ImageField(verbose_name='تصویر', upload_to=path_save_image_medician)

    class Meta:
        verbose_name = 'بهداشت و سلامت تصاویر'
        verbose_name_plural = 'بهداشت و سلامت تصاویر'

    def __str__(self):
        return f'تصاویر بازدیدی از بهداشت:{self.which_medician}'

class Schedule(models.Model):
    which_farm = models.ForeignKey(Farms, on_delete=models.CASCADE, related_name='schedule_farm', verbose_name='انتخاب مزرعه')
    description = models.TextField(verbose_name='برنامه نوردهی')

    class Meta:
        verbose_name = 'برنامه نوردهی به مزرعه'
        verbose_name_plural = 'برنامه نوردهی به مزرعه'

    def __str__(self):
        return f'مزرعه:{self.which_farm}'
    
class Function(models.Model):
    which_farm = models.ForeignKey(Farms, on_delete=models.CASCADE, related_name='function_farm', verbose_name='انتخاب مزرعه')
    production_coefficient = models.FloatField(verbose_name='ضریب تولید')
    prduction_weight = models.FloatField(verbose_name='ضریب وزن')
    date = models.DateField(verbose_name='تاریخ')

    class Meta:
        verbose_name = 'عملکرد'
        verbose_name_plural = 'عملکرد'

    def m2j(self):
        return date2jalali(self.date)

    def __str__(self):
        return f'مزرعه:{self.which_farm}-تولید:{self.production_coefficient}-وزرن:{self.prduction_weight}'

class Incaome(models.Model):
    CHOICE_INCOME = (
        ('F','فروش کود'),
        ('E','فروش تخم مرغ'),
    )
    which_farm = models.ForeignKey(Farms, on_delete=models.CASCADE, related_name='income_farm', verbose_name='انتخاب مزرعه')
    sell = models.CharField(max_length=1, choices=CHOICE_INCOME, verbose_name='فروش')
    price = models.PositiveBigIntegerField(verbose_name='مبلغ')
    date = models.DateField(verbose_name='تاریخ فروش')

    def m2j(self):
        return date2jalali(self.date)

    class Meta:
        verbose_name = 'درآمد'
        verbose_name_plural = 'درآمد'

    def __str__(self):
        return f'مزرعه:{self.which_farm}-مبلغ:{self.price}-فروش{self.sell}-تاریخ:{self.date}'
