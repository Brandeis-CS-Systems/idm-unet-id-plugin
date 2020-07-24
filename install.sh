#!/bin/sh
set -e

SITE_PACKAGES=$(python3 -c 'from sys import version_info as v; print(f"/usr/lib/python{v.major}.{v.minor}/site-packages")')

cp schema.d/89-schemathing.ldif /usr/share/ipa/schema.d/
cp updates/89-schemathing.update /usr/share/ipa/updates/89-schemathing.update

mkdir -p -m 755 /usr/share/ipa/ui/js/plugins/unetuser
cp ui/js/plugins/unetuser/unetuser.js /usr/share/ipa/ui/js/plugins/unetuser/


cp ipaserver/plugins/*.py ${SITE_PACKAGES}/ipaserver/plugins

ipa-ldap-updater \
    -S /usr/share/ipa/schema.d/89-schemathing.ldif \
    /usr/share/ipa/updates/89-schemathing.update

python3 -m compileall ${SITE_PACKAGES}/ipaserver/plugins



ipactl restart