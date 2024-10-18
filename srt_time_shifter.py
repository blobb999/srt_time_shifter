import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import os

def shift_timecode(timecode, shift):
    """Verschiebt den gegebenen SRT-Zeitstempel um die angegebene Anzahl von Sekunden."""
    # Zerlege den Zeitstempel in Stunden, Minuten, Sekunden und Millisekunden
    hours, minutes, seconds_millis = timecode.split(':')
    seconds, millis = seconds_millis.split(',')

    # Konvertiere alles in Millisekunden
    total_millis = (int(hours) * 3600 * 1000) + (int(minutes) * 60 * 1000) + (int(seconds) * 1000) + int(millis)
    
    # Wende die Verschiebung (in Sekunden) auf die Gesamtzeit in Millisekunden an
    new_total_millis = total_millis + int(round(shift * 1000))

    # Stelle sicher, dass die Zeit nicht negativ ist
    if new_total_millis < 0:
        new_total_millis = 0

    # Konvertiere zurück zu Stunden, Minuten, Sekunden und Millisekunden
    new_hours = new_total_millis // 3600000
    new_total_millis = new_total_millis % 3600000
    new_minutes = new_total_millis // 60000
    new_total_millis = new_total_millis % 60000
    new_seconds = new_total_millis // 1000
    new_millis = new_total_millis % 1000

    # Gib den formatierten Zeitstempel im richtigen SRT-Format zurück (hh:mm:ss,SSS)
    return f"{int(new_hours):02}:{int(new_minutes):02}:{int(new_seconds):02},{int(new_millis):03}"

def process_srt(file_path, shift_seconds, output_dir, overwrite=False):
    """Verarbeitet die SRT-Datei und verschiebt alle Zeitstempel."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    timecode_pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")
    new_lines = []
    for line in lines:
        match = timecode_pattern.match(line)
        if match:
            start_time, end_time = match.groups()
            new_start_time = shift_timecode(start_time, shift_seconds)
            new_end_time = shift_timecode(end_time, shift_seconds)
            new_lines.append(f"{new_start_time} --> {new_end_time}\n")
        else:
            new_lines.append(line)

    if overwrite:
        output_file_path = file_path
    else:
        base_name = os.path.basename(file_path)
        output_file_path = os.path.join(output_dir, base_name.replace(".srt", f"_shifted_{shift_seconds}s.srt"))
    
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(new_lines)

    return output_file_path

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("SRT-Dateien", "*.srt")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
    validate_inputs()

def select_output_directory():
    directory = filedialog.askdirectory()
    if directory:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, directory)
    validate_inputs()

def shift_srt():
    file_path = file_entry.get()
    output_dir = output_entry.get()
    if not file_path:
        status_label.config(text=texts[current_language]['status_no_file'], foreground="red")
        return
    if not output_dir and not overwrite_var.get():
        status_label.config(text=texts[current_language]['status_no_output_dir'], foreground="red")
        return
    try:
        shift_seconds = float(shift_entry.get())
    except ValueError:
        status_label.config(text=texts[current_language]['status_invalid_shift'], foreground="red")
        return

    try:
        output_file_path = process_srt(file_path, shift_seconds, output_dir, overwrite=overwrite_var.get())
        status_label.config(text=f"{texts[current_language]['status_success']}: {output_file_path}", foreground="green")
    except Exception as e:
        status_label.config(text=f"{texts[current_language]['status_error']}: {e}", foreground="red")

def validate_inputs(*args):
    file_provided = bool(file_entry.get())
    shift_provided = shift_entry.get().strip() != ''
    output_provided = bool(output_entry.get()) or overwrite_var.get()
    if file_provided and shift_provided and output_provided:
        process_button.config(state='normal')
    else:
        process_button.config(state='disabled')

def change_language(lang):
    global current_language
    current_language = lang
    # Aktualisiere alle Widget-Texte
    title_label.config(text=texts[current_language]['title'])
    file_label.config(text=texts[current_language]['file_label'])
    file_button.config(text=texts[current_language]['browse_button'])
    output_label.config(text=texts[current_language]['output_label'])
    output_button.config(text=texts[current_language]['browse_button'])
    shift_label.config(text=texts[current_language]['shift_label'])
    process_button.config(text=texts[current_language]['process_button'])
    overwrite_checkbutton.config(text=texts[current_language]['overwrite_label'])
    status_label.config(text="")
    # Aktualisiere Tooltip
    tooltip_text = texts[current_language]['tooltip_text']
    shift_tooltip.text = tooltip_text
    # Aktualisiere Sprache des Buttons
    language_button.config(text=texts[current_language]['language_button'])

# Tooltip-Klasse
class CreateToolTip(object):
    """
    Erzeugt einen Tooltip für ein Widget.
    """
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        "Zeigt den Tooltip an."
        if self.tip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Entfernt die Fensterdekorationen
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        "Versteckt den Tooltip."
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

# Sprachressourcen
texts = {
    'en': {
        'title': "SRT Time Shifter",
        'file_label': "Select SRT file:",
        'browse_button': "Browse",
        'output_label': "Output directory:",
        'shift_label': "Shift by (seconds):",
        'process_button': "Shift SRT",
        'overwrite_label': "Overwrite original file",
        'status_no_file': "Please select a file.",
        'status_no_output_dir': "Please select an output directory.",
        'status_invalid_shift': "Please enter a valid number for the shift.",
        'status_success': "File saved as",
        'status_error': "Error",
        'tooltip_text': (
            "Positive shift (e.g., +8 seconds):\n"
            "    Subtitles are shifted 8 seconds forward.\n"
            "    Result: Subtitles appear 8 seconds later than the original.\n"
            "    Use when subtitles appear too early.\n\n"
            "Negative shift (e.g., -8 seconds):\n"
            "    Subtitles are shifted 8 seconds backward.\n"
            "    Result: Subtitles appear 8 seconds earlier than the original.\n"
            "    Use when subtitles appear too late.\n\n"
            "Example:\n"
            "If a subtitle originally appears at 00:00:51,396,\n"
            "applying a positive shift of +8 seconds will change it to 00:00:59,396.\n"
            "The subtitle will appear 8 seconds later.\n\n"
            "Applying a negative shift of -8 seconds will change it to 00:00:43,396.\n"
            "The subtitle will appear 8 seconds earlier."
        ),
        'language_button': "Deutsch",
    },
    'de': {
        'title': "SRT Time Shifter",
        'file_label': "SRT-Datei auswählen:",
        'browse_button': "Durchsuchen",
        'output_label': "Ausgabeverzeichnis:",
        'shift_label': "Verschieben um (Sekunden):",
        'process_button': "SRT verschieben",
        'overwrite_label': "Originaldatei überschreiben",
        'status_no_file': "Bitte wählen Sie eine Datei aus.",
        'status_no_output_dir': "Bitte wählen Sie ein Ausgabeverzeichnis aus.",
        'status_invalid_shift': "Bitte geben Sie eine gültige Zahl für die Verschiebung ein.",
        'status_success': "Datei gespeichert als",
        'status_error': "Fehler",
        'tooltip_text': (
            "Positive Verschiebung (z.B. +8 Sekunden):\n"
            "    Die Untertitel werden um 8 Sekunden nach hinten verschoben.\n"
            "    Ergebnis: Die Untertitel erscheinen 8 Sekunden später als im Original.\n"
            "    Anwendung: Wenn die Untertitel zu früh erscheinen.\n\n"
            "Negative Verschiebung (z.B. -8 Sekunden):\n"
            "    Die Untertitel werden um 8 Sekunden nach vorne verschoben.\n"
            "    Ergebnis: Die Untertitel erscheinen 8 Sekunden früher als im Original.\n"
            "    Anwendung: Wenn die Untertitel zu spät erscheinen.\n\n"
            "Beispiel:\n"
            "Angenommen, ein Untertitel erscheint ursprünglich bei 00:00:51,396.\n"
            "Wenn Sie eine positive Verschiebung von +8 Sekunden anwenden, wird der neue Zeitstempel zu 00:00:59,396.\n"
            "Der Untertitel erscheint also 8 Sekunden später.\n\n"
            "Wenn Sie stattdessen eine negative Verschiebung von -8 Sekunden anwenden,\n"
            "wird der neue Zeitstempel zu 00:00:43,396. Der Untertitel erscheint dann 8 Sekunden früher."
        ),
        'language_button': "English",
    }
}

current_language = 'en'  # Standardsprache ist Englisch

# Erstelle das GUI-Fenster
root = tk.Tk()
root.title("SRT Time Shifter")

# Verwende ttk für moderne Widgets
style = ttk.Style(root)
style.theme_use('clam')

# Hauptframe
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Titel-Label
title_label = ttk.Label(main_frame, text=texts[current_language]['title'], font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

# Sprachbutton
def toggle_language():
    new_lang = 'de' if current_language == 'en' else 'en'
    change_language(new_lang)
    # Aktualisiere Sprache des Buttons
    language_button.config(text=texts[current_language]['language_button'])

language_button = ttk.Button(root, text=texts[current_language]['language_button'], command=toggle_language)
language_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

# Dateiauswahl
file_label = ttk.Label(main_frame, text=texts[current_language]['file_label'])
file_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
file_entry = ttk.Entry(main_frame, width=50)
file_entry.grid(row=1, column=1, padx=5, pady=5)
file_button = ttk.Button(main_frame, text=texts[current_language]['browse_button'], command=open_file)
file_button.grid(row=1, column=2, padx=5, pady=5)

# Ausgabeverzeichnis
output_label = ttk.Label(main_frame, text=texts[current_language]['output_label'])
output_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
output_entry = ttk.Entry(main_frame, width=50)
output_entry.grid(row=2, column=1, padx=5, pady=5)
output_button = ttk.Button(main_frame, text=texts[current_language]['browse_button'], command=select_output_directory)
output_button.grid(row=2, column=2, padx=5, pady=5)

# Checkbox zum Überschreiben
overwrite_var = tk.BooleanVar()
overwrite_var.set(False)
def toggle_output_entry():
    if overwrite_var.get():
        output_entry.config(state='disabled')
        output_button.config(state='disabled')
    else:
        output_entry.config(state='normal')
        output_button.config(state='normal')
    validate_inputs()

overwrite_checkbutton = ttk.Checkbutton(main_frame, text=texts[current_language]['overwrite_label'], variable=overwrite_var, command=toggle_output_entry)
overwrite_checkbutton.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

# Eingabe für die Zeitverschiebung
shift_label = ttk.Label(main_frame, text=texts[current_language]['shift_label'])
shift_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
shift_entry = ttk.Entry(main_frame, width=10)
shift_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

# Tooltip erstellen
shift_tooltip = CreateToolTip(shift_entry, texts[current_language]['tooltip_text'])

# Prozess-Button
process_button = ttk.Button(main_frame, text=texts[current_language]['process_button'], command=shift_srt)
process_button.grid(row=5, column=0, columnspan=3, pady=10)
process_button.config(state='disabled')

# Statusnachricht
status_label = ttk.Label(main_frame, text="")
status_label.grid(row=6, column=0, columnspan=3)

# Spaltengewichte konfigurieren
root.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

# Eingabevalidierung
file_entry.bind('<KeyRelease>', validate_inputs)
shift_entry.bind('<KeyRelease>', validate_inputs)
output_entry.bind('<KeyRelease>', validate_inputs)
overwrite_var.trace_add('write', lambda *args: validate_inputs())

# Starte die GUI-Ereignisschleife
root.mainloop()
