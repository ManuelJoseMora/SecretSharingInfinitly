#                                     ----------------------------------------------
#                                     ------     Secret SharingI Infinitely  -------
#                                     ----------------------------------------------

## Master en Ciberseguridad y Privacidad 2021/2022
### Universisad Rey Juan Carlos

### TFM 2022 - Secret Sharing Infinitly
##### Autor: Manuel Jose Mora Cordero


El siguiente software es un prueba de concepto de como se puede implementar un método de compartición de secretos de manera infnita. es decir, sin necesisas de fijar un número n de participantes.

La idea base esta sacada del documento "How to Share a Secret, Infinitely", Komargodski, Naor & Yogev, 2016. 
(KNY16] Ilan Komargodski, Moni Naor, and Eylon Yogev. How to share a secret, infinitely. In Theory of Cryptography - 14th International Conference, TCC 2016-B, pages 485–514 2016.) [Link](https://eprint.iacr.org/2016/194.pdf).

El proposito de este software es generar una prueba de concepto que acompañe al texto explicativo o memoria del trabajo fin de máster. 
No es proposito de este software desarrollar una herramienta completa, totalmente funcional, sino la de hacer ver como se puede construir este tipo de esquemas de compartición de secretos, basandones en las ideas recogidas en el documento antes mencionado.

El software ha sido desarrollado usando 

> Python 3.8.8 

Librerías y versiones instaladas necesarias:

> shamirs==2.0.2

> pandas==1.2.4

El software esta diseñado como un simple script de Python, ejecutable desde consola de comandos invocandolo mediante el interprete Python desde la ruta donde se encuentre el fichero .py

> python sss_infinitly.py

![alt text](https://github.com/ManuelJoseMora/SecretSharingInfinitly/blob/develop/screenshots/captura_ejecuta_script.JPG)


Deberás introducir un entero positivo que será la clave sobre la que se generarán los "shares" y el "threshold" k ó numero entero positivo que indique el número de participantes necesario para pdoer obtener la clave.

![alt text](https://github.com/ManuelJoseMora/SecretSharingInfinitly/blob/develop/screenshots/captura_key_threshold_menu_principal.JPG)

Indica la opción 1 y ve añadiendo nombres de usuarios:

![alt text](https://github.com/ManuelJoseMora/SecretSharingInfinitly/blob/develop/screenshots/captura_add_usuario.JPG)

Añade nombres de usuarios. Puedes Listarlos usando la opción 4:

![alt text](https://github.com/ManuelJoseMora/SecretSharingInfinitly/blob/develop/screenshots/captura_listar_usuarios.JPG)

Añade una lista separada por comas con los nombres de los usuarios que cumplan con el k "threshold" necesario para poder obtener la clave usando la opción 2:

![alt text](https://github.com/ManuelJoseMora/SecretSharingInfinitly/blob/develop/screenshots/captura_añade_usuarios_desencriptar.JPG)

Usa la opción 6 para reconstruir la clave:

![alt text](https://github.com/ManuelJoseMora/SecretSharingInfinitly/blob/develop/screenshots/captura_desencriptar.JPG







