from django.db import models
from django.core.urlresolvers import reverse


class Site(models.Model):
    siteCode = models.CharField(max_length=10, blank=False)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=5)
    is_closed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('Inventory:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.siteCode


class Config(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    service = ((' ', ' '),
               ("1.5 Mb T1 MPLS", "1.5 Mb T1 MPLS"),
               ('3 Mb T1 MPLS', '3 Mb T1 MPLS'),
               ('4.5 Mb MPLS', '4.5 Mb MPLS'),
               ('10 Mb MPLS', '10 Mb MPLS'),
               ('20 Mb MPLS', '20 Mb MPLS'),
               ('44 Mb MPLS', '44 Mb MPLS'),
               ('50 Mb MPLS', '50 Mb MPLS'),
               ('Broadband', 'Broadband'),
               )
    provider_C = ((" ", " "),
                  ("provider", "provider"),
                  ("provider1", "provider1"),
                  ("provider2", "provider2"),
                  )
    fw_tp = ((' ', ' '),
             ('fw1', 'fw1'),
             ('fw2', 'fw2'),
             )
    sw_tp = ((" ", " "),
             ("sw1", "sw1"),
             ("sw2", "sw2"),
             ("sw3", "sw3"),
             ("sw4", "sw4"),
             )

    provider = models.CharField(max_length=50, choices=provider_C, blank=True)
    circuit_id = models.CharField(max_length=200, blank=True)
    svc_id = models.CharField(max_length=200, choices=service, blank=True)
    prefix = models.CharField(max_length=200, blank=True)
    wan_net = models.CharField(max_length=200, blank=True)
    wan_remote = models.CharField(max_length=200, blank=True)
    wan_local = models.CharField(max_length=200, blank=True)
    name_fw = models.CharField(max_length=200, blank=True)
    fw_type = models.CharField(max_length=200, choices=fw_tp, blank=True)
    name_sw = models.CharField(max_length=200, default='')
    sw_type = models.CharField(max_length=200, choices=sw_tp, blank=True)
    fw_lan = models.CharField(max_length=200, blank=True)
    sw_lan = models.CharField(max_length=200, blank=True)
    fw_lo = models.CharField(max_length=200, blank=True)
    sw_lo = models.CharField(max_length=200, blank=True)
    peer_asn = models.CharField(max_length=200, blank=True)
    local_asn = models.CharField(max_length=200, blank=True)
    ospf_area = models.CharField(max_length=200, blank=True)
    cre_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('Inventory:detail', kwargs={'pk': Config.pk,
                                                   'detail_pk': self.pk})

    def __str__(self):
        return self.name_fw


class Device(models.Model):
    device = models.ForeignKey(Site, null=True, on_delete=models.SET_NULL, blank=True)
    serial = models.CharField(max_length=100)
    mac_add = models.CharField(max_length=30)
    device_name = models.CharField(max_length=40)
    firm_ver = models.CharField(max_length=40)
    hard_type = models.CharField(max_length=50)
    asset_tag = models.CharField(max_length=50, default='None')

    def __str__(self):
        return self.device_name
