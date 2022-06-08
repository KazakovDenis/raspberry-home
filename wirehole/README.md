# VPN + DNS + Adblock

## Installation 
1. Create VM
2. Add new user, copy his ssh key to the server and login  
https://losst.ru/kak-sozdat-polzovatelya-linux

3. Configure SSHD / UFW
Edit /etc/ssh/sshd_config
```shell
Port <some another port>
PermitRootLogin no
PasswordAuthentication no
```

Deny all incoming traffic except specified for SSH
```shell
sudo ufw default deny incoming 
sudo ufw default allow outgoing 
sudo ufw allow <some another port> comment "SSH"
```

4. Clone and set up Wirehole, set peers number
```shell
cd opt && git clone https://github.com/IAmStoxe/wirehole
# edit docker-compose.yml to set required number of peers
docker-compose up -d
```

5. Configure UFW to route traffic to Raspberry Pi  
https://www.procustodibus.com/blog/2021/05/wireguard-ufw/#ufw-configuration-on-host-c

### In addition
Deny all ICMP requests to avoid tunnel recognition  
https://linuxconfig.org/how-to-deny-icmp-ping-requests-on-ubuntu-18-04-bionic-beaver-linux
