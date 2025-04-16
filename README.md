# movies-graph-db

Para cargar la base de datos hay que realizar los siguientes pasos:

1. Colocar los archivos del dataset (`title.basics.tsv`, `title.principals.tsv`, etc.) en la carpeta `data/` del
   proyecto.

2. Crear un archivo llamado `.env` en el directorio del proyecto, que siga la plantilla del archivo `.env.example`,
   reemplazando el usuario, contraseña y nombre de nuestra base de datos local.

3. En el directorio del proyecto, crear un entorno virtual de python con `python3 -m venv .venv`, activarlo con
   `source .venv/bin/activate`, e instalar los requerimientos dentro del mismo con `pip install -r requirements.txt`.

4. Asegurarse de que está andando el DBMS en neo4j Desktop.

5. Finalmente, con el entorno activado, llamamos a los scripts que queramos ejecutar. Los scripts deben llamarse desde
   la carpeta del proyecto, con el flag `-m`, utilizando puntos en lugar de barras, y sin la extensión .py del script.
   Es decir, `python3 -m scripts.<nombre_script>`. Algunos ejemplos son:

    - `scripts.load_everything` Carga todos los .tsv cuyos scripts de carga hayan sido implementados. Cuando hacemos uno
      nuevo, lo agregamos al archivo. Ojo de no ejecutarlo más de una vez porque duplica casi todo. Chequear si ya
      existen los nodos  (usando MERGE en lugar de CREATE) hace que tarde una barbaridad, así que no se hace.

    - `scripts.<script_de_carga>` Carga lo de un solo archivo .tsv. Algunos se pueden ejecutar varias veces de forma
      segura, otros no. Hay que tener cuidado de ejecutarlos según el orden definido en `load_everything`.

    - `scripts.delete` Borra y recrea la base de datos.

    - `scripts.amount` Muestra la cantidad de relaciones y nodos, tanto el total como por tipo. Esta se podría hacer en
      el neo4j browser pero es más cómodo desde la consola.

    - `utils.run_query` No se llamaría directamente desde la consola, aunque se puede. Se puede usar para ejecutar
      rápidamente una query del directorio `cypher/` que no requiera parámetros ni reemplazos de ningún tipo.

## Funcionamiento

Cada script de python para cargar datos (los que empiezan con `load_`) se encarga de un solo `.tsv`. En el script, carga
una plantilla de una query de cypher, que están en `/cypher`, y reemplaza cualquier dato que sea necesario. Por ejemplo,
en el caso de `load_titles.py`, reemplaza la etiqueta TitleType por el tipo de obra a cargar (hay que hacerlo en Python
porque neo4j no permite parametrizar las etiquetas...). Luego, con la librería de neo4j para python, podemos realizar
una transacción indicando una query (que ya cargamos y modificamos), y algunos parámetros.

En los scripts de carga, el parámetro es una lista de filas (ya preprocesadas por python) sobra la cual va a iterar la
query. Se hacen transacciones con cantidad limitada de filas (~5000) para no saturar a la base de datos.