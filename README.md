# SSHake

> Herramienta para facilitar el mapeo de tuneles ssh

![alt text](img/ssh.jpg)

## REQUERIMIENTOS

### 1era opcion
* **Docker**
### 2da opcion
* **Python 3.8+**
* **openssh-server**
* **sshpass**

## EJECUCION

* Para ejecutarlo, pararse en la ruta raiz del proyecto y ejecutar:
```
chmod +x run_dockerized.sh
./run_dockerized.sh path_a_archivo_config_yml
```

## CONFIGURACION
Toda la configuracion necesaria para que funcione la herramienta esta en el archivo yml, el cual tiene los siguientes campos:

* **hops**: En este campo se encuentran en forma de lista todos los hops (o saltos) por los que se ira tuneleando con sus respectivos mapeos ([Ver documentacion hops](hops.md)).
* **logging**: En esta propiedad se especifican los parametros de logueo como:
    - ***dir***: Si se quiere que los logs se dumpeen a un determinado directorio (default=null)
    - ***level***: Nivel al que se logueara (INFO,DEBUG,ERROR,WARNING) (default=DEBUG)
    
## EJEMPLOS
Supongase que se tiene un config en files/config.yml entonces:
* Ejecutar `./run_dockerized.sh files/config.yml`
