import time
from machine import I2C
import bme680 
import xbee 

# --- CONFIGURACIÓN DEL SENSOR ---
# Morales Sanchez Eder Isai --- Escom ---- Router main   
try:
    i2c = I2C(1) 
    sensor = bme680.BME680(i2c=i2c)
    print("Sensor listo. Iniciando transmision...")
except Exception as e:
    print("Error init:", e)

# --- BUCLE PRINCIPAL ---
while True:
    try:
        # 1. LEER DATOS
        t, h = sensor.get_data()
        
        # Tu ajuste de calibración
        temp_final = t - 55.0  
        hum_final = h 
        
        # 2. PREPARAR EL MENSAJE (PAYLOAD)
        # Convertimos los números a texto para enviarlos
        # Formato: "T:23.5,H:40.2"
        # Usamos str() simple para evitar errores de sintaxis
        mensaje = "T:" + str(round(temp_final, 2)) + ",H:" + str(round(hum_final, 2))
        
        # 3. MOSTRAR EN LOCAL (Para que tú veas que funciona)
        print("Enviando ->", mensaje)
        
        # 4. TRANSMITIR POR RADIO (La parte inalambrica)
        # xbee.ADDR_COORDINATOR hace que se envie al jefe de la red
        try:
            xbee.transmit(xbee.ADDR_COORDINATOR, mensaje)
        except Exception as e:
            # Si no hay red o coordinador, esto puede dar error
            print("Fallo al transmitir (¿Esta el Coordinador encendido?)")
        
        # Esperamos 2 segundos (no satures la red enviando cada 0.1s) esto da lata 
        time.sleep(2)
        
    except Exception as e:
        print("Error general:", e)
        time.sleep(1)
