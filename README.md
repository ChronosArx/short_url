## Shoten Url

Este es un backend, para acortar urls el cual esta creado en Python y FastApi..
Este backend cuenta con autentificación de usuario por medio de JWT asi como la aplicación de HASH para
la protección de las contraseñas en la base de datos. Para utilizar este proyecto en local primero se debe de clonar el repositorio

```Bash
git clone git@github.com:ChronosArx/short_url.git
```

Posteriormente de haber clando el repositorio se debera de crear un entorno virtual para poder instalar las dependencias del proyecto mediante el siguiente comando.

```Bash
pip -m venv venv
```

Una vez creado es necesario activar el entorno virtual.

- En Windows:

```Powershell
.\venv\Scripts\activate
```

- En linux y Mac:

```Bash
source ./venv/bin/activate
```

Con el entorno virtual instalado es momento de instalar las dependencias, estas se pueden instalar por medio del siguiente comando.

```Bash
pip install -r requirements.txt
```

Antes de ejecutar el servidor este proyecto necesita de algunas variables de entorno para poder funcionar de manera correcta las variables de entorno son las siguientes.

```env
TOKEN_ALG='HS256'
SECRET=?
EXPIRE_ACCESS=?
EXPIRE_REFRESH=?
DOMAIN_URL=?
DATABASE_URL=?
```

##### TOKEN_ALG:

Algoritmo usado para firmar los tokens,se recomienda usar HS256.

SECRET_KEY es la llave secreta que sera usada para la firam de los tokens JWT se recomienda usar un generador de claves para que sean mucho mas seguros.

EXPIRE_ACCESS es el tiempo que dura el token de acceso a la api se debe colocar un numero entero y el tiempo de este es en minutos se recomienda colocar un tiempo corto entre los 5 y 15 minutos.

EXPIRE_REFRESH es el tiempo que dura el refresh token el cual es de larga duración, igual debe ser un numero entero y este tiempo de expiración es en dias, este se usa para la optención de nuevos access tokens.

DOMAIN_URL es el dominio propio y es el cual se usara para crear los urls acortados y el como se guardaran en la base de datos.

DATABASE_URL es la url de conección para la base de datos.

Una vez que todas las variables de entorno se encuentren en su lugar y correctamente se puede usar el siguiente comando para ejecutar el repsotiroio en modo desarrollo.

```Bash
fastapi dev ./app/main.py
```

## Usando Doker

Este proyecto tambien se puede ejecutar usando Docker para poder ejecutar el proyecto en docker primero se debe crear una imagen del proyecto, esta imagen se puede crear con el siguiente comando:

```Bash
docker build -t shorten:1
```

Para verificar que la imagen fue creada correcta mente ejecute el siguiente comando y deberia de aparecer la imagen:

```Bash
docker images
```

Con esto listo se puede ejecutar el contenedor con el siguiente comando:

> ⚠️ **Warning**: Tanto el primer comando como el ultimo de estos comando con docker deben ejecutarse dentro de la carpeta del proyecto, de igual manera el archivo .env es necesario con sus variables de entorno configuradas correcta mente ya que se pasaran al comando para ejecutar el contenedor.

```Bash
docker run -p8000:8000 --name api --env-file .env shorten:1
```

Una vez ejecutado el contenedor o el proyecto por medio del cli de FastAPI se puede acceder a la documentación intercativa del proyecto en la siguiente URL:

```
http://localhost:8000/docs
```
