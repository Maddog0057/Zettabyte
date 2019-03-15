# Zettabyte
## An Autonomous Country in NationStates

### WHY?
Well, you see, I was bored, and Nation States only gives you an issue every ~1.5 hours, so I figured what would happen if I basically just chose a random response to every issue? How would the state turn out? Horrible dictatorship? Paradise? Socialism? (nah, socialism doesn't work) Then I figued, that's a lot of work... Why don't I just write a bot to do it instead? and after lots of procrastinating (mainly making flags and coming up with stupid robot-related names... damn Mechadonia) I drew up this bot in python.

### Requirements
* Some sort of linux machine that supports Python 3.x, Sorry Windows (Not Sorry)
* Python 3.x (Preferably 3.6+)
* A local copy of this GitHub Repo
* At least a Gig of Disk space
* A Discord Channel with permissions to create a webhook
* A fresh NationStates Puppet (Or main, but that's kinda stupid)

### Setup
#### Puppet Setup
I'm going to assume since you're here you've grasped the general idea of NationStates and know how to create an account. If not I'm gonna leave this one up to you, go out and learn, just make sure you come back with a nation name (just the name, I don't need any of that classification crap) and a password.

#### Discord Setup
Find youself a discord server, I don't care how, make one, steal one, gain the trust of the local inhabitants and claim to be their god, just make sure you get a high enough permission to create webhooks, then hit *edit* (The little gear), *Webhooks*, *Create Webhook* (Big Blue Button, ya can't miss it), and give him (or her), a name and a face, Name doesn't matter it can be the same or different than your Nation, the most important thing here is the link at the bottom, thats what you need (yes, all of it). Then hit save, make note of that link, you'll need it later.

#### Bot Setup (The Fun Stuff)
This is where things start to get tricky, so I'm going to make a few assumptions:

1. You have a working knowlege of basic Linux commands (I'm not making this distro specific)
2. You know when I put things in <brackets> they don't stay in brackets e.g. Password:"\<password>" means replace \<password> with your password, such as Password:"Password123" (If you're panicking right now that your password is part of the documentation, yes, I know your passoword, go change it)
3. You have a working knowlege of basic Linux commands (I don't hold hands)
4. Some of these commands will need to be run as root (sudo) I trust you'll know which ones and I accept no responsability for what you muck up in the process.

Great! Now that we've gotten that out of the way, lets begin.

1. Start off by cloning this repo (The links up there, you can find it, and if you don't have git installed, happy googling)
2. In the folder that you just created, make a copy of config.json.sample and name it (you guessed it) config.json
	```cp config.json.sample config.json```
3. Open config.json in your favorite text editor (no emacs isn't acceptable) and start filling it in section by section
4. Under discord, name should be the name you gave your discord webhook, and url is the link is the one you saved earlier (You haven't lost it already have you)
5. Under ns, useragent can be literally anything, nation states gives more info about this [here](https://www.nationstates.net/pages/api.html#terms), nation is your nation name
6. ns password is probably the trickiest to get, it needs to be a token given to you by nation states in an effort to obfuscate your password (I could have just used your password in plan text, but I feed on the extranious effort of others), you can get the token using the following command:
	```curl -H "X-Password: <Your actual password>" -A "<useragent>" "https://www.nationstates.net/cgi-bin/api.cgi?nation=<nationname>&q=unread" -i |grep x-autologin |cut -d":" -f2```
7. In the system section you only need the location of whatever directory you want to store your logs (I don't care where it is as long as the user that you run the bot as has access to it) e.x.:
	```/opt/Zettabyte/logs/```
8. Save that config and make sure you're in the bot directory
9. Alright I made this one easy (only because it made my life easier) to install dependancies enter the command ```pip3 install -r requirements.txt``` (Trust me it's safe, look for yourself if you want)
10. That about does it for the environment, if you wanna test the bot you can use ```python3 zettabyte.py``` and check the log file, any errors are most likely your fault, I'm perfect. But if you happen to be able to disprove perfection, log a bug and I'll let you know how you're wrong.
11. Running the bot continuously requires some way of backgrounding the process, the easiest is to install screen or tmux (Do I look like google to you? Figure it out for yourself) and run the command from step 10. If you're feeling adventerious I'll (minimally) tell you how to run it as a daemon (If you're lucky).

#### Daemon Setup 
##### For those who wish to put in more than 10% effort
1. Start with zettabyte.service file, rename it whatever you want as long as it ends in .service, it's what you're gonna have to type to start and stop the bot so make it easy.
2. Open the file with your favorite text editor (Seriously, emacs is a no)
3. Most of this file is pretty straight forward, Description is whatever you want it to be, exec start should be the location of your python binary (run ```which python3``` for the path) as well as the location of the zettabyte.py file (or whatever you renamed it to, yes, you can do that)
4. Working directory should be the same as the location of zettabyte.py, excluding "/zettabyte.py"
5. User and Group is based on your setup, I'd advise creating a new user with /sbin/nologin as the shell (Google it if you're staring at the screen like you're simple, see the "no hand-holding" policy) and set both User and Group to the user you just made. Otherwise you can run them as your user, or root (I don't recommend it, nor will I accept any responsabity if you do, I'm just laying out your options).
6. Make sure whatever User you choose to run the bot as has complete permission over the directory where the zettabyte.py and config files live, as well as the logs folder, and has access to the python3 binary. ```chown -R <User>:<Group> /path/to/zettabyte/files```
7. Anything I didn't mention about this file is best not to touch (I probably don't even know what it does)
8. You now want to move this file to wherever your service files are stored (Most people use ```/usr/lib/systemd/system/``` if you don't, I won't judge)
9. Run ```systemctl daemon-reload``` to install the service and ```systemctl start <file.service>``` to start the Bot
10. If you want the bot to run on startup ```systemctl enable <file.service>```

#### Footnotes
##### Read them or don't I don't care
Some say my documentation style is offensive, I really couldn't care less what you think, but if you wanna let me know (I won't read it):

Send me a Telegram [Invernes](https://www.nationstates.net/nation=invernes)
Discord: [Maddog](https://discordapp.com/users/maddog#6554)

Join Our Region (You can try, we require a blood sacrifice) [AROCS](https://www.nationstates.net/region=allied_region_of_conservative_states)

View this project in action [Zettabyte](https://www.nationstates.net/nation=zettabyte)
It's been running since 3/9/19 
