numeri = []

print("Inserisci i numeri (scrivi 'fine' per terminare):")

while True:
    ingresso = input("Numero: ")
    
    if ingresso.lower() == 'fine':
        break
    
    try:
        numero = float(ingresso)
        numeri.append(numero)
    except ValueError:
        print("Errore: inserisci un numero valido")

if len(numeri) > 0:
    media = sum(numeri) / len(numeri)
    print(f"\nNumeri inseriti: {numeri}")
    print(f"Media: {media}")
else:
    print("Nessun numero inserito")
