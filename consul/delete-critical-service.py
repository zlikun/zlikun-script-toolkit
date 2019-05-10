#!/usr/bin/env python
# -- coding: utf-8 --
"""
@AUTHOR     : zlikun <zlikun-dev@hotmail.com>
@DATE       : 2019/05/10 18:00:27
@DESC       : 删除Consul中无效（critical）服务
@Language   : Python3

# 设置Linux每5分钟执行一次
$ crontab -e
*/5 * * * * python /opt/consul/delete-critical-service.py >> /opt/consul/delete.log 2 >& 1
"""

import requests

consul_service = "http://localhost:8500"

# 查询全部无效服务
with requests.get("{}/v1/health/state/critical".format(consul_service)) as response:
    response.raise_for_status()
    data = response.json()
    if not data:
        print("no critical service")
        exit(0)

    # 遍历删除之
    for item in data:
        print("deregister service {}".format(item["ServiceID"]))
        requests.put("{}/v1/agent/service/deregister/{}".format(consul_service, item["ServiceID"]))
