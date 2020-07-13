#!/bin/sh
set -e

SITE_PACKAGES=$(python3 -c 'from sys import version_info as v; print(f"/usr/lib/python{v.major}.{v.minor}/site-packages")')

cp schema.d/89-schemathing.ldif /usr/share/ipa/schema.d/

cp updates/89-schemathing.update /usr/share/ipa/updates

ipa-ldap-updater \
    -S /usr/share/ipa/schema.d/89-schemathing.ldif \
    /usr/share/ipa/updates/89-schemathing.update

ipactl restart