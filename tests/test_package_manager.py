import sqlite3
import os
import pytest

from src.distribution_center import DistributionCenterDB, PackageManager


@pytest.fixture()
def manager(tmp_path):
    db_file = tmp_path / "test_db.db"
    db = DistributionCenterDB(str(db_file))
    db.connect()
    db.initialize_database()
    mgr = PackageManager(db)
    yield mgr
    db.disconnect()
    try:
        os.remove(str(db_file))
    except Exception:
        pass


def test_register_valid(manager):
    ok = manager.register_package('TST100', 10.0, 10.0, 10.0, 10.0, 'City', 'Standard')
    assert ok


def test_reject_negative_weight(manager):
    ok = manager.register_package('NEGW', -5.0, 10.0, 10.0, 10.0, 'City', 'Standard')
    assert not ok


def test_reject_empty_destination(manager):
    ok = manager.register_package('NODEST', 5.0, 10.0, 10.0, 10.0, '', 'Standard')
    assert not ok


def test_case_insensitive_search(manager):
    manager.register_package('CaseXYZ', 5.0, 10.0, 10.0, 10.0, 'City', 'Standard')
    res = manager.search_package('casexyz')
    assert res is not None


def test_lost_frees_location(manager):
    manager.register_package('TOLOSE', 6.0, 10.0, 10.0, 10.0, 'City', 'Standard')
    # get package and location
    p = manager.search_package('TOLOSE')
    assert p is not None
    # update to Lost
    ok = manager.update_package_status('TOLOSE', 'Lost')
    assert ok
    # verify location freed
    manager.db.cursor.execute("SELECT is_occupied FROM Locations WHERE location_code = ?", (p['location'],))
    row = manager.db.cursor.fetchone()
    assert row is not None
    assert row[0] == 0


def test_reuse_released_location(manager):
    # register first package -> should take first slot A01-01
    manager.register_package('P1', 5.0, 10, 10, 10, 'City', 'Standard')
    p1 = manager.search_package('P1')
    assert p1 is not None

    # register second package -> takes next
    manager.register_package('P2', 6.0, 10, 10, 10, 'City', 'Standard')
    p2 = manager.search_package('P2')
    assert p2 is not None

    # free first package
    manager.update_package_status('P1', 'Delivered')

    # register third package -> should reuse location of P1 (deterministic ORDER BY location_id)
    manager.register_package('P3', 7.0, 10, 10, 10, 'City', 'Standard')
    p3 = manager.search_package('P3')
    assert p3 is not None
    assert p3['location'] == p1['location']
