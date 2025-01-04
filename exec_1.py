import pandas as pd
import os
import matplotlib.pyplot as plt

pd.set_option('display.precision', 2)

dtype = {
  'datum': str,
  'uhrzeit_start': str,
  'uhrzeit_ende': str,
  'zaehlstelle': str,
  'richtung_1': 'Int64',
  'richtung_2': 'Int64',
  'gesamt': 'Int64',
  'kommentar': str
}


date_pattern = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
time_pattern = r'[0-9]{2}:[0-9]{2}'


def main():  
  for filename in sorted(os.listdir('data')):
    df = pd.read_csv(f"data/{filename}", dtype=dtype)

    # Überprüfe Datum Spalte auf fehlerhafte Werte
    df = df[df['datum'].str.match(date_pattern)]

    # Überprüfe die Zeit-Spalte auf fehlerhafte Werte
    for column in [df['uhrzeit_start'], df['uhrzeit_ende']]:
      df = df[column.str.match(time_pattern)]
    
    # Filtere die Daten heraus, wo richtung_1, richtung_2 oder gesamt NA als Wert hat
    df = df[df['richtung_1'].notna()]
    df = df[df['richtung_2'].notna()]
    df = df[df['gesamt'].notna()]

    # Filtere Messwerte heraus, die auf den gleichen Zeitintervall verweisen
    df = df[~((df['datum'] == df['uhrzeit_start']) & (df['uhrzeit_start'] == df['uhrzeit_ende']))]

    # Überprüfe, ob gesamt richtung_1 + richtung_2 entspricht
    df = df[(df['richtung_1'] + df['richtung_2']) == df['gesamt']]

    # Deskriptive Statistik

    # Datum: Gibt das Datum des jeweiligen Tages an
    # uhrzeit_start: Gibt die Uhrzeit an, wann die Aufzeichnung der Werte startet
    # uhrzeit_ende: Gibt die Uhrzeit an, wann die Aufzeichnung der Werte endet
    # zaehlstelle: Gibt den Namen der Zählstelle an
    # richtung_1: Gibt die Anzahl an Fahrräder an, die in eine bestimmte Richtung gefahren sind
    # richtung_2: Gibt die Anzahl an Fahrräder an, die in die entgegengesetzte Richtung, wie richtung_1 gefahren sind
    # gesamt: Gibt die Anzahl an Fährräder an, die insgesamt in dem aufgezeichneten Intervall an der jeweiligen Zählstelle vorbeigefahren sind (richtung_1 + richtung_2)
    # min.temp: Gibt die niedrigeste Temperatur, innerhalb des aufgezeichneten Intervalls, an
    # max.temp: Gibt die höchste Temperatur, innerhalb des aufgezeichneten Intervalls, an
    # niederschlag: Gibt die Anzahl an Stunden an, die es innerhalb des aufgezeichneten Intervalls geregnet hat
    # bewoelkung: Gibt in Prozent an, wie lange es bewölkt war innerhalb des aufgezeichneten Intervalls
    # sonnenstunden: Gibt die Anzahl an Sonnenstunden, innerhalb des aufgezeichneten Intervalls, an
    # kommentar: Gibt zusätzliche Informationen, darüber warum eine Zählstelle beispielsweise keine Werte liefert

    if 'tage' in filename:
      print(f"Daten von {filename.split('_')[1]}")
      print(df.describe())
      print('---------------------------------------------------------------------------------------------------')


def get_duplicates(df: pd.DataFrame):
  return df[df.duplicated()]

if __name__ == '__main__':
  main()
