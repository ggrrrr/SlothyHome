# http://www.deanmao.com/2012/08/10/uploading-sketches-to-the-arduino-on-the-pi/

## WiFi router

### Update OS
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install vim
sudo apt install dnsmasq hostapd
sudo apt-get install arduino-mk 
sudo apt-get install git 
sudo apt-get install python3-pip

python3 -m pip install paho.mqtt
python3 -m pip install pySerial
python3 -m pip install requests
```

### Modify file `/etc/sysctl.conf`
```
net.ipv4.ip_forward=1
```
### NAT traffic
```
sudo iptables -t nat -A POSTROUTING -j MASQUERADE
```

### Add static IP for WiFi interface: file `/etc/dhcpcd.conf`

```
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
```

### DHCPD 
### Move default config
```
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
```
### new contenet file `/etc/dnsmasq.conf`
```
interface=wlan0      # Use the require wireless interface - usually wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
```
### file `/etc/hostapd/hostapd.conf`
```
interface=wlan0
driver=nl80211
ssid=pi-wifi
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=peshovotohihi
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```
### Add file /etc/default/hostapd
```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```
### prep services
```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
```


### Restart dhcp client deamon
```
sudo systemctl restart dhcpcd
sudo systemctl reload dnsmasq
```
