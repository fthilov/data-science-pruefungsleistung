import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter


def main():
    data_folder = "./data/cleaned"

    all_data = []

    for file_name in os.listdir(data_folder):
        if "tage" in file_name and file_name.endswith(".csv"):
            file_path = os.path.join(data_folder, file_name)

            try:
                df = pd.read_csv(file_path)

                df = df[["datum", "zaehlstelle", "gesamt"]]

                all_data.append(df)
            except Exception as e:
                print(f"Fehler beim Verarbeiten der Datei {file_name}: {e}")

    # Daten zusammenführen
    combined_data = pd.concat(all_data, ignore_index=True)

    combined_data["datum"] = pd.to_datetime(combined_data["datum"], format="%Y-%m-%d")
    combined_data["jahr"] = combined_data["datum"].dt.year

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

        # Berechne den unteren Rand der y-Achse
        ylim_bottom, ylim_top = plt.gca().get_ylim()

        # Feste Y-Position für die Zahlen in den Balken
        fixed_y_position = ylim_bottom + (ylim_top - ylim_bottom) * 0.05  # 5% vom unteren Rand der y-Achse

        # Werte unten im Balken anzeigen
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,  # X-Position
                fixed_y_position,                                 # Fester Y-Wert (knapp über der Balkenbasis)
                f'{int(height):,}',               # Formatierte Zahl
                ha='center', va='bottom', color='black', fontsize=10, fontweight="bold"
            )

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"./eval_3-1/fahrradaufkommen_{year}.png")
        plt.close()

if __name__ == '__main__':
  main()