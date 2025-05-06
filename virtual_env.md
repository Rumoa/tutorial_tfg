# Cómo lanzar programas usando la qpu y librerías externas

## Creación de entorno virtual e instalación de librerías.
**Esto solo hay que hacerlo una vez para instalar las librerías que uséis**:
- Cargar los módulos de qiskit y la integración de la qpu con qiskit (qmiotools)

`module purge`

`module load qmio/hpc gcc/12.3.0 qmio-tools/0.2.0-python-3.9.9 qiskit/1.2.4-python-3.9.9`
- Crear un venv con acceso a los paquetes del sistema:
`python -m venv --system-site-packages /path/to/new/virtual/environment`. 
Esto crea un venv en el path que defináis 
- Activar el entorno:
`source path/to/new/virtual/environment/bin/activate`
- Comprobad que el python que usáis ahora es el del nuevo venv 
`which python`
- Instalad todo lo que uséis que no sea qiskit o qmiotools


## Slurm job 
En el ejemplo de prueba, lo único que añadimos es que tenemos que activar nuestro venv con las librerías que también vamos a usar.

Para lanzar el trabajo: `sbatch trabajo.sh` (si hemos llamado "trabajo.sh" al slurm job file)
Para comprobar la cola de trabajos: `squeue` (si queréis filtrar por vuestro usuario: `squeue -u tunombredeusuario`)




# Para usar el simulador en casa, tenéis que instalar en vuestro entorno qmiotools

- Activamos el entorno en el cual queremos instalar qmiotools (dependiendo de si usáis conda, venv, ...)
- Clonamos el repositorio
`git clone https://github.com/gomeztato/qmiotools.git`
- Vamos al directorio 
`cd qmiotools`
- Usamos pip para instalar qmiotools
`pip install .` (El punto busca si hay algún fichero setup.py o pyproject.toml)
- Si tenéis errors mirad qué incompatibilidades de versiones de paquetes tenéis. 

Ya podéis usar FakeBackend como en el ejemplo usando el truco del servidor. 

