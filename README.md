# AcqKnowledgeForMax

AcqKnowledgeForMax es una serie de archivos para conectar el software AcqKnowledge con Max 8 a través de NDT, usando TCP y/o OSC.

Este repositorio contiene archivos de python para configurar remotamente el servidor TCP de AcqKnowledge y existen versiones para enviar los datos a través de un servidor TCP a Max o a través del protocolo OSC. Parches de ejemplo en Max 8 también son incluidos.

## Requerimientos

* Python 3.9:
  * python-osc
* AcqKnowledge 5.0:
  * NDT
* Max 8:
  * Sadam Library 20.3.7 (disponible en el Package Manager)

## Uso

###  A través de servidor TCP

1. Abrir AcqKnowledge. Asegurarse que en preferencias está habilitado NDT (Display > Preferences.)

2. Ejecutar `python `/`singleconnection_TCP_MAX.py` . En la línea de comando se especifica el puerto al cual se debe conectar el cliente TCP (por defecto puerto 15020)
3. Abrir `max`/ `AcqKnowledge_TCPClient_example.maxpat`.
4. Al abrir el parche de Max el cliente se activa automáticamente en el puerto 15020, por lo que no es necesario encenderlo. Es muy importante encender el cliente TCP antes de iniciar la adquisición en AcqKnowledge ya que no se permiten conexiones nuevas una vez que se están capturando los datos.
5. Iniciar adquisición en AcqKnowledge.

### A través de protocolo OSC

1. Abrir AcqKnowledge. Asegurarse que en preferencias está habilitado NDT (Display > Preferences.)
2. Abrir `max `/ `AcqKnowledge_OSC_example.maxpat`.
3. Encender cliente OSC en Max.
4. Ejecutar `python`/`singleconnection_TCP_OSC.py`. En la línea de comando se especifica el puerto al cual se debe conectar el cliente OSC (por defecto puerto 5005). La adquisición se inicia automáticamente una vez que la conexión al cliente de AcqKnowledge es exitosa.



## Pendientes

* Orden general de archivos
* Documentación
* Limpiar código
  * ~~`singleconnection_TCP_OSC.py`: Añadir Callback `SendOSCData` y testear~~
  * general: comentar y borrar código innecesario
<<<<<<< HEAD
* Configurar para desactivar auto-recovery
* protocolo XML-RPC a través de node.js en MAX