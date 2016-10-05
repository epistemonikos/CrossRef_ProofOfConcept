#Reference Lookup Service

##Deploy
###Configuraciones previas para hacer deploy automático:
1. Agregar clave pública RSA asociada a la cuenta github en uso a `
~/.ssh/authorized_keys` en el servidor.
2. En el equipo local, agregar lo siguiente a `~/.ssh/config` (`<key>` representa la llave privada RSA asociada a la llave pública anterior):
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
