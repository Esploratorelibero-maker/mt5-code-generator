# MT5 Code Generator

Applicazione desktop Python con interfaccia grafica per generare codice MQL5 per MetaTrader 5.
Funziona su **Windows**, **macOS** e **Linux**.

## Funzionalità

- **Expert Advisor (EA)**: genera EA completi con strategie MA Crossover, RSI, MACD, Bollinger, Stochastic, Engulfing, Breakout
- **Indicatori custom**: genera indicatori con buffer, frecce segnale, livelli, alert popup/email/push
- **Script**: genera script per chiusure, aperture ordini, statistiche, export CSV, Break Even

---

## Installazione su Windows

### Requisiti
- Python 3.8 o superiore → scarica da [python.org](https://python.org)

### Avvio
```
python main.py
```

### Compilare in .exe (opzionale)
```
pip install pyinstaller
pyinstaller --onefile --windowed --name "MT5CodeGenerator" main.py
```
Il file `.exe` si trova nella cartella `dist/`.

---

## Installazione su macOS

### Requisiti
- Python 3 con tkinter

Su macOS, tkinter **non è incluso** con il Python di sistema. Installa Python tramite [Homebrew](https://brew.sh):

```bash
# 1. Installa Homebrew (se non ce l'hai)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Installa Python con tkinter incluso
brew install python-tk

# 3. Avvia l'app
python3 main.py
```

### Compilare in .app (opzionale)
```bash
pip3 install pyinstaller
pyinstaller --onefile --windowed --name "MT5CodeGenerator" main.py
```
Il file `.app` si trova nella cartella `dist/` — trascinalo in Applicazioni.

---

## Come si usa

1. Scegli il tab: **Expert Advisor** / **Indicatore** / **Script**
2. Compila i parametri nel pannello sinistro
3. Clicca **GENERA CODICE**
4. Il codice MQL5 appare nel pannello destro
5. Clicca **Copia** o **Salva .mq5** per usarlo in MetaTrader 5

## Dove mettere i file .mq5 in MetaTrader 5

- **EA**: `MQL5\Experts\`
- **Indicatori**: `MQL5\Indicators\`
- **Script**: `MQL5\Scripts\`

Dopo aver copiato i file, apri MetaEditor (F4) e compilali con F7.
