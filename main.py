import codecs, ctypes, datetime
import people_finder
import sign_finder



def main():
    with codecs.open( "names.txt", "r", "utf_8_sig" ) as f:
        names = f.read().split('\n')
    with codecs.open("men_between_pc.txt", "r", "utf_8_sig" ) as f:
        men_was_close_to_pc = f.read().strip().split('\n')
    try:
        men_was_close_to_pc.remove('')
    except: pass
    man_detection_count = 0
    iteration_count = 5
    target_detection_count = 4
    result, men_in_frame = people_finder.start_find_people(iteration_count, lambda:None)

    for res in result:
        if res.is_man_exist:
            man_detection_count += 1

    print("man in frame count: ", men_in_frame)
    if not man_detection_count >= target_detection_count: ctypes.windll.user32.LockWorkStation()
    sign_finder.find_sign(result, names)
    men_close_to_pc = []
    for res in result:
        if res.similiar_to_exist_name and res.similiar_to_exist_name not in men_close_to_pc: men_close_to_pc.append(res.similiar_to_exist_name)

    with codecs.open("men_between_pc.txt", "w", "utf_8_sig" ) as f:
        f.write('\n'.join(men_close_to_pc))
    with codecs.open('logs.txt', 'a', "utf_8_sig" ) as f:
        f.write('ITERATION STARTED\n')
        for men in men_close_to_pc:
            if men in men_was_close_to_pc:
                f.write(f'{datetime.date.today()} men True {men} steel_in_frame\n')
                men_was_close_to_pc.remove(men)
            else:
                f.write(f'{datetime.date.today()} men True {men} new_in_frame\n')
        print(men_was_close_to_pc)
        for men in  men_was_close_to_pc:
            f.write(f'{datetime.date.today()} men True {men} gone\n')

        for iter in range(0, int(men_in_frame) - int(len(men_close_to_pc))):
            f.write(f'{datetime.date.today()} men False undefined\n')
        f.write('ITERATION STOPPED\n')
main()