#!/usr/bin/python

import sys
sys.path.append('../..')

from server import db
from common import ssh

def main(message):

	if message is None:
		return None
	desc = message.get('desc')
	if desc is None:
		return None
	id_ = message.get('id')
	if id_ is None:
		return None

	hosts = ssh.init(desc)

	master = ssh.filterName('hadoop_master', 'hostname')
	slave = ssh.filterName('hadoop_slave', 'hostname')

	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs stop namenode', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/hadoop-daemon.sh --config /usr/local/hadoop/etc/hadoop --script hdfs stop datanode', False, *slave)
	ssh.cmd('sudo /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop stop resourcemanager', False, *master)
	ssh.cmd('sudo /usr/local/hadoop/sbin/yarn-daemon.sh --config /usr/local/hadoop/etc/hadoop stop nodemanager', False, *slave)

	ssh.close()

	db.u_cluster_update_status(id_, 'S')

if __name__ == '__main__':
	main()
