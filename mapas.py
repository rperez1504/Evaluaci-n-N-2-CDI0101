import requests
import urllib.parse

def obtener_coordenadas(ciudad, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": ciudad, "limit": "1", "key": key})
    
    respuesta = requests.get(url)
    if respuesta.status_code != 200:
        print(f"Error al obtener coordenadas: {respuesta.status_code} - {respuesta.text}")
        return None
    
    datos_json = respuesta.json()
    if not datos_json.get('hits'):
        print("No se encontraron coordenadas para la ciudad.")
        return None
    
    return datos_json['hits'][0]['point']

def obtener_ruta(origen, destino, key):
    route_url = "https://graphhopper.com/api/1/route?"
    points = f"{origen['lat']},{origen['lng']}&point={destino['lat']},{destino['lng']}"
    url = f"{route_url}point={points}&type=json&locale=es&vehicle=car&key={key}"

    print(f"URL de la ruta: {url}")  

    respuesta = requests.get(url)
    if respuesta.status_code != 200:
        print(f"Error al obtener la ruta: {respuesta.status_code} - {respuesta.text}")
        return None
    
    datos_json = respuesta.json()
    if 'paths' not in datos_json or not datos_json['paths']:
        print("No se encontró ninguna ruta.")
        return None
    
    ruta = datos_json['paths'][0]
    distancia = ruta['distance'] / 1000  
    tiempo = ruta['time']  

    return distancia, tiempo

def main():
    key = "84027a94-f5bb-4a03-a2e2-dd2d23789663"  

    print("Ingrese datos:")
    
    while True:
        origen_input = input("Ingrese la Ciudad de Origen (ejemplo: Osorno Chile): ")
        destino_input = input("Ingrese la Ciudad de Destino (ejemplo: Tomé, Chile): ")
        
        rendimiento = float(input("Ingrese el rendimiento del vehículo en km/l: "))
        
        origen_coords = obtener_coordenadas(origen_input, key)
        destino_coords = obtener_coordenadas(destino_input, key)

        if origen_coords and destino_coords:
            resultado = obtener_ruta(origen_coords, destino_coords, key)

            if resultado:
                distancia, tiempo = resultado
                
                
                combustible = distancia / rendimiento
                
                
                horas = tiempo // 3600000
                minutos = (tiempo % 3600000) // 60000
                segundos = (tiempo % 60000) // 1000

                print(f"\nNarrativa del viaje:")
                print(f"Desde: {origen_input} Hasta: {destino_input}")
                print(f"Distancia: {distancia:.2f} km")
                print(f"Duración: {horas} horas, {minutos} minutos, {segundos} segundos")
                print(f"Combustible requerido: {combustible:.2f} litros\n")

        salir = input("Presione 'q' para salir. ")
        if salir.lower() in ['q']:
            print("Saliendo del programa.")
            break

if __name__ == "__main__":
    main()
