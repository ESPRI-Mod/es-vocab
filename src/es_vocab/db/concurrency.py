import multiprocessing
import os
import time

multiprocessing.set_start_method('fork')

SHARED_VARIABLE = multiprocessing.Value('i', 0, lock=True)

def writter_logic():
    while True:
         time.sleep(5)
         with SHARED_VARIABLE.get_lock():
            SHARED_VARIABLE.value += 1


def reader_logic():
    while True:
        print(f'{os.getpid()}: {SHARED_VARIABLE.value}')
        #time.sleep(1)


if __name__ == '__main__':
    p = multiprocessing.Process(target=writter_logic)
    p.start()
    
    for n in range(0, 5):
        p = multiprocessing.Process(target=reader_logic)
        p.start()