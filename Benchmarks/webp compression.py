import imghdr
import io
import logging
import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from zipfile import ZipFile

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle, Rectangle, Arc

from converting_algorithms import list_of_converters as compression_functions

stream_handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s - %(name)20s - %(levelname)8s - %(message)s',
                handlers=[stream_handler]
                # filename='/tmp/myapp.log'
                )
logger = logging.getLogger()

list_of_zipfiles = ['my_zipfile_1.zip', 'my_zipfile_2.zip', ...]
failed_algorithms = []
failed_skipped = []


def generate_manga_images(num_images, zip_file_name):
    # Create a new zip file with the given name
    with ZipFile(zip_file_name, 'w') as zip_file:
        for i in range(num_images):
            # Create a figure and axes
            fig, ax = plt.subplots()

            # Add some geometric shapes to the axes
            ax.add_patch(Circle((50, 50), 30, fill=False))
            ax.add_patch(Rectangle((25, 25), 50, 50, fill=False))
            ax.add_patch(Arc((50, 50), 60, 60, angle=0, theta1=0, theta2=180))

            # Add margins to the sides of the image
            plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

            # create a canvas widget that displays the figure
            canvas = FigureCanvasTkAgg(fig, master=None)

            # save the figure as a JPEG file in a buffer
            buffer = io.BytesIO()
            canvas.print_figure(buffer, format='jpg', dpi=300)

            # add the JPEG file to the zip file
            zip_file.writestr('image{}.jpg'.format(i), buffer.getvalue())

    return zip_file_name
import zipfile
from io import BytesIO
import time


def sort_treeview(treeview, col, descending=None):
    """Sort treeview contents when a column header is clicked on."""

    def sort_key(item):
        """Return a key that can be used to sort the item."""
        if col == 'rate':
            # convert rate to float
            return float(item[0])
        elif col == 'time':
            # extract time in seconds from time string and convert to float
            return float(item[0].split()[0])
        elif col == 'osize' or col == 'size':
            # extract size in MB from size string and convert to float
            return float(item[0].split()[0])
        elif col == 'len_images':
            # extract number of images from string and convert to int
            return int(item[0].split()[0])
        else:
            # for other columns, use the item value as is
            return item[0]
    if descending is None:
        # if descending is not specified, use the current sort state
        # of the column as the sort order
        descending = treeview.heading(col, 'text')[0] == '\u25bc'
    else:
        # update the heading to show the new sort order
        treeview.heading(col, text=col + " " + "\u25bc" if descending else "\u25b2")
    # get current sort state and reverse it if necessary
    data = [(treeview.set(child, col), child) for child in treeview.get_children('')]
    data.sort(key=sort_key, reverse=descending)
    for ix, item in enumerate(data):
        treeview.move(item[1], '', ix)


def bytes_to_megabytes(bytes):
  return bytes / 1024 / 1024
supported_image_formats = ['png', 'jpeg', 'jpg', 'bmp', 'gif']
class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Zip File Compressor')
        self.resizable(False, False)
        self.selected_files = []

        # Create a label to display the selected zip files
        self.zip_files_label = tk.Label(self, text='No files selected')
        self.zip_files_label.pack(padx=10, pady=10)

        # Create a button to select the zip files
        self.select_button = tk.Button(self, text='Select files', command=self.on_select)
        self.select_button.pack(padx=10, pady=(0, 10))

        # Create a progress bar to show the progress of the compression
        self.progress_bar = tk.ttk.Progressbar(self, orient='horizontal', length=200, mode='determinate')
        self.progress_bar.pack(padx=10, pady=(0, 10))

        # Create a treeview to display the results
        self.treeview = tk.ttk.Treeview(self, columns=('algorithm', 'rate', 'time','osize', 'size',"len_images"))
        self.treeview.column('#0', width=0, stretch=False)
        self.treeview.heading('algorithm', text='Algorithm', anchor="center")
        self.treeview.heading('rate', text='Compression rate', anchor="center")
        self.treeview.heading('time', text='Elapsed time', anchor="center")
        self.treeview.heading('osize', text='Initial size', anchor="center")
        self.treeview.heading('size', text='Final size', anchor="center")
        self.treeview.heading('len_images', text='Processed Images', anchor="center")

        self.treeview.bind('<ButtonRelease-1>', lambda event: sort_treeview(self.treeview, self.treeview.identify_column(event.x)))

        self.treeview.pack(padx=10, pady=(0, 10))

        # Create a button to start the compression
        self.compress_button = tk.Button(self, text='Compress', command=self.run_in_background)
        self.compress_button.pack(padx=10, pady=(0, 10))

    def compress_images(self,zip_file, algorithm):
        # Initialize variables to store the results
        compression_rates = []
        elapsed_times = []
        final_sizes = []
        number_processed_images = 0
        alg_name, n_algorithm = self.current_algorithm
        logger.info(f"Compressing images using {algorithm} for file {zip_file}")
        try:
            # Open the zip file in read mode
            with zipfile.ZipFile(zip_file, 'r') as zip_fp:
                # Open a new zip file in write mode
                with zipfile.ZipFile('compressed.zip', 'w') as compressed_zip:
                    # Iterate over the entries in the zip file
                    for i, entry in enumerate(zip_fp.infolist()):
                        # Check if the entry is an image file
                        image_type = imghdr.what(zip_fp.open(entry))
                        if image_type in supported_image_formats:
                            # Read the bytes of the image file
                            image_bytes = zip_fp.read(entry.filename)

                            # Compress the image using the provided algorithm
                            start_time = time.perf_counter()
                            compressed_bytes = algorithm(image_bytes)
                            elapsed_time = time.perf_counter() - start_time

                            # Calculate the compression rate
                            original_size = len(image_bytes)
                            compressed_size = len(compressed_bytes)
                            compression_rate = 1 - compressed_size / original_size

                            # Add the results to the lists
                            compression_rates.append(compression_rate)
                            elapsed_times.append(elapsed_time)
                            final_sizes.append(compressed_size)
                            number_processed_images += 1

                            # Save the compressed image in a new zip file

                            # Create a BytesIO object to write the compressed image to
                            compressed_fp = BytesIO(compressed_bytes)
                            # Add the compressed image to the zip file
                            compressed_zip.writestr(entry.filename, compressed_fp.getvalue())
                            logger.info(f"{alg_name}({n_algorithm}/{len(compression_functions)}) - {os.path.basename(zip_file)} - Image {i}/{len(zip_fp.namelist())}")
                            self.zip_files_label.configure(
                            text=f"Using {alg_name} ({n_algorithm}/{len(compression_functions)}) - Processing {os.path.basename(zip_file)} - Image {i}/{len(zip_fp.namelist())}")
        except zipfile.BadZipFile:
            # Handle the case where the file is not a zip file
            print("The file is not a zip file.")

        except IOError:
            # Handle the case where the file does not exist
            print("The file does not exist.")

        # Delete the new zip file
        try:
            os.remove('compressed.zip')
        except OSError:
            pass

        # Return the results
        return compression_rates, elapsed_times, final_sizes, number_processed_images
    def on_select(self):
        # Open a file dialog to select the zip files
        zip_files = filedialog.askopenfilenames(filetypes=(('CBZ files', '*.CBZ'),))

        # Update the label to show the selected zip files
        self.selected_files = zip_files
        if zip_files:
            self.zip_files_label.config(text=f'{len(self.selected_files)} Files selected')
        else:
            self.zip_files_label.config(text='No files selected')
    def run_in_background(self):
        thread = threading.Thread(target=self.on_compress)
        thread.start()
    def on_compress(self):
        # Get the selected zip files
        zip_files = self.zip_files_label['text']

        # Check if any zip files were selected
        if zip_files == 'No files selected':
            messagebox.showerror('Error', 'No zip files selected')
            return

        # Split the list of zip files into a list
        zip_files = self.selected_files

        # List of algorithm functions to apply
        algorithms = compression_functions

        # Dictionary to store the results for each algorithm
        results = {}

        # Initialize the progress bar
        self.progress_bar['maximum'] = len(zip_files) * len(algorithms)
        self.progress_bar['value'] = 0
        self.current_algorithm = []
        # Iterate over the algorithm functions
        for n_algorithm,algorithm in enumerate(algorithms):
            self.current_algorithm = [algorithm.__name__,n_algorithm]
            # Initialize variables to store the results for this algorithm
            compression_rates = []
            elapsed_times = []
            final_sizes = []
            original_sizes = []
            total_images_processed = 0

            # Iterate over the zip files and apply the compression function
            for zip_file in zip_files:
                # Call the compress_images function with the current algorithm
                if not zipfile.is_zipfile(zip_file):
                    continue
                self.zip_files_label.configure(
                    text=f"Using {algorithm.__name__} ({n_algorithm}/{len(algorithms)}) - Processing {os.path.basename(zip_file)} - Image 0/0")

                try:
                    rates, times, sizes, n_images = self.compress_images(zip_file, algorithm)
                except Exception:
                    logger.exception(f"Error compressing the images with algorithm {algorithm.__name__} for file: '{zip_file}'")
                    print(algorithm.__name__)
                    continue
                # Add the results to the lists
                compression_rates.extend(rates)
                elapsed_times.extend(times)
                final_sizes.extend(sizes)
                total_images_processed += n_images
                image_counter = 0
                # Calculate the original size of the image files
                with zipfile.ZipFile(zip_file, 'r') as zip_fp:

                    for i, entry in enumerate(zip_fp.infolist()):
                        if entry.filename.endswith('.png') or entry.filename.endswith(
                                '.jpg') or entry.filename.endswith('.jpeg'):
                            original_sizes.append(entry.file_size)


                # Update the progress bar
                self.progress_bar['value'] += 1
                self.update_idletasks()

            # Calculate the average compression rate, elapsed time, and final size for this algorithm
            avg_compression_rate = 0 if len(compression_rates) == 0 else sum(compression_rates) / len(compression_rates)
            avg_elapsed_time = 0 if len(elapsed_times) == 0 else sum(elapsed_times) / len(elapsed_times)
            avg_final_size = 0 if len(final_sizes) == 0 else sum(final_sizes) / len(final_sizes)
            avg_original_size = 0 if len(original_sizes) == 0 else sum(original_sizes) / len(original_sizes)

            # Add the results to the dictionary
            results[algorithm.__name__] = (avg_compression_rate, avg_elapsed_time, avg_final_size,avg_original_size,
                                           total_images_processed)

        # Clear the treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Populate the treeview with the results
        for algorithm, (avg_compression_rate, avg_elapsed_time, avg_final_size, avg_original_size,total_images_processed) in results.items():
            self.treeview.insert('', 'end', values=(
            algorithm, f'{avg_compression_rate:.2f}', f'{avg_elapsed_time:.2f} seconds',f'{bytes_to_megabytes(avg_original_size):.2f} MB',
            f'{bytes_to_megabytes(avg_final_size):.2f} MB', f'{total_images_processed} images'))

        # Reset the progress bar
        self.progress_bar['value'] = 0



if __name__ == '__main__':
    window = MainWindow()
    window.mainloop()

# <
# def main():
#     # List of zip files to process
#     zip_files = ['file1.zip', 'file2.zip', 'file3.zip']
#
#     # List of algorithm functions to apply
#     # algorithms = [algorithm_function_1, algorithm_function_2, algorithm_function_3]
#     algorithms = compression_functions
#
#     # Dictionary to store the results for each algorithm
#     results = {}
#
#     # Iterate over the algorithm functions
#     for algorithm in algorithms:
#         # Initialize variables to store the results for this algorithm
#         compression_rates = []
#         elapsed_times = []
#         final_sizes = []
#
#         # Iterate over the zip files and apply the compression function
#         for zip_file in zip_files:
#             # Call the compress_images function with the current algorithm
#             rates, times, sizes = compress_images(zip_file, algorithm)
#
#             # Add the results to the lists
#             compression_rates.extend(rates)
#             elapsed_times.extend(times)
#             final_sizes.extend(sizes)
#
#         # Calculate the average compression rate, elapsed time, and final size for this algorithm
#         avg_compression_rate = sum(compression_rates) / len(compression_rates)
#         avg_elapsed_time = sum(elapsed_times) / len(elapsed_times)
#         avg_final_size = sum(final_sizes) / len(final_sizes)
#
#         # Add the results to the dictionary
#         results[algorithm.__name__] = (avg_compression_rate, avg_elapsed_time, avg_final_size)
#
#     # Print the results for each algorithm
#     for algorithm, (avg_compression_rate, avg_elapsed_time, avg_final_size) in results.items():
#         print(f'Algorithm: {algorithm}')
#         print(f'Average compression rate: {avg_compression_rate:.2f}')
#         print(f'Average elapsed time: {avg_elapsed_time:.2f} seconds')
#         print(f'Average final size: {avg_final_size:.2f} bytes')
#     # Find the algorithm with the highest compression rate
#     best_compression = max(results, key=lambda x: results[x][0])
#     print(f'Algorithm with highest compression: {best_compression}')
#
#     # Find the algorithm with the lowest elapsed time
#     fastest_algorithm = min(results, key=lambda x: results[x][1])
#     print(f'Fastest algorithm: {fastest_algorithm}')
#

#
# def convert_zipfile(zipfile, convert_function):
#     # Initialize the statistics dict
#     statistics = {
#         'num_images': 0,  # Number of images in the zipfile
#         'total_size_before': 0,  # The addition of the sizes of all files before converting
#         'total_size_after': 0,  # The addition of the sizes of all files after converting
#         'final_size': 0,  # The actual file size after being zipped
#         'min_size_before': float('inf'),  # The min size of all the images before converting
#         'min_size_after': float('inf'),  # The min size of all the images after converting
#         'max_size_before': 0,  # The max size of all the images before converting
#         'max_size_after': 0,  # The max size of all the images after converting
#         'min_time': float('inf'),  # The min time a image took to convert
#         'max_time': 0,  # The max time a image took to convert
#         'total_time': 0,  # The total time to convert all images
#     }
#
#     # Open the zipfile in read mode
#     with ZipFile(zipfile, 'r') as zip_file:
#         # Get all the filenames from the zipfile
#         filenames = zip_file.namelist()
#         filename_ = os.path.join(os.path.dirname(zipfile),'converted_' + os.path.basename(zipfile))
#         # Create a new zipfile to save the converted images
#         with ZipFile(filename_, 'w') as new_zip_file:
#             # Iterate over all the filenames in the zipfile
#             for filename in filenames:
#                 # Read the bytes of the image
#                 image_bytes = zip_file.read(filename)
#
#                 # Check if the file is an image
#                 image_type = imghdr.what(None, image_bytes)
#                 if not image_type:
#                     # Skip the file if it is not an image
#                     continue
#
#
#                 # Keep track of the number of images and their sizes before converting
#                 statistics['num_images'] += 1
#                 statistics['total_size_before'] += len(image_bytes)
#                 statistics['min_size_before'] = min(statistics['min_size_before'], len(image_bytes))
#                 statistics['max_size_before'] = max(statistics['max_size_before'], len(image_bytes))
#
#                 # Start a timer to keep track of the time it takes to convert the image
#                 start_time = time.perf_counter()
#
#                 # Convert the image bytes using the provided function
#                 converted_bytes = convert_function(image_bytes)
#
#                 # Stop the timer and calculate the time it took to convert the image
#                 elapsed_time = time.perf_counter() - start_time
#
#                 # Update the statistics dict with the time it took to convert the image
#                 statistics['total_time'] += elapsed_time
#                 statistics['min_time'] = min(statistics['min_time'], elapsed_time)
#                 statistics['max_time'] = max(statistics['max_time'], elapsed_time)
#
#                 # Keep track of the sizes of the converted images
#                 statistics['total_size_after'] += len(converted_bytes)
#                 statistics['min_size_after'] = min(statistics['min_size_after'], len(converted_bytes))
#                 statistics['max_size_after'] = max(statistics['max_size_after'], len(converted_bytes))
#
#                 # Save the converted image to the new zipfile
#                 new_zip_file.writestr(filename, converted_bytes)
#             # Calculate the final size of the new zipfile
#     statistics['final_size'] = os.stat(filename_).st_size
#
#     # Delete the new zipfile
#     os.remove(filename_)
#
#     # Return the statistics dict
#     return statistics
#
#
# # Create a function "benchmark" that takes a zipfile as parameter and a list of functions named list_of_converters.
# # Iterate the list_of_converters and will call convert_zipfile with the passed zipfile and the function.
# # Store the statistics in a dict as "<function_name>_statistics" where "<function_name>" is the name of the function.
# # Then the statistics will be returned.
# def benchmark(zipfile, list_of_converters):
#     # Initialize the statistics dict
#     statistics = {}
#
#     # Iterate over the list of converters
#     for converter in list_of_converters:
#         # Get the name of the converter function
#         converter_name = converter.__name__
#
#         # Call the convert_zipfile function with the zipfile and the converter function
#         try:
#             converter_statistics = convert_zipfile(zipfile, converter)
#         except Exception as e:
#             failed_algorithms.append(converter_name)
#             logger.exception(f"Error converting with '{converter_name}' {zipfile}")
#             continue
#
#
#         # Store the converter statistics in the statistics dict using the converter's name as the key
#         statistics[converter_name + '_statistics'] = converter_statistics
#
#     # Return the statistics dict
#     return statistics
#
#
# # create a function "run_benchmarks" that takes a list_of_zipfiles and a list of functions named list_of_converters.
# # for each zipfile in list_of_zipfiles call benchmark with the file as first parameter and list_of_convertes as second parameter.
# # Store the statistics for each file in a dict.
# # return the statistics
#
# def run_benchmarks(list_of_zipfiles, list_of_converters):
#     # Initialize the statistics dict
#     statistics = {}
#
#     # Iterate over the list of zipfiles
#     for zipfile in list_of_zipfiles:
#         # Call the benchmark function with the zipfile and the list of converter functions
#         zipfile_statistics = benchmark(zipfile, list_of_converters)
#         if not zipfile_statistics:
#             failed_skipped.append(zipfile)
#             continue
#         # Store the zipfile statistics in the statistics dict using the zipfile's name as the key
#         statistics[zipfile + '_statistics'] = zipfile_statistics
#
#     # Return the statistics dict
#     return statistics
#
#
# def display_leaderboards(sorted_time_list, sorted_size_list, total_files, total_images):
#     # Create a new window for the leaderboards
#     leaderboard_window = root
#     leaderboard_window.title("Leaderboards")
#
#     # Create a frame for the time leaderboard
#     time_frame = tk.Frame(leaderboard_window)
#     time_frame.pack(side=tk.LEFT)
#
#     # Create a label for the time leaderboard
#     time_label = tk.Label(time_frame, text="Time Leaderboard")
#     time_label.pack()
#
#     # Create a listbox for the time leaderboard
#     time_listbox = tk.Listbox(time_frame, width=30)
#     time_listbox.pack()
#
#     # Populate the time listbox with the sorted time list
#     for algorithm, avg_time in sorted_time_list:
#         time_listbox.insert(tk.END, f"{algorithm}: {avg_time:.2f}s")
#
#     # Create a frame for the size leaderboard
#     size_frame = tk.Frame(leaderboard_window)
#     size_frame.pack(side=tk.RIGHT)
#
#     # Create a label for the size leaderboard
#     size_label = tk.Label(size_frame, text="Size Leaderboard")
#     size_label.pack()
#
#     # Create a listbox for the size leaderboard
#     size_listbox = tk.Listbox(size_frame, width=30)
#     size_listbox.pack()
#
#     # Populate the size listbox with the sorted size list
#     for algorithm, avg_size in sorted_size_list:
#         size_listbox.insert(tk.END, f"{algorithm}: {avg_size:.2f}KB")
#
#     # Create a label to display the total number of files processed
#     total_files_label = tk.Label(leaderboard_window, text=f"Total files processed: {total_files}")
#     total_files_label.pack()
#
#     # Create a label to display the total number of images
#     total_images_label = tk.Label(leaderboard_window, text=f"Total images: {total_images}")
#     total_images_label.pack()
# if __name__ == '__main__':
#     # Create the GUI window
#     leaderboards = CompressionLeaderboards()
#     leaderboards.mainloop()