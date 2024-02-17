# PNGTOICO

**v.0.1.2**

## Descripción

Script para convertir archivos en formato ```.png``` a un ```.ico``` en multiples resoluciones.

## Uso

1. Copiar a la carpeta en la que se encuentren los archivos ```.png```.
2. Generar el archivo de configuracion ```config.txt```. Ver [ejemplo](./config.txt).
3. Ejecutar el archivo ```.exe```.

Tras esto los archivos ```.png``` deben haberse copiado dentro de una carpeta llamada png y haber sido sustituidos por los archivos ```.ico``` renombrados acorde al archivo de configuración.

Además, se genera un archivo ```log.txt``` que contiene información del proceso, incluido posibles errores.

## Detalles sobre el archivo de configuración

- En caso de no haber resoluciones, el programa no se ejecuta.
- No puede haber líneas vacías.
- Los nombres de los archivos deben estar separados por tabulaciones.
- El primer nombre de archivo indica el nombre del ```.png```, y el segundo el del ```.ico```.
- Si no encuentra un nombre en el lista, usará el nombre original para nombrar al ```.ico```.