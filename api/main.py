from .app_utility import create_app
from .v3Point0.exports import v3_router
from .v2Point1.exports import v2point1_router
from gbfs_importer.generic_importer import GenericImporter

app = create_app()
app.include_router(v3_router, prefix="/v3")
app.include_router(v2point1_router, prefix="/v2.1")


@app.get('/db_version')
async def db_version():
    """
    check the GBFS version that is currently stored in db
    :return: str: the gbfs version currently stored in db
    """
    return GenericImporter.version

