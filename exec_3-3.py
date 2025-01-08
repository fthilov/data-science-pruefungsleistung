import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

data_folder = "./data/initial"

output_folder = "./eval_3-3"
os.makedirs(output_folder, exist_ok=True)

all_data = []

for file_name in os.listdir(data_folder):
    if "tage" in file_name and file_name.endswith(".csv"):
        file_path = os.path.join(data_folder, file_name)

        try:
            df = pd.read_csv(file_path)

            df = df[["datum", "zaehlstelle", "gesamt"]]

            df["datum"] = pd.to_datetime(df["datum"], format="%Y-%m-%d")
            df = df.dropna(subset=["gesamt"])
            all_data.append(df)
        except Exception as e:
            print(f"Fehler beim Verarbeiten der Datei {file_name}: {e}")

# Überprüfen, ob Daten vorhanden sind
if not all_data:
    print("Keine passenden Dateien gefunden oder Daten sind leer.")
    exit()

# Daten zusammenführen
combined_data = pd.concat(all_data, ignore_index=True)

# Jahr extrahieren
combined_data["jahr"] = combined_data["datum"].dt.year

# Gruppieren nach Jahr und Zählstelle und Summieren der "gesamt"-Werte
summary_data = combined_data.groupby(["jahr", "zaehlstelle"])["gesamt"].sum().reset_index()

# Visualisierung erstellen
for zaehlstelle in summary_data["zaehlstelle"].unique():
    data_for_zaehlstelle = summary_data[summary_data["zaehlstelle"] == zaehlstelle]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        data_for_zaehlstelle["jahr"],
        data_for_zaehlstelle["gesamt"],
        color="steelblue"
    )

    # Titel und Achsenbeschriftung
    plt.title(f"Fahrradaufkommen der Zählstelle {zaehlstelle}")
    plt.xlabel("Jahr")
    plt.ylabel("Gesamtanzahl")
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))  # Zahlenformatierung

    # Werte in den Balken anzeigen (senkrecht)
    # Berechne den unteren Rand der y-Achse
    ylim_bottom, ylim_top = plt.gca().get_ylim()

    # Feste Y-Position für die Zahlen in den Balken
    fixed_y_position = ylim_bottom + (ylim_top - ylim_bottom) * 0.05  # 5% vom unteren Rand der y-Achse

    # Werte in den Balken anzeigen (auf gleicher Höhe)
    for bar in bars:
        bar_height = bar.get_height()  # Höhe des Balkens
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # X-Position
            fixed_y_position,  # Feste Y-Position
            f'{int(bar_height):,}',  # Formatierte Zahl
            ha='center', va='bottom', color='black', fontsize=10, fontweight="bold", rotation=90
        )

    # Layout anpassen
    plt.tight_layout()

    plt.savefig(f"./eval_3-3/fahrradaufkommen_{zaehlstelle}.png")
    plt.close()  # Verhindert das Öffnen vieler Fenster