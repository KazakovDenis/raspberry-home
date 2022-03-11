# Backups with rclone

## Installation
Ubuntu 20.04 and higher:
```shell
ssh user@server
curl https://rclone.org/install.sh | sudo bash 
```

## Configuration
### Open remote storage
If you need rclone on a remote headless machine, run before on a host with a browser:
```shell
# Choose your cloud provider from
# https://rclone.org/overview/
rclone authorize "cloudprovidername"
```

Then configure remote storage:
```shell
rclone config
```

### Encrypted remote storage
An encrypted storage is configured using an existing storage (e.g. from previous step):
```shell
rclone config
n/s/q> n
name> secret
Storage> crypt
```
Then follow instructions.

## Usage
Copy your files to a remote storage using the command:
```shell
rclone copy --exclude-from ignore.txt --progress /path/to/source/dir_name remote:dir_name
```
Now you can schedule periodic sync.

## Schedule backups
Move backup.sh to `/opt` and add a job to Cron:
```shell
crontab -e
# paste the following into opened file
# run script everyday at 6 am
0 6 * * * /opt/backup.sh >> /var/log/rclonebackup.log
```
