import json
import networkx as nx
import random
from unidecode import unidecode


grafo_libros = nx.DiGraph()


with open('libros.json', 'r', encoding='utf-8') as f:
    libros = json.load(f)


for libro in libros:
    grafo_libros.add_node(libro['id'], titulo=libro['titulo'], autor=libro['autor'], genero=libro['genero'])
  
    grafo_libros.add_edge(unidecode(libro['autor'].lower()), libro['id'], tipo='autor')

    grafo_libros.add_edge(unidecode(libro['genero'].lower()), libro['id'], tipo='genero')
   
    for palabra in libro['palabras_clave']:
        grafo_libros.add_edge(unidecode(palabra.lower()), libro['id'], tipo='palabra_clave')


def buscar_libro(criterio, valor):
    resultados = set()
    valor_sin_tildes = unidecode(valor.lower())  
    
    if criterio == "titulo":
        for libro in libros:
            if valor_sin_tildes in unidecode(libro['titulo'].lower()):  
                resultados.add(libro['id'])
    elif criterio in ["autor", "genero", "palabras_clave"]:
       
        if valor_sin_tildes in grafo_libros:
            for nodo in grafo_libros.neighbors(valor_sin_tildes):
                resultados.add(nodo)

    return resultados

def recomendar_libro():
    if libros:  
        libro_aleatorio = random.choice(libros)
        return libro_aleatorio
    return None

def usuario():
    print(" buscador de libros")
    
    while True:
        print("Puedes buscar un libro por título, autor, género o palabras clave.")
        criterio = input("Ingresa el criterio de búsqueda (titulo, autor, genero, palabras_clave) o 'salir' para terminar: ").lower()
        if criterio == 'salir':
            print("Gracias por usar el buscador de libros. ")
            break
        
        valor = input(f"Ingresa el {criterio} que estás buscando: ")

        resultados = buscar_libro(criterio, valor)
        
        if resultados:
            print(f"Hemos encontrado {len(resultados)} libro(s) que coinciden con tu búsqueda:")
            for libro_id in resultados:
                libro = next(item for item in libros if item["id"] == libro_id)
                print(f"- {libro['titulo']} de {libro['autor']} (Publicado en {libro['anio_publicacion']})")
        else:
            print("No se encontraron coincidencias exactas.")
         
            libro_recomendado = recomendar_libro()
            if libro_recomendado:
                print(f"Te recomendamos leer: {libro_recomendado['titulo']} de {libro_recomendado['autor']} (Popularidad: {libro_recomendado['popularidad']})")
            else:
                print("No hay libros disponibles para recomendar.")


usuario()

