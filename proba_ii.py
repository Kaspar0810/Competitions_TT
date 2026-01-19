import random
from collections import defaultdict

# Исходные данные
athletes = [
    ["Иванов", "Москва", 450],
    ["Петров", "Москва", 435],
    ["Сидоров", "Москва", 429],
    ["Лазарев", "Москва", 480],
    ["Зырянов", "Москва", 520],
    ["Котов", "Свердловская обл.", 272],
    ["Ветров", "Свердловская обл.", 654],
    ["Лаптев", "Свердловская обл.", 320],
    ["Малышев", "Свердловская обл.", 400],
    ["Реутов", "Свердловская обл.", 250],
    ["Пушкин", "Вологодская обл.", 140],
    ["Клюкин", "Вологодская обл.", 300],
    ["Лермонтов", "Вологодская обл.", 290],
    ["Лапшин", "Вологодская обл.", 570],
    ["Стеклов", "Вологодская обл.", 420],
    ["Кротов", "Нижегородская обл.", 240],
    ["Киселев", "Нижегородская обл.", 235],
    ["Гусев", "Нижегородская обл.", 360],
    ["Бондаренко", "Нижегородская обл.", 125],
    ["Романов", "Нижегородская обл.", 255],
    ["Гладышев", "Тюменская обл.", 710],
    ["Павлов", "Тюменская обл.", 390],
    ["Шибаев", "Самарская обл.", 310],
    ["Лукин", "Самарская обл.", 410],
    ["Стоянов", "Оренбургская обл.", 320],
    ["Орлов", "Ивановская обл.", 515],
    ["Ветров", "Ивановская обл.", 110],
    ["Волков", "Иркутская обл.", 310],
    ["Медведев", "Иркутская обл.", 160],
    ["Зайцев", "Иркутская обл.", 260],
    ["Лосев", "Саратовская обл.", 180],
    ["Тихонов", "Кемеровская обл.", 460]
    ]

# Шаг 1: сортировка по рейтингу (по убыванию)
sorted_athletes = sorted(athletes, key=lambda x: x[2], reverse=True)

# Проверим, что их ровно 32
assert len(sorted_athletes) == 32

# Определим четверти
quarters_positions = [
    list(range(0, 8)), # 1-я четверть
    list(range(8, 16)), # 2-я четверть
    list(range(16, 24)), # 3-я четверть
    list(range(24, 32)) # 4-я четверть
    ]

# Функция определения четверти по индексу
def get_quarter(pos):
    if 0 <= pos <= 7:
        return 0
    elif 8 <= pos <= 15:
        return 1
    elif 16 <= pos <= 23:
        return 2
    elif 24 <= pos <= 31:
        return 3
    else:
        raise ValueError("Invalid position")

# Позиции по посевам
seeds_positions = [
    [0, 31], # Посев 1
    [15, 16], # Посев 2
    [7, 8, 23, 24], # Посев 3
    [3, 4, 11, 12, 19, 20, 27, 28], # Посев 4
    list(set(range(32)) - set([0,31,15,16,7,8,23,24,3,4,11,12,19,20,27,28])) # Посев 5
    ]

# Индексы спортсменов по посевам
seeds_athletes_indices = [[0, 1], [2, 3], [4, 5, 6, 7], list(range(8, 16)),list(range(16, 32)) ]

# Инициализация таблицы
table = [None] * 32

# Подсчёт количества спортсменов по регионам
region_counts = defaultdict(int)
for a in sorted_athletes:
    region_counts[a[1]] += 1

# Отслеживание занятых регионов в четвертях
quarters_regions = [set() for _ in range(4)]

def can_place_in_quarter(region, quarter_idx):
    """Проверяет, можно ли разместить спортсмена из региона в четверти."""
    if region_counts[region] > 4:        
        return region not in quarters_regions[quarter_idx]

def place_athlete_in_position(athlete, pos):
    region = athlete[1]
    quarter = get_quarter(pos)
    table[pos] = athlete
    if region_counts[region] <= 4:
        quarters_regions[quarter].add(region)

# Размещение посевов
for seed_idx in range(5):
    positions = seeds_positions[seed_idx][:]
    athletes_to_place = [sorted_athletes[i] for i in seeds_athletes_indices[seed_idx]]

# Перемешиваем позиции и спортсменов для случайности
random.shuffle(positions)
random.shuffle(athletes_to_place)

# Для каждого спортсмена пробуем найти подходящую позицию
for athlete in athletes_to_place:
    region = athlete[1]
    placed = False

# Сначала пробуем позиции в случайном порядке
for pos in positions:
    quarter = get_quarter(pos)
    if can_place_in_quarter(region, quarter):
        place_athlete_in_position(athlete, pos)
        positions.remove(pos)
        placed = True
        break
# Если не получилось — всё равно ставим (на случай >4 спортсменов из региона)
if not placed:
    pos = positions.pop()
    place_athlete_in_position(athlete, pos)

# Вывод результата
print("Таблица жеребьёвки:")
for i, a in enumerate(table):
    print(f"{i+1:2d}: {a[0]} {a[1]}, {a[2]}")