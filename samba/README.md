# Samba share over WireGuard

## Installation
Mount a device:
```shell
MOUNT_DIR=/media/share
sudo mkdir $MOUNT_DIR
sudo chmod 775 $MOUNT_DIR
sudo mount /dev/sda1 $MOUNT_DIR
echo "/dev/sda1 ${MOUNT_DIR} ntfs defaults 0 0" >> /etc/fstab
```

Install Samba server:
```shell
apt install samba samba-common-bin
cp /etc/samba/smb.conf /etc/samba/backup.conf
cp smb.conf /etc/samba/smb.conf
systemctl enable smbd
ufw allow Samba
```

Note: 
```
bind interfaces only = no
```

Set password for the username
```shell
smbpasswd -a username
service smbd restart
```

## Sources
[Mount a device to Raspbeery Pi](https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-mount-an-external-hard-drive-on-the-raspberry-pi-raspian)
[Set up Samba](https://pimylifeup.com/raspberry-pi-samba/)
