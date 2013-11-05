import zmq

import logging
log = logging.getLogger("app." + __name__)

ZMQ_SOCKET_LINGER = 100

context = zmq.Context()
context.linger = ZMQ_SOCKET_LINGER


def reset_zmq_context(**kwargs):
    log.debug("Resetting ZMQ Context")
    reset_context()


def get_context():
    global context
    if context.closed:
        context = zmq.Context()
        context.linger = ZMQ_SOCKET_LINGER
    return context


def reset_context():
    global context
    context.term()
    context = zmq.Context()
    context.linger = ZMQ_SOCKET_LINGER
