# PNGTOICO

**v.2.0.1**

## Descripci�n

Script para convertir archivos en formato ```.png``` a un ```.ico``` en multiples resoluciones.

## Uso

1. Copiar a una carpeta fija (por ejemplo: ```C:\Programas\pngtoico\```)
2. Preparar su ejecuci�n
   1. Como PATH:
      1. Ir a variables de entorno
      2. A�adir la ruta donde se guardo el exe (por ejemplo: ```C:\Programas\pngtoico\pngtoico.exe```)
   2. Como acci�n en menu contextual
      1. Abrir el editor de registro
      2. Navegar hasta ```Equipo\HKEY_CURRENT_USER\SOFTWARE\Classes\Directory\Background\shell```
      3. Generar una nueva clave con nombre ```pngtoico```
      4. Dentro de ````pngtoico```` generar una nueva clave con nombre ```command``` y modificar el valor a la ruta del exe (por ejemplo: ```C:\Programas\pngtoico\pngtoico.exe```)
2. Generar configuracion 
   1. Configuraci�n Global
      1. A�adir un archivo ```config.txt``` a la misma localizaci�n que el exe.
   2. Configuraci�n Local
      1. A�adir un archivo ```config.txt``` en la localizaci�n donde se va a ejecutar el programa.
3. Ejecutar
   1. Como PATH:
      1. Abrir una consola
      2. Posicionarse en el directorio donde se encuentran los ```png``` a convertir
      3. Escribir en consola ```pngtoico``` y pulsar intro
   2. Como acci�n en el menu contextual
      1. Abrir la carpeta con los ```png``` en el explorador de windows
      2. Clicar con el bot�n derecho del rat�n en el fondo de la carpeta (no en los archivos)
      3. Clickar en ````pngtoico````
4. Gesti�n de errores
   1. Tras cada ejecuci�n se genera un archivo Log con los posibles errores

Tras esto los archivos ```.png``` deben haberse copiado dentro de una carpeta llamada png y haber sido sustituidos por los archivos ```.ico``` renombrados acorde al archivo de configuraci�n.

Adem�s, se genera un archivo ```log.txt``` que contiene informaci�n del proceso, incluido posibles errores.

## Detalles sobre el archivo de configuraci�n

- En caso de no haber resoluciones, el programa no se ejecuta.
- Las resoluciones deben ordenadores de mayor a menor.
- Puede a�adirse una linea con el caracter ```-``` para diferenciar las resoluciones altas de las bajas. Esto es �til cuando se generan icos a partir de dos im�genes. Las resoluciones altas usan la primera imagen y las altas para la segunda.
- Los nombres de los archivos deben estar separados por tabulaciones.
- El primer nombre de archivo indica el nombre del ```.png```, y el segundo el del ```.ico```.
- Si no encuentra un nombre en el lista, usar� el nombre original para nombrar al ```.ico```.