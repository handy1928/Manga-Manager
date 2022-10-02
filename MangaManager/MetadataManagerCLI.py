import logging
import pathlib
import sys

from MetadataManagerLib.MetadataManager import AppCli

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
    app.parse_args()
    app.loadedComicInfo_List, app.origin_LoadedcInfo = app.loadFiles()
    app.copyCInfo()
    app.saveFiles()
