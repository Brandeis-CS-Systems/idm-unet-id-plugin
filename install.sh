#!/bin/sh
set -e

SITE_PACKAGES=$(python3 -c 'from sys import version_info as v; print(f"/usr/lib/python{v.major}.{v.minor}/site-packages")')

cp schema.d/89-schemathing.ldif /usr/share/ipa/schema.d/

mkdir -p -m 755 /usr/share/ipa/ui/js/plugins/unetuser
cp -v ui/js/plugins/unetuser/unetuser.js /usr/share/ipa/ui/js/plugins/unetuser/


cp -v ipaserver/plugins/*.py ${SITE_PACKAGES}/ipaserver/plugins

ipa-ldap-updater \
    -S /usr/share/ipa/schema.d/89-schemathing.ldif

python3 -m compileall ${SITE_PACKAGES}/ipaserver/plugins



ipactl restart
