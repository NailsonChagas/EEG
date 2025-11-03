import serial
import struct

# Porta e baud rate
ser = serial.Serial(
    port='/dev/ttyACM0',   # ou 'COM3' no Windows
    baudrate=209700,
    timeout=1
)

print("Conectado em", ser.name)

while True:
    # Lê 8 bytes (tamanho de FilteredData)
    data = ser.read(8)

    if len(data) == 8:
        ch1, ch2 = struct.unpack('<ff', data)
        print(f"CH1={ch1:.3f} V, CH2={ch2:.3f} V")
