import json

from omlet_common.message_queue import RabbitQueue

# with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
#     config = json.load(f)


class OmletBoard:
    def __init__(self, hostname: str = '', port: int = 5672):
        self._queue = RabbitQueue(host=hostname, port=port)

    def write(self, routing_key: str, **kwargs):
        message = json.dumps(kwargs)
        self._queue.publish(message=message, routing_key=routing_key)
