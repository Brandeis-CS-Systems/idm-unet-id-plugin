#!/bin/sh
set -e

SITE_PACKAGES=$(python3 -c 'from sys import version_info as v; print(f"/usr/lib/python{v.major}.{v.minor}/site-packages")')

cp -v schema.d/89-schemathing.ldif /usr/share/ipa/schema.d/
mkdir -p -m 755 /usr/share/ipa/ui/js/plugins/brandeiscosciperson
cp -v ui/js/plugins/brandeiscosciperson/brandeiscosciperson.js /usr/share/ipa/ui/js/plugins/brandeiscosciperson/

cp -v ipaserver/plugins/*.py ${SITE_PACKAGES}/ipaserver/plugins
chcon system_u:object_r:lib_t:s0 \
    /usr/lib/python3.6/site-packages/ipaserver/plugins/brandeiscosciperson.py

ipa-ldap-updater -S /usr/share/ipa/schema.d/89-schemathing.ldif
python3 -m compileall ${SITE_PACKAGES}/ipaserver/plugins

ipactl restart
