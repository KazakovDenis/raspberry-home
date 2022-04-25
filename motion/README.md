# Motion over WireGuard

## Installation
Note: 
```
daemon           off
stream_localhost off
```

Edit config
```shell
# motion.conf
webcontrol_authentication username:password
stream_authentication username:password
```

Install Motion:
```shell
apt install motion
cp /etc/motion/motion.conf /etc/motion/backup.conf
cp motion.conf /etc/motion/motion.conf
systemctl enable motion
ufw allow 8080/tcp "Motion"
```

Add a rule on a WireGuard server:
```shell
ufw route allow in on wg0 proto tcp to <wireguard-peer-ip> port 8080 "Motion"
```

## Usage
Visit [http://wireguard-peer-ip:8080](http://wireguard-peer-ip:8080)
