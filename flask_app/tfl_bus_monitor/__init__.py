"""
tfl_bus_monitor - download bus data from TFL
"""
from .tfl_bus_monitor import TFLBusMonitor
get_stops = TFLBusMonitor().get_stops
