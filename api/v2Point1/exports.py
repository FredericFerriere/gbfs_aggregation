from fastapi import APIRouter, HTTPException

from gbfs_importer.generic_importer import GenericImporter

v2point1_router = APIRouter()


@v2point1_router.get('/dummy_version_mismatch')
async def dummy_v2_test():
    """
    dummy function to illustrate behaviour when a user tries to access v2.1 endpoint whereas GBFS file format imported
    are in a different version
    :return: str: the gbfs version currently stored in db
    """
    if GenericImporter.version != "2.1":
        raise HTTPException(status_code=404, detail="Trying to access v2.1 endpoint but data stored in {} format"
                            .format(GenericImporter.version))
    return "version ok"
