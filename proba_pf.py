import random
from peewee import *

# Подключение к базе данных
db = MySQLDatabase('your_database', user='your_user', password='your_password', host='localhost')

# Определение моделей
class Choice(Model):
    family = CharField()  # фамилия имя/регион
    region = CharField()  # регион
    group = CharField()   # группа в предварительном этапе (например, "1 группа")
    mesto_group = IntegerField()  # занятое место в предварительном этапе
    semi_final = IntegerField(null=True)  # номер полуфинала (1 или 2)
    sf_group = CharField(null=True)  # группа в полуфинале (например, "1 группа")
    posev_sf = IntegerField(null=True)  # порядковый номер в группе полуфинала
    
    class Meta:
        database = db
        table_name = 'Choice'

class Result(Model):
    system_stage = CharField(null=True)  # этап соревнований (1-й полуфинал, 2-й полуфинал)
    number_group = CharField(null=True)  # номер группы в полуфинале
    tours = CharField(null=True)  # номера игроков, которые встречаются (1-2, 3-4 и т.д.)
    player1 = CharField()  # фамилия имя/регион первого игрока
    player2 = CharField()  # фамилия имя/регион второго игрока
    winner = CharField(null=True)  # победитель
    points_win = IntegerField(default=2, null=True)  # очки победителя
    score_in_game = CharField(null=True)  # счет в игре (например, "3:0")
    score_win = CharField(null=True)  # забитые очки победителя (например, "3,7,6")
    loser = CharField(null=True)  # проигравший
    points_loser = IntegerField(default=1, null=True)  # очки проигравшего
    score_loser = CharField(null=True)  # счет проигравшего (например, "0:3")
    
    class Meta:
        database = db
        table_name = 'Result'

# Создание таблиц (если не существуют)
db.connect()
db.create_tables([Choice, Result], safe=True)

def get_players_by_group_and_place(group_num, places):
    """
    Получение игроков из указанной группы по местам
    group_num: номер группы (1-32)
    places: список мест (например, [1, 2])
    """
    group_name = f"{group_num} группа"
    players = []
    for place in places:
        player = Choice.select().where(
            (Choice.group == group_name) & (Choice.mesto_group == place)
        ).first()
        if player:
            players.append(player)
    return players

def create_semi_final_1():
    """
    Создание групп 1-го полуфинала
    Игроки с 1-2 мест из групп 1-16 и 17-32 образуют 16 групп
    """
    print("="*60)
    print("1-Й ПОЛУФИНАЛ")
    print("="*60)
    print("Начинаем формирование 1-го полуфинала...")
    
    # Шаг 1: Берем игроков с 1-2 мест из групп 1-16 (они будут на 1-2 позициях)
    groups_1_16 = []
    for group_num in range(1, 17):
        players = get_players_by_group_and_place(group_num, [1, 2])
        if len(players) == 2:
            groups_1_16.append({
                'group_num': group_num,
                'players': players
            })
            print(f"  Группа {group_num}: 1-е место - {players[0].family} ({players[0].region}), 2-е место - {players[1].family} ({players[1].region})")
    
    # Шаг 2: Создаем список игроков из групп 17-32 для распределения (3-4 позиции)
    groups_17_32 = []
    for group_num in range(17, 33):
        players = get_players_by_group_and_place(group_num, [1, 2])
        if len(players) == 2:
            groups_17_32.append({
                'group_num': group_num,
                'players': players
            })
    
    print(f"\nГруппы 17-32 для распределения:")
    for g in groups_17_32:
        print(f"  Группа {g['group_num']}: 1-е место - {g['players'][0].family} ({g['players'][0].region}), 2-е место - {g['players'][1].family} ({g['players'][1].region})")
    
    # Шаг 3: Распределяем группы 17-32 к группам 1-16 с учетом регионов
    sf_groups = []
    
    for idx in range(16):
        group_1_16 = groups_1_16[idx]
        source_idx = 15 - idx
        if source_idx >= 0 and source_idx < len(groups_17_32):
            group_17_32 = groups_17_32[source_idx]
        else:
            continue
        
        print(f"\nФормируем группу {idx+1} из групп {group_1_16['group_num']} и {group_17_32['group_num']}")
        
        # Проверяем регионы первых мест
        first_place_1_16 = group_1_16['players'][0]
        first_place_17_32 = group_17_32['players'][0]
        
        # Если регионы совпадают, ищем другую группу
        if first_place_1_16.region == first_place_17_32.region:
            print(f"  СОВПАДЕНИЕ РЕГИОНОВ: {first_place_1_16.region}")
            
            found = False
            for offset in range(1, 16):
                new_idx = source_idx + offset
                if new_idx < len(groups_17_32):
                    candidate_group = groups_17_32[new_idx]
                    candidate_first = candidate_group['players'][0]
                    
                    if first_place_1_16.region != candidate_first.region:
                        print(f"  Найдена подходящая группа {candidate_group['group_num']}")
                        group_17_32 = candidate_group
                        found = True
                        break
            
            if not found:
                print(f"  Не найдено подходящей группы, оставляем как есть")
        
        sf_group = {
            'sf_group_num': idx + 1,
            'players': [
                group_1_16['players'][0],
                group_1_16['players'][1],
                group_17_32['players'][0],
                group_17_32['players'][1]
            ]
        }
        sf_groups.append(sf_group)
        
        print(f"  Сформирована группа {idx+1}:")
        for i, p in enumerate(sf_group['players'], 1):
            print(f"    {i}. {p.family} ({p.region})")
    
    # Заполняем данные в таблице Choice
    for sf_group in sf_groups:
        for idx, player in enumerate(sf_group['players'], 1):
            player.semi_final = 1
            player.sf_group = f"{sf_group['sf_group_num']} группа"
            player.posev_sf = idx
            player.save()
    
    print(f"\nИТОГО: Сформировано {len(sf_groups)} групп 1-го полуфинала")
    return sf_groups

def create_semi_final_2():
    """
    Создание групп 2-го полуфинала по 5-ти этапной схеме
    """
    print("\n" + "="*60)
    print("2-Й ПОЛУФИНАЛ")
    print("="*60)
    
    # ============ 1-й ЭТАП: Создаем 16 групп из 3-4 мест групп 1-16 ============
    print("\n--- 1-й ЭТАП: Создание 16 групп из 3-4 мест групп 1-16 ---")
    
    # Собираем игроков с 3-4 мест из групп 1-16
    groups_1_16_players = []
    for group_num in range(1, 17):
        players = get_players_by_group_and_place(group_num, [3, 4])
        groups_1_16_players.append({
            'group_num': group_num,
            'players': players
        })
        if players:
            print(f"  Группа {group_num}: {len(players)} игроков")
            for p in players:
                print(f"    - {p.family} ({p.region}) - {p.mesto_group} место")
    
    # Создаем 16 групп по принципу 1+16, 2+15, 3+14 и т.д.
    sf2_groups = []
    for i in range(1, 17):
        group1_num = i
        group2_num = 17 - i
        
        players1 = groups_1_16_players[group1_num - 1]['players']
        players2 = groups_1_16_players[group2_num - 1]['players']
        
        all_players = players1 + players2
        
        sf2_groups.append({
            'sf_group_num': i,
            'players': all_players,
            'from_groups': [group1_num, group2_num]
        })
    
    print(f"\nСоздано {len(sf2_groups)} групп:")
    for group in sf2_groups:
        print(f"  Группа {group['sf_group_num']}: {len(group['players'])} игроков (из групп {group['from_groups']})")
    
    # ============ 2-й, 3-й, 4-й ЭТАПЫ: Добавляем игроков из групп 17-32 ============
    print("\n--- 2-й, 3-й, 4-й ЭТАПЫ: Добавление игроков из групп 17-32 ---")
    
    # Собираем игроков с 3-4 мест из групп 17-32
    groups_17_32_players = []
    for group_num in range(17, 33):
        players = get_players_by_group_and_place(group_num, [3, 4])
        if players:
            groups_17_32_players.append({
                'group_num': group_num,
                'players': players
            })
    
    print(f"\nИгроки из групп 17-32 для добавления:")
    for g in groups_17_32_players:
        print(f"  Группа {g['group_num']}: {len(g['players'])} игроков")
        for p in g['players']:
            print(f"    - {p.family} ({p.region}) - {p.mesto_group} место")
    
    # Список для отслеживания обработанных групп 17-32
    processed_groups = set()
    skipped_groups = []
    
    # Проходим по группам 17-32 в порядке возрастания
    for source_group in groups_17_32_players:
        source_group_num = source_group['group_num']
        
        # Определяем целевую группу полуфинала (17→16, 18→15, 19→14 и т.д.)
        target_group_num = 33 - source_group_num
        
        print(f"\n--- Обработка группы {source_group_num} (целевая группа {target_group_num}) ---")
        print(f"  Игроки для добавления: {[p.family for p in source_group['players']]}")
        
        # Находим целевую группу полуфинала
        target_group = None
        for g in sf2_groups:
            if g['sf_group_num'] == target_group_num:
                target_group = g
                break
        
        if target_group:
            # Проверяем текущее количество игроков в целевой группе
            current_count = len(target_group['players'])
            new_count = current_count + len(source_group['players'])
            
            print(f"  Текущее количество в группе {target_group_num}: {current_count}")
            print(f"  После добавления будет: {new_count}")
            
            if new_count >= 3:
                # Если после добавления будет 3 или более игроков, добавляем
                print(f"  ✓ Добавляем игроков в группу {target_group_num}")
                target_group['players'].extend(source_group['players'])
                target_group['from_groups'].append(source_group_num)
                processed_groups.add(source_group_num)
            else:
                # Если менее 3, ищем группу выше для перемещения
                print(f"  ✗ После добавления будет {new_count} игроков (<3)")
                print(f"  Ищем группу выше для перемещения...")
                
                # Ищем группу с меньшим номером (выше по порядку)
                found = False
                for check_group_num in range(target_group_num - 1, 0, -1):
                    # Находим группу для проверки
                    check_group = None
                    for g in sf2_groups:
                        if g['sf_group_num'] == check_group_num:
                            check_group = g
                            break
                    
                    if check_group:
                        check_count = len(check_group['players'])
                        new_check_count = check_count + len(source_group['players'])
                        
                        print(f"    Проверяем группу {check_group_num}: текущее {check_count}, после добавления {new_check_count}")
                        
                        if new_check_count >= 3:
                            print(f"    ✓ Добавляем игроков в группу {check_group_num}")
                            check_group['players'].extend(source_group['players'])
                            check_group['from_groups'].append(source_group_num)
                            processed_groups.add(source_group_num)
                            found = True
                            break
                        else:
                            print(f"    ✗ В группе {check_group_num} после добавления будет {new_check_count} (<3)")
                            # Продолжаем искать выше
                            continue
                
                if not found:
                    # Если не нашли подходящую группу, добавляем в самую нижнюю возможную
                    print(f"  Не найдено подходящей группы выше, добавляем в группу {target_group_num}")
                    target_group['players'].extend(source_group['players'])
                    target_group['from_groups'].append(source_group_num)
                    processed_groups.add(source_group_num)
                    skipped_groups.append(source_group_num)
    
    # ============ 5-й ЭТАП: Заполняем группы и создаем встречи ============
    print("\n--- 5-й ЭТАП: Финальное формирование групп ---")
    
    # Сортируем группы по номеру
    sf2_groups.sort(key=lambda x: x['sf_group_num'])
    
    print("\nИТОГОВЫЕ ГРУППЫ 2-ГО ПОЛУФИНАЛА:")
    for group in sf2_groups:
        print(f"\nГруппа {group['sf_group_num']}: {len(group['players'])} игроков")
        print(f"  Исходные группы: {group['from_groups']}")
        for idx, player in enumerate(group['players'], 1):
            print(f"  {idx}. {player.family} ({player.region}) - {player.mesto_group} место из группы {player.group}")
    
    # Заполняем данные в таблице Choice
    for sf_group in sf2_groups:
        for idx, player in enumerate(sf_group['players'], 1):
            player.semi_final = 2
            player.sf_group = f"{sf_group['sf_group_num']} группа"
            player.posev_sf = idx
            player.save()
    
    print(f"\nИТОГО: Сформировано {len(sf2_groups)} групп 2-го полуфинала")
    
    return sf2_groups

def create_matches_for_semi_final(semi_final_num, sf_groups):
    """
    Создание встреч для групп полуфинала
    """
    print(f"\n" + "="*60)
    print(f"СОЗДАНИЕ ВСТРЕЧ ДЛЯ {semi_final_num}-ГО ПОЛУФИНАЛА")
    print("="*60)
    
    # Туры для разного количества игроков
    tours_mapping = {
        4: ['1-2', '3-4', '1-4', '2-3', '1-3', '2-4'],
        3: ['1-2', '1-3', '2-3'],
        2: ['1-2']
    }
    
    matches_created = 0
    
    for sf_group in sf_groups:
        group_name = f"{sf_group['sf_group_num']} группа"
        players = sf_group['players']
        num_players = len(players)
        
        print(f"\nГруппа {group_name} ({num_players} игроков):")
        
        tours = tours_mapping.get(num_players, [])
        
        for tour in tours:
            positions = tour.split('-')
            pos1 = int(positions[0])
            pos2 = int(positions[1])
            
            if pos1 <= num_players and pos2 <= num_players:
                player1 = players[pos1 - 1]
                player2 = players[pos2 - 1]
                
                # Проверяем, играли ли эти игроки в предварительном этапе
                previous_match = Result.select().where(
                    ((Result.player1 == player1.family) & (Result.player2 == player2.family)) |
                    ((Result.player1 == player2.family) & (Result.player2 == player1.family))
                ).first()
                
                if previous_match and previous_match.winner:
                    # Копируем результаты предыдущей встречи
                    Result.create(
                        system_stage=f"{semi_final_num}-й полуфинал",
                        number_group=group_name,
                        tours=tour,
                        player1=player1.family,
                        player2=player2.family,
                        winner=previous_match.winner,
                        points_win=previous_match.points_win,
                        score_in_game=previous_match.score_in_game,
                        score_win=previous_match.score_win,
                        loser=previous_match.loser,
                        points_loser=previous_match.points_loser,
                        score_loser=previous_match.score_loser
                    )
                    print(f"  {tour}: {player1.family} - {player2.family} (результат перенесен из предварительного этапа)")
                else:
                    # Создаем пустую встречу
                    Result.create(
                        system_stage=f"{semi_final_num}-й полуфинал",
                        number_group=group_name,
                        tours=tour,
                        player1=player1.family,
                        player2=player2.family
                    )
                    print(f"  {tour}: {player1.family} - {player2.family} (новая встреча)")
                matches_created += 1
    
    print(f"\nИТОГО: Создано {matches_created} встреч для {semi_final_num}-го полуфинала")

def transfer_matches_from_previous_stage():
    """
    Перенос результатов встреч, сыгранных в предварительном этапе
    """
    print("\n" + "="*60)
    print("ПЕРЕНОС РЕЗУЛЬТАТОВ ИЗ ПРЕДВАРИТЕЛЬНОГО ЭТАПА")
    print("="*60)
    
    semi_matches = Result.select().where(Result.system_stage.is_null(False))
    transferred_count = 0
    
    for match in semi_matches:
        if match.tours in ['1-2', '3-4'] and not match.winner:
            previous_match = Result.select().where(
                ((Result.player1 == match.player1) & (Result.player2 == match.player2)) |
                ((Result.player1 == match.player2) & (Result.player2 == match.player1))
            ).where(Result.system_stage.is_null()).first()
            
            if previous_match and previous_match.winner:
                match.winner = previous_match.winner
                match.points_win = previous_match.points_win
                match.score_in_game = previous_match.score_in_game
                match.score_win = previous_match.score_win
                match.loser = previous_match.loser
                match.points_loser = previous_match.points_loser
                match.score_loser = previous_match.score_loser
                match.save()
                transferred_count += 1
                print(f"Перенесен результат: {match.player1} - {match.player2} -> {match.winner}")
    
    print(f"\nИТОГО: Перенесено результатов: {transferred_count}")

def print_final_statistics():
    """
    Вывод финальной статистики
    """
    print("\n" + "="*60)
    print("ФИНАЛЬНАЯ СТАТИСТИКА")
    print("="*60)
    
    for semi_final in [1, 2]:
        players = Choice.select().where(Choice.semi_final == semi_final)
        groups = players.distinct(Choice.sf_group)
        
        print(f"\n{semi_final}-й полуфинал:")
        print(f"  Всего игроков: {players.count()}")
        print(f"  Всего групп: {groups.count()}")
        
        groups_list = list(groups)
        groups_list.sort(key=lambda x: int(x.sf_group.split()[0]))
        
        min_players = 100
        max_players = 0
        total_players = 0
        
        for group in groups_list:
            group_players = players.where(Choice.sf_group == group.sf_group)
            count = group_players.count()
            total_players += count
            min_players = min(min_players, count)
            max_players = max(max_players, count)
            print(f"  Группа {group.sf_group}: {count} игроков")
        
        print(f"  Среднее количество игроков: {total_players / len(groups_list):.1f}")
        print(f"  Мин/Макс игроков: {min_players}/{max_players}")

def main():
    """
    Основная функция
    """
    try:
        # Очищаем предыдущие данные полуфиналов
        Choice.update(
            semi_final=None,
            sf_group=None,
            posev_sf=None
        ).where(
            (Choice.semi_final == 1) | (Choice.semi_final == 2)
        ).execute()
        
        Result.delete().where(
            Result.system_stage.is_null(False)
        ).execute()
        
        # Создаем 1-й полуфинал
        sf1_groups = create_semi_final_1()
        
        # Создаем 2-й полуфинал по 5-ти этапной схеме
        sf2_groups = create_semi_final_2()
        
        # Создаем встречи для обоих полуфиналов
        if sf1_groups:
            create_matches_for_semi_final(1, sf1_groups)
        if sf2_groups:
            create_matches_for_semi_final(2, sf2_groups)
        
        # Переносим результаты из предварительного этапа
        transfer_matches_from_previous_stage()
        
        # Выводим финальную статистику
        print_final_statistics()
        
        print("\n" + "="*60)
        print("ЖЕРЕБЬЕВКА ПОЛУФИНАЛОВ УСПЕШНО ЗАВЕРШЕНА!")
        print("="*60)
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()