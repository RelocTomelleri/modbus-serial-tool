# ModBus Serial Command Tool

Uno script Python semplice ma efficace per inviare comandi Modbus RTU e leggere la risposta via porta seriale.

Utilizzabile per test, diagnostica e automazioni su dispositivi Modbus (PLC, gateway, I/O remoti) tramite RS-232 o RS-485.

---

## ✅ Requisiti

- Python 3.x
- Libreria `pyserial`

Installa `pyserial` con:

```bash
pip install pyserial
```

---

## 📝 Struttura di config.json
```json
{
  "port": "/dev/ttyAMA2",   // Nome della porta seriale
  "baudrate": 9600,         // Velocità di trasmissione
  "bytesize": 8,            // Dimensione byte (tipicamente 8)
  "parity": "N",            // Parità: N (nessuna), E (pari), O (dispari)
  "stopbits": 1,            // Bit di stop (1 o 2)
  "timeout": 1              // Timeout lettura in secondi
}
```
---

## 🚀 Utilizzo
* Spegni tutte le uscite
```bash
python3 recomputer_modbus_send_receive.py --command "01 0F 00 00 00 08 01 00 FE 95"
```
* Accendit tutte le uscite
```bash
python3 recomputer_modbus_send_receive.py --command "01 0F 00 00 00 08 01 FF BE D5"
```
Assicurati che i comandi includano il CRC finale
* Specifica un fle di configurazione
```bash
python3 recomputer_modbus_send_receive.py --config miofile.json --command "..."
```