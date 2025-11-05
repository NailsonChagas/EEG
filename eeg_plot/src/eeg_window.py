import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore

class EegWindow(pg.GraphicsLayoutWidget):
    """Gráficos: sinais no tempo e FFT em dB"""
    def __init__(self, reader, sample_rate: float = 3300.0, update_rate: int = 60):
        super().__init__()
        self.setWindowTitle("EEG + FFT (dB)")
        self.resize(1000, 800)
        self.setMinimumSize(800, 600)
        self.reader = reader
        self.sample_rate = sample_rate

        pg.setConfigOptions(antialias=True)
        layout = self.ci

        # sinais no tempo
        self.p1 = layout.addPlot(title="EEG - Canal 1 (Tempo - µV)")
        self._setup_plot(self.p1, 'r')
        self.curve_ch1 = self.p1.plot(pen='r')

        self.p3 = layout.addPlot(title="EEG - Canal 2 (Tempo - µV)")
        self._setup_plot(self.p3, 'b')
        self.curve_ch2 = self.p3.plot(pen='b')

        layout.nextRow()

        # FFT
        self.p2 = layout.addPlot(title="EEG - Canal 1 (FFT em dB)")
        self._setup_fft_plot(self.p2)
        self.curve_fft1 = self.p2.plot(pen='r')

        self.p4 = layout.addPlot(title="EEG - Canal 2 (FFT em dB)")
        self._setup_fft_plot(self.p4)
        self.curve_fft2 = self.p4.plot(pen='b')

        # timer
        freq = int(1000 / update_rate)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(freq)

    def _setup_plot(self, plot, color):
        plot.setLabel('bottom', 'Amostras')
        plot.setLabel('left', 'Amplitude (µV)')
        plot.setYRange(-900, 900)
        plot.setLimits(yMin=-900, yMax=900)
        plot.setMouseEnabled(x=False, y=True)
        plot.showGrid(x=True, y=True)

    def _setup_fft_plot(self, plot):
        plot.setLabel('bottom', 'Frequência (Hz)')
        plot.setLabel('left', 'Magnitude (dB)')
        plot.showGrid(x=True, y=True)
        plot.setYRange(-120, 0)
        plot.setLimits(yMin=-130, yMax=100)
        plot.setMouseEnabled(x=False, y=True)

    def update_plots(self):
        with self.reader.lock:
            ch1 = np.array(self.reader.data_ch1)
            ch2 = np.array(self.reader.data_ch2)

        if len(ch1) < 64:
            return

        self.curve_ch1.setData(ch1)
        self.curve_ch2.setData(ch2)

        try:
            fft1 = np.abs(np.fft.rfft(ch1 - np.mean(ch1)))
            fft2 = np.abs(np.fft.rfft(ch2 - np.mean(ch2)))
            freqs = np.fft.rfftfreq(len(ch1), 1 / self.sample_rate)

            fft1_db = 20 * np.log10(fft1 / np.max(fft1) + 1e-12)
            fft2_db = 20 * np.log10(fft2 / np.max(fft2) + 1e-12)

            self.curve_fft1.setData(freqs[1:], fft1_db[1:])
            self.curve_fft2.setData(freqs[1:], fft2_db[1:])
        except Exception as e:
            print("Erro na FFT:", e)
