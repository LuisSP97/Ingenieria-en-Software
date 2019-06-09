Para poder usar MySQL deben descargar el driver desde este link:

https://pypi.org/project/mysqlclient/

Van a necesitar tener instalado el pip, deberían tenerlo instalado ya que es necesario para instalar Django.

Una vez lo instalen tienen que ir a la carpeta del proyecto y abrir el archivo “settings.py”. Luego van al apartado “DATABASES” y ahí tienen que reemplazarlo por lo siguiente:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'NOMBRE_BDD',
        'USER': 'root',
        'PASSWORD': 'SU_PASSWORD_ROOT',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

Y con eso ya tienen conectada la base de datos al proyecto de Django.
