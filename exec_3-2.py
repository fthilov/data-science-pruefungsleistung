import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

data_folder = "./data/cleaned"

all_data = []

for file_name in os.listdir(data_folder):
    if "tage" in file_name and file_name.endswith(".csv"):
        file_path = os.path.join(data_folder, file_name)

        try:
            df = pd.read_csv(file_path)

            df = df[["datum", "gesamt"]]

            all_data.append(df)
        except Exception as e:
            print(f"Fehler beim Verarbeiten der Datei {file_name}: {e}")


# Alle Daten zusammenführen
combined_data = pd.concat(all_data, ignore_index=True)

combined_data["datum"] = pd.to_datetime(combined_data["datum"], format="%Y-%m-%d")

combined_data["jahr"] = combined_data["datum"].dt.year
combined_data["quartal"] = combined_data["datum"].dt.quarter

quarterly_data = combined_data.groupby(["jahr", "quartal"])["gesamt"].sum().reset_index()

# Visualisierung pro Jahr
for year in quarterly_data["jahr"].unique():
    data_for_year = quarterly_data[quarterly_data["jahr"] == year]
    quartals = data_for_year["quartal"]
    values = data_for_year["gesamt"]

    # Dynamische Beschriftungen
    tick_labels = [f"Q{int(q)}" for q in quartals]

    plt.figure(figsize=(8, 6))
    bars = plt.bar(quartals, values, color="steelblue", tick_label=tick_labels)
    plt.title(f"Fahrradaufkommen pro Quartal im Jahr {year}")
    plt.xlabel("Quartale")
    plt.ylabel("Gesamtanzahl")
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    ylim_bottom, ylim_top = plt.gca().get_ylim()

    # Feste Y-Position für die Zahlen in den Balken
    fixed_y_position = ylim_bottom + (ylim_top - ylim_bottom) * 0.05  # 5% vom unteren Rand der y-Achse

    # Werte in den Balken anzeigen
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # X-Position
            fixed_y_position,
            f'{int(height):,}',  # Formatierte Zahl
            ha='center', va='bottom', color='black', fontsize=10, fontweight="bold"
        )

    plt.tight_layout()
    plt.savefig(f"./eval_3-2/quartal{year}.png")  # Optional: Speichere die Grafik
    plt.close()