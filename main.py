import time, ctypes
import people_finder
import sign_finder

man_detection_count = 0
iteration_count = 5
target_detection_count=4

result = people_finder.start_find_people(iteration_count, lambda:None)

for res in result:
    if res.is_man_exist:
        man_detection_count += 1
        
print("man in frame detection count: ", man_detection_count, '\nman target detection count: ', target_detection_count)
if not man_detection_count >= target_detection_count: ctypes.windll.user32.LockWorkStation()
sign_finder.find_sign(result)
time.sleep(1)