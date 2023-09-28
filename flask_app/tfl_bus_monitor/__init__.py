"""
tfl_bus_monitor - download bus data from TFL
"""
__author__ = 'David Klein'
__version__ = '0.1'
from .tfl_bus_monitor import TFLBusMonitor
get_stops = TFLBusMonitor().get_stops
