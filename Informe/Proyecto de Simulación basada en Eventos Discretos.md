# Proyecto de Simulación basada en Eventos Discretos



## Osmany Pérez Rodríguez C-412

#### osmany.perez@estudiantes.matom.uh.cu



### 1- Orden del Problema

### Happy Computing

Happy Computing es un taller de reparaciones electrónicas se realizan las siguientes actividades (el precio de cada servicio se muestra entre paréntesis):

1. Reparación por garantía (Gratis)
2.  Reparación fuera de garantía (\$350)
3. Cambio de equipo (\$500) 
4.  Venta de equipos reparados ($750)

 Se conoce además que el taller cuenta con 3 tipos de empleados: Vendedor, Técnico y Técnico Especializado. 

Para su funcionamiento, cuando un cliente llega al taller, es atendido por un vendedor y en caso de que el servicio que requiera sea una Reparación (sea de tipo 1 o 2) el cliente debe ser atendido por un técnico (especializado o no). Además en caso de que el cliente quiera un cambio de equipo este debe ser atendido por un técnico especializado. Si todos los empleados que pueden atender al cliente están ocupados, entonces se establece una cola para sus servicios. Un técnico especializado sólo realizará Reparaciones si no hay ningún cliente que desee un cambio de equipo en la cola. 

Se conoce que los clientes arriban al local con un intervalo de tiempo que distribuye poisson con λ = 20 minutos y que el tipo de servicios que requieren pueden ser descrito mediante la tabla de probabilidades: 



| Tipo de Servicio | Probabilidad |
| ---------------- | ------------ |
| 1                | 0.45         |
| 2                | 0.25         |
| 3                | 0.1          |
| 4                | 0.2          |



Además se conoce que un técnico tarda un tiempo que distribuye exponencial con λ = 20 minutos, en realizar una Reparación Cualquiera. Un técnico especializado tarda un tiempo que distribuye exponencial con λ = 15 minutos para realizar un cambio de equipos y la vendedora puede atender cualquier servicio en un tiempo que distribuye normal (N(5 min, 2mins)). 

El dueño del lugar desea realizar una simulación de la ganancia que tendría en una jornada laboral si tuviera 2 vendedores, 3 técnicos y 1 t técnico especializado.



## 2- Principales ideas seguidas para la solución del problema

La solución esta basada en un modelo de eventos discretos. En este se maneja el evento que tenga el tiempo más próximo al tiempo actual. Este procesamiento permite mantener un orden de eventos, y como cada uno genera el tiempo de su próxima ejecución no se pasa por alto que un mismo evento pueda ocurrir dos veces consecutivas si su tiempo de ejecución se mantiene menor que el del resto de los eventos.

La base del problema se realiza análogo a dos conjuntos de servidores conectados en serie. El primero contiene dos que este caso serían los vendedores que trabajan en paralelo. El segundo serían los 4 técnicos (incluyendo el especializado) que de igual manera están conectados en paralelo.

El proceso comienza con la generación de clientes respetando la distribución requerida en el problema (arribo). Este contiene un tipo, que es el que nos dice que servicio es el que requiere. Este a su vez pasa a ser procesado por un vendedor si hay alguno disponible, si no se guarda en el estado actual del problema que simula una cola para los vendedores. Como es de suponer, esta cola se procesa en orden de la llegada de los clientes, una vez que se desocupa cualquiera de los vendedores.

Es necesario primeramente que todos los clientes sean atendidos por los vendedores, que toma un tiempo definido por la distribución en el problema. Estos definen si el cliente es de un tipo que requiere de un técnico o no. Si el caso fuese que no lo necesita, entonces es atendido y deja el sistema.  Aquellos que requieren de un técnico se guardan en una cola y los que necesiten de un técnico especializado se guardan en otra. Inmediatamente, se realiza un chequeo si alguno de los técnicos está disponible y sale un cliente de la cola para prestarle el servicio. Para asignarle un cliente al técnico especializado es necesario hacer una revisión previa de la cola que lo requiere a él específicamente, si hubiese algún cliente ahí, este pasa a ser atendido. En caso de que la cola para el técnico especializado esté vacía entonces se le asigna un cliente de los que solo requiere un técnico. Cuando se saca de una de las colas un cliente, se crea el tiempo de culminación del servicio por parte del técnico, de forma que este también se toma en cuenta a la hora de mover el tiempo al evento que tenga la culminación más proxima.

Una vez que el técnico finaliza con un cliente, este sale del sistema. Dicho técnico pasa a revisar si hay alguien en la cola esperando para ser atendido (el especializado siempre revisando primero la cola que solo él puede atender). Si existe alguien esperando para ser atendido, se hace el proceso análogo de crear el tiempo al que culmina el servicio para ser comparado con la finalización de los demás y en caso de ser el menor se atiende.

Una vez que el tiempo de arribo al local sobrepasa el tiempo de simulación predefinido en un inicio, no se acepta más ningún cliente. Y pasan a ser atendidos solo aquellos que ya estén en sistema, los que estén en la cola inicial, aunque después requieran ser atendidos además por algún técnico. Es evidente que aquellos que ya están en la cola para ser atendidos por algún técnico por supuesto que también son atendidos. Básicamente se mantiene el funcionamiento pero sin aceptar nuevos clientes, de forma en algún horario todos serán atendidos y ahí culmina el procesamiento en general, cuando todas las colas estén vacías.

A modo de resumen el proceso del cliente va de la siguiente forma:

- Llega el cliente.
- Si todos vendedores están ocupados, se agrega a la cola en espera de su turno.

- Una vez su turno llega es atendido por un vendedor, si este es el encargado del servicio requerido, lo atiende y le da de baja en el sistema. En otro caso, se asigna a la cola de técnicos y la del técnico especializado atendiendo a sus necesidades.
- Luego el técnico correspondiente lo recibe y resuelve su problema, y lo retira del sistema. Siempre teniendo en cuenta que si un cliente está en la cola del técnico especializado tiene prioridad para ser atendido una vez q este sea liberado o esté libre.



## 3- Modelo de Simulación de Eventos Discretos desarrollado para resolver el problema:

1- Variables de tiempo:

- $t$    tiempo general
- $t\_a$    tiempo de arribo
- $t\_d1$   tiempo de salida del vendedor 1
- $t\_d2$   tiempo de salida del vendedor 2
- $t\_dt1$   tiempo de salida del técnico 1
- $t\_dt2$   tiempo de salida del técnico 2
- $t\_dt3$   tiempo de salida del técnico 3
- $t\_dEsp$   tiempo de salido del técnico especializado

2- Variables contadoras:

- $n\_a$    cantidad de arribos,   $a$ diccionario
- $n\_d1$   cantidad de partidas del vendedor 1,   $d1$ diccionario
- $n\_d2$   cantidad de partidas del vendedor 2,   $d2$ diccionario
- $n\_dt1$   cantidad de partidas del técnico 1,    $dt1$ diccionario
- $n\_dt2$  cantidad de partidas del técnico 2,   $dt2$ diccionario
- $n\_dt3$   cantidad de partidas del técnico 3,   $dt3$ diccionario   
- $n\_dEsp$   tiempo de salido del técnico especializado, $dtEsp$ diccionario

3-Variables de estado:

- $SS$  = (n, i1, i2, i3, .., in) n número de clientes para vendedores, i1 cliente en vendedor 1 (0 si no hay), i2 cliente en vendedor, i3, .., in la cola para los vendedores.

  

  Técnicos:

  - $rep\_queue$      cola de los clientes esperando para ser atendidos por un técnico
  - $rep\_esp\_queue$    cola de los clientes esperando para ser atendidos por un técnico especializado
  - $dt1\_client$     cliente que está siendo atendido por el técnico 1 (0 si no hay)
  - $dt2\_client$     cliente que está siendo atendido por el técnico 2 (0 si no hay)
  - $dt3\_client$     cliente que está siendo atendido por el técnico 3 (0 si no hay) 
  - $dtEsp\_client$     cliente que está siendo atendido por el técnico especializado (0 si no hay)

  ​	

## 4- Consideraciones obtenidas a partir de la ejecución de las simulaciones del problema:

El problema tiene como principal objetivo simular la ganancia del taller en una jornada laboral dado un personal. Se asume que la jornada laboral es de 8 horas y después de tomar el promedio de las ganancias tras realizar 1000 simulaciones, se obtiene una ganancia que oscila entre  \$6700 y \$6900. Usualmente centrado en los $6800. Esta información proviene de realizar este proceso de las 1000 simulaciones en repetidas ocasiones. Además como información extra se tiene que se atienden como promedio a 23.5 personas en una jornada laboral, pero como no se puede atender a la mitad de una persona, entonces se atienden 23. Además un detalle a notar es que más allá del tiempo que se defina como jornada laboral, en realidad el taller no cierra en ese tiempo, a partir de ese momento no se permiten más arribos, pero es necesario brindar el servicio a aquellos clientes que ya están en el sistema.  Sim embargo, analizando aquellos casos que se extienden después de dicho tiempo, el tiempo extra tiene un average de 2.9 minutos, alrededor de 174 segundos.



## 5- Enlace a repositorio del proyecto en GitHub:

https://github.com/osmany-perez-1998/simulation-project-1

