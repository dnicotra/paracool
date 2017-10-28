# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
	. "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

while [ ! -f "/lib/paracool/MASTER_IP" ]
do
	sudo python /lib/paracool/bin/slave_authentication.py
done
master_ip=$( < /lib/paracool/MASTER_IP )
uid=$( < /lib/paracool/UID )
echo "Got Master @ $master_ip ... adding to hosts"
sudo sh -c "echo '$master_ip master' >> /etc/hosts"
#sudo /lib/paracool/bin/hostname_changer.sh "slave$uid"
sudo sed -i "s/slave/slave$uid/g" /etc/hosts
sudo hostnamectl set-hostname "slave$uid"
echo "Sleeping before mounting /home"
echo "3"
sleep 1
echo "2"
sleep 1
echo "1"
sleep 1


echo "Mounting master:/home -> /home"
sudo mount -t nfs master:/home /home
#MOUNT