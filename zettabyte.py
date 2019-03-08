import requests
import nationstates as ns
import json
import time
import xmltodict
from discord_webhook import DiscordWebhook, DiscordEmbed
from random import *

with open("config.json", 'r') as json_data_file:
    config = json.load(json_data_file);

useragent = config["ns"]["useragent"]
password = config["ns"]["password"]
nationName = config["ns"]["nation"]
discordUrl = config["discord"]["url"]
hours = 6

api = ns.Nationstates(useragent)
nation = api.nation(nationName, autologin=password)

logDir = config["system"]["log"]
logFile = logDir+config["discord"]["name"]+".log"


class StreamToLogger(object):

   def __init__(self, logger, log_level=logging.INFO):
      self.logger = logger
      self.log_level = log_level
      self.linebuf = ''

   def write(self, buf):
      for line in buf.rstrip().splitlines():
         self.logger.log(self.log_level, line.rstrip())

handler = RotatingFileHandler(logFile,"a",maxBytes=1048576,backupCount=5)

logging.basicConfig(
   level=logging.INFO,
   format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
   handlers = [ handler ]
)


stdout_logger = logging.getLogger('STDOUT')
sl = StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl

stderr_logger = logging.getLogger('STDERR')
sl = StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl

def get_pin():
	headers = {'user-agent': useragent, 'X-Autologin': password}
	purl = "https://www.nationstates.net/cgi-bin/api.cgi?nation="+nationName+"&q=unread"
	r = requests.head(url=purl, headers=headers)
	pin = r.headers['X-pin']
	return pin

def get_issues():
	pin = get_pin()
	headers = {'user-agent': useragent, 'X-Pin': pin}
	lurl = "https://www.nationstates.net/cgi-bin/api.cgi?nation="+nationName+"&q=issues"
	issues = requests.get(lurl, headers=headers)
	issue = xmltodict.parse(str(issues.text))
	return issue

def get_ids(issue, iss_count, ids):
	count = 0
	while True:
		iss_id = issue["NATION"]["ISSUES"]["ISSUE"][count]["@id"]
		resp_count = len(issue["NATION"]["ISSUES"]["ISSUE"][count]["OPTION"])
		ids.update({iss_id:resp_count})
		count = int(count)+1
		if (int(count) == int(iss_count)):
			False
			return ids
		else:
			True

def send_discord(data, iid, ch, count):
	if int(data["NATION"]["ISSUES"]["ISSUE"][count]["@id"]) == int(iid):
		iss = str(data["NATION"]["ISSUES"]["ISSUE"][count]["TEXT"])
		title = str(data["NATION"]["ISSUES"]["ISSUE"][count]["TITLE"])
		ans = str(data["NATION"]["ISSUES"]["ISSUE"][count]["OPTION"][ch]["#text"])
		embed = DiscordEmbed(title=title, description=iss, color=0e9319)
		embed.add_embed_field(name="Zettabyte Chose (Option "+str(ch)+"): ", value=ans)
		webhook = DiscordWebhook(url=discordUrl)
		webhook.add_embed(embed)
		webhook.execute()
		del webhook

def choose_issues(choices):
	for key, value in choices.items():
		print("issue is: "+str(key)+" Choice is: "+str(value))
		response = nation.pick_issue(int(key), int(value))
		print(response["issue"]["desc"])


def main():
		issue = get_issues()
		issue_count = len(issue["NATION"]["ISSUES"]["ISSUE"])
		issue_ids = {}
		issue_ids = get_ids(issue, issue_count, issue_ids)
		choices = {}
		count = 0
		for key, value in issue_ids.items():
			rint = randint(0, int(value)-1)
			print("ID: "+str(key)+" Choice: "+str(rint))
			send_discord(issue, key, rint, count)
			choices.update({key:rint})
			count = int(count)+1
		choose_issues(choices)

while True:
	issue = get_issues()
	if issue["NATION"]["ISSUES"] is not None:
		main()
		print("Sleeping for 6 Hours")
		time.sleep(hours*3600)
	else:
		print("Sleeping for 1 Hour")
		time.sleep(3600)





