import ctypes, datetime
import people_finder
import sign_finder
import store


def main():
    avalible_names, men_was_close_to_pc = store.get_initial_data("names.txt", "men_between_pc.txt")
    man_detection_count = 0
    iteration_count = 5
    target_detection_count = 4
    result, men_in_frame = people_finder.start_find_people(iteration_count, lambda:None)

    for res in result:
        if res.is_man_exist:
            man_detection_count += 1

    if not man_detection_count >= target_detection_count: ctypes.windll.user32.LockWorkStation()
    sign_finder.find_sign(result, avalible_names)
    men_close_to_pc = []
    for res in result:
        if res.similiar_to_exist_name and res.similiar_to_exist_name not in men_close_to_pc: 
            men_close_to_pc.append(res.similiar_to_exist_name)
    if not men_close_to_pc: ctypes.windll.user32.LockWorkStation()
    store.write_logs(men_in_frame, men_close_to_pc, men_was_close_to_pc)
    