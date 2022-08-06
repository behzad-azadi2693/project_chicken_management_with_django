from django import forms
from django.forms import fields
from django.shortcuts import get_object_or_404
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from .models import (
            Farms, Function, ImageLabratore, Incaome, Losses, MakBery, Medician, 
            ProfileChickens, Vaccination, Manufacturing, 
            Schedule, FarmManage,ImageMedician, labratore
        )

messages = {
    'required':'این فیلد الزامی است',
    'invalid':'این فیلد صحیح نمیباشد',
    'max_length':'اندازه فیلد بیشتر از حد مجاز',
    'min_length':'اندازه فیلد کمتر از حد مجاز',
}

class FarmForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FarmForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            self.fields['date_start'] = JalaliDateField(label='تاریخ شروع',widget=AdminJalaliDateWidget)
            self.fields[field].error_messages = messages

    class Meta:
        model = Farms
        fields = '__all__'

class ProfilechickenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfilechickenForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            self.fields['which_farm'].widget.attrs['readonly'] = True
            self.fields['time_into_farm'] = JalaliDateField(label='زمان وروذ یه مزرعه',widget=AdminJalaliDateWidget)
            self.fields[field].error_messages = messages

    class Meta:
        model = ProfileChickens
        fields = '__all__'


class VaccinationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VaccinationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            self.fields['which_farm'].widget.attrs['readonly'] = True
            self.fields['date_injection'] = JalaliDateField(label='تاریخ تزریق',widget=AdminJalaliDateWidget)
            self.fields[field].error_messages = messages

    class Meta:
        model = Vaccination
        fields = '__all__'

class ManufacturingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ManufacturingForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            self.fields['date'] = JalaliDateField(label='تاریخ تولید',widget=AdminJalaliDateWidget)
            self.fields['which_farm'].widget.attrs['readonly'] = True
            self.fields[field].error_messages = messages

    class Meta:
        model = Manufacturing
        fields = '__all__'

class LossesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LossesForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            self.fields['which_farm'].widget.attrs['readonly'] = True
            self.fields['date'] = JalaliDateField(label='تاریخ تلقات',widget=AdminJalaliDateWidget)
            self.fields[field].error_messages = messages

    class Meta:
        model = Losses
        fields = '__all__'

class IncaomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IncaomForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            self.fields['which_farm'].widget.attrs['readonly'] = True
            self.fields['date'] = JalaliDateField(label='تاریخ فروش',widget=AdminJalaliDateWidget)
            self.fields[field].error_messages = messages

    class Meta:
        model = Incaome
        fields = '__all__'

class FunctionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FunctionForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            self.fields['which_farm'].widget.attrs['readonly'] = True
            self.fields['date'] = JalaliDateField(label='تاریخ عملکرد',widget=AdminJalaliDateWidget)
            self.fields[field].error_messages = messages

    class Meta:
        model = Function
        fields = '__all__'

class ScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            self.fields['which_farm'].widget.attrs['readonly'] = True

            self.fields[field].error_messages = messages

    class Meta:
        model = Schedule
        fields = '__all__'


class ManagerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ManagerForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            self.fields['phone_number'].widget.attrs['placeholder'] = '09120000000'
            self.fields['phone_number'].widget.attrs['style'] = 'direction:ltr'

    class Meta:
        model = FarmManage
        exclude = ('which_farm',)

class ScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            self.fields['which_farm'].widget.attrs['readonly'] = True
            self.fields[field].error_messages = messages

    class Meta:
        model = Schedule
        fields = '__all__'

class MakeBeryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MakeBeryForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            self.fields['which_farm'].widget.attrs['readonly'] = True
            self.fields['date_start'] = JalaliDateField(label='تاریخ شروع',widget=AdminJalaliDateWidget)
            self.fields['date_end'] = JalaliDateField(label='تاریخ پایان',widget=AdminJalaliDateWidget)
            self.fields[field].error_messages = messages

    class Meta:
        model = MakBery
        fields = '__all__'

class MedicianForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MedicianForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            self.fields['which_farm'].widget.attrs['readonly'] = True
            self.fields['date'] = JalaliDateField(label='تاریخ بازدید',widget=AdminJalaliDateWidget)
            self.fields[field].error_messages = messages

    class Meta:
        model = Medician
        fields = '__all__'


class ImageMedicianForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ImageMedicianForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            #self.fields['which_medician'].widget.attrs['readonly'] = True
            self.fields['image'].widget.attrs['multiple'] = True
            self.fields[field].error_messages = messages

    class Meta:
        model = ImageMedician
        fields = ('image',)



class LabratoreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LabratoreForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            self.fields['which_farm'].widget.attrs['readonly'] = True
            self.fields['date'] = JalaliDateField(label='تاریخ بازدید',widget=AdminJalaliDateWidget)
            self.fields[field].error_messages = messages

    class Meta:
        model = labratore
        fields = '__all__'


class ImageLabratoreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageLabratoreForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'direction:rtl'
            #self.fields['labratore'].widget.attrs['readonly'] = True
            self.fields['image'].widget.attrs['multiple'] = True
            self.fields[field].error_messages = messages

    class Meta:
        model = ImageLabratore
        fields = ('image',)
