from .wakeonlan import BROADCAST_IP
from .wakeonlan import DEFAULT_PORT
from .wakeonlan import create_magic_packet
from .wakeonlan import main
from .wakeonlan import send_magic_packet


__all__ = (
    "BROADCAST_IP",
    "DEFAULT_PORT",
    "create_magic_packet",
    "send_magic_packet",
    "main",
)
