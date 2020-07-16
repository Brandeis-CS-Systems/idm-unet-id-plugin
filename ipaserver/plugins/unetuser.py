from ipalib import _
from ipalib.parameters import Str

from ipaserver.plugins.baseuser import baseuser
from ipaserver.plugins.user import user, user_add, user_mod

if "unetuser" not in user.possible_objectclasses:
    user.possible_objectclasses.append("unetuser")

unetuser_attributes = ["unetid"]
user.default_attributes.extend(unetuser_attributes)
takes_params = (
    Str('unetid?',
        cli_name="unetid",
        maxlength=64,
        label=_("User UNET uid")),
)

user.takes_params += takes_params

user.managed_permissions.update(
    {
        "System: Read UNET ID": {
            "replaces_global_anonymous_aci": True,
            "ipapermbindruletype": "anonymous",
            "ipapermright": {"read", "search", "compare"},
            "ipapermtargetfilter": ["(objectclass=unetUser)"],
            "ipapermdefaultattr": set(unetuser_attributes),
        },
        
    }
)

# def useradd_precallback(self, ldap, dn, entry, attrs_list,*keys, **options):
#     entry['objectclass'].append('unetuser')
#     return dn

# user_add.register_pre_callback(useradd_precallback)

def usermod_precallback(self, ldap, dn, entry, attrs_list,*keys, **options):
    if 'objectclass' not in entry.keys():
        old_entry = ldap.get_entry(dn, ['objectclass'])
        entry['objectclass'] = old_entry['objectclass']
    if not self.obj.has_objectclass(entry["objectclass"], 'unetuser'):
        entry['objectclass'].append('unetuser')
    return dn

user_mod.register_pre_callback(usermod_precallback)