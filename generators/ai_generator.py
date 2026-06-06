import urllib.request
import urllib.error
import json
import os

SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".mt5gen_settings.json")

SYSTEM_PROMPT = """Sei un esperto programmatore MQL5 per MetaTrader 5.
Il tuo compito è generare codice MQL5 completo e funzionante in base alla descrizione dell'utente.

Regole IMPORTANTI:
1. Rispondi SOLO con il codice MQL5, nient'altro. Nessuna spiegazione, nessun testo prima o dopo.
2. Il codice deve essere completo, compilabile in MetaEditor senza errori.
3. Includi sempre l'intestazione con #property copyright, #property version.
4. Per Expert Advisor: includi OnInit(), OnDeinit(), OnTick(). Usa CTrade da Trade.mqh.
5. Per Indicatori: includi #property indicator_chart o indicator_separate, SetIndexBuffer, OnInit, OnCalculate.
6. Per Script: includi #property script_show_inputs e OnStart().
7. Usa le best practice MQL5 moderne: handle di indicatori, CopyBuffer, ArraySetAsSeries.
8. I parametri input devono avere commenti descrittivi in italiano.
9. Aggiungi commenti in italiano per spiegare le sezioni principali.
10. Il codice deve essere robusto: controlla gli errori, verifica i handle degli indicatori.
"""


def load_api_key():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                return data.get("api_key", "")
    except Exception:
        pass
    return ""


def save_api_key(key):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"api_key": key}, f)
        return True
    except Exception:
        return False


def generate_with_ai(description, api_key, model="gpt-4o-mini"):
    """
    Chiama l'API OpenAI per generare codice MQL5 dalla descrizione.
    Restituisce (codice, errore) dove errore è None se ok.
    """
    if not api_key or not api_key.strip():
        return None, "Inserisci la tua chiave API OpenAI nelle impostazioni."

    if not description or not description.strip():
        return None, "Scrivi una descrizione prima di generare."

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": description.strip()}
        ],
        "temperature": 0.2,
        "max_tokens": 4000
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key.strip()}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            code = result["choices"][0]["message"]["content"].strip()
            if code.startswith("```"):
                lines = code.split("\n")
                code = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])
            return code, None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            err = json.loads(body)
            msg = err.get("error", {}).get("message", str(e))
        except Exception:
            msg = str(e)
        if e.code == 401:
            return None, "Chiave API non valida. Controlla la tua chiave OpenAI."
        elif e.code == 429:
            return None, "Troppo richieste o credito esaurito. Attendi qualche secondo e riprova."
        elif e.code == 400:
            return None, f"Errore richiesta: {msg}"
        else:
            return None, f"Errore API ({e.code}): {msg}"
    except urllib.error.URLError as e:
        return None, f"Errore di connessione. Controlla la tua connessione internet.\nDettaglio: {e.reason}"
    except Exception as e:
        return None, f"Errore imprevisto: {str(e)}"
