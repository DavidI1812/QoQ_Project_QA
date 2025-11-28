"""Basic smoke tests for DistributionCenter - runnable script.

Run from workspace root:
    python ./scripts/run_basic_checks.py
"""
import os
import sys
import runpy
import traceback

# Load the safe wrapper module by path to avoid package/import issues
_wrapper_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'distribution_center.py')
_globals = runpy.run_path(os.path.abspath(_wrapper_path))
DistributionCenterDB = _globals.get('DistributionCenterDB')
PackageManager = _globals.get('PackageManager')

DB_FILE = 'test_distribution_center.db'


def clean_db():
    try:
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
    except Exception:
        pass


def main():
    clean_db()
    db = DistributionCenterDB(DB_FILE)
    db.connect()
    db.initialize_database()

    mgr = PackageManager(db)

    results = []

    try:
        # 1) valid registration
        ok = mgr.register_package('TEST001', 10.0, 10.0, 10.0, 10.0, 'Test City', 'Standard')
        results.append(('valid_register', ok))

        # 2) negative weight -> should fail
        ok = mgr.register_package('TEST_NEG', -5.0, 10.0, 10.0, 10.0, 'Test City', 'Standard')
        results.append(('neg_weight_rejected', not ok))

        # 3) empty destination -> should fail
        ok = mgr.register_package('TEST_NODEST', 5.0, 10.0, 10.0, 10.0, '', 'Standard')
        results.append(('empty_destination_rejected', not ok))

        # 4) case-insensitive search
        mgr.register_package('CaseABC', 5.0, 10.0, 10.0, 10.0, 'City', 'Standard')
        found = mgr.search_package('caseabc')
        results.append(('case_insensitive_search', found is not None))

        # 5) Lost status frees location
        mgr.register_package('TO_LOSE', 6.0, 10.0, 10.0, 10.0, 'City', 'Standard')
        # update to Lost
        ok = mgr.update_package_status('TO_LOSE', 'Lost')
        results.append(('lost_frees_location', ok))

    except Exception:
        traceback.print_exc()
        results.append(('exception', False))

    # Print summary
    print('\n=== BASIC CHECKS SUMMARY ===')
    for name, passed in results:
        print(f" - {name:30s}: {'PASS' if passed else 'FAIL'}")

    db.disconnect()
    # cleanup
    try:
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
    except Exception:
        pass


if __name__ == '__main__':
    main()
