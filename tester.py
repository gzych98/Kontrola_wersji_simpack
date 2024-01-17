import time
import random

def testowy_proces(arguments):
    print(f"Rozpoczynam proces z argumentami: {arguments}")

    # Symulacja trwania procesu (np. 5 sekund)
    time.sleep(5)

    # Symulacja generowania wyniku
    wynik = f"Wynik procesu dla {arguments}: {random.randint(1, 100)}"
    print(wynik)

    return wynik
