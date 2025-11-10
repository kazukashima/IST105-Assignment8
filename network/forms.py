from django import forms

class NetworkForm(forms.Form):
    mac_address = forms.CharField(
        label="MAC Address",
        max_length=17,
        widget=forms.TextInput(attrs={'placeholder': '00:1A:2B:3C:4D:5E'})
    )
    dhcp_version = forms.ChoiceField(
        label="DHCP Version",
        choices=[('DHCPv4', 'DHCPv4'), ('DHCPv6', 'DHCPv6')]
    )
