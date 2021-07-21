# idm-unet-id-plugin

Extends the Red Hat IDM 389ds schema to include fields related to CS
user accounts.

Helpful links:
* https://www.freeipa.org/images/5/5b/FreeIPA33-extending-freeipa.pdf

Somewhat poorly based on https://github.com/fedora-infra/freeipa-fas

# Changing UNET attribute permissions

Before a change to `System: Read UNET ID` can take effect, you need to
remove the existing permission from LDAP (just running `install.sh` won't
overwrite the existing permission):
```
ldapmodify -h localhost -p 389 -D "cn=Directory Manager" -w $PASSWORD < delete_unet_permission.ldif
```
