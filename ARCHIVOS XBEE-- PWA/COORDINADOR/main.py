import xbee
import time

print("--- RECEPTOR INICIADO ---")
print("Esperando datos de temperatura...")

while True:
    try:
        # receive() devuelve None si no hay nada, o un paquete si llega algo
	# Morales Sanchez Eder Isai --- Escom ---- Coordinador main   
        packet = xbee.receive()
        
        if packet:
            
            # payload es lo que envio el otro XBee (ej: "T:23.5,H:40.2")
            mensaje_bytes = packet.get('payload')
            mensaje_texto = mensaje_bytes.decode('utf-8')
            
            print(mensaje_texto)
            
        else:
           
            time.sleep(0.1)
            
    except Exception as e:
        print("Error:", e)
        time.sleep(1)