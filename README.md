#Reference Lookup Service

##Deploy
###Configuraciones previas para hacer deploy automático:
1. Agregar clave pública RSA asociada a la cuenta github en uso a `~/.ssh/authorized_keys` en el servidor.
2. Debe existir un archivo `.env` en `/home/ubuntu` con el siguiente contenido:
```
export REFSERVICE_SECRETKEY='<secret_key>'
```
Donde `<secret_key>` es un string aleatorio y secreto. Se utiliza en el servicio para serializar cosas, y en el futuro podría ocuparse para la segurida del mismo.
3. Agregar la siguiente línea al principio de `/home/ubuntu/.bashrc` en el servidor:
```
source ./.env
```
4. En el equipo local, agregar lo siguiente a `~/.ssh/config` (`<key>` representa la llave privada RSA asociada a la llave pública anterior):
```
Host epistemonikos 52.3.221.80
    Hostname 52.3.221.80
    Port 22
    IdentityFile ~/.ssh/<key>
    User ubuntu
    ForwardAgent yes
```


###Comando para hacer deploy:
`ssh epistemonikos "cd ReferenceLookupService && sh deploy.sh"`

Este comando se encarga de actualizar el repositorio desde git, y de 
reiniciar el servicio web.
