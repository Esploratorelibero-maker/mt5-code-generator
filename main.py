import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
from generators.ea_generator import generate_ea
from generators.indicator_generator import generate_indicator
from generators.script_generator import generate_script


class MT5CodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MT5 Code Generator")
        self.root.geometry("1100x750")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, True)

        self._build_ui()

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#1a1a2e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#16213e", foreground="#e0e0e0",
                        padding=[16, 8], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#0f3460")],
                  foreground=[("selected", "#00d4ff")])
        style.configure("TFrame", background="#1a1a2e")
        style.configure("TLabelframe", background="#1a1a2e", foreground="#00d4ff",
                        bordercolor="#0f3460", font=("Segoe UI", 9, "bold"))
        style.configure("TLabelframe.Label", background="#1a1a2e", foreground="#00d4ff")
        style.configure("TLabel", background="#1a1a2e", foreground="#e0e0e0",
                        font=("Segoe UI", 9))
        style.configure("TEntry", fieldbackground="#16213e", foreground="#e0e0e0",
                        insertcolor="#00d4ff", bordercolor="#0f3460")
        style.configure("TCombobox", fieldbackground="#16213e", foreground="#e0e0e0",
                        selectbackground="#0f3460")
        style.configure("TCheckbutton", background="#1a1a2e", foreground="#e0e0e0",
                        font=("Segoe UI", 9))
        style.configure("TSpinbox", fieldbackground="#16213e", foreground="#e0e0e0")

        title_frame = tk.Frame(self.root, bg="#0f3460", pady=12)
        title_frame.pack(fill="x")
        tk.Label(title_frame, text="⚡ MT5 Code Generator",
                 font=("Segoe UI", 18, "bold"), bg="#0f3460", fg="#00d4ff").pack()
        tk.Label(title_frame, text="Genera codice MQL5 per Expert Advisor, Indicatori e Script",
                 font=("Segoe UI", 9), bg="#0f3460", fg="#a0b4c8").pack()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.ea_tab = EATab(self.notebook)
        self.indicator_tab = IndicatorTab(self.notebook)
        self.script_tab = ScriptTab(self.notebook)

        self.notebook.add(self.ea_tab.frame, text="  Expert Advisor  ")
        self.notebook.add(self.indicator_tab.frame, text="  Indicatore  ")
        self.notebook.add(self.script_tab.frame, text="  Script  ")


class EATab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self._build()

    def _build(self):
        paned = tk.PanedWindow(self.frame, orient=tk.HORIZONTAL, bg="#1a1a2e",
                               sashwidth=6, sashrelief=tk.FLAT)
        paned.pack(fill="both", expand=True)

        left = tk.Frame(paned, bg="#1a1a2e")
        paned.add(left, minsize=380)

        canvas = tk.Canvas(left, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#1a1a2e")
        self.scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._build_form(self.scroll_frame)

        right = tk.Frame(paned, bg="#1a1a2e")
        paned.add(right, minsize=400)
        self._build_output(right)

    def _build_form(self, parent):
        pad = {"padx": 10, "pady": 4}

        general = ttk.LabelFrame(parent, text="Informazioni Generali", padding=10)
        general.pack(fill="x", **pad)

        self._field(general, "Nome EA:", "ea_name", "MyExpertAdvisor")
        self._field(general, "Autore:", "ea_author", "Trader")
        self._field(general, "Versione:", "ea_version", "1.00")
        self._field(general, "Copyright:", "ea_copyright", "2025")

        money = ttk.LabelFrame(parent, text="Gestione Denaro", padding=10)
        money.pack(fill="x", **pad)

        self._field(money, "Lotto fisso:", "ea_lot", "0.01")
        self.ea_use_mm = tk.BooleanVar(value=False)
        ttk.Checkbutton(money, text="Usa Money Management dinamico",
                        variable=self.ea_use_mm).pack(anchor="w")
        self._field(money, "Rischio % per trade:", "ea_risk", "1.0")
        self._field(money, "Stop Loss (pips):", "ea_sl", "50")
        self._field(money, "Take Profit (pips):", "ea_tp", "100")
        self._field(money, "Trailing Stop (pips, 0=disabilitato):", "ea_trail", "0")

        signal = ttk.LabelFrame(parent, text="Segnale di Entrata", padding=10)
        signal.pack(fill="x", **pad)

        tk.Label(signal, text="Strategia:", bg="#1a1a2e", fg="#e0e0e0",
                 font=("Segoe UI", 9)).pack(anchor="w")
        self.ea_strategy = ttk.Combobox(signal, values=[
            "MA Crossover (SMA veloce/lenta)",
            "RSI Overbought/Oversold",
            "MACD Signal Cross",
            "Bollinger Bands Breakout",
            "Stochastic Crossover",
            "Candlestick Pattern (Engulfing)",
            "Breakout High/Low N candele",
            "Doppia MA + RSI Filter"
        ], state="readonly", width=35)
        self.ea_strategy.current(0)
        self.ea_strategy.pack(anchor="w", fill="x", pady=4)

        self._field(signal, "Periodo MA veloce:", "ea_fast_ma", "9")
        self._field(signal, "Periodo MA lenta:", "ea_slow_ma", "21")
        self._field(signal, "Periodo RSI:", "ea_rsi_period", "14")
        self._field(signal, "RSI Oversold:", "ea_rsi_os", "30")
        self._field(signal, "RSI Overbought:", "ea_rsi_ob", "70")

        filters = ttk.LabelFrame(parent, text="Filtri Aggiuntivi", padding=10)
        filters.pack(fill="x", **pad)

        self.ea_filter_trend = tk.BooleanVar(value=False)
        ttk.Checkbutton(filters, text="Filtro trend (MA 200)",
                        variable=self.ea_filter_trend).pack(anchor="w")
        self.ea_filter_session = tk.BooleanVar(value=False)
        ttk.Checkbutton(filters, text="Filtro sessione (Londra/NY)",
                        variable=self.ea_filter_session).pack(anchor="w")
        self.ea_filter_spread = tk.BooleanVar(value=False)
        ttk.Checkbutton(filters, text="Filtro spread massimo",
                        variable=self.ea_filter_spread).pack(anchor="w")
        self._field(filters, "Spread max (punti):", "ea_max_spread", "30")

        options = ttk.LabelFrame(parent, text="Opzioni Aggiuntive", padding=10)
        options.pack(fill="x", **pad)

        self.ea_breakeven = tk.BooleanVar(value=False)
        ttk.Checkbutton(options, text="Break Even automatico",
                        variable=self.ea_breakeven).pack(anchor="w")
        self.ea_partial_close = tk.BooleanVar(value=False)
        ttk.Checkbutton(options, text="Chiusura parziale (50% al 1:1)",
                        variable=self.ea_partial_close).pack(anchor="w")
        self.ea_magic = tk.BooleanVar(value=True)
        ttk.Checkbutton(options, text="Usa Magic Number",
                        variable=self.ea_magic).pack(anchor="w")
        self._field(options, "Magic Number:", "ea_magic_num", "12345")

        tk.Button(parent, text="⚡ GENERA CODICE EA",
                  command=self._generate,
                  bg="#00d4ff", fg="#0f3460", font=("Segoe UI", 11, "bold"),
                  relief=tk.FLAT, pady=10, cursor="hand2").pack(fill="x", padx=10, pady=12)

    def _field(self, parent, label, attr, default):
        f = tk.Frame(parent, bg="#1a1a2e")
        f.pack(fill="x", pady=2)
        tk.Label(f, text=label, bg="#1a1a2e", fg="#a0b4c8",
                 font=("Segoe UI", 9), width=28, anchor="w").pack(side="left")
        var = tk.StringVar(value=default)
        setattr(self, attr, var)
        ttk.Entry(f, textvariable=var, width=18).pack(side="left", padx=4)

    def _build_output(self, parent):
        tk.Label(parent, text="Codice MQL5 Generato", bg="#1a1a2e", fg="#00d4ff",
                 font=("Segoe UI", 10, "bold")).pack(pady=(8, 4))
        self.output = scrolledtext.ScrolledText(parent, bg="#0d1117", fg="#c9d1d9",
                                                 font=("Consolas", 10), insertbackground="#00d4ff",
                                                 selectbackground="#0f3460", relief=tk.FLAT,
                                                 wrap=tk.NONE)
        self.output.pack(fill="both", expand=True, padx=8, pady=4)
        btn_frame = tk.Frame(parent, bg="#1a1a2e")
        btn_frame.pack(fill="x", padx=8, pady=6)
        tk.Button(btn_frame, text="📋 Copia", command=self._copy,
                  bg="#0f3460", fg="#e0e0e0", font=("Segoe UI", 9, "bold"),
                  relief=tk.FLAT, padx=16, pady=6, cursor="hand2").pack(side="left", padx=4)
        tk.Button(btn_frame, text="💾 Salva .mq5", command=self._save,
                  bg="#0f3460", fg="#e0e0e0", font=("Segoe UI", 9, "bold"),
                  relief=tk.FLAT, padx=16, pady=6, cursor="hand2").pack(side="left", padx=4)

    def _generate(self):
        params = {
            "name": self.ea_name.get(),
            "author": self.ea_author.get(),
            "version": self.ea_version.get(),
            "copyright": self.ea_copyright.get(),
            "lot": self.ea_lot.get(),
            "use_mm": self.ea_use_mm.get(),
            "risk": self.ea_risk.get(),
            "sl": self.ea_sl.get(),
            "tp": self.ea_tp.get(),
            "trail": self.ea_trail.get(),
            "strategy": self.ea_strategy.get(),
            "fast_ma": self.ea_fast_ma.get(),
            "slow_ma": self.ea_slow_ma.get(),
            "rsi_period": self.ea_rsi_period.get(),
            "rsi_os": self.ea_rsi_os.get(),
            "rsi_ob": self.ea_rsi_ob.get(),
            "filter_trend": self.ea_filter_trend.get(),
            "filter_session": self.ea_filter_session.get(),
            "filter_spread": self.ea_filter_spread.get(),
            "max_spread": self.ea_max_spread.get(),
            "breakeven": self.ea_breakeven.get(),
            "partial_close": self.ea_partial_close.get(),
            "use_magic": self.ea_magic.get(),
            "magic_num": self.ea_magic_num.get(),
        }
        code = generate_ea(params)
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", code)

    def _copy(self):
        code = self.output.get("1.0", tk.END)
        self.frame.clipboard_clear()
        self.frame.clipboard_append(code)
        messagebox.showinfo("Copiato", "Codice copiato negli appunti!")

    def _save(self):
        from tkinter import filedialog
        name = self.ea_name.get() or "MyEA"
        path = filedialog.asksaveasfilename(
            defaultextension=".mq5",
            filetypes=[("MQL5 Files", "*.mq5"), ("All Files", "*.*")],
            initialfile=f"{name}.mq5"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.output.get("1.0", tk.END))
            messagebox.showinfo("Salvato", f"File salvato in:\n{path}")


class IndicatorTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self._build()

    def _build(self):
        paned = tk.PanedWindow(self.frame, orient=tk.HORIZONTAL, bg="#1a1a2e",
                               sashwidth=6, sashrelief=tk.FLAT)
        paned.pack(fill="both", expand=True)

        left = tk.Frame(paned, bg="#1a1a2e")
        paned.add(left, minsize=380)

        canvas = tk.Canvas(left, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#1a1a2e")
        self.scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._build_form(self.scroll_frame)

        right = tk.Frame(paned, bg="#1a1a2e")
        paned.add(right, minsize=400)
        self._build_output(right)

    def _build_form(self, parent):
        pad = {"padx": 10, "pady": 4}

        general = ttk.LabelFrame(parent, text="Informazioni Generali", padding=10)
        general.pack(fill="x", **pad)

        self._field(general, "Nome Indicatore:", "ind_name", "MyIndicator")
        self._field(general, "Autore:", "ind_author", "Trader")
        self._field(general, "Versione:", "ind_version", "1.00")

        ind_type = ttk.LabelFrame(parent, text="Tipo Indicatore", padding=10)
        ind_type.pack(fill="x", **pad)

        tk.Label(ind_type, text="Tipo:", bg="#1a1a2e", fg="#e0e0e0",
                 font=("Segoe UI", 9)).pack(anchor="w")
        self.ind_type = ttk.Combobox(ind_type, values=[
            "Moving Average (SMA/EMA/WMA)",
            "Oscillatore RSI",
            "MACD personalizzato",
            "Bande di Bollinger",
            "Stocastico personalizzato",
            "CCI (Commodity Channel Index)",
            "ATR (Average True Range)",
            "Momentum",
            "Williams %R",
            "Doppia MA con segnali freccia",
            "Canale di regressione lineare",
            "Volume personalizzato"
        ], state="readonly", width=35)
        self.ind_type.current(0)
        self.ind_type.pack(anchor="w", fill="x", pady=4)

        tk.Label(ind_type, text="Posizione:", bg="#1a1a2e", fg="#e0e0e0",
                 font=("Segoe UI", 9)).pack(anchor="w")
        self.ind_window = ttk.Combobox(ind_type, values=[
            "Finestra principale (sul grafico)",
            "Finestra separata"
        ], state="readonly", width=35)
        self.ind_window.current(0)
        self.ind_window.pack(anchor="w", fill="x", pady=4)

        params_f = ttk.LabelFrame(parent, text="Parametri", padding=10)
        params_f.pack(fill="x", **pad)

        self._field(params_f, "Periodo principale:", "ind_period", "14")
        self._field(params_f, "Periodo segnale:", "ind_signal", "9")
        tk.Label(params_f, text="Metodo MA:", bg="#1a1a2e", fg="#e0e0e0",
                 font=("Segoe UI", 9)).pack(anchor="w")
        self.ind_ma_method = ttk.Combobox(params_f, values=[
            "MODE_SMA", "MODE_EMA", "MODE_SMMA", "MODE_LWMA"
        ], state="readonly", width=20)
        self.ind_ma_method.current(0)
        self.ind_ma_method.pack(anchor="w", pady=4)

        tk.Label(params_f, text="Applicato a:", bg="#1a1a2e", fg="#e0e0e0",
                 font=("Segoe UI", 9)).pack(anchor="w")
        self.ind_applied = ttk.Combobox(params_f, values=[
            "PRICE_CLOSE", "PRICE_OPEN", "PRICE_HIGH", "PRICE_LOW",
            "PRICE_MEDIAN", "PRICE_TYPICAL", "PRICE_WEIGHTED"
        ], state="readonly", width=20)
        self.ind_applied.current(0)
        self.ind_applied.pack(anchor="w", pady=4)

        buffers = ttk.LabelFrame(parent, text="Buffer e Colori", padding=10)
        buffers.pack(fill="x", **pad)

        self._field(buffers, "Numero buffer:", "ind_buffers", "1")
        self.ind_arrows = tk.BooleanVar(value=False)
        ttk.Checkbutton(buffers, text="Aggiungi frecce segnale (BUY/SELL)",
                        variable=self.ind_arrows).pack(anchor="w")
        self.ind_levels = tk.BooleanVar(value=False)
        ttk.Checkbutton(buffers, text="Aggiungi livelli orizzontali (es. 70/30)",
                        variable=self.ind_levels).pack(anchor="w")
        self._field(buffers, "Livello alto:", "ind_level_high", "70")
        self._field(buffers, "Livello basso:", "ind_level_low", "30")

        alerts = ttk.LabelFrame(parent, text="Alert", padding=10)
        alerts.pack(fill="x", **pad)

        self.ind_alert = tk.BooleanVar(value=False)
        ttk.Checkbutton(alerts, text="Alert popup", variable=self.ind_alert).pack(anchor="w")
        self.ind_email = tk.BooleanVar(value=False)
        ttk.Checkbutton(alerts, text="Notifica email", variable=self.ind_email).pack(anchor="w")
        self.ind_push = tk.BooleanVar(value=False)
        ttk.Checkbutton(alerts, text="Notifica push mobile", variable=self.ind_push).pack(anchor="w")

        tk.Button(parent, text="⚡ GENERA CODICE INDICATORE",
                  command=self._generate,
                  bg="#00d4ff", fg="#0f3460", font=("Segoe UI", 11, "bold"),
                  relief=tk.FLAT, pady=10, cursor="hand2").pack(fill="x", padx=10, pady=12)

    def _field(self, parent, label, attr, default):
        f = tk.Frame(parent, bg="#1a1a2e")
        f.pack(fill="x", pady=2)
        tk.Label(f, text=label, bg="#1a1a2e", fg="#a0b4c8",
                 font=("Segoe UI", 9), width=28, anchor="w").pack(side="left")
        var = tk.StringVar(value=default)
        setattr(self, attr, var)
        ttk.Entry(f, textvariable=var, width=18).pack(side="left", padx=4)

    def _build_output(self, parent):
        tk.Label(parent, text="Codice MQL5 Generato", bg="#1a1a2e", fg="#00d4ff",
                 font=("Segoe UI", 10, "bold")).pack(pady=(8, 4))
        self.output = scrolledtext.ScrolledText(parent, bg="#0d1117", fg="#c9d1d9",
                                                 font=("Consolas", 10), insertbackground="#00d4ff",
                                                 selectbackground="#0f3460", relief=tk.FLAT,
                                                 wrap=tk.NONE)
        self.output.pack(fill="both", expand=True, padx=8, pady=4)
        btn_frame = tk.Frame(parent, bg="#1a1a2e")
        btn_frame.pack(fill="x", padx=8, pady=6)
        tk.Button(btn_frame, text="📋 Copia", command=self._copy,
                  bg="#0f3460", fg="#e0e0e0", font=("Segoe UI", 9, "bold"),
                  relief=tk.FLAT, padx=16, pady=6, cursor="hand2").pack(side="left", padx=4)
        tk.Button(btn_frame, text="💾 Salva .mq5", command=self._save,
                  bg="#0f3460", fg="#e0e0e0", font=("Segoe UI", 9, "bold"),
                  relief=tk.FLAT, padx=16, pady=6, cursor="hand2").pack(side="left", padx=4)

    def _generate(self):
        params = {
            "name": self.ind_name.get(),
            "author": self.ind_author.get(),
            "version": self.ind_version.get(),
            "type": self.ind_type.get(),
            "window": self.ind_window.get(),
            "period": self.ind_period.get(),
            "signal": self.ind_signal.get(),
            "ma_method": self.ind_ma_method.get(),
            "applied": self.ind_applied.get(),
            "buffers": self.ind_buffers.get(),
            "arrows": self.ind_arrows.get(),
            "levels": self.ind_levels.get(),
            "level_high": self.ind_level_high.get(),
            "level_low": self.ind_level_low.get(),
            "alert": self.ind_alert.get(),
            "email": self.ind_email.get(),
            "push": self.ind_push.get(),
        }
        code = generate_indicator(params)
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", code)

    def _copy(self):
        code = self.output.get("1.0", tk.END)
        self.frame.clipboard_clear()
        self.frame.clipboard_append(code)
        messagebox.showinfo("Copiato", "Codice copiato negli appunti!")

    def _save(self):
        from tkinter import filedialog
        name = self.ind_name.get() or "MyIndicator"
        path = filedialog.asksaveasfilename(
            defaultextension=".mq5",
            filetypes=[("MQL5 Files", "*.mq5"), ("All Files", "*.*")],
            initialfile=f"{name}.mq5"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.output.get("1.0", tk.END))
            messagebox.showinfo("Salvato", f"File salvato in:\n{path}")


class ScriptTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self._build()

    def _build(self):
        paned = tk.PanedWindow(self.frame, orient=tk.HORIZONTAL, bg="#1a1a2e",
                               sashwidth=6, sashrelief=tk.FLAT)
        paned.pack(fill="both", expand=True)

        left = tk.Frame(paned, bg="#1a1a2e")
        paned.add(left, minsize=380)

        canvas = tk.Canvas(left, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#1a1a2e")
        self.scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._build_form(self.scroll_frame)

        right = tk.Frame(paned, bg="#1a1a2e")
        paned.add(right, minsize=400)
        self._build_output(right)

    def _build_form(self, parent):
        pad = {"padx": 10, "pady": 4}

        general = ttk.LabelFrame(parent, text="Informazioni Generali", padding=10)
        general.pack(fill="x", **pad)

        self._field(general, "Nome Script:", "sc_name", "MyScript")
        self._field(general, "Autore:", "sc_author", "Trader")
        self._field(general, "Versione:", "sc_version", "1.00")

        sc_type = ttk.LabelFrame(parent, text="Tipo Script", padding=10)
        sc_type.pack(fill="x", **pad)

        tk.Label(sc_type, text="Funzione:", bg="#1a1a2e", fg="#e0e0e0",
                 font=("Segoe UI", 9)).pack(anchor="w")
        self.sc_type = ttk.Combobox(sc_type, values=[
            "Chiudi tutte le posizioni",
            "Chiudi solo posizioni BUY",
            "Chiudi solo posizioni SELL",
            "Chiudi posizioni in perdita",
            "Chiudi posizioni in profitto",
            "Apri ordine BUY a mercato",
            "Apri ordine SELL a mercato",
            "Cancella tutti gli ordini pendenti",
            "Modifica SL/TP di tutte le posizioni",
            "Calcola statistiche giornaliere",
            "Esporta trade history in CSV",
            "Imposta Break Even su tutte le posizioni"
        ], state="readonly", width=35)
        self.sc_type.current(0)
        self.sc_type.pack(anchor="w", fill="x", pady=4)

        params_f = ttk.LabelFrame(parent, text="Parametri", padding=10)
        params_f.pack(fill="x", **pad)

        self._field(params_f, "Lotto (se apre ordine):", "sc_lot", "0.01")
        self._field(params_f, "Stop Loss (pips):", "sc_sl", "50")
        self._field(params_f, "Take Profit (pips):", "sc_tp", "100")
        self._field(params_f, "Magic Number (0=tutti):", "sc_magic", "0")
        self._field(params_f, "Slippage:", "sc_slippage", "3")

        options = ttk.LabelFrame(parent, text="Opzioni", padding=10)
        options.pack(fill="x", **pad)

        self.sc_confirm = tk.BooleanVar(value=True)
        ttk.Checkbutton(options, text="Chiedi conferma prima di eseguire",
                        variable=self.sc_confirm).pack(anchor="w")
        self.sc_alert = tk.BooleanVar(value=True)
        ttk.Checkbutton(options, text="Mostra alert con risultato",
                        variable=self.sc_alert).pack(anchor="w")
        self.sc_comment = tk.BooleanVar(value=True)
        ttk.Checkbutton(options, text="Aggiungi commento dettagliato al codice",
                        variable=self.sc_comment).pack(anchor="w")

        tk.Button(parent, text="⚡ GENERA CODICE SCRIPT",
                  command=self._generate,
                  bg="#00d4ff", fg="#0f3460", font=("Segoe UI", 11, "bold"),
                  relief=tk.FLAT, pady=10, cursor="hand2").pack(fill="x", padx=10, pady=12)

    def _field(self, parent, label, attr, default):
        f = tk.Frame(parent, bg="#1a1a2e")
        f.pack(fill="x", pady=2)
        tk.Label(f, text=label, bg="#1a1a2e", fg="#a0b4c8",
                 font=("Segoe UI", 9), width=28, anchor="w").pack(side="left")
        var = tk.StringVar(value=default)
        setattr(self, attr, var)
        ttk.Entry(f, textvariable=var, width=18).pack(side="left", padx=4)

    def _build_output(self, parent):
        tk.Label(parent, text="Codice MQL5 Generato", bg="#1a1a2e", fg="#00d4ff",
                 font=("Segoe UI", 10, "bold")).pack(pady=(8, 4))
        self.output = scrolledtext.ScrolledText(parent, bg="#0d1117", fg="#c9d1d9",
                                                 font=("Consolas", 10), insertbackground="#00d4ff",
                                                 selectbackground="#0f3460", relief=tk.FLAT,
                                                 wrap=tk.NONE)
        self.output.pack(fill="both", expand=True, padx=8, pady=4)
        btn_frame = tk.Frame(parent, bg="#1a1a2e")
        btn_frame.pack(fill="x", padx=8, pady=6)
        tk.Button(btn_frame, text="📋 Copia", command=self._copy,
                  bg="#0f3460", fg="#e0e0e0", font=("Segoe UI", 9, "bold"),
                  relief=tk.FLAT, padx=16, pady=6, cursor="hand2").pack(side="left", padx=4)
        tk.Button(btn_frame, text="💾 Salva .mq5", command=self._save,
                  bg="#0f3460", fg="#e0e0e0", font=("Segoe UI", 9, "bold"),
                  relief=tk.FLAT, padx=16, pady=6, cursor="hand2").pack(side="left", padx=4)

    def _generate(self):
        params = {
            "name": self.sc_name.get(),
            "author": self.sc_author.get(),
            "version": self.sc_version.get(),
            "type": self.sc_type.get(),
            "lot": self.sc_lot.get(),
            "sl": self.sc_sl.get(),
            "tp": self.sc_tp.get(),
            "magic": self.sc_magic.get(),
            "slippage": self.sc_slippage.get(),
            "confirm": self.sc_confirm.get(),
            "alert": self.sc_alert.get(),
            "comment": self.sc_comment.get(),
        }
        code = generate_script(params)
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", code)

    def _copy(self):
        code = self.output.get("1.0", tk.END)
        self.frame.clipboard_clear()
        self.frame.clipboard_append(code)
        messagebox.showinfo("Copiato", "Codice copiato negli appunti!")

    def _save(self):
        from tkinter import filedialog
        name = self.sc_name.get() or "MyScript"
        path = filedialog.asksaveasfilename(
            defaultextension=".mq5",
            filetypes=[("MQL5 Files", "*.mq5"), ("All Files", "*.*")],
            initialfile=f"{name}.mq5"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.output.get("1.0", tk.END))
            messagebox.showinfo("Salvato", f"File salvato in:\n{path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MT5CodeGeneratorApp(root)
    root.mainloop()
