#!/bin/bash
# sudo chroot /home/kali/Development/CTF/dev/qctf-2017/tasks/passengers/service
echo "[*] You have 30 seconds! Hurry up!"
echo ""
cd /home/kali/Development/CTF/dev/qctf-2017/tasks/passengers/service/
bash -c "timeout 30s /home/kali/Development/CTF/dev/qctf-2017/tasks/passengers/service/main $1"
# echo "Your session is finished"