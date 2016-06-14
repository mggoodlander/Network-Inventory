from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView
from .models import Site, Config, Device
from .form import UserForm, SiteForm, ConfigForm, DeviceForm


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


def create_detail(request, pk):
    form = ConfigForm(request.POST or None)
    sites = get_object_or_404(Site, pk=pk)
    if form.is_valid():
        site_details = sites.config_set.all()
        details = form.save(commit=False)
        details.sites = sites
        details.save()
        return render(request, 'Inventory/detail.html', {'sites': sites})
    context = {
        'sites': sites,
        'form': form
    }
    return render(request, 'Inventory/config_form.html', context)


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
    success_url = '/Inventory/sites'


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
            Q(city__contains=query)
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
            Q(device__address__contains=query) |
            Q(mac_add__contains=query) |
            Q(serial__contains=query) |
            Q(hard_type=query)|
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


class DeviceUpdate(UpdateView):
    model = Device
    fields = ['device']
    success_url = '/Inventory/devices'


class DeviceDelete(DeleteView):
    model = Device
    success_url = reverse_lazy('Inventory:devices')