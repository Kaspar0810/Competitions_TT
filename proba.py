import random
from collections import defaultdict

class Athlete:
    def __init__(self, id, rating, region, coach):
        self.id = id
        self.rating = rating
        self.region = region
        self.coach = coach
        self.group = None
    
    def __repr__(self):
        return f"Athlete({self.id}, rating={self.rating}, region='{self.region}', coach='{self.coach}')"

def create_distribution(athletes):
    # Сортируем спортсменов по рейтингу (от большего к меньшему)
    athletes.sort(key=lambda x: x.rating, reverse=True)
    
    # Создаем 8 групп
    groups = [[] for _ in range(8)]
    
    # Функция для проверки конфликтов в группе
    def has_conflicts(group, athlete):
        group = groups[group_idx]
        regions = [a.region for a in group]
        # coaches = [a.coach for a in group]
        
        # Проверяем, есть ли уже спортсмен из того же региона
        if athlete.region in regions:
            return True
        
        # # Проверяем, есть ли уже спортсмен от того же тренера
        # if athlete.coach in coaches:
        #     return True
            
        # return False
    
    # Базовая распределение без учета конфликтов
    for i in range(4):
        if i % 2 == 0:  # 1-й и 3-й посевы (прямой порядок)
            for j in range(8):
                athlete_index = i * 8 + j
                if athlete_index < len(athletes):
                    groups[j].append(athletes[i * 8 + j])
        else:  # 2-й и 4-й посевы (обратный порядок)
            for j in range(8):
                athlete_index = i * 8 + j
                if athlete_index < len(athletes):
                    # find_best_alternative(current_group_idx, athlete, current_round)
                    groups[7 - j].append(athletes[i * 8 + j])
    
    # Функция для поиска альтернативной группы с минимальным конфликтами
    def find_best_alternative(current_group_idx, athlete, current_round):
        best_group = current_group_idx
        min_conflicts = float('inf')
        
        # Проверяем соседние группы в текущем посеве
        for offset in [-1, 1, -2, 2, -3, 3]:
            test_group = (current_group_idx + offset) % 8
            if 0 <= test_group < 8 and len(groups[test_group]) == current_round:
                if not has_conflicts(groups[test_group], athlete):
                    return test_group
                
                # Считаем конфликты
                conflict_count = sum(1 for a in groups[test_group] 
                                   if a.region == athlete.region or a.coach == athlete.coach)
                if conflict_count < min_conflicts:
                    min_conflicts = conflict_count
                    best_group = test_group
        
        return best_group
    
    # Корректируем распределение для разрешения конфликтов
    for round_num in range(4):
        for group_idx in range(8):
            if len(groups[group_idx]) > round_num:
                athlete = groups[group_idx][round_num]
                
                # Проверяем конфликты в текущей группе
                if has_conflicts(groups[group_idx][:round_num], athlete):
                    # Ищем лучшую альтернативную группу
                    best_alt = find_best_alternative(group_idx, athlete, round_num)
                    
                    if best_alt != group_idx:
                        # Меняем спортсменов местами
                        swap_athlete = groups[best_alt][round_num]
                        groups[group_idx][round_num] = swap_athlete
                        groups[best_alt][round_num] = athlete
    
    return groups

# Пример использования
def main():
    # Создаем тестовые данные
    athletes = []
    regions = ['Москва', 'СПб', 'Казань', 'Екатеринбург', 'Новосибирск', 'Краснодар', 'Владивосток', 'Сочи']
    coaches = ['Иванов', 'Петров', 'Сидоров', 'Кузнецов', 'Смирнов', 'Попов', 'Васильев', 'Соколов']
    
    for i in range(32):
        region = random.choice(regions)
        coach = random.choice(coaches)
        rating = random.randint(1000, 2000)
        athletes.append(Athlete(i+1, rating, region, coach))
    
    # Сортируем по рейтингу для наглядности
    athletes.sort(key=lambda x: x.rating, reverse=True)
    
    print("Список спортсменов (отсортированный по рейтингу):")
    for i, athlete in enumerate(athletes, 1):
        print(f"{i:2d}. ID: {athlete.id:2d}, Рейтинг: {athlete.rating:4d}, "
              f"Регион: {athlete.region:12s}, Тренер: {athlete.coach:8s}")
    
    # Распределяем по группам
    groups = create_distribution(athletes)
    
    print("\n" + "="*80)
    print("ФИНАЛЬНОЕ РАСПРЕДЕЛЕНИЕ ПО ГРУППАМ:")
    print("="*80)
    
    for i, group in enumerate(groups, 1):
        print(f"\nГруппа {i}:")
        print("-" * 40)
        for j, athlete in enumerate(group, 1):
            print(f"  Место {j}: ID {athlete.id:2d}, Рейтинг: {athlete.rating:4d}, "
                  f"Регион: {athlete.region:12s}, Тренер: {athlete.coach:8s}")
    
    # Проверка конфликтов
    print("\n" + "="*80)
    print("ПРОВЕРКА КОНФЛИКТОВ:")
    print("="*80)
    
    has_conflicts = False
    for i, group in enumerate(groups, 1):
        regions_in_group = defaultdict(int)
        coaches_in_group = defaultdict(int)
        
        for athlete in group:
            regions_in_group[athlete.region] += 1
            coaches_in_group[athlete.coach] += 1
        
        region_conflicts = [region for region, count in regions_in_group.items() if count > 1]
        coach_conflicts = [coach for coach, count in coaches_in_group.items() if count > 1]
        
        if region_conflicts or coach_conflicts:
            has_conflicts = True
            print(f"Группа {i} имеет конфликты:")
            if region_conflicts:
                print(f"  Регионы с повторениями: {region_conflicts}")
            if coach_conflicts:
                print(f"  Тренеры с повторениями: {coach_conflicts}")
    
    if not has_conflicts:
        print("Конфликтов не обнаружено!")

if __name__ == "__main__":
    main()