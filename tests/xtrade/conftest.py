"""tests/xtrade — har doim XTRADE serverda ishlaydi + `xtrade` markeri."""
import pytest

from config.servers import resolve_server


@pytest.fixture
def server(request) -> dict:
    """Root'dagi `server` fixture'ni override qiladi — doim xtrade (--email/--password qo'llaniladi)."""
    cfg = resolve_server(
        "xtrade",
        request.config.getoption("--email"),
        request.config.getoption("--password"),
    )
    print(f"\n[CONFIG] Server: xtrade | {cfg['base_url']}")
    return cfg


def pytest_collection_modifyitems(items):
    """Bu papkadagi barcha testlarga avtomatik `xtrade` markerini qo'yadi."""
    for item in items:
        item.add_marker(pytest.mark.xtrade)
