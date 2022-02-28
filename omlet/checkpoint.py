import json
import logging
import os
import requests
import shutil
import uuid
from typing import Optional

import tensorflow as tf

from omlet_common.storage.services import MinioStorage, CheckpointStorageService
from omlet_common.requests import CreateCheckpointRequest

with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
    config = json.load(f)

logger = logging.Logger(__name__)

BASE_URL = 'host.docker.internal'


def save_checkpoint(model, checkpoint_path: str, episode: Optional[int] = 0):
    """학습된 모델의 `Checkpoint`를 저장한 후, 서버의 `MinioStorage`에 등록합니다.

    1. 로컬 경로에 `Checkpoint` 파일을 저장합니다.
    2. 1에서 저장한 파일을 `MinioStorage`에 저장합니다.
    3. 2에서 얻은 `Checkpoint`의 메타데이터를 서버에 등록 요청합니다.

    Args:
        :param :py:class:`tensorflow.keras.Model` model: `Checkpoint`를 저장할 모델 객체
        :param str checkpoint_path: `Checkpoint`를 저장할 경로
        :param Optional[int] episode: `Checkpoint` 저장 시점의 학습 횟수 (epochs)
    """
    model.save(checkpoint_path)
    archive_path = shutil.make_archive(checkpoint_path, format='gztar', root_dir=checkpoint_path)
    service = CheckpointStorageService(storage=MinioStorage(BASE_URL, access_key='root', secret_key='00000000'))
    checkpoint = service.put(archive_path, episode=episode, session_id=config.get('Session', 0))
    print(f'[Checkpoint] Saved: {checkpoint}')

    request = CreateCheckpointRequest(session_id=config.get('Session', 0), object_name=checkpoint.object_name,
                                      etag=checkpoint.etag, episode=episode)
    print(f'request.dict(): {request.dict()}')
    response = requests.post(f'http://{BASE_URL}:8000/checkpoint', json=request.dict())
    print(f'Checkpoint Response: {response.status_code}')


def load_checkpoint(object_name: str):
    """저장된 `SavedModel` 형식의 데이터를 통해 모델을 복원합니다.

    Args:
        :param str object_name: 불러올 `Checkpoint`의 `object_name`

    Returns:
        :returns: :py:class:`tensorflow.keras.Model`
    """
    service = CheckpointStorageService(
        storage=MinioStorage(
            endpoint=BASE_URL, access_key='root', secret_key='00000000'
        ))
    file_path = os.path.join(os.path.dirname(__file__), str(uuid.uuid4()) + '.gztar')
    info = service.get(object_name, file_path=file_path)
    logger.info(f'CheckpointInfo: {info}')
    if not os.path.exists(dir_path := os.path.splitext(file_path)[0]):
        os.mkdir(dir_path)
    shutil.unpack_archive(file_path, extract_dir=dir_path, format='gztar')

    return tf.keras.models.load_model(dir_path)
