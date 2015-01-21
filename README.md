IPSwitch
========
Simple DNS management utility. Monitors for changes to IP address and updates DNS records on detection of a change. Built to run as a *nix daemon.

Uses a simple provider model under the hood for both IP address resolution and DNS management. Currently supports the following,

##### IP Address Resolution
whatsmyip.com  
realip.info

##### DNS Providers
GoDaddy

##### Notification Providers
NotifyMyAndroid.com  
PushBullet

### Usage
`./ipswitch start|stop|restart` 

### Dependencies
apscheduler (version 2.1.2) `pip install apscheduler==2.1.2`  
Mechanize  
Beautiful Soup 4




