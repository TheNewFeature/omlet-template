import json
import os
import requests
import shutil
from typing import Optional

from omlet_common.storage.services import MinioStorage, CheckpointStorageService
from omlet_common.requests import CreateCheckpointRequest

with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
    config = json.load(f)

BASE_URL = 'host.docker.internal'


def save(model, checkpoint_path: str, episode: Optional[int] = 0):
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
