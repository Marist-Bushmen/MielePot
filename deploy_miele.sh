#!/bin/bash
docker login
docker pull dgisolfi/mielepot
docker run --rm --name miele_prod --env HPID=$(dbus-uuidgen) -p4400:4400 -d dgisolfi/mielepot
