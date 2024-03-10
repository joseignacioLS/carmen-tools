# PNGTOICO

**v.2.0.1**

## Descripción

Script para convertir archivos en formato ```.png``` a un ```.ico``` en multiples resoluciones.

## Uso

1. Copiar a una carpeta fija (por ejemplo: ```C:\Programas\pngtoico\```)
2. Preparar su ejecución
   1. Como PATH:
      1. Ir a variables de entorno
      2. Añadir la ruta donde se guardo el exe (por ejemplo: ```C:\Programas\pngtoico\pngtoico.exe```)
   2. Como acción en menu contextual
      1. Abrir el editor de registro
      2. Navegar hasta ```Equipo\HKEY_CURRENT_USER\SOFTWARE\Classes\Directory\Background\shell```
      3. Generar una nueva clave con nombre ```pngtoico```
      4. Dentro de ````pngtoico```` generar una nueva clave con nombre ```command``` y modificar el valor a la ruta del exe (por ejemplo: ```C:\Programas\pngtoico\pngtoico.exe```)
2. Generar configuracion 
   1. Configuración Global
      1. Añadir un archivo ```config.txt``` a la misma localización que el exe.
   2. Configuración Local
      1. Añadir un archivo ```config.txt``` en la localización donde se va a ejecutar el programa.
3. Ejecutar
   1. Como PATH:
      1. Abrir una consola
      2. Posicionarse en el directorio donde se encuentran los ```png``` a convertir
      3. Escribir en consola ```pngtoico``` y pulsar intro
   2. Como acción en el menu contextual
      1. Abrir la carpeta con los ```png``` en el explorador de windows
      2. Clicar con el botón derecho del ratón en el fondo de la carpeta (no en los archivos)
      3. Clickar en ````pngtoico````
4. Gestión de errores
   1. Tras cada ejecución se genera un archivo Log con los posibles errores

Tras esto los archivos ```.png``` deben haberse copiado dentro de una carpeta llamada png y haber sido sustituidos por los archivos ```.ico``` renombrados acorde al archivo de configuración.

Además, se genera un archivo ```log.txt``` que contiene información del proceso, incluido posibles errores.

## Detalles sobre el archivo de configuración

- En caso de no haber resoluciones, el programa no se ejecuta.
- Las resoluciones deben ordenadores de mayor a menor.
- Puede añadirse una linea con el caracter ```-``` para diferenciar las resoluciones altas de las bajas. Esto es útil cuando se generan icos a partir de dos imágenes. Las resoluciones altas usan la primera imagen y las altas para la segunda.
- Los nombres de los archivos deben estar separados por tabulaciones.
- El primer nombre de archivo indica el nombre del ```.png```, y el segundo el del ```.ico```.
- Si no encuentra un nombre en el lista, usará el nombre original para nombrar al ```.ico```.