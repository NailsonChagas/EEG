import sys
import struct
import serial
import platform
import threading
import numpy as np
from collections import deque
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg


class SerialReader(threading.Thread):
    """Thread que lê dados da UART continuamente"""
    def __init__(self, port: str, baudrate: int, queue_size: int = 3300):
        super().__init__(daemon=True)
        self.port = port
        self.baudrate = baudrate
        self.running = True
        self.lock = threading.Lock()
        self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=1)
        self.data_ch1 = deque(maxlen=queue_size)
        self.data_ch2 = deque(maxlen=queue_size)

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

                # descartar valores fora da faixa esperada
                if not (0 <= ch1 <= 3.5 and 0 <= ch2 <= 3.5):
                    continue

                with self.lock:
                    self.data_ch1.append(ch1)
                    self.data_ch2.append(ch2)

            except Exception as e:
                print("Erro na leitura serial:", e)
                self.ser.reset_input_buffer()

        self.ser.close()

    def stop(self):
        self.running = False


class PlotWindow(pg.GraphicsLayoutWidget):
    """Gráficos: sinais no tempo e FFT em dB"""
    def __init__(self, reader: SerialReader, sample_rate: float = 3300.0, update_rate: int = 60):
        super().__init__()
        self.setWindowTitle("Leitura UART + FFT (dB) em tempo real")
        self.resize(1000, 800)
        self.reader = reader
        self.sample_rate = sample_rate

        pg.setConfigOptions(antialias=True)
        layout = self.ci

        # linha 1: sinais no tempo
        self.p1 = layout.addPlot(title="Canal 1 (Tempo)")
        self.p1.setYRange(0, 3.5)
        self.p1.showGrid(x=True, y=True)
        self.curve_ch1 = self.p1.plot(pen='r')

        self.p3 = layout.addPlot(title="Canal 2 (Tempo)")
        self.p3.setYRange(0, 3.5)
        self.p3.showGrid(x=True, y=True)
        self.curve_ch2 = self.p3.plot(pen='b')

        layout.nextRow()

        # linha 2: FFTs em dB
        self.p2 = layout.addPlot(title="Canal 1 (FFT em dB)")
        self.p2.showGrid(x=True, y=True)
        self.curve_fft1 = self.p2.plot(pen='r')

        self.p4 = layout.addPlot(title="Canal 2 (FFT em dB)")
        self.p4.showGrid(x=True, y=True)
        self.curve_fft2 = self.p4.plot(pen='b')

        # timer para atualizar o frame
        freq = int(1000 / update_rate)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(freq)

    def update_plots(self):
        with self.reader.lock:
            ch1 = np.array(self.reader.data_ch1)
            ch2 = np.array(self.reader.data_ch2)

        if len(ch1) < 64: # garante que tem valores o bastante para calcular a fft
            return

        # Atualiza sinais no tempo
        self.curve_ch1.setData(ch1)
        self.curve_ch2.setData(ch2)

        # FFT em dB
        # 1. fft  -> magnitude da FFT (amplitude de cada componente de frequência)
        # 2. np.max(fft) -> valor máximo da FFT usado para normalizar (o pico vira 0 dB)
        # 3. + 1e-12 -> evita log(0), que causaria -inf (erro numérico)
        # 4. np.log10(...) -> converte para escala logarítmica (base 10)
        # 5. 20 * (...) -> converte amplitude para decibéis (pois potência ∝ amplitude²)
        try:
            fft1 = np.abs(np.fft.rfft(ch1 - np.mean(ch1)))
            fft2 = np.abs(np.fft.rfft(ch2 - np.mean(ch2)))
            freqs = np.fft.rfftfreq(len(ch1), 1 / self.sample_rate)

            fft1_db = 20 * np.log10(fft1 / np.max(fft1) + 1e-12)
            fft2_db = 20 * np.log10(fft2 / np.max(fft2) + 1e-12)

            # self.curve_fft1.setData(freqs, fft1_db)
            # self.curve_fft2.setData(freqs, fft2_db)
            # teste para remover linha do inicio
            self.curve_fft1.setData(freqs[1:], fft1_db[1:])
            self.curve_fft2.setData(freqs[1:], fft2_db[1:])

            # eixo Y típico de FFT em dB
            self.p2.setYRange(-120, 0)
            self.p4.setYRange(-120, 0)

        except Exception as e:
            print("Erro na FFT:", e)


def main():
    port = "COM3" if platform.system() == "Windows" else "/dev/ttyACM0"
    baud = 209700

    reader = SerialReader(port, baud)
    reader.start()

    app = QtWidgets.QApplication(sys.argv)
    win = PlotWindow(reader, sample_rate=3300.0, update_rate=60)
    win.show()

    try:
        sys.exit(app.exec_())
    finally:
        reader.stop()


if __name__ == "__main__":
    main()
