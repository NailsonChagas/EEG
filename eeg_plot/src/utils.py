from serial.tools.list_ports import comports

def serial_port_selector():
    ports = [p for p in comports() if p.vid is not None and p.pid is not None]

    if not ports:
        print("Nenhuma porta serial ativa encontrada.")
        return None

    print("\nDispositivos seriais conectados:\n")
    for i, port in enumerate(ports):
        print(f"[{i}] {port.device}")
        print(f"    Nome: {port.name}")
        print(f"    Descrição: {port.description or 'n/a'}")
        print(f"    Hardware ID: {port.hwid or 'n/a'}")
        print(f"    USB Vendor ID (VID): {port.vid}")
        print(f"    USB Product ID (PID): {port.pid}")
        if port.serial_number:
            print(f"    Serial Number: {port.serial_number}")
        print("-" * 88)

    while True:
        try:
            escolha = int(input("\nSelecione o número da porta desejada: "))
            if 0 <= escolha < len(ports):
                return ports[escolha].device
            print("Índice inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite apenas o número correspondente à porta.")