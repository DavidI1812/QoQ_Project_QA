import os
import runpy

# Wrapper that imports the original script (which has an unusual filename)
_path = os.path.join(os.path.dirname(__file__), 'distribution_center (1).py')
_globals = runpy.run_path(_path)

# Re-export useful classes
DistributionCenterDB = _globals.get('DistributionCenterDB')
PackageManager = _globals.get('PackageManager')
generate_random_barcode = _globals.get('generate_random_barcode')
display_menu = _globals.get('display_menu')
main = _globals.get('main')
register_package_ui = _globals.get('register_package_ui')
search_package_ui = _globals.get('search_package_ui')
update_status_ui = _globals.get('update_status_ui')
display_report = _globals.get('display_report')
generate_sample_packages = _globals.get('generate_sample_packages')

__all__ = ['DistributionCenterDB', 'PackageManager', 'generate_random_barcode', 'display_menu', 'main']

