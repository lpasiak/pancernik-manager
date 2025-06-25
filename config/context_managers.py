def context_menu():
    menu_text = """--------------------------------
Z czym dziś chcesz pracować?
0. Eksportować produkty
1. Rozprawić się z outletami
Akcja: """
    return str(input(menu_text))

def context_menu_export():
    menu_text = """--------------------------------
Skąd chcesz pobrać dane?
1. Shoper
2. Shopify Light
3. Shopify Bizon
4. EasyStorage Pancernik
5. EasyStorage Bizon
6. IdoSell
all. Wszystko powyżej
q żeby wyjść.
Akcja: """
    return str(input(menu_text))

def context_menu_outlet():
    menu_text = """--------------------------------
Co chcesz zrobić?
1. Wystawić outlety
2. Obniżki na outlety
3. Usunąć stare przekierowania
4. Przenieść sprzedane/archiwalne
5. Atrybuty produktów
all. Wszystko powyżej
q żeby wyjść.
Akcja: """
    return str(input(menu_text))