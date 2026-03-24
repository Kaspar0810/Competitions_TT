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
            print(f"  Ищем группу выше для перемещения, начиная с самой верхней...")
            
            # Ищем группу, начиная с самой верхней (группа 1)
            found = False
            for check_group_num in range(1, target_group_num):
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
                        # Продолжаем искать дальше
                        continue
            
            if not found:
                # Если не нашли подходящую группу, добавляем в самую нижнюю возможную
                print(f"  Не найдено подходящей группы выше, добавляем в группу {target_group_num}")
                target_group['players'].extend(source_group['players'])
                target_group['from_groups'].append(source_group_num)
                processed_groups.add(source_group_num)
                skipped_groups.append(source_group_num)