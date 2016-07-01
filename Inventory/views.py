from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Site, Config, Device, Phone
from .form import UserForm, SiteForm, ConfigForm, DeviceForm
#TODO add comments for class and def funtions
#TODO clean up Imports


def index(request):
    return render(request, 'Inventory/index.html')


def create_site(request):
    form = SiteForm(request.POST or None)
    if request.POST:
        t = request.POST.get("siteCode")
        if form.is_valid():
            sites = form.save(commit=False)
            try:
                Site.objects.get(siteCode=t)
                context = {
                    'sites': sites,
                    'form': form,
                    'error_message': "Site Code already Used"
                }
                return render(request, 'Inventory/site_form.html', context)
            except Site.DoesNotExist:
                sites.save()
                return render(request, 'Inventory/detail.html', {'site': sites})

    context = {
        "form": form,
    }
    return render(request, 'Inventory/site_form.html', context)


class SiteUpdate(UpdateView):
    model = Site
    fields = ['siteCode', 'city', 'state', 'address', 'zipcode']


class CreateDetail(CreateView):
    model = Config
    fields = [
        'site', 'provider', 'circuit_id', 'svc_id', 'prefix', 'wan_net', 'wan_remote', 'wan_local', 'name_fw',
        'fw_type', 'name_sw', 'sw_type', 'fw_lan', 'sw_lan', 'fw_lo', 'sw_lo', 'peer_asn', 'local_asn',
        'ospf_area'
    ]
    success_url = '/netops/sites'


def delete_detail(request, pk, detail_id):
    sites = get_object_or_404(Site, pk)
    for details in Config.objects.get(pk=detail_id):
        details.delete()
    return render(request, 'Inventory/detail.html', {'sites': sites})


def detail(request, pk):
    sites = get_object_or_404(Site, pk=pk)
    return render(request, 'Inventory/detail.html', {'site': sites})


class DetailUpdate(UpdateView):
    model = Config
    fields = [
        'site', 'provider', 'circuit_id', 'svc_id', 'prefix', 'wan_net', 'wan_remote', 'wan_local', 'name_fw',
        'fw_type', 'name_sw', 'sw_type', 'fw_lan', 'sw_lan', 'fw_lo', 'sw_lo', 'peer_asn', 'local_asn',
        'ospf_area'
    ]
    success_url = '/netops/sites'


def closed(request, pk):
    sites = get_object_or_404(Site, pk=pk)
    if sites.is_closed:
        sites.is_closed = False
        sites.save()
        return render(request, 'Inventory/sites.html', {'success_message': 'Site is Reactivated'})

    else:
        sites.is_closed = True
        sites.save()
        return render(request, 'Inventory/sites.html', {'success_message': 'Site is now Closed'})


def site(request):
    sites = Site.objects.filter()
    details = Site.objects.all()
    query = request.GET.get("q")
    if query:
        sites = sites.filter(
            Q(siteCode__contains=query) |
            Q(city__contains=query) |
            Q(config__svc_id__icontains=query)
        ).distinct()
        return render(request, 'Inventory/sites.html', {'sites': sites,
                                                        'details': details})
    else:
        return render(request, 'Inventory/sites.html', {'sites': sites})


def device(request):
    devices = Device.objects.filter()
    query = request.GET.get("q")
    if query:
        devices = devices.filter(
            Q(device__address__icontains=query) |
            Q(mac_add__icontains=query) |
            Q(serial__icontains=query) |
            Q(hard_type=query) |
            Q(asset_tag=query)
        ).distinct()
        return render(request, 'Inventory/devices.html', {'object_list': devices})
    else:
        devices = Device.objects.all()
        return render(request, 'Inventory/devices.html', {'object_list': devices})


def create_device(request):
    form = DeviceForm(request.POST or None)
    if request.POST:
        t = request.POST.get("serial")
        if form.is_valid():
            devices = form.save(commit=False)
            try:
                Device.objects.get(serial=t)
                context = {
                    'Device': devices,
                    'form': form,
                    'error_message': "Serial already Used"
                }
                return render(request, 'Inventory/device_form.html', context)
            except Device.DoesNotExist:
                devices.save()
                return render(request, 'Inventory/devices.html', {'devices': devices})

    context = {
        "form": form,
    }
    return render(request, 'Inventory/device_form.html', context)


class DeviceToSite(UpdateView):
    model = Device
    fields = ['device', 'device_name']
    success_url = '/netops/devices'


class DeviceDelete(DeleteView):
    model = Device
    success_url = reverse_lazy('Inventory:devices')


def remove_device(request, device_id):
    devices = Device.objects.get(pk=device_id)
    t = devices.device.pk
    if devices.device is not None:
        devices.device = None
        devices.save()
        return detail(request, pk=t)


class CreatePhone(CreateView):
    model = Phone
    fields = ['site', 'device_name', 'desc', 'device_pool', 'device_type', 'dir_num']
    success_url = reverse_lazy('Inventory:phones')


def phone(request):
    phones = Phone.objects.filter()
    query = request.GET.get("q")
    if query:
        phones = phones.filter(
            Q(device_name__icontains=query) |
            Q(desc__icontains=query) |
            Q(device_pool__icontains=query) |
            Q(device_type__icontains=query) |
            Q(dir_num__icontains=query)
        ).distinct()
        return render(request, 'Inventory/phones.html', {'object_list': phones})
    else:
        phones = Phone.objects.all()
        return render(request, 'Inventory/phones.html', {'object_list': phones})


def remove_phone(request, phone_id):
    phones = Phone.objects.get(pk=phone_id)
    t = phones.site.pk
    if phones.site is not None:
        phones.site = None
        phones.save()
        return detail(request, pk=t)


class PhoneToSite(UpdateView):
    model = Phone
    fields = ['site', 'device_name', 'device_pool']
    success_url = '/netops/phones'


class UpdatePhone(UpdateView):
    model = Phone
    fields = ['site', 'device_name', 'desc', 'device_pool', 'dir_num']
    success_url = '/netops/phones'


class DeletePhone(DeleteView):
    model = Phone
    success_url = reverse_lazy('Inventory:phones')

