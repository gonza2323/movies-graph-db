import os
from scripts import load_titles
from scripts import load_names
from scripts import load_crew

def run():
    load_titles.run()
    load_names.run()
    load_crew.run()

if __name__ == "__main__":
    filename = os.path.basename(__file__)
    print(f"PRECAUCIÓN: Ejecutar {filename} cuando ya se han cargado los datos, creará datos duplicados.")
    while True:
        user_input = input("Quiere proceder? [y/n]: ").strip().lower()
        if user_input in ("y", "yes"):
            run()
            break
        elif user_input in ("n", "no"):
            print("Cancelado.")
            break
        else:
            print("Input inválido. Ingrese y(es) / n(o).")
