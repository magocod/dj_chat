"""
in process
note: canceled exception
"""

# third-party
from channels.testing import WebsocketCommunicator

TOKENS = (
    "20fd382ed9407b31e1d5f928b5574bb4bffe6120",
    "20fd382ed9407b31e1d5f928b5574bb4bffe6130",
    "20fd382ed9407b31e1d5f928b5574bb4bffe6140",
)


async def generate_ws_comunicators(fut, tokens, room: int, consumer, route: str):
    """
    ...
    """
    communicators = []
    for token in tokens:
        communicator = WebsocketCommunicator(consumer, route)
        connected, _ = await communicator.connect()
        assert connected
        communicators.append(communicator)

    fut.set_result(communicators)
