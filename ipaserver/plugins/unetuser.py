from ipalib import _
from ipalib.parameters import Str

from ipaserver.plugins.baseuser import baseuser
from ipaserver.plugins.user import user, user_add, user_mod

if "unetUser" not in user.possible_objectclasses:
    user.possible_objectclasses.append("unetUser")

unetuser_attributes = ["unetID"]
user.default_attributes.extend(unetuser_attributes)
takes_params = (
    Str('unetid',
        cli_name="unetid",
        maxlength=64,
        label=_("User UNET uid")),
)

user.takes_params += takes_params

user.managed_permissions.update(
    {
        "System: Read UNET ID": {
            "replaces_global_anonymous_aci": True,
            "ipapermbindruletype": "all",
            "ipapermright": {"read", "search", "compare"},
            "ipapermtargetfilter": ["(objectclass=unetUser)"],
            "ipapermdefaultattr": set(unetuser_attributes),
        },
        
    }
)

def useradd_precallback(self, ldap, dn, entry, attrs_list,*keys, **options):
    entry['objectclass'].append('unetUser')
    return dn

user_add.register_pre_callback(useradd_precallback)

def usermod_precallback(self, ldap, dn, entry, attrs_list,*keys, **options):
    if 'objectclass' not in entry.keys():
        old_entry = ldap.get_entry(dn, ['objectclass'])
        entry['objectclass'] = old_entry['objectclass']
    entry['objectclass'].append('unetUser')
    return dn

user_mod.register_pre_callback(usermod_precallback)