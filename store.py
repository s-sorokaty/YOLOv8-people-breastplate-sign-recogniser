import codecs
from datetime import datetime
from typing import Union
from models import MenStatus, ResultSchema

def get_initial_data(available_names_filename: str, already_detected_names_filename: str) -> Union[list[str], list[str]]:
    with codecs.open(available_names_filename, "r", "utf_8_sig" ) as f:
        available_names = [name.strip() for name in f.readlines() if name.strip()]
    with codecs.open(already_detected_names_filename, "r", "utf_8_sig" ) as f:
         men_was_close_to_pc = [name.strip() for name in f.readlines() if name.strip()]
    return available_names, men_was_close_to_pc

def write_logs(men_in_frame:list[ResultSchema], men_close_to_pc:list[str], men_was_close_to_pc:list[str]):
    with codecs.open("men_between_pc.txt", "w", "utf_8_sig" ) as f:
        f.write('\n'.join(men_close_to_pc))
    with codecs.open('logs.txt', 'a', "utf_8_sig" ) as f:
        f.write('ITERATION STARTED\n')
        for men in men_close_to_pc:
            if men in men_was_close_to_pc:
                f.write(f'{datetime.now()} men True {men} {MenStatus.steel_in_frame.value}\n')
                men_was_close_to_pc.remove(men)
            else:
                f.write(f'{datetime.now()} men True {men} {MenStatus.new_in_frame.value}\n')

        for men in men_was_close_to_pc:
            f.write(f'{datetime.now()} men True {men} {MenStatus.gone.value}\n')

        for _ in range(0, int(men_in_frame) - int(len(men_close_to_pc))):
            f.write(f'{datetime.now()} men False undefined\n')
        f.write(f'ITERATION STOPPED\n')