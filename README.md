# movies-graph-db

Para cargar la base de datos hay que realizar los siguientes pasos:

1. Colocar los archivos del dataset (`title.basics.tsv`, `title.principals.tsv`, etc.) en la carpeta `data/` del proyecto.

2. Crear un archivo llamado `.env` en el directorio del proyecto, que siga la plantilla del archivo `.env.example`, reemplazamos el usuario y la contraseña por el de nuestra base de datos local.

3. En el directorio del proyecto, crear un entorno virtual de python con `python3 -m venv .venv`, activarlo con `source /.venv/bin/activate`, e instalar los requerimientos dentro del mismo con `pip install -r requirements.txt`.

4. Asegurarse de que está andando el DBMS en neo4j Desktop.

5. Finalmente, con el entorno activado, llamamos a los scripts que queramos ejecutar. Los scripts deben llamarse desde la carpeta del proyecto, con el flag `-m`, utilizando puntos en lugar de barras, y sin la extensión .py del script. Es decir, `python3 -m scripts.<nombre_script>`. Por ejemplo:

    - `python3 -m scripts.load_titles` Carga las obras y los géneros en la base de datos (Tarda como 5-10 minutos). Ojo de no ejecutarlo más de una vez porque duplica todo. Chequear si ya existen los nodos  (usando MERGE en lugar de CREATE) hace que tarde una barbaridad, así que no lo hace.

    - `python3 -m scripts.delete` Borra absolutamente todo. Aunque creo que es más rápido borrar la base de datos y volverla a armar. Tarda unos minutos. El neo4j browser tampoco se banca esta operación si no se hace de a tandas.

    - `python3 -m scripts.amount` Muestra la cantidad de relaciones, nodos, y distintos tipos de nodos. Esta se podría hacer en el neo4j browser pero es más cómodo desde la consola.

## Funcionamiento

Cada script de python para cargar datos se encarga de un solo `.tsv` (solo hay uno por ahora que carga `title.basics.tsv`). En el script, carga una plantilla de una query de cypher, que están en `/cypher`, y reemplaza cualquier dato que sea necesario. Por ejemplo, en el caso de `load_titles.py`, reemplaza la etiqueta TitleType por el tipo de obra a cargar (hay que hacerlo en Python porque neo4j no permite parametrizar las etiquetas...). Luego, con la librería de neo4j para python, podemos realizar una transacción indicando una query (que ya cargamos y modificamos), y parámetros. En este caso, el parámetro es una lista de filas (ya preprocesadas por python) sobra la cual va a itera la query.

Envía una cantidad limitada de filas (~5000) por transacción, así no satura a la base de datos.