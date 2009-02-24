#!/bin/sh

# Script para regenerar planeta PyAr
cd ~/.rawdog

# Regenerar la configuración
python merge-config.py

# Bajar los feeds
rawdog -u

# Regenerar planeta full
LANG=es_ES rawdog -c config-full -w

# Regenerar planeta solo python
LANG=es_ES rawdog -c config-python -w

# Subir a github
git commit -a
git push origin master 
