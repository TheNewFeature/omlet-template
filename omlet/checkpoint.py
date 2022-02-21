import json
import os
import shutil
from typing import Optional

from omlet_common.storage.services import MinioStorage, CheckpointStorageService

with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
    config = json.load(f)


def save(model, checkpoint_path: str, episode: Optional[int] = 0):
    model.save(checkpoint_path)
    archive_path = shutil.make_archive(checkpoint_path, format='gztar', root_dir=checkpoint_path)
    service = CheckpointStorageService(storage=MinioStorage('localhost', access_key='root', secret_key='00000000'))
    checkpoint = service.put(archive_path, episode=episode, session_id=config.get('Session', 0))
    print(f'[Checkpoint] Saved: {checkpoint}')
