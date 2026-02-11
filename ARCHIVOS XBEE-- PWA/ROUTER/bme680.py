from machine import I2C
import time

# Direcciones I2C del sensor
# Morales Sanchez Eder Isai --- Escom ---- libreria simplificada para controlar el sensor bme680
_ADDR_PRI = 0x77
_ADDR_SEC = 0x76

class BME680:
    def __init__(self, i2c, addr=None):
        self.i2c = i2c
        self.addr = addr
        if self.addr is None:
            self.addr = _ADDR_PRI
        
        
        try:
            self.i2c.writeto(self.addr, b'')
        except OSError:
            # Si falla, probamos la secundaria
            self.addr = _ADDR_SEC
            
        # Configuracion inicial (Reset y lectura forzada)
        
        try:
            self._write_byte(0xE0, 0xB6) # Soft Reset
            time.sleep(0.2)
            
            # Configurar precision (Humedad x1, Temp x2)
            self._write_byte(0x72, 0x01) 
            self._write_byte(0x74, 0x54) 
            self._write_byte(0x75, 0x00) 
        except Exception as e:
            print("Error config:", e)

    def _read_byte(self, reg):
        # Lectura simple de un byte
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]

    def _write_byte(self, reg, val):
        # Escritura simple
        self.i2c.writeto_mem(self.addr, reg, bytes([val]))

    def get_data(self):
        try:
            # Despertar sensor para medir (--Forced Mode--)
            ctrl = self._read_byte(0x74)
            self._write_byte(0x74, (ctrl & 0xFC) | 0x01)
            
            # medicion
            for i in range(10):
                status = self._read_byte(0x74)
                if not (status & 0x03):
                    break
                time.sleep(0.01)
                
            #  Leer bloque de datos 
            data = self.i2c.readfrom_mem(self.addr, 0x1F, 8)
            
            # Calculo simplificado de Temperatura
            # Une los registros MSB, LSB y XLSB
            temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
            temperature = (temp_raw / 5120.0) - 20.0 

            # Calculo simplificado de Humedad
            hum_raw = (data[6] << 8) | data[7]
            humidity = hum_raw / 1024.0 
            
            return temperature, humidity
            
        except Exception as e:
            print("Error lectura:", e)
            return 0, 0