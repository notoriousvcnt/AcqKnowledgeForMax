# AcqKnowledgeForMax : dev

AcqKnowledgeForMax es una serie de archivos para conectar el software AcqKnowledge con Max 8 a través de Network Data Transfer (NDT), usando TCP y/o OSC. Es necesario tener una licencia de NDT para utilizar dicha funcionalidad en AcqKnowledge.

Este repositorio contiene archivos de python para configurar remotamente el servidor TCP de AcqKnowledge y existen versiones para enviar los datos a través de un servidor TCP a Max o a través del protocolo OSC. Parches de ejemplo en Max 8 también son incluidos.

Los archivos `.py` son modificaciones de las implementaciones entregadas por BIOPAC al adquirir NDT. Gran parte del código se encarga de configurar el servidor para enviar la información de la forma requerida según el cliente a través del protocolo XML-RPC. El detalle de los comandos y sus funciones está extensamente documentado en el software AcqKnowledge o en el manual de uso en PDF de AcqKnowledge.

Por otra parte, los archivos `.maxpat` se encargan de recibir y decodificar la información entregada desde AcqKnowledge o Python (ver sección de Uso) usando la librería Sadam disponible en el Package Manager de Max.  Los parches están adaptados para recibir seis (6) entradas correspondientes al Zephyr BioHarness, pero puede adaptarse para otras configuraciones.

## Requerimientos

* Python 3.9:
  * python-osc
* AcqKnowledge 5.0:
  * NDT
* Max 8:
  * Sadam Library 20.3.7 (disponible en el Package Manager)

## Uso

Lo primero que se debe realizar es configurar el servidor de AcqKnowledge para enviar datos según la configuración deseable.  Esto se realiza a través del protocolo XML-RPC y se utiliza el código de Python implementado por BIOPAC (sólo modificado para que funcione en python 3.x).  La implementación de este repositorio configura el envío en modo 'single' y con entradas que posean la misma frecuencia de muestreo. Para más información sobre manejo de señales con frecuencia de muestreo variables revisar la documentación de NDT.

A continuación se muestran dos formas de recibir los datos fuera de AcqKnowledge: a través de un servidor TCP directamente desde AcqKnowledge, y a través del protocolo OSC que utiliza como intermediario un servidor TCP implementado en python para recibir los datos desde AcqKnowledge y que luego se envían por OSC. **En ambos casos el archivo `.py` se encarga de configurar el servidor y prepararlo para el correcto envío de los datos**.  

###  A través de servidor TCP

1. Abrir AcqKnowledge. Asegurarse que en preferencias está habilitado NDT (Display > Preferences.)

2. Ejecutar `python `/`singleconnection_multioption.py` . 
3. Abrir `max`/ `AcqKnowledge_TCPClient_example.maxpat`.
4. Al abrir el parche de Max el cliente se activa automáticamente en el puerto 15020, por lo que no es necesario encenderlo. Es muy importante encender el cliente TCP antes de iniciar la adquisición en AcqKnowledge ya que no se permiten conexiones nuevas una vez que se están capturando los datos.
5. Iniciar adquisición en AcqKnowledge.

### A través de protocolo OSC

1. Abrir AcqKnowledge. Asegurarse que en preferencias está habilitado NDT (Display > Preferences.)
2. Abrir `max `/ `AcqKnowledge_OSC_example.maxpat`.
3. Encender cliente OSC en Max.
4. Ejecutar `python`/`singleconnection_multioption.py` con el argumento opcional ``-osc`` . En la línea de comando se entrega la información sobre el puerto al cual se debe conectar el cliente OSC (por defecto puerto 5005). 
5. Iniciar adquisición en AcqKnowledge.

### Argumentos opcionales

Adicionalmente,  se puede ejecutar ``singleconnection_multioption.py -h`` para ver todas los argumentos opcionales disponibles. Se pueden agregar los siguientes argumentos:

``-h`` o ``--help`` Muestra esta lista.

``-ch <hostname>``  o ``--controlHost <hostname>`` para configurar el hostname de control del servidor AcqKnowledge a través del protocolo XML-RPC.

``-cp <port>``  o ``--controlPort <port>`` para configurar el puerto de control del servidor AcqKnowledge a través del protocolo XML-RPC.

``-ah <hostname>``  o ``--AcqHost <hostname>`` para configurar el hostname del servidor TCP de Adquisición de Datos.

``-ap <port>``  o ``--AcqPort <port>`` para configurar el puerto del servidor TCP de Adquisición de Datos.

``-osc`` o ``--oscActivated`` para activar el envío de datos por OSC en vez de TCP.

``-oh <hostname>``  o ``--OSCHost <hostname>`` para configurar el hostname de envío de datos vía OSC (sin efecto si no se especifica la opción ``--oscActivated``).

``-op <port>``  o `` --OSCport <port>`` para configurar el puerto de envío de datos vía OSC (sin efecto si no se especifica la opción ``--oscActivated``).

## Archivos del proyecto

### `python`

Contiene las implementaciones y ejemplos para recibir datos desde AcqKnowledge vía NDT a través de una conexión TCP. Estos archivos están basados en los ejemplos entregados por BIOPAC para trabajar con NDT y en particular están adaptados para manejar la información adquirida a través del sistema Zehpyr BioHarness, pero podría recibir información de otras configuraciones si se hacen los cambios correspondientes.

* `biopacndt.py` : Implementación del módulo de Python biopacndt con clases y funciones que simplifican el control de instancias remotas de AcqKnowledge y procesamiento de datos binarios enviados por AcqKnowledge a través de internet.  Esta implementación ha sido desarrollada por BIOPAC y forma parte de los archivos de ejemplos de NDT disponibles en los archivos de AcqKnowledge pero ha sido modificada para funcionar en python 3.x y se ha agregado la funcionalidad de enviar la información fuera de python a través del protocol OSC.
* ``singleconnection_multioption.py``: Archivo de ejemplo para configurar y recibir información desde el servidor de AcqKnowledge en modo 'single connection' vía TCP o OSC.  Se puede ejecutar ``singleconnection_multioption.py -h`` para ver todas los argumentos opcionales disponibles.  
  * En el caso del envío vía TCP el programa **no** recibe información. La implementación del **cliente** que recibe los datos está disponible en ``AcqKnowledge_TCPClient_example.maxpat`` . Por default la información es enviada hacia `127.0.0.1` en el puerto `15020` .
  * Si se ejecuta ``singleconnection_multioption.py -osc``  se realiza el envío de los datos a través del protocolo OSC a la dirección `127.0.0.1` en el puerto `5005` con la etiqueta `/BioHarness`. 

### `max`

Archivos de ejemplo para recibir los datos de AcqKnowledge en Max. En particular, están adaptados para manejar la información adquirida a través del sistema Zehpyr BioHarness, pero podría recibir información de otras configuraciones si se hacen los cambios correspondientes.

* `AcqKnowledge_OSC_example.maxpat ` : Parche de ejemplo que recibe datos del archivo `python/singleconnection_TCP_OSC.py` a través de OSC. Este archivo está adaptado a recibir seis datos correspondiente al sistema Zephyr BioHarness, pero podría adaptarse a otras configuraciones de entradas.
* `AcqKnowledge_TCPClient_example.maxpat` : Parche de ejemplo que recibe datos directamente desde el servidor de AcqKnowledge vía TCP y los decodifica según las configuraciones de bytes y *endianness* especificadas en la clase `AcqNdtServer` del archivo `biopacndt.py`.
* `test_samplerate.maxpat` : Abstracción utilizada para medir la frecuencia de muestreo de una señal. Solo utilizado para fines de testeo, no afecta en el envío de datos desde AcqKnowledge.

### `resources`

Archivos de utilidad.

* `BioHarnessTemplate6inputs.gtl` : Plantilla para configurar y preparar seis entradas del BioHarness. Útil para evitar la configuración de las entradas del BioHarness cada vez que se inicia AcqKnowledge. Contiene las siguientes entradas:
  * A1 ECG Raw
  * A2 Breathing Data
  * A7 Posture
  * A12 Y Acceleration Peak
  * A14 X Acceleration Peak
  * A16 Z Acceleration Peak

* `BioHarnessExampleData.acq` : Este archivo contiene información adquirida directamente desde el BioHarness usando la plantilla `BioHarnessTemplate6inputs.gtl`, útil para testear cadena de conexión si no se tiene acceso al BioHarness.

## Problemas conocidos

* No ha sido testeado en macOS.
* Al enviar vía OSC se registran los siguientes problemas:
  * si se termina la conexión antes de haber activado por lo menos una vez la adquisición de datos en AcqKnowledge el programa no puede cerrarse al utilizar Ctrl + C, por lo que se debe cerrar la terminal de manera forzada.
  * No es posible reanudar el envío de datos una vez que es pausado en AcqKnowledge. Se debe cerrar la conexión (Ctrl+C) y abrirla de nuevo.

## Pendientes

* protocolo XML-RPC a través de node.js en MAX
