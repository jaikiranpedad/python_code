import json,requests,re
from requests.auth import HTTPBasicAuth
import argparse

baseurl = "https://solutions.atlassian.net/wiki/rest/api/content/"
headers = {"Accept": "application/json", "Content-Type": "application/json"}
get_api_url = "?expand=body.storage"

def getResponse(url, auth, method, data=None):
   try:
      url = baseurl + url
      return requests.request(method ,url, headers=headers,auth=auth, data=data)
   except Exception as e:
      print "Error while connecting " + str(e)
      exit(1)

def getPage(pageid, auth):
   response = getResponse(pageid + get_api_url, auth, "GET")
   body = json.loads(response.text)
   content =  body["body"]["storage"]["value"]
   return content

def updatePage(pageid, data, auth):
   metadata = getResponse(pageid, auth, "GET")
   meta_json = json.loads(metadata.text)
   id = meta_json['space']['id']
   title = meta_json['title']
   version = meta_json['version']['number']
   type = meta_json['type']

   page_content = json.dumps(
      {
         "id": pageid,
		 "type": type,
		 "title": title,
		 "body": {
		    "storage": {
			"value": data,
			"representation":"storage"
			}
		 },
		 "version": {
		    "number": int(version) + 1
		 }
	  })
   response = getResponse(pageid, auth, "PUT", page_content)
   return response

if __name__ == '__main__':
  '''
  Main function for add/update confluence page
  '''
  try:
    parser = argparse.ArgumentParser()
    # Argparser to enable command line named args
    parser.add_argument('-pageid', dest='pageid', action='store', default=None,help='Confluence Page Id')
    parser.add_argument('-method',  dest='method', action='store', default=None,help='HTTP method')
    parser.add_argument('-userid', dest='userid', action='store', default=None,help='User Id for Confluence')
    parser.add_argument('-token', dest='token', action='store', default=None,help='User Token')
    parser.add_argument('-data', dest='data', action='store', default=None,help='Page Content')

    results = parser.parse_args()

    pageid   = results.pageid
    method    = results.method
    userid   = results.userid
    token   = results.token
    data   = results.data

   # If any required arguments is not passed, checking for None and exiting
    if None in [ pageid, method, userid, token ]:
      raise Exception('Required arguments are not specified')
  except Exception as e :
    print "Please provide all the args: "+str(e)
    exit(1)

  auth = HTTPBasicAuth(userid, token)
  if method == "GET":
  	print getPage(pageid, auth)
  elif method == "PUT":
  	print updatePage(pageid, data, auth)
  else:
  	print "Invalid method"
  	exit(1)