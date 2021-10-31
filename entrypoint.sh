#!/bin/bash

case ${1} in
    server)
        exec poetry run gunicorn -c python:app.settings_gunicorn app.wsgi
        ;;
    *)
        echo "using ${0} [server]"
        exit 1
        ;;
esac
