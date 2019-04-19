#!/bin/bash
echo "-------------PRE-CONFIG---------------"


nohup python /devicesrc/RPCWebInterface.py &
python /devicesrc/Client.py
