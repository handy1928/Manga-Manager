import logging
import time
import tkinter as tk
from tkinter import ttk

from CommonLib.HelperFunctions import get_elapsed_time
from CommonLib.HelperFunctions import get_estimated_time

logger = logging.getLogger(__name__)
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


def printProgressBar(total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r",
                     last=False, iteration=0, start_time=0.0, final_message=None):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    msg = f'{prefix} |{bar}| {percent}% - {iteration}/{total} {suffix}\nElapsed: {get_elapsed_time(start_time)} | Estimated: {get_estimated_time(start_time, processed_files=iteration, total_files=total)}'
    print(ERASE_LINE + CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    # print(' ' * _last_print_lenght, end=)
    print("\r" + msg)
    # Print New Line on Complete

    if iteration >= total or last:
        print(ERASE_LINE + CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
        print("\r" + msg)
        if last:
            print(final_message)


class ProgressBar:
    def __init__(self, UI_isInitialized: bool, pb_root: tk.Frame, total: int):

        self.UI_isInitialized = UI_isInitialized
        self._pb_root = pb_root
        self.total = total

        self.start_time = time.time()
        self.processed_counter = 0
        self.processed_errors = 0

        if UI_isInitialized:
            self.label_progress_text = tk.StringVar()
            self._init_ui_initialized()
        else:
            self._init_nogui()

            return

    def _init_nogui(self):
        self._last_print_length = 0
        printProgressBar(self.total, start_time=self.start_time)

    def _init_ui_initialized(self):
        self.style = ttk.Style(self._pb_root)
        self.style.layout('text.Horizontal.TProgressbar',
                          [
                              ('Horizontal.Progressbar.trough',
                               {
                                   'children': [
                                       ('Horizontal.Progressbar.pbar',
                                        {
                                            'side': 'left',
                                            'sticky': 'ns'
                                        }
                                        )
                                   ],
                                   'sticky': 'nswe'
                               }
                               ),
                              ('Horizontal.Progressbar.label',
                               {
                                   'sticky': 'nswe'
                               }
                               )
                          ]
                          )
        self.style.configure('text.Horizontal.TProgressbar', text='0 %', anchor='center')

        self.pb = ttk.Progressbar(self._pb_root, length=400, style='text.Horizontal.TProgressbar',
                                  mode="determinate")  # create progress bar
        self.pb.grid(row=0, column=0, sticky=tk.E + tk.W)
        self.pb_text = tk.Label(self._pb_root, textvariable=self.label_progress_text, anchor=tk.W, justify="right")
        self.pb_text.grid(row=1, column=0, sticky=tk.E)

        logger.info("Initialized progress bar")

        # self.convert_images = self.checkbox2_settings_val.get()
        self.label_progress_text.set(
            f"Processed: {(self.processed_counter + self.processed_errors)}/{self.total} files - {self.processed_errors} errors\n"
            f"Elapsed time  : {get_elapsed_time(self.start_time)}\n"
            f"Estimated time: {get_estimated_time(self.start_time, self.processed_counter, self.total)}")

    def increaseCount(self):
        if self.processed_counter + 1 > self.total:
            printProgressBar(self.total, start_time=self.start_time,
                             iteration=self.processed_counter, last=True)
            return
        self.processed_counter += 1
        self.updatePB()

    def increaseError(self):
        if self.processed_counter >= self.total:
            return
        self.processed_counter += 1
        self.processed_errors += 1
        self.updatePB()

    def updatePB(self):

        if self.UI_isInitialized:
            self._pb_root.update()
            percentage = ((self.processed_counter + self.processed_errors) / self.total) * 100
            self.style.configure('text.Horizontal.TProgressbar',
                                 text='{:g} %'.format(round(percentage, 2)))  # update label
            self.pb['value'] = percentage
            self.label_progress_text.set(
                f"Processed: {(self.processed_counter + self.processed_errors)}/{self.total} files - {self.processed_errors} errors\n"
                f"Elapsed time  : {get_elapsed_time(self.start_time)}\n"
                f"Estimated time: {get_estimated_time(self.start_time, self.processed_counter, self.total)}")
        else:
            printProgressBar(self.total, start_time=self.start_time,
                             iteration=self.processed_counter)

    def send_final_message(self, message):
        printProgressBar(self.total, start_time=self.start_time,
                         iteration=self.processed_counter, last=True, final_message=message)
