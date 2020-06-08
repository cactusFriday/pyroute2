import json
import socket
from pyroute2 import NDB
from pyroute2.common import basestring
from pyroute2.ndb.transport import Messenger, Transport


def init(config):

    if isinstance(config, basestring):
        config = json.loads(config)
    else:
        config = json.load(config)
    hostname = config['local'].get('hostname', socket.gethostname())
    messenger = Messenger(Transport(config['local']['address'],
                                    config['local']['port']))

    for target in config['local'].get('targets', []):
        messenger.targets.add(target)

    if not messenger.targets:
        messenger.targets.add(hostname)

    for neighbour in config['neighbours']:
        messenger.add_neighbour(*neighbour)

    sources = config['local'].get('sources')
    if sources is None:
        sources = [{'target': hostname, 'kind': 'local'}]

    return NDB(log=config.get('log', 'debug'),
               sources=sources,
               messenger=messenger)
