# Motion over WireGuard

## Installation
Note: 
```
daemon           off
stream_localhost off
```

Generate SSL certificate:
```shell
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -out /etc/motion/cert/motion.crt -keyout /etc/motion/cert/motion.key
chmod motion:motion /etc/motion/cert/motion.crt
chmod motion:motion /etc/motion/cert/motion.key
```

Edit config
```shell
# motion.conf
stream_authentication username:password
webcontrol_cert       /etc/motion/cert/motion.crt
webcontrol_key        /etc/motion/cert/motion.key
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

## Add sound recording
Check your audio devices:
```shell
sudo arecord -l
```
Get specification:
```shell
pactl list sinks | grep Specification
```

Then edit `on_movie_start.sh` with given card & device number and uncomment the line in `motion.conf`:
```
on_movie_start /etc/motion/on_movie_start.sh %f
on_movie_end   /etc/motion/on_movie_end.sh %f
```
Ensure these scripts are executable by motion.
