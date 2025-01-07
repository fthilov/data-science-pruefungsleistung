import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

# Pfad zum Datenordner
data_folder = "./data"

# Leere Liste für Daten
all_data = []

# Suche nach Dateien mit "tage" im Namen
for file_name in os.listdir(data_folder):
    if "tage" in file_name and file_name.endswith(".csv"):
        file_path = os.path.join(data_folder, file_name)

        # CSV-Datei einlesen
        try:
            df = pd.read_csv(file_path)

            # Bereinigen: Nur relevante Spalten auswählen
            df = df[["datum", "zaehlstelle", "gesamt"]]

            # Hinzufügen zur Liste
            all_data.append(df)
        except Exception as e:
            print(f"Fehler beim Verarbeiten der Datei {file_name}: {e}")

# Daten zusammenführen
combined_data = pd.concat(all_data, ignore_index=True)

# Datum in datetime umwandeln und Jahr extrahieren
combined_data["datum"] = pd.to_datetime(combined_data["datum"], format="%Y-%m-%d")
combined_data["jahr"] = combined_data["datum"].dt.year

# Gruppieren nach Jahr und Zählstelle, Summieren der "gesamt"-Werte
yearly_data = combined_data.groupby(["jahr", "zaehlstelle"])["gesamt"].sum().reset_index()

# Visualisierung pro Jahr erstellen
for year in yearly_data["jahr"].unique():
    data_for_year = yearly_data[yearly_data["jahr"] == year]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(data_for_year["zaehlstelle"], data_for_year["gesamt"])
    plt.title(f"Fahrradaufkommen pro Zählstelle im Jahr {year}")
    plt.xlabel("Zählstelle")
    plt.ylabel("Gesamtanzahl")
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    # Werte unten im Balken anzeigen
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # X-Position
            5,                                 # Fester Y-Wert (knapp über der Balkenbasis)
            f'{int(height):,}',               # Formatierte Zahl
            ha='center', va='bottom', color='white', fontsize=10, fontweight="bold"
        )

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"./eval_3-1/fahrradaufkommen_{year}.png")  # Optional: Speichere die Grafik
    plt.show()