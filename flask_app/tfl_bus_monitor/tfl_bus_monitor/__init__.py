"""
tfl_bus_monitor - download bus data from TFL
"""
__author__ = 'David Klein'
__email__ = 'david@soinkleined.com'
__version__ = '0.4'
from .tfl_bus_monitor import TFLBusMonitor, get_config_path
get_stops = TFLBusMonitor().get_stops
