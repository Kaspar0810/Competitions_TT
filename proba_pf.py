import random
from peewee import *

# Подключение к базе данных
db = MySQLDatabase('your_database', user='your_user', password='your_password', host='localhost')

# Определение моделей
class Choice(Model):
    id_player = IntegerField()
    family = CharField()
    region = CharField()
    group = CharField()  # номер группы («1 группа» и т.д.)
    mesto_group = IntegerField()  # место занятое в группе
    semi_final = CharField(null=True)  # номер полуфинала
    posev_sf = IntegerField(null=True)  # порядковый номер игрока в группе полуфинала
    sf_group = CharField(null=True)  # номер группы полуфинала
    
    class Meta:
        database = db
        table_name = 'Choice'

class Result(Model):
    tours = CharField()  # номера игроков в таблице, которые встречаются
    player1 = CharField()
    player2 = CharField()
    winner = CharField(null=True)
    points_win = IntegerField(default=2)
    score_in_game = CharField(null=True)
    score_in_win = CharField(null=True)
    loser = CharField(null=True)
    points_loser = IntegerField(default=1)
    score_loser = CharField(null=True)
    
    class Meta:
        database = db
        table_name = 'Result'

# Создание таблиц (если не существуют)
db.connect()
db.create_tables([Choice, Result], safe=True)

def create_semi_final_groups():
    """Создание групп 1-го полуфинала с учетом регионов"""
    
    # Получаем всех спортсменов, занявших 1 и 2 места в предварительных группах
    players = []
    for group_num in range(1, 33):  # 32 группы
        group_name = f"{group_num} группа"
        
        # Получаем 1-е место
        first_place = Choice.select().where((Choice.group == group_name) & (Choice.mesto_group == 1)).first()
        
        # Получаем 2-е место
        second_place = Choice.select().where((Choice.group == group_name) & (Choice.mesto_group == 2)).first()
        
        if first_place and second_place:
            players.append({
                'group_num': group_num,
                'first': first_place,
                'second': second_place
            })
    
    # Принцип стыковых встреч: 1-32, 2-31, 3-30 и т.д.
    semi_groups = []
    used_groups = set()
    
    # Сначала формируем пары групп по принципу стыковых встреч
    pairs = []
    for i in range(1, 17):
        group1_num = i
        group2_num = 33 - i
        pairs.append((group1_num, group2_num))
    
    # Функция для проверки регионов
    def check_regions(first1, first2):
        return first1.region != first2.region
    
    # Формируем группы полуфинала с учетом регионов
    for group1_num, group2_num in pairs:
        group1 = next(p for p in players if p['group_num'] == group1_num)
        group2 = next(p for p in players if p['group_num'] == group2_num)
        
        first1, second1 = group1['first'], group1['second']
        first2, second2 = group2['first'], group2['second']
        
        # Проверяем регионы первых мест
        if not check_regions(first1, first2):
            # Если регионы совпадают, ищем замену
            swapped = False
            
            # Ищем соседнюю группу для обмена
            for swap_offset in [1, -1, 2, -2]:  # пробуем соседние группы
                swap_group_num = group1_num + swap_offset
                if 1 <= swap_group_num <= 32 and swap_group_num not in [g for g, _ in pairs]:
                    swap_group = next((p for p in players if p['group_num'] == swap_group_num), None)
                    if swap_group:
                        swap_first = swap_group['first']
                        if check_regions(first1, swap_first):
                            # Меняем группы
                            pairs[pairs.index((group1_num, group2_num))] = (swap_group_num, group2_num)
                            swapped = True
                            break
            
            if not swapped:
                # Если не нашли замену, оставляем как есть
                pass
        
        # Создаем группу полуфинала
        sf_group = {
            'sf_group_num': len(semi_groups) + 1,
            'players': [first1, second1, first2, second2]
        }
        semi_groups.append(sf_group)
    
    return semi_groups

def fill_semi_final_columns(semi_groups):
    """Заполнение столбцов semi_final, posev_sf, sf_group в таблице Choice"""
    
    for sf_group in semi_groups:
        sf_group_num = sf_group['sf_group_num']
        players = sf_group['players']
        
        # Порядковый номер в группе: 1-4
        for idx, player in enumerate(players, 1):
            player.semi_final = '1-й полуфинал'
            player.posev_sf = idx
            player.sf_group = f"{sf_group_num} группа"
            player.save()

def create_semi_final_matches():
    """Создание встреч для групп полуфинала"""
    
    # Получаем все группы полуфинала
    sf_groups = Choice.select().where(
        (Choice.semi_final == '1-й полуфинал') & (Choice.sf_group.is_null(False))
    ).distinct(Choice.sf_group)
    
    for sf_group in sf_groups:
        group_name = sf_group.sf_group
        
        # Получаем игроков группы, отсортированных по posev_sf
        players = list(Choice.select().where(
            (Choice.sf_group == group_name)
        ).order_by(Choice.posev_sf))
        
        if len(players) == 4:
            # Туры для 4-х спортсменов в группе
            tours = [
                (1, 3), (2, 4),  # 1 тур
                (1, 2), (3, 4),  # 2 тур
                (1, 4), (2, 3)   # 3 тур
            ]
            
            for tour_num, (pos1, pos2) in enumerate(tours, 1):
                player1 = players[pos1 - 1]
                player2 = players[pos2 - 1]
                
                # Создаем запись в Result
                Result.create(
                    tours=f"{tour_num}-й тур",
                    player1=player1.family,
                    player2=player2.family,
                    points_win=2,
                    points_loser=1
                )

def transfer_previous_matches():
    """Перенос встреч, которые уже игрались в предварительном этапе"""
    
    # Получаем все встречи полуфинала
    semi_matches = Result.select().where(
        Result.tours.contains('тур')
    )
    
    for match in semi_matches:
        # Ищем в таблице Result встречи из предварительного этапа
        previous_match = Result.select().where(
            (Result.player1 == match.player1) & 
            (Result.player2 == match.player2) &
            (Result.tours != match.tours)
        ).first()
        
        if previous_match:
            # Копируем данные из предыдущей встречи
            match.winner = previous_match.winner
            match.score_in_game = previous_match.score_in_game
            match.score_in_win = previous_match.score_in_win
            match.loser = previous_match.loser
            match.score_loser = previous_match.score_loser
            match.save()
        else:
            # Ищем встречу с переставленными игроками
            previous_match_rev = Result.select().where(
                (Result.player1 == match.player2) & 
                (Result.player2 == match.player1) &
                (Result.tours != match.tours)
            ).first()
            
            if previous_match_rev:
                match.winner = previous_match_rev.winner
                match.score_in_game = previous_match_rev.score_in_game
                match.score_in_win = previous_match_rev.score_in_win
                match.loser = previous_match_rev.loser
                match.score_loser = previous_match_rev.score_loser
                match.save()

def main():
    """Основная функция"""
    try:
        print("Начинаем формирование полуфиналов...")
        
        # 1. Создаем группы полуфинала
        semi_groups = create_semi_final_groups()
        print(f"Сформировано {len(semi_groups)} групп полуфинала")
        
        # 2. Заполняем столбцы в таблице Choice
        fill_semi_final_columns(semi_groups)
        print("Заполнены данные о полуфиналах в таблице Choice")
        
        # 3. Создаем встречи в таблице Result
        create_semi_final_matches()
        print("Созданы встречи для полуфиналов")
        
        # 4. Переносим результаты предыдущих встреч
        transfer_previous_matches()
        print("Перенесены результаты предыдущих встреч")
        
        print("Жеребьевка полуфинала успешно завершена!")
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()