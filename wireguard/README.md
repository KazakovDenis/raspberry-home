# VPN with WireGuard

## Server
### Installation
Ubuntu 20.04 and higher:
```shell
ssh user@server
# Install 
apt update && apt upgrade 
apt install wireguard
# Allow port forwarding
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p
# Generate server keys
wg genkey | tee /etc/wireguard/privatekey | wg pubkey | tee /etc/wireguard/publickey
```

### Configuration
Replace variables in the config and load to a server:
```shell
cp wg0.server.conf backup.conf
scp wg0.server.conf user@server:/etc/wireguard/wg0.conf
scp backup.conf user@server:/etc/wireguard/
```

### Usage
First start (without peers):
```shell
wg-quick up wg0
systemctl enable wg-quick@wg0
wg show wg0
```

To reload configuration execute:
```shell
wg-quick down wg0
cp backup.conf wg0.conf
wg-quick up wg0
```

### [Configure firewall](https://www.procustodibus.com/blog/2021/05/wireguard-ufw/#hub-and-spoke-steps)

## Linux client
### Installation
Ubuntu 20.04 and higher:
```shell
# Install
apt update && apt upgrade 
apt install wireguard
# Generate client keys
wg genkey | tee /etc/wireguard/privatekey | wg pubkey | tee /etc/wireguard/publickey
```

### Configuration
Replace variables in `wg0.client.conf` and copy to `/etc`:
```shell
cp wg0.client.conf /etc/wireguard/wg0.conf
cp wg0.client.conf /etc/wireguard/backup.conf
```

Then get the next ip from a server config and set a peer public key there.
**Restart a server**.

### Usage
Start and connect to a server:
```shell
wg-quick up wg0
systemctl enable wg-quick@wg0
wg show wg0
```

## Mobile client
### Installation
Download Wireguard from your application store.

### Configuration
Generate keys for a mobile client:
```shell
wg genkey | tee /etc/wireguard/mobile/privatekey | wg pubkey | tee /etc/wireguard/mobile/publickey
```

Replace variables in `wg0.client.conf` and copy to `/etc`:
```shell
cp wg0.client.conf /etc/wireguard/mobile/wg0.conf
```

Then get the next ip from a server config and set a peer public key there.
**Restart a server**.

Create a QR-code:
```shell
apt install qrencode
qrencode -t ansiutf8 < /etc/wireguard/mobile/wg0.conf
```

### Usage
Open an app on your mobile and scan a QR-code.
