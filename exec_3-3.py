import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

def main():
    data_folder = "./data/cleaned"

    output_folder = "./eval_3-3"
    os.makedirs(output_folder, exist_ok=True)

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

    # Überprüfen, ob Daten vorhanden sind
    if not all_data:
        print("Keine passenden Dateien gefunden oder Daten sind leer.")
        exit()

    # Daten zusammenführen
    combined_data = pd.concat(all_data, ignore_index=True)

    combined_data["datum"] = pd.to_datetime(combined_data["datum"], format="%Y-%m-%d")

    combined_data["jahr"] = combined_data["datum"].dt.year

    summary_data = combined_data.groupby(["jahr", "zaehlstelle"])["gesamt"].sum().reset_index()

    # Visualisierung erstellen
    for zaehlstelle in summary_data["zaehlstelle"].unique():
        data_for_zaehlstelle = summary_data.loc[summary_data["zaehlstelle"] == zaehlstelle].copy()
        data_for_zaehlstelle["wachstumsrate"] = data_for_zaehlstelle["gesamt"].pct_change() * 100
        data_for_zaehlstelle.loc[(data_for_zaehlstelle["wachstumsrate"] > 160) | (data_for_zaehlstelle["wachstumsrate"] < -50), "wachstumsrate"] = None

        fig, ax1 = plt.subplots(figsize=(10, 6))

        bars = ax1.bar(
            data_for_zaehlstelle["jahr"],
            data_for_zaehlstelle["gesamt"],
            color="steelblue"
        )

        ax1.set_xlabel("Jahr")
        ax1.set_ylabel("Gesamtanzahl")
        ax1.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))  # Zahlenformatierung
        ax1.tick_params(axis='y')

        for bar in bars:
            bar_height = bar.get_height()
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                bar_height,
                f'{int(bar_height):,}',
                ha='center', va='bottom', color='black', fontsize=10, fontweight="bold"
            )

        ax2 = ax1.twinx()
        ax2.plot(
            data_for_zaehlstelle["jahr"],
            data_for_zaehlstelle["wachstumsrate"],
            color="darkgreen",
            marker="o",
            label="Wachstumsrate"
        )
        ax2.set_ylabel("Wachstumsrate (%)")
        ax2.tick_params(axis='y')

        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc="upper left")

        plt.title(f"Fahrradaufkommen der Zählstelle {zaehlstelle} mit Wachstumsrate")
        plt.tight_layout()
        plt.savefig(f"./eval_3-3/fahrradaufkommen_{zaehlstelle}.png")
        plt.close()

    # Graph für alle Standorte zusammen
    combined_summary = combined_data.groupby("jahr")["gesamt"].sum().reset_index()
    combined_summary["wachstumsrate"] = combined_summary["gesamt"].pct_change() * 100

    # Durchschnittliche Wachstumsrate der letzten 8 Jahre berechnen
    recent_years = combined_summary.tail(8)
    avg_growth_rate = recent_years["wachstumsrate"].mean()

    fig, ax1 = plt.subplots(figsize=(10, 6))

    bars = ax1.bar(
        combined_summary["jahr"],
        combined_summary["gesamt"],
        color="darkorange",
        label="Gesamtanzahl"
    )
    ax1.set_xlabel("Jahr")
    ax1.set_ylabel("Gesamtanzahl")
    ax1.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))  # Zahlenformatierung
    ax1.tick_params(axis='y')

    for bar in bars:
        bar_height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar_height,
            f'{int(bar_height):,}',
            ha='center', va='bottom', color='black', fontsize=10, fontweight="bold"
        )

    ax2 = ax1.twinx()
    ax2.plot(
        combined_summary["jahr"],
        combined_summary["wachstumsrate"],
        color="blue",
        marker="o",
        label="Wachstumsrate"
    )
    ax2.set_ylabel("Wachstumsrate (%)")
    ax2.tick_params(axis='y')

    # Durchschnittliche Wachstumsrate als horizontale Linie anzeigen
    ax2.axhline(y=avg_growth_rate, color='red', linestyle='--', linewidth=2, label=f'Durchschnitt letzte 8 Jahre: {avg_growth_rate:.2f}%', alpha=1.0)

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="upper left")

    plt.title("Gesamtes Fahrradaufkommen aller Zählstellen mit Wachstumsrate")
    plt.tight_layout()
    plt.savefig(f"./eval_3-3/gesamt_fahrradaufkommen_mit_wachstumsrate.png")
    plt.close()

    # Graph für Gesamtanzahl pro Zählstelle
    total_per_zaehlstelle = combined_data.groupby("zaehlstelle")[["gesamt"]].sum().reset_index().sort_values(by="gesamt", ascending=False)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        total_per_zaehlstelle["zaehlstelle"],
        total_per_zaehlstelle["gesamt"],
        color="seagreen"
    )

    plt.title("Gesamtanzahl pro Zählstelle")
    plt.xlabel("Zählstelle")
    plt.ylabel("Gesamtanzahl")
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))  # Zahlenformatierung

    for bar in bars:
        bar_height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar_height,
            f'{int(bar_height):,}',
            ha='center', va='bottom', color='black', fontsize=10, fontweight="bold"
        )

    plt.tight_layout()
    plt.savefig(f"./eval_3-3/gesamtanzahl_pro_zaehlstelle.png")
    plt.close()

if __name__ == '__main__':
    main()
