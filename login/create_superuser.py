# create_superuser.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def main():
    numero = '020508'
    password = '020508admin'
    
    # Verifica si el superusuario ya existe
    if not User.objects.filter(numero=numero).exists():
        User.objects.create_superuser(numero=numero, password=password)
        print(f'Superusuario creado con documento: {numero}')
    else:
        print(f'El superusuario con documento {numero} ya existe.')

if __name__ == '__main__':
    main()
