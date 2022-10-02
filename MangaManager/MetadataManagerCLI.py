import argparse
import logging
import os
import pathlib
import sys

from MetadataManagerLib.MetadataManager import AppCli
def is_dir_path(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
if __name__ == '__main__':
    # <Logger>
    logger = logging.getLogger()
    logging.getLogger('PIL').setLevel(logging.WARNING)
    # formatter = logging.Formatter()

    PROJECT_PATH = pathlib.Path(__file__).parent
    # rotating_file_handler = RotatingFileHandler(f"{PROJECT_PATH}/logs/MangaManager.log", maxBytes=5725760,
    #                                             backupCount=2)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s',
                        handlers=[logging.StreamHandler(sys.stdout)]
                        # filename='/tmp/myapp.log'
                        )
    # logger.debug('DEBUG LEVEL - MAIN MODULE')
    # logger.info('INFO LEVEL - MAIN MODULE\n\n')
    # </Logger>

    app = AppCli()
    """
            Parses the argument provided on the execution of the script.

            **AppCli.copyFrom** The path to the origin file to copy from\n
            **AppCli.copyTo** The path to the destination paths\n
            **AppCli.keepNumeration** 3 options {'numeration','volume','chapter'}Whether to keep numeration from destination path or remove when pasting\n
            """
    parser = argparse.ArgumentParser()

    parser.add_argument("--copyfrom", help="The path to the file you want to copy the metatada from.\n "
                                           "(Volume and number are not parsed)", type=is_dir_path,
                        metavar="<path>")
    parser.add_argument("--copyto", type=is_dir_path, help="The path of the files to modify."
                                                           " (Accepts shell-style wildcards)",
                        metavar="<path>", nargs="+")
    parser.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.INFO)

    # parser = argparse.ArgumentParser(description='some description')

    list_of_choices = ["numeration", "volume", "chapter"]
    parser.add_argument("--keep",
                        help="Should the modified file keep the numbering (volume, chapter number or both)",
                        choices=list_of_choices,
                        dest="arg_keep_value")
    app.args = parser.parse_args()
    logger.setLevel(app.args.loglevel)
    from glob import glob

    if app.args.copyfrom:
        app.origin_path = glob(app.args.copyfrom)[0]
    if app.args.copyto:
        if isinstance(app.args.copyto, list):
            selected_files = app.args.copyto
        else:
            selected_files = glob(app.args.copyto)
        app.selected_files = selected_files

    app.keepNumeration = app.args.arg_keep_value

    app.loadedComicInfo_List, app.origin_LoadedcInfo = app.loadFiles()
    app.copyCInfo()
    app.saveFiles()
