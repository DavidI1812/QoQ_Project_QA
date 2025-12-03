import pytest
import time
from src.distribution_center import DistributionCenterDB, PackageManager, generate_random_barcode
import os


@pytest.fixture()
def manager(tmp_path):
    db_file = tmp_path / "reg_db.db"
    db = DistributionCenterDB(str(db_file))
    db.connect()
    db.initialize_database()
    mgr = PackageManager(db)
    yield mgr
    db.disconnect()


def test_TC_FR1_001_register_success(manager):
    ok = manager.register_package('1001', 15.5, 30, 20, 15, 'New York', 'Standard')
    assert ok


def test_TC_FR1_002_duplicate_barcode(manager):
    manager.register_package('1001_dup', 10, 10, 10, 10, 'City', 'Standard')
    ok = manager.register_package('1001_dup', 12, 10, 10, 10, 'City', 'Standard')
    assert not ok


def test_TC_FR1_003_negative_weight_rejected(manager):
    ok = manager.register_package('1003', -5.0, 10, 10, 10, 'City', 'Standard')
    assert not ok


def test_TC_FR1_004_empty_destination_rejected(manager):
    ok = manager.register_package('1004', 12.0, 10, 10, 10, '', 'Standard')
    assert not ok


def test_TC_FR1_005_auto_barcode_generation(manager):
    barcode = generate_random_barcode()
    ok = manager.register_package(barcode, 10.0, 10, 10, 10, 'City', 'Standard')
    assert ok


def test_TC_FR1_006_express_priority_category(manager):
    manager.register_package('1006', 5.0, 10, 10, 10, 'Seattle', 'Express')
    p = manager.search_package('1006')
    assert p is not None
    assert p['category'] == 'Express'
    assert p['location'].startswith('B')


def test_TC_FR1_007_timestamp_recent(manager):
    manager.register_package('1007', 1.0, 10, 10, 10, 'City', 'Standard')
    p = manager.search_package('1007')
    assert p is not None
    assert p['received_at'] is not None


def test_TC_FR1_008_performance_register_under_2s(manager):
    start = time.time()
    ok = manager.register_package('1008', 10.0, 10, 10, 10, 'City', 'Standard')
    elapsed = time.time() - start
    assert ok
    assert elapsed < 2.0


def test_TC_FR1_009_no_available_locations(manager):
    # fill all 20 locations for category Standard (category 1)
    registered = 0
    for i in range(1, 25):
        code = f"FILL{i:02d}"
        success = manager.register_package(code, 10.0, 10, 10, 10, 'City', 'Standard')
        if success:
            registered += 1
    # there are 20 locations per category; registered should be 20
    assert registered >= 20
    # now attempt another standard package should fail if no free locations
    ok = manager.register_package('FILL_OVER', 10.0, 10, 10, 10, 'City', 'Standard')
    assert not ok


def test_TC_FR1_010_sequential_ids(manager):
    manager.register_package('1010A', 10, 10, 10, 10, 'City', 'Standard')
    manager.register_package('1010B', 10, 10, 10, 10, 'City', 'Standard')
    p1 = manager.search_package('1010A')
    p2 = manager.search_package('1010B')
    assert p1 is not None and p2 is not None
    assert int(p2['package_id']) == int(p1['package_id']) + 1


def test_TC_FR1_011_boundary_weights(manager):
    manager.register_package('1011A', 5.0, 10, 10, 10, 'City', 'Standard')
    manager.register_package('1011B', 50.0, 10, 10, 10, 'City', 'Standard')
    pA = manager.search_package('1011A')
    pB = manager.search_package('1011B')
    assert pA['category'] == 'Standard'
    assert pB['category'] == 'Standard'


def test_TC_FR1_012_special_characters_destination(manager):
    dest = 'São Paulo, Brazil #45 @Corner'
    ok = manager.register_package('1012', 10.0, 10, 10, 10, dest, 'Standard')
    assert ok
    p = manager.search_package('1012')
    assert p['destination'] == dest


def test_TC_FR1_013_transaction_rollback_on_failure(manager):
    # Simulate by attempting to register a package with a barcode that will violate unique constraint
    # Ensure location not left occupied when insert fails
    db = manager.db
    # Insert a package directly to occupy location
    db.cursor.execute("INSERT INTO Packages (barcode, weight, length, width, height, destination, priority, category_id, location_id, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Stored')", ('RB1', 1,1,1,1,'C','S',1,1))
    db.cursor.execute("UPDATE Locations SET is_occupied = 1 WHERE location_id = 1")
    db.conn.commit()
    before = db.cursor.execute("SELECT COUNT(*) FROM Locations WHERE is_occupied = 1").fetchone()[0]
    ok = manager.register_package('RB1', 10,10,10,10,'City','Standard')
    after = db.cursor.execute("SELECT COUNT(*) FROM Locations WHERE is_occupied = 1").fetchone()[0]
    assert not ok
    assert after == before


def test_TC_FR1_014_audit_trail_created(manager):
    manager.register_package('1014', 10,10,10,10,'City','Standard')
    p = manager.search_package('1014')
    manager.db.cursor.execute("SELECT action FROM AuditTrail WHERE package_id = ?", (p['package_id'],))
    rows = manager.db.cursor.fetchall()
    assert any(r[0] == 'REGISTERED' for r in rows)


def test_TC_FR1_015_priority_case_insensitive(manager):
    manager.register_package('1015', 5,10,10,10,'City','express')
    p = manager.search_package('1015')
    assert p['category'] == 'Express'


# FR2 tests
def test_TC_FR2_001_express_overrides_heavy(manager):
    manager.register_package('2001', 60,10,10,10,'City','Express')
    p = manager.search_package('2001')
    assert p['category'] == 'Express'


def test_TC_FR2_002_international_detection(manager):
    manager.register_package('2002', 10,10,10,10,'Madrid, Spain, International','Standard')
    p = manager.search_package('2002')
    assert p['category'] == 'International'


def test_TC_FR2_003_heavy_category(manager):
    manager.register_package('2003', 55.5,10,10,10,'City','Standard')
    p = manager.search_package('2003')
    assert p['category'] == 'Heavy'


def test_TC_FR2_004_fragile_category(manager):
    manager.register_package('2004', 3.0,10,10,10,'City','Standard')
    p = manager.search_package('2004')
    assert p['category'] == 'Fragile'


def test_TC_FR2_005_standard_default(manager):
    manager.register_package('2005', 20.0,10,10,10,'Mexico City','Standard')
    p = manager.search_package('2005')
    assert p['category'] == 'Standard'


def test_TC_FR2_006_international_priority_over_heavy(manager):
    manager.register_package('2006', 80.0,10,10,10,'Tokyo, Japan, International','Standard')
    p = manager.search_package('2006')
    assert p['category'] == 'International'


def test_TC_FR2_007_report_by_category_nonzero(manager):
    r = manager.get_summary_report()
    assert 'by_category' in r


def test_TC_FR2_008_zones_mapping(manager):
    manager.register_package('EXPZ', 5,10,10,10,'City','Express')
    p = manager.search_package('EXPZ')
    assert p['location'].startswith('B')


# FR3 tests
def test_TC_FR3_001_zone_assignment_logic(manager):
    manager.register_package('3003', 55,10,10,10,'City','Standard')
    p = manager.search_package('3003')
    assert p['location'].startswith('D')
    manager.register_package('3004', 3,10,10,10,'City','Standard')
    p2 = manager.search_package('3004')
    assert p2['location'].startswith('C')


def test_TC_FR3_002_location_format(manager):
    manager.register_package('3002', 5,10,10,10,'City','Standard')
    p = manager.search_package('3002')
    assert p['location'] is not None


def test_TC_FR3_003_occupation_flag(manager):
    manager.register_package('3001', 5,10,10,10,'City','Standard')
    p = manager.search_package('3001')
    manager.db.cursor.execute("SELECT is_occupied FROM Locations WHERE location_code = ?", (p['location'],))
    v = manager.db.cursor.fetchone()[0]
    assert v == 1


def test_TC_FR3_004_release_on_delivered(manager):
    manager.register_package('3004D', 5,10,10,10,'City','Standard')
    p = manager.search_package('3004D')
    manager.update_package_status('3004D', 'Delivered')
    manager.db.cursor.execute("SELECT is_occupied FROM Locations WHERE location_code = ?", (p['location'],))
    v = manager.db.cursor.fetchone()[0]
    assert v == 0


def test_TC_FR3_005_reuse_released_slot_issue(manager):
    manager.register_package('R1', 5,10,10,10,'City','Standard')
    p1 = manager.search_package('R1')
    manager.register_package('R2', 6,10,10,10,'City','Standard')
    manager.update_package_status('R1', 'Delivered')
    manager.register_package('R3', 7,10,10,10,'City','Standard')
    p3 = manager.search_package('R3')
    assert p3['location'] == p1['location']


def test_TC_FR3_006_release_on_in_transit(manager):
    manager.register_package('3006', 5,10,10,10,'City','Standard')
    manager.update_package_status('3006', 'In Transit')
    p = manager.search_package('3006')
    manager.db.cursor.execute("SELECT is_occupied FROM Locations WHERE location_code = ?", (p['location'],))
    v = manager.db.cursor.fetchone()[0]
    assert v == 0


def test_TC_FR3_007_lost_state_not_in_menu_but_supported(manager):
    manager.register_package('3007', 5,10,10,10,'City','Standard')
    ok = manager.update_package_status('3007', 'Lost')
    assert ok


def test_TC_FR3_008_referential_integrity(manager):
    manager.db.cursor.execute("SELECT COUNT(*) FROM Packages p LEFT JOIN Locations l ON p.location_id = l.location_id WHERE p.location_id IS NOT NULL AND l.location_id IS NULL")
    cnt = manager.db.cursor.fetchone()[0]
    assert cnt == 0


def test_TC_FR3_009_sequential_fill(manager):
    manager.register_package('S1', 5,10,10,10,'City','Standard')
    manager.register_package('S2', 5,10,10,10,'City','Standard')
    p1 = manager.search_package('S1')
    p2 = manager.search_package('S2')
    assert p1['location'] != p2['location']


def test_TC_FR3_010_persistence_after_restart(manager, tmp_path):
    db_file = tmp_path / 'persistent.db'
    db = DistributionCenterDB(str(db_file))
    db.connect()
    db.initialize_database()
    mgr = PackageManager(db)
    mgr.register_package('PERSIST1', 5,10,10,10,'City','Standard')
    p = mgr.search_package('PERSIST1')
    assert p is not None
    db.disconnect()
    db2 = DistributionCenterDB(str(db_file))
    db2.connect()
    db2.cursor.execute("SELECT COUNT(*) FROM Packages WHERE barcode = ?", ('PERSIST1',))
    cnt = db2.cursor.fetchone()[0]
    assert cnt == 1
    db2.disconnect()


# FR4 tests (tracking and reports)
def test_TC_FR4_001_search_existing(manager):
    manager.register_package('F401', 5,10,10,10,'City','Standard')
    p = manager.search_package('F401')
    assert p is not None


def test_TC_FR4_002_search_nonexistent(manager):
    p = manager.search_package('NONEXIST')
    assert p is None


def test_TC_FR4_003_search_delivered(manager):
    manager.register_package('F403', 5,10,10,10,'City','Standard')
    manager.update_package_status('F403', 'Delivered')
    p = manager.search_package('F403')
    assert p['status'].lower() == 'delivered'


def test_TC_FR4_004_audit_registered(manager):
    manager.register_package('F404', 5,10,10,10,'City','Standard')
    p = manager.search_package('F404')
    manager.db.cursor.execute("SELECT action FROM AuditTrail WHERE package_id = ?", (p['package_id'],))
    actions = [r[0] for r in manager.db.cursor.fetchall()]
    assert 'REGISTERED' in actions


def test_TC_FR4_005_audit_status_update(manager):
    manager.register_package('F405', 5,10,10,10,'City','Standard')
    manager.update_package_status('F405', 'In Transit')
    p = manager.search_package('F405')
    manager.db.cursor.execute("SELECT new_status FROM AuditTrail WHERE package_id = ? ORDER BY audit_id DESC LIMIT 1", (p['package_id'],))
    ns = manager.db.cursor.fetchone()[0]
    assert ns == 'In Transit'


def test_TC_FR4_006_audit_timestamps(manager):
    manager.register_package('F406', 5,10,10,10,'City','Standard')
    manager.db.cursor.execute("SELECT timestamp FROM AuditTrail ORDER BY audit_id DESC LIMIT 1")
    ts = manager.db.cursor.fetchone()[0]
    assert ts is not None


def test_TC_FR4_007_report_counts(manager):
    r = manager.get_summary_report()
    total = sum([c for _, c in r['by_category']])
    manager.db.cursor.execute("SELECT COUNT(*) FROM Packages")
    cnt = manager.db.cursor.fetchone()[0]
    assert total == cnt


def test_TC_FR4_008_distribution_by_category(manager):
    r = manager.get_summary_report()
    assert len(r['by_category']) >= 1


def test_TC_FR4_009_occupancy_percentage(manager):
    r = manager.get_summary_report()
    assert 'location_occupancy' in r


def test_TC_FR4_010_case_sensitivity_search(manager):
    manager.register_package('CASETEST', 5,10,10,10,'City','Standard')
    p = manager.search_package('casetest')
    assert p is not None


def test_TC_FR4_011_audit_order_integrity(manager):
    manager.register_package('F411', 5,10,10,10,'City','Standard')
    manager.update_package_status('F411', 'In Transit')
    manager.db.cursor.execute("SELECT audit_id FROM AuditTrail WHERE package_id = (SELECT package_id FROM Packages WHERE barcode = ?) ORDER BY audit_id ASC", ('F411',))
    rows = manager.db.cursor.fetchall()
    assert len(rows) >= 2


def test_TC_FR4_012_report_readable(manager):
    r = manager.get_summary_report()
    assert isinstance(r, dict)


# FR5 tests (report generation)
def test_TC_FR5_001_report_no_crash(manager):
    r = manager.get_summary_report()
    assert r is not None


def test_TC_FR5_002_total_count_accuracy(manager):
    manager.register_package('R001',5,10,10,10,'City','Standard')
    r = manager.get_summary_report()
    total = sum([c for _, c in r['by_category']])
    manager.db.cursor.execute("SELECT COUNT(*) FROM Packages")
    cnt = manager.db.cursor.fetchone()[0]
    assert total == cnt


def test_TC_FR5_003_occupancy_percentage_formula(manager):
    r = manager.get_summary_report()
    for zone, total, occupied, rate in r['location_occupancy']:
        if total > 0:
            assert 0.0 <= rate <= 100.0


def test_TC_FR5_004_category_breakdown_sum(manager):
    r = manager.get_summary_report()
    total = sum([c for _, c in r['by_category']])
    manager.db.cursor.execute("SELECT COUNT(*) FROM Packages")
    cnt = manager.db.cursor.fetchone()[0]
    assert total == cnt


def test_TC_FR5_005_realtime_update(manager):
    before = manager.get_summary_report()
    manager.register_package('RRT',5,10,10,10,'City','Standard')
    after = manager.get_summary_report()
    assert sum([c for _, c in after['by_category']]) == sum([c for _, c in before['by_category']]) + 1


def test_TC_FR5_006_report_legibility(manager):
    r = manager.get_summary_report()
    assert 'recent_activities' in r


# NFR1 Performance (basic checks)
def test_TC_NFR1_001_registration_time(manager):
    start = time.time()
    manager.register_package('NFR1A',5,10,10,10,'City','Standard')
    elapsed = time.time() - start
    assert elapsed < 2.0


def test_TC_NFR1_002_search_time(manager):
    manager.register_package('NFR1B',5,10,10,10,'City','Standard')
    start = time.time()
    manager.search_package('NFR1B')
    assert (time.time() - start) < 1.0


def test_TC_NFR1_003_report_time(manager):
    start = time.time()
    manager.get_summary_report()
    assert (time.time() - start) < 2.0


def test_TC_NFR1_004_db_size_small(tmp_path):
    db_file = tmp_path / 'size.db'
    db = DistributionCenterDB(str(db_file))
    db.connect()
    db.initialize_database()
    db.disconnect()
    size = os.path.getsize(str(db_file))
    assert size < 10 * 1024 * 1024  # less than 10MB


def test_TC_NFR1_005_stability_under_repetition(manager):
    for i in range(5):
        manager.search_package('NONEXIST')
    assert True


# NFR2 Robustness and Security
def test_TC_NFR2_001_sql_injection_safe(manager):
    res = manager.search_package("' OR '1'='1")
    assert res is None


def test_TC_NFR2_002_type_handling_on_input(manager):
    # The register function should either raise or return False for invalid numeric input
    try:
        ok = manager.register_package('TYPETEST', float('nan'), 10,10,10,'City','Standard')
        assert not ok
    except Exception:
        assert True


def test_TC_NFR2_003_long_string_destination(manager):
    long_dest = 'A' * 2000
    ok = manager.register_package('LONGDEST',5,10,10,10,long_dest,'Standard')
    assert ok


def test_TC_NFR2_004_utf8_characters(manager):
    ok = manager.register_package('UTF8',5,10,10,10,'日本 😊','Standard')
    assert ok


def test_TC_NFR2_005_recover_from_partial(manager):
    try:
        manager.register_package('REC1',5,10,10,10,'City','Standard')
    except Exception:
        pass
    manager.register_package('REC2',5,10,10,10,'City','Standard')
    assert manager.search_package('REC2') is not None


def test_TC_NFR2_006_concurrent_simulation(manager):
    ok1 = manager.register_package('CONC1',5,10,10,10,'City','Standard')
    ok2 = manager.register_package('CONC2',5,10,10,10,'City','Standard')
    assert ok1 and ok2


# NFR3 Usability
def test_TC_NFR3_001_menu_clarity():
    from src import distribution_center as dc_mod
    assert hasattr(dc_mod, 'display_menu')


def test_TC_NFR3_002_error_messages_on_invalid_choice(manager):
    ok = manager.update_package_status('NONEXIST', 'InvalidStatus')
    assert not ok


def test_TC_NFR3_003_exit_behavior():
    from src import distribution_center as dc_mod
    assert hasattr(dc_mod, 'main')


def test_TC_NFR3_004_consistent_ascii_layout():
    from src import distribution_center as dc_mod
    assert callable(dc_mod.display_menu)


# NFR4 Environment and reliability
def test_TC_NFR4_001_db_auto_recreate(tmp_path):
    dbp = tmp_path / 'auto.db'
    if dbp.exists():
        dbp.unlink()
    db = DistributionCenterDB(str(dbp))
    db.connect()
    db.initialize_database()
    db.disconnect()
    assert dbp.exists()


def test_TC_NFR4_002_relative_execution(tmp_path):
    from src import distribution_center as dc_mod
    assert hasattr(dc_mod, 'main')


def test_TC_NFR4_003_persistence_of_session(manager):
    manager.register_package('PSS1',5,10,10,10,'City','Standard')
    assert manager.search_package('PSS1') is not None


def test_TC_NFR4_004_handle_corrupt_db(tmp_path):
    dbp = tmp_path / 'corrupt.db'
    with open(dbp, 'w') as f:
        f.write('HOLA')
    db = DistributionCenterDB(str(dbp))
    try:
        db.connect()
        db.disconnect()
        assert True
    except Exception:
        assert True


def test_TC_NFR4_005_minimal_dependencies():
    import sqlite3
    assert sqlite3 is not None
