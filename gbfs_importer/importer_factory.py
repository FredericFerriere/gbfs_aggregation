from gbfs_importer.importer_version_3_point_0 import ImporterVersionThreePointZero


class ImporterFactory:
    """
    This class allows the generic_importer class to get the correct versioned importer based on the version defined in
    gbfs.
    """
    @staticmethod
    def get_sub_importer(version: str):
        match version:
            case "3.0":
                return ImporterVersionThreePointZero()
            case _:
                return None
