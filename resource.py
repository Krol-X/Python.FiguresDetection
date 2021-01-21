# Служебные константы
NEXT_ID = 100

# Основные константы
STR_CAPTION = "Figures detection app"

ID_SRCIMAGE = 100
ID_NEWIMAGE = 101

# Меню
ID_MENU = 30000

MENU = [
    ["File", "Open", "Save as...", "Exit"],
    ["Image", "Detect figures"]
]

MENU_ID = [
    ["FILE", "OPEN", "SAVEAS", "EXIT"],
    ["IMAGE", "DETECT"]
]

# Генерация ID для элементов меню
for j in range(len(MENU_ID)):
    items = MENU_ID[j]
    for i in range(len(items)):
        exec("ID_" + items[i] + "=" + str(ID_MENU + NEXT_ID * j + i))
