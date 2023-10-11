# Hops

> Los hops son los saltos que se deben ir haciendo entre nodos para poder establecer los distintos tuneles ssh

Se componen de:
- **host**: Es el host al cual se va a establecer la sesion de ssh.
- **port**: Es el puerto del host al cual se va a establecer la sesion de ssh (default=22).
- **user**: User que se usara para la sesion de ssh.
- **auth**: Aqui se encuentra lo relacionado a autenticacion en la sesion, contiene:
    - ***key (opcional)***: Ruta de archivo rsa/key para poder autenticarse (default=null).
    - ***password (opcional)***: Contraseña que se usara para loguearse, tambien soporta que se le ingrese una ruta de archivo el cual debera contener la contraseña (default=null).
- **tunnels**: Tienen el formato *ip_local:host_remoto:ip_remota* y son basicamente los mapeos de puertos que se haran por cada salto.

Un ejemplo seria:
```
host: 192.168.0.1
user: root
auth:
    password: "UnaPass"
tunnels:
    - 2202:192.168.0.2:22
    - 2203:192.168.0.3:22
```
El cual mapea el puerto **22** de *192.168.0.2* al puerto **2202** local y el puerto **22** de *192.168.0.3* al puerto **2203** local a traves del host *192.168.0.1* con el user *root* y la pass *UnaPass*

# Aclaraciones
- Por lo general el penultimo mapeo mapea el puerto 22 de algun host intermedio a un puerto local, para despues poder autenticarse contra a ese desde el puerto local y crear la mayoria de los tuneles que se necesitan.
- En el campo **auth** pueden ir en simultaneo ***key*** y ***password***, pero siempre deber haber al menos una.

[**Volver**](README.md)
