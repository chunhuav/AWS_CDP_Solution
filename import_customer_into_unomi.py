from calendar import c
import csv
import time
import uuid
from requests import post
from datetime import datetime

#sessionid=str(uuid.uuid1())
sessionid='session_import_101'
#You need to modify unomi EC2 address to your own.
unomiurl='http://35.77.40.65:8181'

with open('mock_customer_list.csv', newline='\n') as f:
    reader = csv.reader(f)
    #  skip csv reader
    next(reader)
    for row in reader:
        # print(row)
        profileid=str(uuid.uuid1())
        customername=row[1]
        username=row[2]
        email=row[3]
        address=row[4]
        city=row[5]
        zipcode=row[6]
        interesttag=row[7]
        """
        Make a request to Unomi to create a profile with ID = 10
        """
        profile = {
            "itemId":profileid,
            "itemType":"profile",
            "version":None,
            "properties": {
                "firstName": customername,
                "username":username,
                "email":email,
                "address":address,
                "city":city,
                "zipcode":zipcode,
                "interesttag":interesttag

            },
            "systemProperties":{},
            "segments":[],
            "scores":{},
            "mergedWith":None,
            "consents":{}
        }

        session = {
            "itemId": sessionid,
            "itemType":"session",
            "scope":None,
            "version":1,
            "profileId":profileid,
            "profile": profile,
            "properties":{},
            "systemProperties":{},
            "timeStamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        print(profile)
        print(session)
        
        #Create or update profile
        r = post(unomiurl+'/cxs/profiles/',
                auth=('karaf','karaf'),
                json=profile)
        print(r)
        print(r.content)


        # Create session
        r = post(unomiurl+'/cxs/profiles/sessions/'+sessionid,
                auth=('karaf', 'karaf'),
                json=session)

        print(r)
        print(r.content)

        time.sleep(1)
        







