import sys
from PyQt5 import QtWidgets
from src.eeg_window import EegWindow
from src.utils import serial_port_selector
from src.serial_reader import SerialReader


def main():
    port = serial_port_selector()

    if port == None: 
        return

    baud = 209700
    reader = SerialReader(port, baud)

    selection = input("Deseja salvar os dados recebidos em arquivo CSV? (s/n): ").strip().lower()
    if selection == "s":
        reader.enable_saving(flush_interval=10.0)

    reader.start()

    app = QtWidgets.QApplication(sys.argv)
    win = EegWindow(reader, sample_rate=3300.0, update_rate=60)
    win.show()

    try:
        sys.exit(app.exec_())
    finally:
        reader.stop()

if __name__ == "__main__":
    main()
