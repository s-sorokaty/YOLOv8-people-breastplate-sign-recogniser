import ctypes
import people_finder
import sign_finder
import store

def main():
    # Получение начальных данных из файлов
    available_names, men_was_close_to_pc = store.get_initial_data("names.txt", "men_between_pc.txt")
    
    # Инициализация переменных
    man_detection_count = 0
    iteration_count = 5
    target_detection_count = 4

    # Запуск поиска людей на кадрах
    result, mens_in_frame = people_finder.start_find_people(iteration_count, lambda: None)

    # Подсчет обнаруженных людей
    man_detection_count = sum(1 for res in result if res.is_man_exist)

    # Проверка достижения целевого количества обнаруженных людей
    if man_detection_count < target_detection_count:
        ctypes.windll.user32.LockWorkStation()

    # Поиск знаков на кадрах
    sign_finder.find_sign(result, available_names)

    # Формирование списка людей, находящихся рядом с ПК
    men_close_to_pc = []
    for res in result:
        if res.similar_to_exist_name and res.similar_to_exist_name not in men_close_to_pc:
            men_close_to_pc.append(res.similar_to_exist_name)

    # Проверка наличия людей рядом с ПК
    if not men_close_to_pc:
        ctypes.windll.user32.LockWorkStation()

    # Запись логов
    store.write_logs(mens_in_frame, men_close_to_pc, men_was_close_to_pc)
