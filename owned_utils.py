#!/usr/bin/python3

# Author: Patrick Hurd, Penetration Tester, Coalfire Federal 2019

import requests, json
import getopt, sys

def main(argv):
	node_type = ''
	node_label = ''
	request = ''
	domain = ''

	try:
		opts, args = getopt.getopt(argv,"hr:t:l:d:",["request=", "type=","label=","domain="])
	except getopt.GetoptError:
		print('test.py -r <request type> -t <node type> -l <node label>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('test.py -r <request type> -t <node type> -l <node label>')
			sys.exit()
		elif opt in ("-r", "--request"):
			request = arg
		elif opt in ("-t", "--type"):
			node_type = arg
		elif opt in ("-l", "--label"):
			node_label = arg
		elif opt in ("-d", "--domain"):
			domain = arg
	mux(request, node_type, node_label)

def mux(request, node_type, node_label):
	if request == 'domains':
		get_domains();
	elif request == 'owned':
		mark_owned(node_type, node_label)
	elif request == 'create':
		create(node_type, node_label)
	elif request == 'exists':
		exists(node_type, node_label)
	elif request == 'exists_like':
		exists_starts_with(node_type, node_label)
	else:
		print("Error: unknown request type")

def mark_owned(nodetype, nodelabel):
	statement = 'Match (n:*) WHERE lower(n.name) = "' + nodelabel.lower() + '" SET n.owned = TRUE'
	headers = { "Accept": "application/json; charset=UTF-8",
		"Content-Type": "application/json",
		"Authorization": "bmVvNGo6Qmxvb2RIb3VuZA==" }
	data = {"statements": [{'statement': statement}]}
	url = 'http://localhost:7474/db/data/transaction/commit'
	r = requests.post(url=url,headers=headers,json=data)
	print(r.text)

def create(nodetype, nodelabel):
	statement = "CREATE (n:" + nodetype + ') SET n.name="' + nodelabel + '"'
	headers = { "Accept": "application/json; charset=UTF-8",
		"Content-Type": "application/json",
		"Authorization": "bmVvNGo6Qmxvb2RIb3VuZA==" }
	data = {"statements": [{'statement': statement}]}
	url = 'http://localhost:7474/db/data/transaction/commit'
	r = requests.post(url=url,headers=headers,json=data)

def exists_starts_with(nodetype, nodelabel):
	statement = 'MATCH (n:' + nodetype + ') WHERE lower(n.name) STARTS WITH "' + nodelabel.lower() + '" RETURN n'
	headers = { "Accept": "application/json; charset=UTF-8",
		"Content-Type": "application/json",
		"Authorization": "bmVvNGo6Qmxvb2RIb3VuZA==" }
	data = {"statements": [{'statement': statement}]}
	url = 'http://localhost:7474/db/data/transaction/commit'
	r = requests.post(url=url,headers=headers,json=data)
	if nodelabel in r.text:
		print(1)
	else:
		print(r.text)
		print(0)

def exists(nodetype, nodelabel):
	statement = 'MATCH (n:*) WHERE lower(n.name) = "' + nodelabel.lower() + '" RETURN n'
	headers = { "Accept": "application/json; charset=UTF-8",
		"Content-Type": "application/json",
		"Authorization": "bmVvNGo6Qmxvb2RIb3VuZA==" }
	data = {"statements": [{'statement': statement}]}
	url = 'http://localhost:7474/db/data/transaction/commit'
	r = requests.post(url=url,headers=headers,json=data)
	if nodelabel in r.text:
		return 1
	else:
		return 0

def get_domains():
	statement = "MATCH (n:Domain) RETURN n"
	headers = { "Accept": "application/json; charset=UTF-8",
		"Content-Type": "application/json",
		"Authorization": "bmVvNGo6Qmxvb2RIb3VuZA==" }
	data = {"statements": [{'statement': statement}]}
	url = 'http://localhost:7474/db/data/transaction/commit'
	r = requests.post(url=url,headers=headers,json=data)
	j = json.loads(r.text)
	output = ''
	for x in range(len(j["results"][0]["data"])):
		output = output + j["results"][0]["data"][x]["row"][0]["name"] + ','
	print(output[0:len(output)-1])

def test(nodetype, nodelabel):
	statement = "MATCH (n:" + nodetype + " {name:'" + nodelabel + "'}) RETURN n"
	headers = { "Accept": "application/json; charset=UTF-8",
		"Content-Type": "application/json",
		"Authorization": "bmVvNGo6Qmxvb2RIb3VuZA==" }
	data = {"statements": [{'statement': statement}]}
	url = 'http://localhost:7474/db/data/transaction/commit'
	r = requests.post(url=url,headers=headers,json=data)
	print(r.text)

main(sys.argv[1:])
