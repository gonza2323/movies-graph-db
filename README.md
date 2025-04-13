# movies-graph-db

Para cargar la base de datos hay que realizar los siguientes pasos:

1. Colocar los archivos del dataset (`title.basics.tsv`, `title.principals.tsv`, etc.) en la carpeta `data` del proyecto.

2. Crear un archivo llamado `.env` que siga la plantilla del archivo `.env.example`. Reemplazamos el usuario y la contraseña por el de nuestra base de datos local.

3.  Crear un entorno virtual de python con `python3 -m venv .venv` e instalar los requerimientos con `pip install -r requirements.txt`.

4. Finalmente, con el entorno activado `source /.venv/bin/activate`, llamamos a los scripts que queramos ejecutar. Los scripts deben llamarse desde la carpeta del proyecto, con el flag `-m`, utilizando puntos en lugar de barras, y sin la extensión .py del script. De la siguiente forma `python3 -m scripts.<nombre_script>`. Por ejemplo:

    - `python3 -m scripts.load_titles` Carga las obras y los géneros en la base de datos (Tarda como 5-10 minutos). Ojo de no ejecutarlo más de una vez porque duplica todo. Chequear si ya existen los nodos hace que tarde una barbaridad, así que no lo hace.

    - `python3 -m scripts.delete` Borra absolutamente todo. Aunque creo que es más rápido borrar la base de datos y volverla a armar. Tarda unos minutos.

    - `python3 -m scripts.amount` Muestra la cantidad de relaciones, nodos, y distintos tipos de nodos.