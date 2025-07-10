import argparse
import subprocess
import sys

"""
CMD: turn_on_off_relay
    Es: 01 05 00 00 FF 00 8C 3A
        1° byte è un indirizzo del dispositivo.
        2° byte è il codice funzione.
        3° e il 4° byte sono indirizzi relè/registro. Così può essere 0x0000, 0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006, 0x, 0x0007.
        5° e 6° byte sono dati relè/registro. 01 significa relè di accensione e 00 significa relè di spegnimento.
        7° e l'8° byte sono il codice CRC.
"""

# === Dizionario comandi ===
COMMANDS = {
    "set_addr_1": "00 10 00 00 00 01 02 00 01 6A 00",
    "set_addr_2": "00 10 00 00 00 01 02 00 02 2A 01",
    "set_addr_3": "00 10 00 00 00 01 02 00 03 EB C1",
    "get_address": "00 03 00 00 00 01 85 DB",

    "turn_on_relay_0": "01 05 00 00 FF 00 8C 3A",
    "turn_on_relay_1": "01 05 00 01 FF 00 DD FA",
    "turn_on_relay_2": "01 05 00 02 FF 00 2D FA",
    "turn_on_relay_3": "01 05 00 03 FF 00 7C 3A",
    "turn_off_relay_0": "01 05 00 00 00 00 CD CA",
    "turn_off_relay_1": "01 05 00 01 00 00 9C 0A",
    "turn_off_relay_2": "01 05 00 02 00 00 6C 0A",
    "turn_off_relay_3": "01 05 00 03 00 00 3D CA",

    "turn_off_all_relay": "01 0F 00 00 00 08 01 00 FE 95",
    "turn_on_all_relay": "01 0F 00 00 00 08 01 FF BE D5",

    "get_rele_status_0": "01 01 00 00 00 01 FD CA",
    "get_rele_status_1": "01 01 00 01 00 01 AC 0A",
    "get_rele_status_2": "01 01 00 02 00 01 5C 0A",
    "get_rele_status_3": "01 01 00 03 00 01 0D CA",
}

# === Funzione per eseguire il comando ===
def send_command(command_str, config_file):
    try:
        cmd = [
            "python3",
            "../v0_ReComputer/recomputer_modbus_send_receive.py",
            "--config", config_file,
            "--command", command_str
        ]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando: {e}")

# === Menù Interattivo ===
def interactive_menu(config_file=""):
    print("=== Menù Comandi Modbus ===")
    for idx, name in enumerate(COMMANDS.keys(), start=1):
        print(f"[{idx}] {name}")
    print("[0] Esci")

    while True:
        choice = input("Seleziona un comando da eseguire: ")
        if not choice.isdigit():
            print("Inserire un numero valido.")
            continue

        choice = int(choice)
        if choice == 0:
            print("Uscita dal menù.")
            break
        elif 1 <= choice <= len(COMMANDS):
            command_name = list(COMMANDS.keys())[choice - 1]
            print(f">>> Eseguo: {command_name}")
            send_command(COMMANDS[command_name], config_file)
        else:
            print("Scelta non valida.")

# === Main ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Menù comandi Modbus per relè.")
    parser.add_argument("--config", default="../v0_ReComputer/config.json", help="File di configurazione (default: config.json)")
    parser.add_argument("--command", choices=COMMANDS.keys(), help="Comando da eseguire direttamente")

    args = parser.parse_args()

    if args.command:
        # Esecuzione diretta
        print(f"Esecuzione comando '{args.command}'...")
        send_command(COMMANDS[args.command], args.config)
    else:
        # Menù interattivo
        interactive_menu(args.config)
