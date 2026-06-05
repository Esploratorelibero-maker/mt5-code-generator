# MT5 Code Generator

Applicazione desktop Python con interfaccia grafica per generare codice MQL5 per MetaTrader 5.

## Funzionalità

- **Expert Advisor (EA)**: genera EA completi con strategie MA Crossover, RSI, MACD, Bollinger, Stochastic, Engulfing, Breakout
- **Indicatori custom**: genera indicatori con buffer, frecce segnale, livelli, alert popup/email/push
- **Script**: genera script per chiusure, aperture ordini, statistiche, export CSV, Break Even

## Requisiti

- Python 3.8 o superiore
- tkinter (incluso con Python su Windows)

## Installazione e avvio

```bash
# 1. Clona o scarica i file
# 2. Avvia l'app
python main.py
```

Su Windows tkinter è già incluso con Python, non servono installazioni aggiuntive.

## Compilare in .exe (opzionale)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "MT5CodeGenerator" main.py
```

Il file `.exe` viene creato nella cartella `dist/`.

## Come si usa

1. Scegli il tab (Expert Advisor / Indicatore / Script)
2. Compila i parametri nel pannello sinistro
3. Clicca **GENERA CODICE**
4. Il codice MQL5 appare nel pannello destro
5. Clicca **Copia** o **Salva .mq5** per usarlo in MetaTrader 5

## Dove mettere i file .mq5 in MetaTrader 5

- **EA**: `MQL5\Experts\`
- **Indicatori**: `MQL5\Indicators\`
- **Script**: `MQL5\Scripts\`

Dopo aver copiato i file, apri MetaEditor (F4) e compilali con F7.
