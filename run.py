import os
import time

start_time = time.time()
# os.system('python3 comparer_runner.py boats.mp4 cvat --available_classes boat')
# os.system('python3 comparer_runner.py highway.mp4 cvat --available_classes car')
# os.system('python3 comparer_runner.py pitbull.mp4 cvat --available_classes dog person bicycle handbag')
# os.system('python3 comparer_runner.py street.mp4 cvat --available_classes person bus car bicycle motorcycle truck')
# os.system('python3 comparer_runner.py street2.mp4 cvat --available_classes person bus car bicycle motorcycle truck')
# os.system('python3 comparer_runner.py birds3.mp4 cvat --available_classes bird')
# os.system('python3 comparer_runner.py bench.mp4 cvat --available_classes person car bicycle apple bench handbag umbrella parking_meter')
# os.system('python3 comparer_runner.py park.mp4 cvat --available_classes person dog bicycle bench')
# os.system('python3 comparer_runner.py park2.mp4 cvat --available_classes person dog bicycle backpack bench')
# os.system('python3 comparer_runner.py bike.mp4 cvat --available_classes person bicycle')
os.system('python3 comparer_runner.py gdynia.mp4 cvat --available_classes person car bicycle apple bench handbag umbrella boat chair')
os.system('python3 comparer_runner.py gdynia2.mp4 cvat --available_classes person car bicycle apple bench handbag umbrella boat chair')
os.system('python3 comparer_runner.py gdynia3.mp4 cvat --available_classes person car bicycle apple bench handbag umbrella boat chair')
e = int(time.time() - start_time)
print('WHOLE TIME: ' + '{:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))