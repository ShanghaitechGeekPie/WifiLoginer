#!/usr/bin/fish
# credit: https://campus-rover.gitbook.io/lab-notebook/infrastructure/linux_terminal_eduroam_setup

set student_id   "for example 2090335114"
set ids_password 'your password for https://ids.shanghaitech.edu.cn/'

nmcli connection delete ShanghaiTech
nmcli connection add \
	type wifi \
	con-name "ShanghaiTech" \
	ifname wlp1s0 \
	ssid "ShanghaiTech" \
	wifi-sec.key-mgmt wpa-eap \
	802-1x.identity "$student_id" \
	802-1x.password "$ids_password" \
	802-1x.system-ca-certs yes \
	802-1x.eap "peap" \
	802-1x.phase2-auth mschapv2
nmcli connection up ShanghaiTech
