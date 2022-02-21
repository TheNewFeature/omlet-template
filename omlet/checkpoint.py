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
    model.save(checkpoint_path)
    archive_path = shutil.make_archive(checkpoint_path, format='gztar', root_dir=checkpoint_path)
    service = CheckpointStorageService(storage=MinioStorage(BASE_URL, access_key='root', secret_key='00000000'))
    checkpoint = service.put(archive_path, episode=episode, session_id=config.get('Session', 0))
    print(f'[Checkpoint] Saved: {checkpoint}')

    # headers = {'Authorization': f'Bearer {config.get("Token")}'}
    request = CreateCheckpointRequest(session_id=config.get('Session', 0), object_name=checkpoint.object_name, etag=checkpoint.etag, episode=episode)
    print(f'request.dict(): {request.dict()}')
    response = requests.post(f'http://{BASE_URL}:8000/checkpoint', json=request.dict())
    print(f'Checkpoint Response: {response.status_code}')
