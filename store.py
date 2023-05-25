import codecs, datetime
from models import MenStatus
def get_initial_data(avalible_names_filename:str, alredy_detected_names_filename:str) -> list[list, str]:
    with codecs.open(avalible_names_filename, "r", "utf_8_sig" ) as f:
        avalible_names = f.read().split('\n')
    with codecs.open(alredy_detected_names_filename, "r", "utf_8_sig" ) as f:
        men_was_close_to_pc = f.read().strip().split('\n')
    try:
        men_was_close_to_pc.remove('')
    except: pass
    return avalible_names, men_was_close_to_pc

def write_logs(men_in_frame, men_close_to_pc, men_was_close_to_pc):
    with codecs.open("men_between_pc.txt", "w", "utf_8_sig" ) as f:
        f.write('\n'.join(men_close_to_pc))
    with codecs.open('logs.txt', 'a', "utf_8_sig" ) as f:
        f.write('ITERATION STARTED\n')
        for men in men_close_to_pc:
            if men in men_was_close_to_pc:
                f.write(f'{datetime.date.today()} men True {men} {MenStatus.steel_in_frame.value}\n')
                men_was_close_to_pc.remove(men)
            else:
                f.write(f'{datetime.date.today()} men True {men} {MenStatus.new_in_frame.value}\n')
        print(men_was_close_to_pc)
        for men in men_was_close_to_pc:
            f.write(f'{datetime.date.today()} men True {men} {MenStatus.gone.value}\n')

        for iter in range(0, int(men_in_frame) - int(len(men_close_to_pc))):
            f.write(f'{datetime.date.today()} men False undefined\n')
        f.write('ITERATION STOPPED\n')