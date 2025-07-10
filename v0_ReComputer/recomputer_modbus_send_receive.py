import serial
import json
import argparse
import time
import os

"""
=== Esempio Esecuzione ===
    python3 modbus_send_receive.py --command "01 0F 00 00 00 08 01 00 FE 95"
se vuoi usare un file di configurazione diverso:
    python3 modbus_send_receive.py --config myconfig.json --command "..."
"""

def convert_pin(port):
    pin = None
    if port == "/dev/ttyAMA2":
        pin = 6
    elif port == "/dev/ttyAMA3":
        pin = 17
    elif port == "/dev/ttyAMA5":
        pin = 24

    return pin

# Funzione per abilitare il trasmettitore (de/tx)
def enable_transmit(port):
    pin = convert_pin(port)
    print(f"Master: Abilitazione trasmissione su GPIO{pin}")
    os.system(f'sudo raspi-gpio set {pin} op dh')  # Imposta gpio6 per trasmettere (Alta)

# Funzione per disabilitare il trasmettitore (rx)
def disable_transmit(port):
    pin = convert_pin(port)
    print(f"Master: Disabilitazione trasmissione su GPIO{pin}")
    os.system(f'sudo raspi-gpio set {pin} op dl')  # Disabilita la trasmissione (Bassa)

def parse_hex_command(hex_str):
    """Converte una stringa come '01 0F 00 00' in bytes"""
    return bytes(int(b, 16) for b in hex_str.strip().split())

def load_config(config_file):
    """Carica la configurazione da file JSON"""
    with open(config_file, 'r') as f:
        return json.load(f)

# Parser degli argomenti della CLI
parser = argparse.ArgumentParser(description="Invia un comando Modbus RTU leggendo la config da file.")
parser.add_argument('--config', default='config.json', help='File di configurazione (default: config.json)')
parser.add_argument('--command', required=True, help='Comando esadecimale da inviare, es: "01 0F 00 00 00 08 01 00 FE 95"')
args = parser.parse_args()

# Carica configurazione
config = load_config(args.config)

# Mappa parità da lettera a costante pyserial
parity_map = {
    'N': serial.PARITY_NONE,
    'E': serial.PARITY_EVEN,
    'O': serial.PARITY_ODD,
    'M': serial.PARITY_MARK,
    'S': serial.PARITY_SPACE
}

# Prepara la porta seriale
ser = serial.Serial(
    port=config['port'],
    baudrate=config['baudrate'],
    bytesize=config['bytesize'],
    parity=parity_map[config['parity'].upper()],
    stopbits=config['stopbits'],
    timeout=config['timeout']
)

# === Abilita la trasmissione ===
enable_transmit(config['port'])

# === Invio comando ===
# Converte il comando da inviare
cmd = parse_hex_command(args.command)

# Invia il comando
ser.write(cmd)
print("Comando inviato:", args.command)

# Disabilita la trasmissione per permettere la ricezione
disable_transmit(config['port'])

# Attende un attimo per ricevere risposta

# Legge fino a 256 byte dalla seriale
response = ""
while True:  # Timeout di 5 secondi
    response = ser.read(256)
    if response:
        break

# Stampa risposta esadecimale
print("Risposta ricevuta:", response.hex(' ').upper())

# === FINE ===
# Chiude la porta
ser.close()
