# MODBUS-SERIAL-TOOL – Utils

# relè_modbus_cmd_menu.py
Script che utilizza v0_ReComputer/recomputer_modbus_send_receive.py & v0_ReComputer/config.json per poter comandare il dispositivo relè modbus esterno collegato alla porta RS-485 del reComputer

## 🚀 Esecuzione
### 🔘 Modalità Interattiva
Per avviare il menù interattivo:

```bash
python3 relay_modbus_cmd_menu.py
```
Ti verrà mostrato un menù con i comandi disponibili. Seleziona un numero per eseguire il comando corrispondente.

### ⚡ Modalità Diretta (senza menù)
Puoi eseguire direttamente un comando specifico senza passare per il menù:
```bash
python3 relay_modbus_cmd_menu.py --command accendi_tutti
```

### 🔧Comandi disponibili
**Imposta l'indirizzo Modbus del dispositivo relè:**
- set_addr_1
- set_addr_2
- set_addr_3
- get_address
**Accendi/spegni i relè:**
- turn_on_relay_0
- turn_on_relay_1
- turn_on_relay_2
- turn_on_relay_3
- turn_off_relay_0
- turn_off_relay_1
- turn_off_relay_2
- turn_off_relay_3
- turn_off_all_relay
- turn_on_all_relay
**Restituisci lo stato del relè:**
- get_rele_status_0
- get_rele_status_1
- get_rele_status_2
- get_rele_status_3

| Byte       | Significato           | Dettagli                                 |
|------------|------------------------|------------------------------------------|
| 1° byte    | Modbus Address         | Indirizzo del dispositivo (es. `01`)     |
| 2° byte    | Function Code          | Codice funzione Modbus (es. `01` per Read Coil Status) |
| 3° byte    | Byte Count             | Numero di byte successivi contenenti dati (es. `01`) |
| 4° byte    | Stato Relè             | `00` = Spento, `01` = Acceso             |
| 5° byte    | CRC (parte 1)          | Controllo di ridondanza ciclico          |
| 6° byte    | CRC (parte 2)          |                                          |

---

## 📄 Specificare un file di configurazione diverso
Se vuoi usare un file di configurazione differente dal default (v0_ReComputer/config.json):
```bash
python3 relay_modbus_cmd_menu.py --config ./path/to/config.json
```
Puoi anche combinarlo con un comando:
```bash
python3 relay_modbus_cmd_menu.py --config ./myconfig.json --command get_address
```