"""WSGI Transport Driver"""

from toystory.transport.falcon import driver

# Hoist into package namespace
Driver = driver.DriverBase
