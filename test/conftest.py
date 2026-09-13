from __future__ import annotations

import sys
import types


protocol = types.ModuleType("protocol")
base = types.ModuleType("protocol.base")
credential_guard = types.ModuleType("protocol.credential_guard")
class ProtocolProvider:
    def __init__(self, *args, **kwargs):
        del args, kwargs


base.ProtocolProvider = ProtocolProvider
credential_guard.get_adapter_credential_status = lambda _name, config: {
    "configured": bool((config or {}).get("enabled")),
    "missing_fields": [],
}
protocol.base = base
protocol.credential_guard = credential_guard
sys.modules.setdefault("protocol", protocol)
sys.modules.setdefault("protocol.base", base)
sys.modules.setdefault("protocol.credential_guard", credential_guard)
