from ipalib import _
from ipalib.parameters import Str, Bool, Int

from ipaserver.plugins.user import user, user_add, user_mod
from ipaserver.plugins.stageuser import stageuser, stageuser_add, stageuser_mod

if "brandeiscosciperson" not in user.possible_objectclasses:
    user.possible_objectclasses.append("brandeiscosciperson")

brandeiscosciperson_attributes = [
    "unetid",
    "sponsor",
    "expectedgraduation",
    "allowunetreset",
    "favoriteicecream",
]
user.default_attributes.extend(brandeiscosciperson_attributes)
stageuser.default_attributes.extend(brandeiscosciperson_attributes)

takes_params = (
    Str("unetid?", cli_name="unetid", maxlength=64, label=_("User UNET uid")),
    Str("sponsor?", cli_name="sponsor", maxlength=64, label=_("Sponsor")),
    Int(
        "expectedgraduation?",
        cli_name="expectedgraduation",
        label=_("Expected graduation year"),
    ),
    Bool(
        "allowunetreset?",
        cli_name="allowunetreset",
        label=_("Allow reset with UNET ID"),
    ),
    Bool(
        "favoriteicecream?",
        cli_name="favoriteicecream",
        label=_("Favorite ice cream flavor"),
    ),
)
user.takes_params += takes_params
stageuser.takes_params += takes_params

read_unet_id_permission = {
    "System: Read COSCI Person Attributes": {
        "replaces_global_anonymous_aci": True,
        "ipapermbindruletype": "all",
        # "ipapermbindruletype": "anonymous",
        "ipapermright": {"read", "search", "compare"},
        "ipapermtargetfilter": ["(objectclass=brandeiscosciperson)"],
        "ipapermdefaultattr": set(brandeiscosciperson_attributes),
    },
}
user.managed_permissions.update(read_unet_id_permission)
# stageuser.managed_permissions.update(read_unet_id_permission)


def useradd_precallback(self, ldap, dn, entry, attrs_list, *keys, **options):
    entry["objectclass"].append("brandeiscosciperson")
    return dn


user_add.register_pre_callback(useradd_precallback)
stageuser_add.register_pre_callback(useradd_precallback)


def usermod_precallback(self, ldap, dn, entry, attrs_list, *keys, **options):
    if "objectclass" not in entry.keys():
        old_entry = ldap.get_entry(dn, ["objectclass"])
        entry["objectclass"] = old_entry["objectclass"]
    if not self.obj.has_objectclass(entry["objectclass"], "brandeiscosciperson"):
        entry["objectclass"].append("brandeiscosciperson")
    return dn


user_mod.register_pre_callback(usermod_precallback)
stageuser_mod.register_pre_callback(usermod_precallback)
