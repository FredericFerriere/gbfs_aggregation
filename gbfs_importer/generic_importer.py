import requests
import logging

from gbfs_importer.importer_factory import ImporterFactory

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class GbfsVersionError(Exception):
    pass


class GenericImporter:
    """
    Used to manage GBFS file imports into the DB.
    Based on the version of the file it is provided, the class will be allocated a versioned_importer by the
    importer_factory. This versioned_importer knows what format to expect to save data in db.
    """
    version: str = 'undefined'
    versioned_importer = None
    url_list = []

    @staticmethod
    def validate_version(gbfs_version: str) -> bool:
        if gbfs_version in ['3.0']:
            return True
        return False

    @staticmethod
    def import_data(gbfs_url: str):
        """
        This is the entry point to import all files.
        From gbfs we get the version number, so we can determine which file types to expect
        :param gbfs_url: the url of the gbfs file
        :return:
        """
        logger.log(level=logging.INFO, msg="Checking for GBFS files updates")

        GenericImporter.import_gbfs_file(gbfs_url)
        GenericImporter.versioned_importer.import_sub_files(GenericImporter.url_list)

    @staticmethod
    def import_gbfs_file(gbfs_url: str):
        # read main file and get version

        response = requests.get(gbfs_url)
        data = response.json()

        # check version is allowed
        file_gbfs_version = data['version']
        if GenericImporter.validate_version(file_gbfs_version):
            GenericImporter.version = file_gbfs_version
        else:
            raise GbfsVersionError('Unhandled GBFS version: {}'.format(file_gbfs_version))

        GenericImporter.versioned_importer = ImporterFactory.get_sub_importer(GenericImporter.version)
        GenericImporter.url_list = data['data']['feeds']
