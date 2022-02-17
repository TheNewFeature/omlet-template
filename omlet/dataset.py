import logging
import os
import shutil

from omlet_common.storage.services import MinioStorage, DatasetStorageService

logger = logging.Logger(__name__)


class OmletDatasetLoader:
    pass


def download_dataset(object_name: str):
    logger.info(f'Loading dataset({object_name}) from remote storage..')
    service = DatasetStorageService(
        storage=MinioStorage(
            endpoint='localhost', access_key='root', secret_key='00000000'))
    file_path = os.path.join(os.path.dirname(__file__), object_name + '.zip')
    if os.path.exists(dir_path := os.path.splitext(file_path)[0]):
        logger.info(f'Dataset({object_name}) already exists on local machine.')
        return dir_path
    info = service.get(object_name, file_path=file_path)
    logger.info(f'DatasetInfo: {info}')
    shutil.unpack_archive(file_path, extract_dir=dir_path, format='zip')
    os.remove(file_path)
    return dir_path
