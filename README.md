## Shoten Url 
Este es un backend, para acortar urls el cual esta creado en Python y FastApi..
Este backend cuenta con autentificación de usuario por medio de JWT asi como la aplicación de HASH para 
la protección de las contraseñas en la base de datos. Para utilizar este proyecto en local primero se debe de clonar el repositorio

``` Bash
git clone git@github.com:ChronosArx/short_url.git
```
Posteriormente de haber clando el repositorio se debera de crear un entorno virtual para poder instalar las dependencias del proyecto mediante el siguiente comando.

``` Bash
pip -m venv venv
```
Una vez creado es necesario activar el entorno virtual.

* En Windows:

```Powershell
.\venv\Scripts\activate
```

* En linux y Mac: 

``` Bash
source ./venv/bin/activate
```
Con el entorno virtual instalado es momento de instalar las dependencias, estas se pueden instalar por medio del siguiente comando.

``` Bash
pip install -r requirements.txt
```

Antes de ejecutar el servidor este proyecto necesita de algunas variables de entorno para poder funcionar de manera correcta las variables de entorno son las siguientes.

``` env
TOKEN_ALG='HS256'
SECRET=?
EXPIRE_ACCESS=?
EXPIRE_REFRESH=?
DOMAIN_URL=?
```
La primera de las variables de entorno es el algoritmo de hash que se usara esta herramienta usa la libreria bcrypt para los hash asi que recomendaria usar HS256 pero hay libertad de usar algun otro que sea compatible. Secret es la clave secreta que sera usada para la firam de los tokens JWT se recomendaria usar una generada de manea aletoria. Expire access es el tiempo que dura el token de acceso a la api se debe colocar un numero entero y el tiempo de este es en minutos se recomienda colocar un tiempo corto entre los 5 y 15 minutos, expire refresh es el tiempo que dura el refresh token el cual es un token de larga duración igual un numero entero y este tiempo de expiración es en dias, este se usa para la optención de nuevos acces tokens.
