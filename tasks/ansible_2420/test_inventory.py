# -*- coding: utf-8 -*-




from inventory import BaseInventory


def  Test():
        """
        返回主机信息，组信息，组内主机信息
        :return:
        """
        host_list = [{
            "hostname": "testserver1",
            "ip": "102.1.1.1",
            "port": 22,
            "username": "root",
            "password": "password",
            "private_key": "/tmp/private_key",
            "become": {
                "method": "sudo",
                "user": "root",
                "pass": None,
            },
            "groups": ["group1", "group2"],
            "vars": {"sexy": "yes"},
        }, {
            "hostname": "testserver2",
            "ip": "8.8.8.8",
            "port": 2222,
            "username": "root",
            "password": "password",
            "private_key": "/tmp/private_key",
            "become": {
                "method": "su",
                "user": "root",
                "pass": "123",
            },
            "groups": ["group3", "group4"],
            "vars": {"love": "yes"},
        }]

        inventory = BaseInventory(host_list=host_list)


        print("#"*10 + "Hosts" + "#"*10)
        for host in inventory.hosts:
            print(host)


        print("#" * 10 + "Groups" + "#" * 10)
        for group in inventory.groups:
            print(group)


        print("#" * 10 + "all group hosts" + "#" * 10)
        group = inventory.get_group('all')
        print(group.hosts)


if __name__ == '__main__':
     Test()
