# Motion over WireGuard

## Installation
Note: 
```
daemon           off
stream_localhost off
```

Generate SSL certificate:
```shell
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -out motion.crt -keyout motion.key
chmod motion:motion motion.crt
chmod motion:motion motion.key
```

Edit config
```shell
# motion.conf
stream_authentication username:password
webcontrol_cert       /full/path/to/certificate.pem
webcontrol_key        /full/path/to/privatekey.pem
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
