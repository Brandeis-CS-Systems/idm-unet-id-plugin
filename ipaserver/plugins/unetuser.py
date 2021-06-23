from ipalib import _
from ipalib.parameters import Str, Bool, Int

from ipaserver.plugins.baseuser import baseuser
from ipaserver.plugins.user import user, user_add, user_mod
from ipaserver.plugins.stageuser import stageuser_add, stageuser_mod

if "unetuser" not in user.possible_objectclasses:
    user.possible_objectclasses.append("unetuser")

unetuser_attributes = ["unetid", "sponsor", "fwdemail", "expectedgraduation", "allowunetreset"]
user.default_attributes.extend(unetuser_attributes)
takes_params = (
    Str('unetid?',
        cli_name="unetid",
        maxlength=64,
        label=_("User UNET uid")),
    Str('sponsor?',
        cli_name="sponsor",
        maxlength=64,
        label=_("Sponsor")),
    Bool('fwdemail?',
        cli_name="fwdemail",
        label="Forward email?"),
    Int('expectedgraduation?',
        cli_name='expectedgraduation',
        label=_("Expected graduation year")),
    Bool('allowunetreset?',
        cli_name='allowunetreset',
        label=_("Allow reset with UNET ID"))
)

user.takes_params += takes_params

user.managed_permissions.update(
    {
        "System: Read UNET ID": {
            "replaces_global_anonymous_aci": True,
            "ipapermbindruletype": "all",
            "ipapermright": {"read", "search", "compare"},
            "ipapermtargetfilter": ["(objectclass=unetuser)"],
            "ipapermdefaultattr": set(unetuser_attributes),
        },
        
    }
)

def useradd_precallback(self, ldap, dn, entry, attrs_list,*keys, **options):
    entry['objectclass'].append('unetuser')
    return dn

user_add.register_pre_callback(useradd_precallback)
stageuser_add.register_pre_callback(useradd_precallback)

def usermod_precallback(self, ldap, dn, entry, attrs_list,*keys, **options):
    if 'objectclass' not in entry.keys():
        old_entry = ldap.get_entry(dn, ['objectclass'])
        entry['objectclass'] = old_entry['objectclass']
    if not self.obj.has_objectclass(entry["objectclass"], 'unetuser'):
        entry['objectclass'].append('unetuser')
    return dn

user_mod.register_pre_callback(usermod_precallback)
stageuser_mod.register_pre_callback(usermod_precallback)
