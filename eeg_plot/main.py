import sys
from PyQt5 import QtWidgets
from src.eeg_window import EegWindow
from src.utils import serial_port_selector
from src.serial_reader import SerialReader

FLUSH_WRITE_BUFFER = 10
WINDOW_UPDATE_RATE = 60
BAUD_RATE = 330000
FS = 3300


def main():
    port = serial_port_selector()

    if port == None: 
        return

    reader = SerialReader(port, BAUD_RATE)

    selection = input("Deseja salvar os dados recebidos em arquivo CSV? (s/n): ").strip().lower()
    if selection == "s":
        reader.enable_saving(flush_interval=FLUSH_WRITE_BUFFER)

    reader.start()

    app = QtWidgets.QApplication(sys.argv)
    win = EegWindow(reader, sample_rate=FS, update_rate=WINDOW_UPDATE_RATE)
    win.show()

    try:
        sys.exit(app.exec_())
    finally:
        reader.stop()

if __name__ == "__main__":
    main()
