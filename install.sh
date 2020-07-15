#!/bin/sh
set -e

SITE_PACKAGES=$(python3 -c 'from sys import version_info as v; print(f"/usr/lib/python{v.major}.{v.minor}/site-packages")')

cp schema.d/89-schemathing.ldif /usr/share/ipa/schema.d/


ipa-ldap-updater \
    -S /usr/share/ipa/schema.d/89-schemathing.ldif

cp ipaserver/plugins/*.py ${SITE_PACKAGES}/ipaserver/plugins
python3 -m compileall ${SITE_PACKAGES}/ipaserver/plugins


ipactl restart