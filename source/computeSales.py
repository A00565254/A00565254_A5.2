# pylint: disable=invalid-name
"""
Guillermo Contreras Pedroza
A00565254
computeSales.py
Programa para calcular el costo total de ventas desde un catálogo de precios.
Cumple con requerimientos de manejo de errores, PEP8 y registro de tiempo.
"""

import json
import sys
import time


def load_json_file(file_path):
    """Carga un archivo JSON y maneja errores de lectura."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no existe.")
    except json.JSONDecodeError:
        print(f"Error: El archivo '{file_path}' no tiene un formato válido.")
    except OSError as e:
        print(f"Error inesperado al leer '{file_path}': {e}")
    return None


def calculate_total_sales(catalogue, sales):
    """Calcula el costo total cruzando ventas con el catálogo."""
    # Convertimos el catálogo a un diccionario para búsqueda rápida O(1)
    # Req 6: Esto permite manejar miles de items eficientemente
    price_map = {item['title']: item['price'] for item in catalogue
                 if 'title' in item and 'price' in item}

    total_cost = 0.0
    errors = []

    for record in sales:
        product_name = record.get('Product')
        quantity = record.get('Quantity', 0)

        if product_name in price_map:
            try:
                total_cost += price_map[product_name] * float(quantity)
            except (ValueError, TypeError):
                errors.append(f"Dato inválido en venta: {record}")
        else:
            errors.append(f"Producto no encontrado: {product_name}")

    return total_cost, errors


def main():
    """Función principal para la ejecución del programa."""
    start_time = time.time()

    # Req 5: Validación de argumentos de línea de comandos
    if len(sys.argv) != 3:
        print("""Uso: python computeSales.py priceCatalogue.json
              salesRecord.json""")
        sys.exit(1)

    catalogue_file = sys.argv[1]
    sales_file = sys.argv[2]

    # Carga de datos
    catalogue_data = load_json_file(catalogue_file)
    sales_data = load_json_file(sales_file)

    if catalogue_data is None or sales_data is None:
        sys.exit(1)

    # Procesamiento
    total, process_errors = calculate_total_sales(catalogue_data, sales_data)

    # Req 3: Mostrar errores en consola sin detener la ejecución
    if process_errors:
        print("\n--- Errores encontrados durante el proceso ---")
        for error in process_errors:
            print(error)

    # Cálculo de tiempo (Req 7)
    elapsed_time = time.time() - start_time

    # Formateo de resultados (Req 2)
    results_output = (
        "==========================================\n"
        "       RESULTADOS DE VENTAS TOTALES       \n"
        "==========================================\n"
        f"Costo Total de Ventas: ${total:,.2f}\n"
        f"Tiempo de ejecución:   {elapsed_time:.4f} segundos\n"
        "==========================================\n"
    )

    # Mostrar en pantalla y guardar en archivo
    print("\n" + results_output)
    try:
        with open("SalesResults.txt", "w", encoding='utf-8') as f:
            f.write(results_output)
    except OSError as e:
        print(f"Error al escribir el archivo de resultados: {e}")


if __name__ == "__main__":
    main()
