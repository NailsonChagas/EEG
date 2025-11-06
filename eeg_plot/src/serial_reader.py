import os
import csv
import time
import serial
import struct
import threading
from collections import deque

ADC_VOLTAGE_TO_EEG = (1 / 2062.5) * 1e6  # µV
OFFSET = 1.65 # V

class SerialReader(threading.Thread):
    """Thread que lê dados da UART continuamente"""
    def __init__(self, port: str, baudrate: int, queue_size: int = 3300, conv: float = ADC_VOLTAGE_TO_EEG):
        super().__init__(daemon=True)
        self.port = port
        self.baudrate = baudrate
        self.conv = conv
        self.running = True
        self.lock = threading.Lock()
        self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=1)
        self.data_ch1 = deque(maxlen=queue_size)
        self.data_ch2 = deque(maxlen=queue_size)

        self.save_enabled = False
        self.csv_file = None
        self.csv_writer = None
        self.save_buffer = []
        self.last_flush = time.time()
        self.flush_interval = 5.0

    def enable_saving(self, filename=None, flush_interval=5.0):
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"eeg_data_{timestamp}.csv"
        filepath = os.path.join(output_dir, filename)

        try:
            self.csv_file = open(filepath, "w", newline="")
            self.csv_writer = csv.writer(self.csv_file)
            self.csv_writer.writerow(["timestamp", "ch1_uV", "ch2_uV"])
            self.save_enabled = True
            self.flush_interval = flush_interval
            print(f"\nSalvando dados em: {filepath} (flush a cada {flush_interval}s)")
        except Exception as e:
            print("Erro ao criar arquivo CSV:", e)

    def run(self):
        print(f"Conectado em {self.ser.name}")
        while self.running:
            try:
                start = self.ser.read(1)
                if start != b'$':
                    continue

                data = self.ser.read(8)
                if len(data) != 8:
                    continue

                end = self.ser.read(1)
                if end != b'\n':
                    continue

                ch1, ch2 = struct.unpack('<ff', data)

                if not (0 <= ch1 <= 3.5 and 0 <= ch2 <= 3.5):
                    continue

                ch1 = (ch1 - OFFSET) * self.conv
                ch2 = (ch2 - OFFSET) * self.conv

                with self.lock:
                    self.data_ch1.append(ch1)
                    self.data_ch2.append(ch2)

                if self.save_enabled:
                    timestamp = time.time()
                    self.save_buffer.append((timestamp, ch1, ch2))
                    now = time.time()
                    if now - self.last_flush >= self.flush_interval:
                        self.flush_to_disk()
                        self.last_flush = now

            except Exception as e:
                print("Erro na leitura serial:", e)
                self.ser.reset_input_buffer()

        if self.save_enabled:
            self.flush_to_disk()

        self.ser.close()
        if self.csv_file:
            self.csv_file.close()

    def flush_to_disk(self):
        if not self.csv_writer or not self.save_buffer:
            return
        try:
            self.csv_writer.writerows(self.save_buffer)
            self.csv_file.flush()
            self.save_buffer.clear()
        except Exception as e:
            print("Erro ao salvar buffer:", e)

    def stop(self):
        self.running = False
