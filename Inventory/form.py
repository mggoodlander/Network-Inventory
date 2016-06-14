from django.contrib.auth.models import User
from django import forms
from .models import Site, Config, Device


class SiteForm(forms.ModelForm):

    class Meta:
        model = Site
        fields = ['siteCode', 'city', 'state', 'address', 'zipcode']


class ConfigForm(forms.ModelForm):

    class Meta:
        model = Config
        fields = [
            'site', 'provider', 'circuit_id', 'svc_id', 'prefix', 'wan_net', 'wan_remote', 'wan_local', 'name_fw',
            'fw_type', 'name_sw', 'sw_type', 'fw_lan', 'sw_lan', 'fw_lo', 'sw_lo', 'peer_asn', 'local_asn',
            'ospf_area'
        ]


class DeviceForm(forms.ModelForm):

        class Meta:
            model = Device
            fields = [ 'device', 'serial', 'mac_add', 'device_name', 'firm_ver', 'hard_type', 'asset_tag']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields =['username', 'email', 'password']