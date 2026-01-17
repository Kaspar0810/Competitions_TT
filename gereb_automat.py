import random
from typing import List, Dict, Tuple, Optional

class Sportsman:
    def __init__(self, id: int, region: str, rating: int):
        self.id = id
        self.region = region
        self.rating = rating

class TournamentDraw:
    def __init__(self):
    # Таблица на 32 позиции (индексы 0-31, но отображаем как 1-32)
        self.table = [None] * 32

        # Определяем четверти
        self.quarters = {
        1: list(range(0, 8)), # номера 1-8
        2: list(range(8, 16)), # номера 9-16
        3: list(range(16, 24)), # номера 17-24
        4: list(range(24, 32)) # номера 25-32
        }

        # Определяем посевы (номера в таблице, начиная с 0)
        self.seeds = {
        1: [0, 31], # 1 и 32
        2: [15, 16], # 16 и 17
        3: [7, 8, 23, 24], # 8, 9, 24, 25
        4: [3, 4, 11, 12, 19, 20, 27, 28], # 4, 5, 12, 13, 20, 21, 28, 29
        5: [i for i in range(32) if i not in [0, 31, 15, 16, 7, 8, 23, 24, 3, 4, 11, 12, 19, 20, 27, 28]]
        }

        # Половины таблицы
        self.halves = {
        'верхняя': list(range(0, 16)), # номера 1-16
        'нижняя': list(range(16, 32)) # номера 17-32
        }

        # Для отслеживания распределения регионов по четвертям
        self.region_quarters: Dict[str, List[int]] = {}
        self.region_counts: Dict[str, int] = {}

def generate_sportsmen(self) -> List[Sportsman]:
    """Генерация тестовых данных спортсменов"""
    regions = ['Москва'] * 5 + ['Нижегородская область'] * 5 + \
    ['Свердловская область'] * 3 + ['Ярославская область'] * 4

    # Остальные из случайных регионов
    other_regions = ['Республика Татарстан', 'Краснодарский край',
    'Санкт-Петербург', 'Новосибирская область', 'Ростовская область',
    'Республика Башкортостан', 'Пермский край', 'Самарская область']

    regions += [random.choice(other_regions) for _ in range(32 - len(regions))]

    # Сортировка по убыванию рейтинга (от сильного к слабому)
    sportsmen = []
    for i in range(32):
        # Генерация рейтинга от 1000 до 2000 с убыванием
        rating = 2000 - i * 30 + random.randint(-50, 50)
        sportsmen.append(Sportsman(i + 1, regions[i], rating))

    return sorted(sportsmen, key=lambda x: x.rating, reverse=True)

def get_quarter_for_position(self, position: int) -> int:
    """Определить четверть для позиции в таблице"""
    for quarter, positions in self.quarters.items():
        if position in positions:
            return quarter
    return 0

def can_place_in_quarter(self, region: str, quarter: int) -> bool:
    """Можно ли разместить спортсмена из региона в указанной четверти"""
    if region not in self.region_quarters:
        return True

    # Если регион уже есть в этой четверти, проверяем количество
    quarters_with_region = self.region_quarters[region]
    if quarter in quarters_with_region:
    # Проверяем, сколько уже спортсменов этого региона в четверти
        count_in_quarter = quarters_with_region.count(quarter)
        return count_in_quarter < 1 # Не более 1 на четверть для первых 4 спортсменов

    return True

def update_region_tracking(self, region: str, position: int):
    """Обновить отслеживание распределения регионов"""
    quarter = self.get_quarter_for_position(position)

    if region not in self.region_quarters:
        self.region_quarters[region] = []
        self.region_counts[region] = 0

        self.region_quarters[region].append(quarter)
        self.region_counts[region] += 1

def place_sportsmen(self, sportsmen: List[Sportsman], seed: int, seed_positions: List[int]):
    """Разместить спортсменов на позиции посева"""
    # Количество спортсменов в этом посеве
    num_sportsmen = len(seed_positions)

    # Если это 1-й посев (фиксированное размещение)
    if seed == 1:
        self.table[seed_positions[0]] = sportsmen[0] # Самый сильный
        self.table[seed_positions[1]] = sportsmen[1] # Второй по силе
        self.update_region_tracking(sportsmen[0].region, seed_positions[0])
        self.update_region_tracking(sportsmen[1].region, seed_positions[1])
        return sportsmen[2:]

    # Для остальных посевов
    sportsmen_to_place = sportsmen[:num_sportsmen]
    remaining_sportsmen = sportsmen[num_sportsmen:]

    # Перемешиваем позиции для случайного распределения
    random.shuffle(seed_positions)

    # Пытаемся разместить с учетом ограничений
    placed = [False] * num_sportsmen

    for attempt in range(100): # Максимум 100 попыток
        all_placed = True

    for i, sportsman in enumerate(sportsmen_to_place):
        if placed[i]:
            continue

    # Проверяем доступные позиции для этого спортсмена
    available_positions = []

    for pos in seed_positions:
        if self.table[pos] is not None:
            continue

        quarter = self.get_quarter_for_position(pos)

        # Проверяем ограничения по регионам
        if self.region_counts.get(sportsman.region, 0) < 4:
            # Для первых 4 спортсменов региона - ограничение по четвертям
            if not self.can_place_in_quarter(sportsman.region, quarter):
                continue

        # Для 2-го посева проверяем разные половины для спортсменов из одного региона
        if seed == 2 and len(sportsmen_to_place) == 2:
            other_idx = 0 if i == 1 else 1
            other_sportsman = sportsmen_to_place[other_idx]

        if sportsman.region == other_sportsman.region:
            # Определяем половину позиции
            half = 'верхняя' if pos < 16 else 'нижняя'

        # Ищем позицию в другой половине для второго спортсмена
        if placed[other_idx]:
            # Если другой уже размещен, проверяем, что этот в другой половине
            other_pos = seed_positions[other_idx]
        if (pos < 16 and other_pos < 16) or (pos >= 16 and other_pos >= 16):
            continue

        available_positions.append(pos)

        if available_positions:
            # Выбираем позицию
            chosen_pos = random.choice(available_positions)
            self.table[chosen_pos] = sportsman
            self.update_region_tracking(sportsman.region, chosen_pos)
            placed[i] = True
        else:
            all_placed = False

        if all_placed:
            break

        # Если не все размещены, сбрасываем и пробуем снова
        if not all_placed and attempt < 99:
            for i, pos in enumerate(seed_positions):
                if placed[i]:
                    sportsman = self.table[pos]
        if sportsman:
            # Удаляем из отслеживания
            region  = sportsman.region
        quarter = self.get_quarter_for_position(pos)
        if region in self.region_quarters and quarter in self.region_quarters[region]:
            self.region_quarters[region].remove(quarter)
            self.region_counts[region] -= 1
            self.table[pos] = None
            placed = [False] * num_sportsmen
            random.shuffle(seed_positions)

    return remaining_sportsmen

def draw(self) -> List[Optional[Sportsman]]:
    """Провести жеребьевку"""
    # Генерация спортсменов
    sportsmen = self.generate_sportsmen()

    print("Спортсмены (отсортированы по рейтингу):")
    for i, s in enumerate(sportsmen, 1):
        print(f"{i:2d}. ID: {s.id:2d}, Регион: {s.region:25s}, Рейтинг: {s.rating}")
    print()

    # Посевная жеребьевка
    remaining_sportsmen = sportsmen

    for seed_num in range(1, 6):
        seed_positions = self.seeds[seed_num]
    print(f"Посев {seed_num} (позиции {[p+1 for p in seed_positions]}):")

    remaining_sportsmen = self.place_sportsmen(
    remaining_sportsmen, seed_num, seed_positions.copy()
    )

    # Выводим размещение для этого посева
    for pos in seed_positions:
        if self.table[pos]:
            print(f" Позиция {pos+1:2d}: {self.table[pos].region:25s} (ID: {self.table[pos].id:2d})")
    print()

    return self.table

def print_draw(self):
    """Вывести итоговую таблицу жеребьевки"""
    print("\n" + "="*70)
    print("ИТОГОВАЯ ТАБЛИЦА ЖЕРЕБЬЕВКИ")
    print("="*70)

    for i in range(32):
        s = self.table[i]
        if s:
            quarter = self.get_quarter_for_position(i)
            print(f"Позиция {i+1:2d} (четверть {quarter}): "
            f"ID: {s.id:2d}, Регион: {s.region:25s}, Рейтинг: {s.rating}")
        else:
            print(f"Позиция {i+1:2d}: ПУСТО")

    print("\n" + "="*70)
    print("РАСПРЕДЕЛЕНИЕ ПО ЧЕТВЕРТЯМ:")
    print("="*70)

    # Анализ распределения
    region_analysis: Dict[str, Dict[int, int]] = {}

    for i, s in enumerate(self.table):
        if s:
            quarter = self.get_quarter_for_position(i)
        if s.region not in region_analysis:
            region_analysis[s.region] = {1: 0, 2: 0, 3: 0, 4: 0}
            region_analysis[s.region][quarter] += 1

    for region, quarters in region_analysis.items():
        total = sum(quarters.values())
        quarters_str = ', '.join([f"{q}:{count}" for q, count in quarters.items()])
        print(f"{region:30s} - всего {total:2d}: [{quarters_str}]")

    # Запуск жеребьевки
if __name__ == "__main__":
    tournament = TournamentDraw()
    draw()# tournament.draw()
    tournament.print_draw()
    # ```

# Пояснение алгоритма:

# 1. Структура данных:

# · Sportsman - класс спортсмена с ID, регионом и рейтингом
# · TournamentDraw - основной класс для жеребьевки

# 2. Ключевые элементы:

# · Четверти: 1-8, 9-16, 17-24, 25-32
# · Посевы: 5 уровней распределения позиций
# · Половины таблицы: верхняя (1-16) и нижняя (17-32)

# 3. Алгоритм жеребьевки:

# 1. Генерация 32 спортсменов с разными регионами и рейтингами
# 2. Сортировка по рейтингу (от сильного к слабому)
# 3. Последовательное размещение по посевам:
# · 1-й посев: фиксированное размещение самых сильных
# · 2-й посев: случайное распределение с проверкой половин для одинаковых регионов
# · 3-й посев: случайное распределение по 4 позициям
# · 4-й и 5-й посевы: размещение с учетом ограничений по четвертям

# 4. Ограничения:

# · Первые 4 спортсмена из одного региона должны быть в разных четвертях
# · Во 2-м посеве спортсмены из одного региона должны попасть в разные половины
# · Если региона больше 4 спортсменов, ограничения снимаются

# 5. Особенности реализации:

# · Используется backtracking (повторные попытки) при невозможности размещения
# · Ведется учет распределения регионов по четвертям
# · Случайность обеспечивается random.shuffle()

