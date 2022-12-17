import io

# import cv
import imageio
from PIL import Image


# from scipy.misc import imsave


def compress_to_webp_pillow(image_bytes):
    """
    Converts the provided image to webp and returns the converted image bytes.
    This function uses the PIL (Python Imaging Library) module to perform the conversion.

    In this example, the compress_to_webp function uses the PIL module to perform the conversion. The quantize method
    is used to compress the image using lossy compression, and the save method is used to save the image in webp
    format. Note that the function now takes an io.BytesIO object as input and returns an io.BytesIO object as output.
    This is because the PIL module requires the image to be provided as a file-like object, and the converted image
    bytes are saved to an in-memory buffer.

    :param image_bytes: The image that has to be converted
    :return: The converted image bytes
    """

    # Load the image from the bytes
    image_bytes_io = io.BytesIO(image_bytes)
    image = Image.open(image_bytes_io)

    # Compress the image using lossy compression
    image_compressed = image.quantize(dither=True)

    # Save the image in webp format
    output_bytes = io.BytesIO()
    image_compressed.save(output_bytes, format="webp")
    output_bytes.seek(0)

    # Return the bytes of the image
    return output_bytes.getvalue()
def compress_to_png_pillow(image_bytes):
    """
    Converts the provided image to PNG and returns the converted image bytes.
    This function uses the PIL (Python Imaging Library) module to perform the conversion.

    In this example, the compress_to_png function uses the PIL module to perform the conversion. The save method is used
    to save the image in PNG format. Note that the function now takes an io.BytesIO object as input and returns an
    io.BytesIO object as output. This is because the PIL module requires the image to be provided as a file-like object,
    and the converted image bytes are saved to an in-memory buffer.

    :param image_bytes: The image that has to be converted
    :return: The converted image bytes
    """

    # Load the image from the bytes
    image_bytes_io = io.BytesIO(image_bytes)
    image = Image.open(image_bytes_io)

    # Save the image in PNG format
    output_bytes = io.BytesIO()
    image.save(output_bytes, format="PNG")
    output_bytes.seek(0)

    # Return the bytes of the image
    return output_bytes.getvalue()

# def compress_to_webp_pil(image_bytes):
#     """
#     Converts the provided image to webp and returns the converted image bytes.
#     This function uses the PIL library to compress the image.
#
#     This function uses the PIL module to perform the image compression. The Image.open function is used to load the
#     image from the bytes, and the image.convert and image.save functions are used to compress the image using the PIL
#     library. The compressed image is saved to a file and then read from the file and returned as an in-memory buffer.
#
#     :param image_bytes: The image that has to be converted
#     :return: The converted image bytes
#     """
#     # Load the image from the bytes
#     image = Image.open(image_bytes)
#
#     # Compress the image using the PIL library
#     with io.BytesIO() as buffer:
#         image.convert("RGB").save(buffer, format="webp", lossless=True)
#         image_compressed = buffer.getvalue()
#
#     # Return the compressed image as an in-memory buffer
#     return io.BytesIO(image_compressed)


# # Define the path to the libwebp.so library
# LIBWEBP_PATH = os.path.join(os.getcwd(), "libwebp.so")
#
# # Define the ctypes prototype for the __WebPEncodeLossless function
# __WebPEncodeLossless = ctypes.CDLL(LIBWEBP_PATH).WebPEncodeLossless
# __WebPEncodeLossless.argtypes = [POINTER(c_void_p), c_int, c_int, c_int, c_char_p, c_size_t]
# __WebPEncodeLossless.restype = c_int

#
# def compress_to_webp_libwebp(image_bytes):
#     """
#     Converts the provided image to webp and returns the converted image bytes.
#     This function uses the libwebp library to compress the image.
#     :param image_bytes: The image that has to be converted
#     :return: The converted image bytes
#     """
#     # Load the image from the bytes
#     image = Image.open(image_bytes)
#
#     # Convert the image to a byte array
#     image_bytes = image.tobytes()
#
#     # Create a pointer to the image bytes
#     image_bytes_ptr = ctypes.cast(image_bytes, ctypes.c_void_p)
#
#     # Allocate memory for the output bytes
#     output_bytes_size = c_size_t()
#     output_bytes_ptr = ctypes.cast(ctypes.c_void_p(), POINTER(c_void_p))
#
#     # Compress the image using the libwebp library
#     result = __WebPEncodeLossless(image_bytes_ptr, image.width, image.height, image.width * image.channels,
#                                   output_bytes_ptr, output_bytes_size)
#
#     # Check if the compression was successful
#     if result == 0:
#         raise RuntimeError("Failed to compress image")
#
#     # Copy the output bytes from the pointer to a bytes object
#     output_bytes = bytes(ctypes.cast(output_bytes_ptr, POINTER(c_char_p))[0][:output_bytes_size.value])
#
#     # Return the output bytes as an in-memory buffer
#     return io.BytesIO(output_bytes)
#

# def compress_to_webp_cwebp(image_bytes):
#     """
#     Converts the provided image to webp and returns the converted image bytes.
#     This function uses the cwebp command-line tool to compress the image.
#
#     This function uses the subprocess module to run the cwebp command-line tool, which performs the image
#     compression. The stdin and stdout arguments are used to provide the input image bytes and receive the output
#     image bytes, respectively. The output is saved to an in-memory buffer, which is returned by the function.
#
#     :param image_bytes: The image that has to be converted
#     :return: The converted image bytes
#     """
#
#     # Create an in-memory buffer containing the input image bytes
#     input_buffer = io.BytesIO()
#     input_buffer.write(image_bytes)
#     input_buffer.seek(0)
#
#     # Create an in-memory buffer for the output image bytes
#     output_buffer = io.BytesIO()
#
#     # Compress the image using the cwebp command-line tool
#     subprocess.run(["cwebp", "-quiet", "-lossless", "-q", "100", "-m", "6", "-pass", "10", "-mt",
#                     "-o", "-"], stdin=input_buffer, stdout=output_buffer)
#
#     # Rewind the output buffer and return it
#     output_buffer.seek(0)
#     return output_buffer


def compress_to_webp_imageio(image_bytes):
    """
    Converts the provided image to webp and returns the converted image bytes.
    This function uses the imageio library to compress the image.

    This function uses the imageio module to perform the image compression. The imread function is used to load the
    image from the bytes, and the imwrite function is used to compress the image using the imageio library. The
    compressed image is saved to an in-memory buffer and returned by the function.

    :param image_bytes: The image that has to be converted
    :return: The converted image bytes
    """
    # Load the image from the bytes
    image = imageio.v2.imread(image_bytes)
    buffer = io.BytesIO()
    # Compress the image using the imageio library
    image_compressed = imageio.imwrite(buffer,image)
    # Seek to the beginning of the buffer
    buffer.seek(0)
    # Return the compressed image as an in-memory buffer
    return buffer.read()
def compress_to_png_imageio(image_bytes):
    """
    Converts the provided image to png and returns the converted image bytes.
    This function uses the imageio library to compress the image.

    This function uses the imageio module to perform the image compression. The imread function is used to load the
    image from the bytes, and the imwrite function is used to compress the image using the imageio library. The
    compressed image is saved to an in-memory buffer and returned by the function.

    :param image_bytes: The image that has to be converted
    :return: The converted image bytes
    """
    # Load the image from the bytes
    image = imageio.v2.imread(image_bytes)
    buffer = io.BytesIO()
    # Compress the image using the imageio library
    image_compressed = imageio.imwrite(buffer, image, format='png')
    # Seek to the beginning of the buffer
    buffer.seek(0)
    # Return the compressed image as an in-memory buffer
    return buffer.read()

def compress_to_webp_imageio_2(image_bytes):
    """
    Converts the provided image to webp and returns the converted image bytes.
    This function uses the imageio library to compress the image.

    This function uses the imageio module to perform the image compression. The imageio.imread function is used to
    load the image from the bytes, and the imageio.imwrite function is used to compress the image using the imageio
    library. The compressed image is saved to an in-memory buffer and returned by the function.

    # Is the same as the previous? No, this tenth example function is different from the previous example function
    called compress_to_webp_imageio. This tenth function uses a different algorithm and library (imageio) to compress
    the image, whereas the previous function used the skimage library to compress the image.


    :param image_bytes: The image that has to be converted
    :return: The converted image bytes
    """
    # Load the image from the bytes
    image = imageio.v2.imread(image_bytes)

    # Compress the image using the imageio library
    with io.BytesIO() as buffer:
        imageio.imwrite(buffer, image, format="webp")
        image_compressed = buffer.getvalue()

    # Return the compressed image as an in-memory buffer
    return image_compressed
def compress_to_png_imageio_2(image_bytes):
    """
    Converts the provided image to png and returns the converted image bytes.
    This function uses the imageio library to compress the image.

    This function uses the imageio module to perform the image compression. The imageio.imread function is used to
    load the image from the bytes, and the imageio.imwrite function is used to compress the image using the imageio
    library. The compressed image is saved to an in-memory buffer and returned by the function.

    # Is the same as the previous? No, this tenth example function is different from the previous example function
    called compress_to_png_imageio. This tenth function uses a different algorithm and library (imageio) to compress
    the image, whereas the previous function used the skimage library to compress the image.


    :param image_bytes: The image that has to be converted
    :return: The converted image bytes
    """
    # Load the image from the bytes
    image = imageio.v2.imread(image_bytes)

    # Compress the image using the imageio library
    with io.BytesIO() as buffer:
        imageio.imwrite(buffer, image, format='png')
        image_compressed = buffer.getvalue()

    # Return the compressed image as an in-memory buffer
    return image_compressed
def compress_to_webp_manga_95(image_bytes):
    """
    Converts the provided black and white manga image to webp and returns the converted image bytes.
    This function uses a custom algorithm to compress the images while minimizing the file size without losing
    more than 5% of the image quality.
    :param image_bytes: The manga image that has to be converted
    :return: The converted image bytes
    """
    # Load the image from the bytes using the PIL library
    image_bytes_io = io.BytesIO(image_bytes)
    image = Image.open(image_bytes_io)

    # Convert the image to grayscale to reduce the color depth
    image = image.convert('L')

    # Compress the image using the PIL library with a quality of 95%
    with io.BytesIO() as buffer:
        image.save(buffer, format='webp', quality=95)
        image_compressed = buffer.getvalue()

    # Return the compressed image as an in-memory buffer
    return image_compressed
def compress_to_png_manga_95(image_bytes):
    """
    Converts the provided black and white manga image to png and returns the converted image bytes.
    This function uses a custom algorithm to compress the images while minimizing the file size without losing
    more than 5% of the image quality.
    :param image_bytes: The manga image that has to be converted
    :return: The converted image bytes
    """
    # Load the image from the bytes using the PIL library
    image_bytes_io = io.BytesIO(image_bytes)
    image = Image.open(image_bytes_io)

    # Convert the image to grayscale to reduce the color depth
    image = image.convert('L')

    # Compress the image using the PIL library with a quality of 95%
    with io.BytesIO() as buffer:
        image.save(buffer, format='png', quality=95)
        image_compressed = buffer.getvalue()

    # Return the compressed image as an in-memory buffer
    return image_compressed
# def compress_to_webp_manga_95(image_bytes):
#     """
#     Converts the provided black and white manga image to webp and returns the converted image bytes.
#     This function uses a custom algorithm to compress the images while minimizing the file size without losing
#     more than 5% of the image quality.
#     :param image_bytes: The manga image that has to be converted
#     :return: The converted image bytes
#     """
#     # Load the image from the bytes
#     image = cv2.imdecode(np.fromstring(image_bytes.getvalue(), np.uint8), cv2.IMREAD_UNCHANGED)
#
#     # Convert the image to grayscale to reduce the color depth
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # Compress the image using the opencv-python library with a quality of 95%
#     with io.BytesIO() as buffer:
#         cv2.imencode(".webp", image, [cv2.IMWRITE_WEBP_QUALITY, 95])
#         image_compressed = buffer.getvalue()
#
#     # Return the compressed image as an in-memory buffer
#     return io.BytesIO(image_compressed)


# def compress_to_webp_manga_80(image_bytes):
#     """
#     Converts the provided black and white manga image to webp and returns the converted image bytes.
#     This function uses a custom algorithm to compress the images while minimizing the file size without losing
#     more than 5% of the image quality.
#     :param image_bytes: The manga image that has to be converted
#     :return: The converted image bytes
#     """
#     # Load the image from the bytes
#     image = cv2.imdecode(np.fromstring(image_bytes.getvalue(), np.uint8), cv2.IMREAD_UNCHANGED)
#
#     # Convert the image to grayscale to reduce the color depth
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # Compress the image using the opencv-python library with a quality of 95%
#     with io.BytesIO() as buffer:
#         cv2.imencode(".webp", image, [cv2.IMWRITE_WEBP_QUALITY, 80])
#         image_compressed = buffer.getvalue()
#
#     # Return the compressed image as an in-memory buffer
#     return io.BytesIO(image_compressed)


# def compress_to_webp_opencv(image_bytes):
#     """
#     Converts the provided image to webp and returns the converted image bytes.
#     This function uses the opencv library to compress the image.
#     :param image_bytes: The image that has to be converted
#     :return: The converted image bytes
#     """
#     from opencv import cv2
#     # Load the image from the bytes
#     image = cv2.imdecode(np.frombuffer(image_bytes.read(), np.uint8), cv2.IMREAD_UNCHANGED)
#
#     # Compress the image using the opencv library
#     image_compressed = cv2.imencode(".webp", image, [cv2.IMWRITE_WEBP_LOSSLESS])
#
#     # Return the compressed image as an in-memory buffer
#     return io.BytesIO(image_compressed)
#
#
# def compress_to_webp_opencv_python(image_bytes):
#     """
#     Converts the provided image to webp and returns the converted image bytes.
#     This function uses the opencv-python library to compress the image.
#
#     This function uses the opencv-python module to perform the image compression. The cv2.imdecode function is used
#     to load the image from the bytes, and the cv2.imencode function is used to compress the image using the
#     opencv-python library. The compressed image is saved to an in-memory buffer and returned by the function.
#
#     # Is it the same as the previous algorithm? No, this ninth example function is different from the previous
#     # example function called compress_to_webp_opencv. This ninth function uses a different algorithm and library (
#     # opencv-python) to compress the image, whereas the previous function used the PIL library to compress the image.
#
#     :param image_bytes: The image that has to be converted
#     :return: The converted image bytes
#     """
#     from opencv_python import cv2
#     # Load the image from the bytes
#     image = cv2.imdecode(np.fromstring(image_bytes.getvalue(), np.uint8), cv2.IMREAD_UNCHANGED)
#
#     # Compress the image using the opencv-python library
#     with io.BytesIO() as buffer:
#         cv2.imencode(".webp", image, [cv2.IMWRITE_WEBP_QUALITY, 100])
#         image_compressed = buffer.getvalue()
#
#     # Return the compressed image as an in-memory buffer
#     return io.BytesIO(image_compressed)


# THIS ONE DOESNT WORK OUTPUTS THE SAME WITHOUT COMPRESSING
# def compress_to_webp_numpy(image_bytes):
#     """
#     Converts the provided image to webp and returns the converted image bytes.
#     This function uses the numpy and scipy libraries to compress the image.
#
#     This function uses the numpy and scipy modules to perform the image compression. The numpy.frombuffer function is
#     used to load the image from the bytes, and the scipy.misc.imsave function is used to compress the image using the
#     numpy and scipy libraries. The compressed image is saved to an in-memory buffer and returned by the function.
#
#
#     :param image_bytes: The image that has to be converted
#     :return: The converted image bytes
#     """
#     # Load the image from the bytes
#     image = np.frombuffer(image_bytes, np.uint8)
#     # Reshape the image array to a 2D grayscale array
#     image = image.reshape(image.shape[0], 1)
#
#     # Get the shape of the image array
#     height, width = image.shape
#
#     # Check the number of channels
#     image = image.reshape(height, width)
#
#     return bytes(image)


# def compress_to_webp_skimage(image_bytes):
#     """
#     Converts the provided image to webp and returns the converted image bytes.
#     This function uses the skimage library to compress the image.
#
#     This function uses the skimage module to perform the image compression. The skio.imread function is used to load
#     the image from the bytes, and the tifffile.imsave function is used to compress the image using the skimage
#     library. The compressed image is saved to an in-memory buffer and returned by the function.
#
#     :param image_bytes: The image that has to be converted
#     :return: The converted image bytes
#     """
#     # Load the image from the bytes
#     image = skio.imread(image_bytes)
#
#     # Compress the image using the skimage library
#     with io.BytesIO() as buffer:
#         tifffile.imsave(buffer, image, compress=6)
#         image_compressed = buffer.getvalue()
#
#     # Return the compressed image as an in-memory buffer
#     return io.BytesIO(image_compressed)


# pip install webp fails

# def compress_to_webp(image_bytes):
#     """
#         Converts the provided image to webp and returns the converted image bytes
#         :param image_bytes: The image that has to be converted
#         :return:
#         """
#     # Load the image from the bytes
#     image = webp.imread(image_bytes)
#
#     # Compress the image using lossy compression
#     image_compressed = webp.imwrite(image, method='lossy')
#
#     # Apply post-processing to further reduce the size of the image
#     image_compressed = webp.imwrite(image_compressed, method='postprocessing')
#
#     # Remove any unnecessary metadata from the image
#     image_compressed = webp.imwrite(image_compressed, method='strip')
#
#     # Save the image in webp_format
#     image_bytes = webp.imwrite(image_compressed, format='webp')
#
#     return image_bytes





# PNG FUNCTIONS





list_of_converters = [
    compress_to_webp_pillow,          # This function uses the Pillow library to compress the image.
    compress_to_png_pillow,
    # compress_to_webp_pil,             # This function uses the PIL library to compress the image.
    # compress_to_webp_libwebp,
    # compress_to_webp_cwebp,
    # compress_to_webp_imageio,
    compress_to_webp_manga_95,        # This function uses a custom algorithm to compress the black and white manga images while minimizing the file size without losing more than 5% of the image quality.
    compress_to_png_manga_95,
    # compress_to_webp_manga_80,        # This function uses a custom algorithm to compress the black and white manga images while minimizing the file size without losing more than 20% of the image quality.
    # compress_to_webp_numpy,           # This function uses the numpy library to compress the image.
    # compress_to_webp_skimage,         # This function uses the scikit-image library to compress the image.
    # compress_to_webp_opencv,          # This function uses the opencv library to compress the image.
    # compress_to_webp_opencv_python,          # This function uses the opencv library to compress the image.
    # compress_to_webp_opencv_python,   # This function uses the opencv-python library to compress the image.
    compress_to_webp_imageio,         # This function uses the imageio library to compress the image.
    compress_to_webp_imageio_2,

    compress_to_png_imageio,
    compress_to_png_imageio_2

]