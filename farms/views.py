from django.contrib import messages
from django.core.paginator import Paginator
from django.forms.models import modelformset_factory

from django.shortcuts import get_object_or_404, redirect, render
from .models import (
            FarmManage, Farms, Function, ImageLabratore, ImageMedician, Incaome, Losses, MakBery, ProfileChickens, 
            Schedule, Vaccination, Manufacturing, Medician, labratore
        )
from .forms import (
            FarmForm, FunctionForm, ImageLabratoreForm, ImageMedicianForm, IncaomForm, LabratoreForm, LossesForm, 
            ManufacturingForm, ProfilechickenForm, ScheduleForm, MakeBeryForm, 
            VaccinationForm,MedicianForm, ManagerForm, ImageMedician
        )
from django.db.models import Sum
# Create your views here.
from django.db import connection, reset_queries
import time

def debugger(func):
    def wrapper(*args, **kwargs):
        reset_queries()
        st=time.time()
        value = func(*args, **kwargs)
        et=time.time()

        queries = len(connection.queries)
        print(f"'--------------------------------------',{queries} ,' ----time:',{et-st}")
        return value
    return wrapper


def farms(request):
    farmses = Farms.objects.only('pk','image','name_type','active','date_start').order_by('-active','-id')
    paginator = Paginator(farmses, 24) 
    page = request.GET.get('page')
    farms = paginator.get_page(page)
    context = {
        'farms':farms
    }

    return render(request, 'farms.html', context)


def farm(request, pk):
    farm = get_object_or_404(Farms, pk=pk)
    manage = farm.farms_farmmanage.all()

    context = {
        'farm':farm,
        'manage':manage
    }
    
    return render(request, 'farm.html', context)


def create_farm(request):
    if request.method == 'POST':
        form = FarmForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save()
            return redirect('farms:farm', obj.pk)
        else:
            form = FarmForm(request.POST, request.FILES)
            context = {
                'form':form
            }
            return render(request, 'create.html', context)
    else:
        form = FarmForm()
        return render(request, 'create.html',{'form':form})


def edit_farm(request, pk):
    farm = get_object_or_404(Farms, pk=pk)

    if not farm.active:
        messages.warning(request, 'این مزرعه فعال نمی باشد', 'warning')
        return redirect('farms:farm', pk)

    if request.method == 'POST':
        form = FarmForm(request.POST, request.FILES, instance=farm)
        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save()
            return redirect('farms:farm', obj.pk)
        else:
            form = FarmForm(request.POST, request.FILES)
            context = {
                'form':form
            }
            return render(request, 'create.html', context)
    else:
        form = FarmForm(instance=farm)
        return render(request, 'create.html',{'form':form})


def profilechicken(request, pk):
    profile = ProfileChickens.objects.select_related('which_farm').filter(which_farm__pk=pk).first()

    context = {
        'profile':profile
    }

    return render(request, 'medicians.html', {'profile':profile})


def create_profilechicken(request, pk):
    try:
        ProfileChickens.objects.get(which_farm__pk=pk)
        messages.error(request, 'این مزرعه زیر کشت می باشد', 'error')
        return redirect('farms:farm', pk)

    except ProfileChickens.DoesNotExist:
        farm = get_object_or_404(Farms, pk=pk)
    
        if not farm.active:
            messages.warning(request, 'این مزرعه فعال نمی باشد', 'warning')
            return redirect('farms:farm', farm.pk)

        if request.method == 'POST':
            form = ProfilechickenForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                obj = form.save()
                return redirect('farms:profilechicken', obj.pk)
            else:
                form = ProfilechickenForm(request.POST)
                context = {
                    'form':form
                }
                return render(request, 'create.html', context)
        else:

            data = {'which_farm':farm}
            form = ProfilechickenForm(initial=data)
            return render(request, 'create.html',{'form':form})
    

def edit_profilechicken(request, pk):
    farm = get_object_or_404(ProfileChickens, pk=pk)
    
    if not farm.which_farm.active:
        messages.warning(request, 'این مزرعه فعال نمی باشد', 'warning')
        return redirect('farms:profilechicken', farm.which_farm.pk)

    if request.method == 'POST':
        form = ProfilechickenForm(request.POST, instance=obj)
        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save()
            return redirect('farms:profilechicken', obj.pk)
        else:
            form = ProfilechickenForm(request.POST)
            context = {
                'form':form
            }
            return render(request, 'create.html', context)

    else:

        form = ProfilechickenForm(instance=farm)
        return render(request, 'create.html',{'form':form})   


def vaccinations(request, pk):
    queries = Vaccination.objects.select_related('which_farm').filter(which_farm__pk=pk)

    context = {
        'vaccinations':queries
    }

    return render(request, 'medicians.html', context)


def create_vaccination(request, pk):
    obj = get_object_or_404(Farms, pk=pk)

    if not obj.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', obj.pk)

    if request.method == 'POST':
        form = VaccinationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            return redirect('farms:vaccinations', obj.pk)
        else:
            form = VaccinationForm(request.POST)
            context = {
                'form':form
            }
            return render(request, 'create.html', context)
    else:
        data = {'which_farm': obj}
        form = VaccinationForm(initial=data)
        return render(request, 'create.html',{'form':form})

def edit_vaccination(request, pk):

    obj = get_object_or_404(Vaccination, pk=pk)
    if not obj.which_farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:vaccinations', obj.which_farm.pk)
    
    if request.method == 'POST':
        form = VaccinationForm(request.POST, instance=obj)
        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save()
            return redirect('farms:vaccination', obj.pk)
        else:
            form = VaccinationForm(request.POST)
            context = {
                'form':form
            }
            return render(request, 'create.html', context)

    else:

        form = VaccinationForm(instance=obj)
        return render(request, 'create.html',{'form':form})



def functions(request, pk):
    functions = Function.objects.select_related('which_farm').filter(which_farm__pk=pk)
    context = {
        'functions': functions
    }

    return render(request, 'medicians.html', context)

def create_function(request, pk):
    farm = get_object_or_404(Farms, pk=pk)

    if not farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', farm.pk)


    if request.method == 'POST':
        form = FunctionForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            return redirect('farms:functions', pk)
        else:
            form = FunctionForm(request.POST)
            return render(request, 'create.html', {'form':form})
    else:
        data = {'which_farm': farm}
        form = FunctionForm(initial=data)
        return render(request, 'create.html', {'form':form})

def edit_function(request, pk):
    farm = get_object_or_404(Function, pk=pk)

    if not farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', farm.pk)

    if request.method == 'POST':
        form = FunctionForm(request.POST, instance=farm)

        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save()
            pk = obj.which_farm.pk
            return redirect('farms:functions', pk)
        else:
            return render(request, 'create.html', {'form':form})
    else:
        form = FunctionForm(instance=farm)
        return render(request, 'create.html', {'form':form})

def schedules(request, pk):
    schedules = Schedule.objects.select_related('which_farm').filter(which_farm__pk=pk)

    context = {
        'schedules': schedules
    }

    return render(request, 'medicians.html', context)


def create_schedule(request, pk):
    farm = get_object_or_404(Farms, pk=pk)

    if not farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', farm.pk)

    if request.method == 'POST':
        form = ScheduleForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            return redirect('farms:schedules', farm.pk)
        else:
            form = ScheduleForm(request.POST)
            return render(request, 'create.html', {'form':form})
    else:
        
        data = {'which_farm': farm}
        form = ScheduleForm(initial=data)
        return render(request, 'create.html', {'form':form})

def edit_schedule(request, pk):
    obj = get_object_or_404(Schedule, pk=pk)
    if not obj.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', obj.pk)

    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=obj)

        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save()
            pk = obj.which_farm.pk
            return redirect('farms:schedules', pk)
        else:
            return render(request, 'create.html', {'form':form})
    else:
        form = ScheduleForm(instance=obj)
        return render(request, 'create.html', {'form':form})

def edit_manage(request, pk):
    user = get_object_or_404(FarmManage, pk=pk)

    if not user.which_farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', user.which_farm.pk)

    if request.method == 'POST':
        form = ManagerForm(request.POST, instance=user)
        if form.is_valid():
            obj = form.save()
            pk = obj.which_farm.pk
            return redirect('farms:farm', pk)
        else:
            return render(request, 'create.html', {'form':form})

    else:
        form = ManagerForm(instance=user)
        return render(request, 'create.html', {'form':form})


def create_manage(request, pk):    
    farm = get_object_or_404(Farms, pk=pk)

    manageformset = modelformset_factory(FarmManage, ManagerForm, fields=('__all__'), extra=3)

    if not farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', farm.pk)

    if request.method == 'POST':
        formset = manageformset(data=request.POST)
        print(formset)
        if formset.is_valid():
            managers = [FarmManage(**field_dict, which_farm=farm) for field_dict in formset.cleaned_data]
            FarmManage.objects.bulk_create(managers)
        return redirect('farms:farm', pk)

    else:
        
        form = manageformset(queryset=FarmManage.objects.none())
        context = {
            'formset':form
        }
        return render(request, 'create.html', context)


def make_bery(request, pk):
    all_mak_bery = MakBery.objects.select_related('which_farm').filter(which_farm__pk=pk)
    return render(request, 'medicians.html', {'all_mak_bery':all_mak_bery})

def create_make_bery(request, pk):
    farm = get_object_or_404(Farms, pk=pk)

    if not farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', farm.pk)

    if request.method == 'POST':
        form = MakeBeryForm(request.POST)
        if form.is_valid():
            obj = form.save()
            pk = obj.which_farm.pk
            return redirect('farms:make_bery', pk)
        else:
            return render(request, 'create.html', {'form':form})
    else:
        
        data = {'which_farm':farm}
        form = MakeBeryForm(initial=data)
        return render(request, 'create.html', {'form':form})

def edit_make_bery(request, pk):
    obj = get_object_or_404(MakBery, pk=pk)
    
    if not obj.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', obj.pk)


    if request.method == 'POST':
        form = MakeBeryForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            pk = obj.which_farm.pk
            return redirect('farms:schedule', pk)
        else:
            return render(request, 'schedule/html', {'form':form})
    else:
        form = MakeBeryForm(instance=obj)
        return render(request, 'create.html', {'form':form})

def medicians(request, pk):
    all_medician = Medician.objects.select_related('which_farm').filter(which_farm__pk=pk).order_by('-date')
    context = {
        'all_medician':all_medician,
    }

    return render(request, 'medicians.html', context)

def create_medician(request, pk):
    farm = get_object_or_404(Farms, pk=pk)

    if not farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', farm.pk)

    if request.method == 'POST':
        form = MedicianForm(request.POST)
        if form.is_valid():
            obj = form.save()
            pk = obj.which_farm.pk
            return redirect('farms:medicians', pk)
        else:
            return render(request, 'create.html',{'form':form})

    else:
        data = {'which_farm':farm}
        form = MedicianForm(initial=data)
        return render(request, 'create.html', {'form':form})

def edit_medician(request, pk):
    obj = get_object_or_404(Medician, pk=pk)

    if not obj.which_farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:medicians', obj.which_farm.pk)

    if request.method == 'POST':
        form = MedicianForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            pk = obj.which_farm.pk
            return redirect('farms:medicians', pk)
        else:
            return render(request, 'create.html',{'form':form})
            
    else:
        form = MedicianForm(instance=obj)
        return render(request, 'create.html', {'form':form})


def add_image_to_medician(request, pk):
    mdc = get_object_or_404(Medician.objects.select_related(), pk=pk)

    if not mdc.which_farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:medicians', mdc.which_farm.pk)

    if request.method == 'POST':
        form = ImageMedicianForm(request.POST, request.FILES)
        if form.is_valid():
            files = [ImageMedician(image=i,which_medician=mdc ) for i in request.FILES.getlist('image')]
            ImageMedician.objects.bulk_create(files)
            pk = mdc.which_farm.pk
            return redirect('farms:medicians', pk)
        else:
            return render(request, 'create.html', {'form':form})
    else:
        data = {'which_medician':mdc}
        form = ImageMedicianForm(initial=data)
        return render(request, 'create.html', {'form':form})

def all_image_medician(request, pk):
    imgs = ImageMedician.objects.select_related().filter(which_medician__pk=pk)
    return render(request, 'show_image.html', {'imgsM':imgs})

def remove_image_medician(request, pk):
    img = get_object_or_404(ImageMedician, pk=pk)

    if not img.which_medician.which_farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:all_image_medician', img.which_medician.pk)

    pk = img.which_medician.pk
    img.delete()
    return redirect('farms:all_image_medician', pk)


def labratores(request, pk):
    all_labratore = labratore.objects.select_related('which_farm').filter(which_farm__pk=pk).order_by('-date')

    context = {
        'all_labratore':all_labratore
    }

    return render(request, 'medicians.html', context)

def create_labratore(request, pk):
    farm = get_object_or_404(Farms, pk=pk)

    if not farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', farm.pk)

    if request.method == 'POST':
        form = LabratoreForm(request.POST)
        if form.is_valid():
            obj = form.save()
            pk = obj.which_farm.pk
            return redirect('farms:labratores', pk)
        else:
            return render(request, 'create.html',{'form':form})

    else:
        data = {'which_farm':farm}
        form = LabratoreForm(initial=data)
        return render(request, 'create.html', {'form':form})

def edit_labratore(request, pk):
    obj = get_object_or_404(labratore, pk=pk)

    if not obj.which_farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:labratores', obj.which_farm.pk)

    if request.method == 'POST':
        form = LabratoreForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            pk = obj.which_farm.pk
            return redirect('farms:labratores', pk)
        else:
            return render(request, 'create.html',{'form':form})
            
    else:
        form = LabratoreForm(instance=obj)
        return render(request, 'create.html', {'form':form})


def add_image_to_labratore(request, pk):
    lab = get_object_or_404(labratore.objects.select_related(), pk=pk)

    if not lab.which_farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:labratores', lab.which_farm.pk)

    if request.method == 'POST':
        form = ImageLabratoreForm(request.POST, request.FILES)
        if form.is_valid():
            files = [labratore(image=image, labratore=lab) for image in request.FILES.getlist('image')]
            ImageLabratore.objects.bulk_create(files)
            pk = lab.which_farm.pk
            return redirect('farms:labratores', pk)
        else:
            return render(request, 'create.html', {'form':form})
    else:
        data = {'labratore':lab}
        form = ImageLabratoreForm(initial=data)
        return render(request, 'create.html', {'form':form})


def all_image_labratore(request, pk):
    imgs = ImageLabratore.objects.select_related().filter(labratore__pk = pk)
    return render(request, 'show_image.html', {'imgsA':imgs})

def remove_image_labratore(request, pk):
    img = get_object_or_404(ImageLabratore, pk=pk)

    if not img.labratore.which_farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:all_image_labratore', img.labratore.pk)

    pk = img.labratore.pk
    img.delete()
    return redirect('farms:all_image_labratore', pk)

def manufacturing_farm(request, pk):
    manu = Manufacturing.objects.select_related('which_farm').filter(which_farm__pk=pk).order_by('date')

    num_brokn = [i.Broken for i in manu]
    num_normal = [i.normal for i in manu]
    num_egg = [i.eggـyolk for i in manu]

    sum_broken = manu.aggregate(broken=Sum('Broken'),norm=Sum('normal'),egg=Sum('eggـyolk'))


    context = {
        'broken' :sum_broken['broken'],
        'normal' :sum_broken['norm'],
        'eggyolk':sum_broken['egg'],
        'manu': manu,
        'num_broken':num_brokn,
        'num_normal':num_normal,
        'num_egg':num_egg,
    }
    return render(request, 'manufacturing_farm.html', context)

def create_manufacturing(request, pk):
    obj = get_object_or_404(Farms, pk=pk)

    if not obj.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', obj.pk)

    if request.method == 'POST':
        form = ManufacturingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save()
            return redirect('farms:manufacturing_farm', obj.which_farm.pk)
        else:
            form = ManufacturingForm(request.POST)
            context = {
                'form':form
            }
            return render(request, 'create.html', context)
    else:
        data = {'which_farm': obj}
        form = ManufacturingForm(initial=data)
        return render(request, 'create.html',{'form':form})

def edit_manufacturing(request, pk):
    obj = get_object_or_404(Manufacturing, pk=pk)

    if not obj.which_farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', obj.pk)

    if request.method == 'POST':
        form = ManufacturingForm(request.POST, instance=obj)
        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save()
            return redirect('farms:manufacturing_farm', obj.which_farm.pk)
        else:
            form = ManufacturingForm(request.POST)
            context = {
                'form':form
            }
            return render(request, 'create.html', context)

    else:
        form = ManufacturingForm(instance=obj)
        return render(request, 'create.html',{'form':form})

def losses(request, pk):
    all_losses = Losses.objects.select_related('which_farm').filter(which_farm__pk=pk)
    
    sum = all_losses.aggregate(hit=Sum('hit_back'),sick=Sum('sickness'),suff=Sum('suffocation'),phys=Sum('physics'))
 
    context = {
        'hit_back' :sum['hit'],
        'sickness' :sum['sick'],
        'suffocation':sum['suff'],
        'physics':sum['phys'],
        'losses':all_losses,
    }

    return render(request, 'losse.html', context)

def losse(request, pk):
    losse = get_object_or_404(Losses ,pk=pk)

    context = {
        'losse':losse
    }
    return render(request, 'losse.html', context)

def create_losse(request, pk):
    obj = get_object_or_404(Farms, pk=pk)

    if not obj.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', obj.pk)

    if request.method == 'POST':
        form = LossesForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save()
            return redirect('farms:losse', obj.pk)
        else:
            form = LossesForm(request.POST)
            return render(request, 'create.html', {'form':form})
    else:
        data = {'which_farm': obj}
        form = LossesForm(initial=data)
        return render(request, 'create.html', {'form':form})

def edit_losse(request, pk):
    obj = get_object_or_404(Losses, pk=pk)

    if not obj.which_farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:losse', obj.pk)

    if request.method == 'POST':
        form = LossesForm(request.POST, instance=obj)

        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save()
            return redirect('farms:losse', obj.pk)
        else:
            form = LossesForm(request.POST)
            return render(request, 'create.html', {'form':form})
    else:
        form = LossesForm(instance=obj)
        return render(request, 'create.html', {'form':form})

def incaomes(request, pk):

    incaomes = Incaome.objects.select_related('which_farm').filter(which_farm__pk =pk).order_by('date')
    price_cood = incaomes.filter(sell='F').aggregate(Sum('price'))
    price_egg = incaomes.filter(sell='E').aggregate(Sum('price'))

    context = {
        'incaomes':incaomes,
        'price_cood':price_cood['price__sum'] or 0,
        'price_egg':price_egg['price__sum'] or 0,
    }
    return render(request, 'incaome.html', context)

def create_incaome(request, pk):
    farm = get_object_or_404(Farms, pk=pk)

    if not farm.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:farm', farm.pk)

    if request.method == 'POST':
        form = IncaomForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            return redirect('farms:incaomes', farm.pk)
        else:
            form = IncaomForm(request.POST)
            return render(request, 'create.html', {'form':form})
    else:
        data = {'which_farm': farm}
        form = IncaomForm(initial=data)
        return render(request, 'create.html', {'form':form})

def edit_incaome(request, pk):
    obj = get_object_or_404(Incaome, pk=pk)

    if not obj.active:
        messages.error(request, 'این مزرعه فعال نمی باشد', 'error')
        return redirect('farms:incaomes', obj.which_farm.pk)

    if request.method == 'POST':
        form = IncaomForm(request.POST, instance=obj)

        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save()
            pk = obj.which_farm.pk
            return redirect('farms:incaomes', pk)
        else:
            return render(request, 'create.html', {'form':form})
    else:
        form = IncaomForm(instance=obj)
        return render(request, 'create.html', {'form':form})