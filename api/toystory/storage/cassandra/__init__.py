"""Storage Driver"""

from toystory.storage.cassandra import driver

# Hoist classes into package namespace
Driver = driver.CassandraStorageDriver
