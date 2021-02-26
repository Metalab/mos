#!/bin/ash

for i in $(seq 1 15); do
    nc -z "${MYSQL_HOST:=db}" "3306" > /dev/null 2>&1 && break
    echo "waiting for DB $MYSQL_HOST ($i)"
    sleep 1
done

if [ "$#" -ge "1" ]; then
    if [ "$1" == "run-dockerdev" ]; then
        set -x
        python3 manage.py migrate
        python3 manage.py runserver 0.0.0.0:8020
    else
        set -x
        python3 manage.py $@
    fi
else
    set -x
    python3 manage.py migrate || exit 1 # fail container if migration fails
    python3 manage.py collectstatic --no-input --clear --no-post-process -i "*.txt" -i "LICENSE" &
    daphne -b 0.0.0.0 -p ${DAPHNE_PORT:-3031} mos.asgi:application
fi
