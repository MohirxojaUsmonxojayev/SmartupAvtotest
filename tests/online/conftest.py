"""tests/online — har doim ONLINE serverda ishlaydi + `online` markeri."""
import pytest

from config.servers import resolve_server


@pytest.fixture
def server(request) -> dict:
    """Root'dagi `server` fixture'ni override qiladi — doim online (--email/--password qo'llaniladi)."""
    cfg = resolve_server(
        "online",
        request.config.getoption("--email"),
        request.config.getoption("--password"),
    )
    print(f"\n[CONFIG] Server: online | {cfg['base_url']}")
    return cfg


def pytest_collection_modifyitems(items):
    """Bu papkadagi barcha testlarga avtomatik `online` markerini qo'yadi."""
    for item in items:
        item.add_marker(pytest.mark.online)
