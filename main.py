from ast import Num, Try
from asyncio.windows_events import NULL
from distutils.log import error
from sqlite3 import Date
from traceback import print_tb
from warnings import catch_warnings
import xmltodict
import json
import requests
from xml.etree import ElementTree as Et
from sheet import sheetCall


class BillsFixed:
    def __init__(self, date, ref, party):
        self.date = date
        self.ref = ref
        self.party = party


def get_data(payload):
    print("Fetching data from TallyPrime....")
    req = NULL
    try:
        req = requests.post(url="http://localhost:9002", data=payload)

    except Exception as error:
        print(error)

    if(req not  ''):

        data_dict = xmltodict.parse(
            req.text)['ENVELOPE']['BODY']['DATA']['TALLYMESSAGE']

        for item in data_dict[:(len(data_dict)-1)]:
            # print(item)
            for innerItem in item['VOUCHER']:
                if(innerItem[0] != '@' and item['VOUCHER'][innerItem] != '' and (type(item['VOUCHER'][innerItem]) == str or type(item['VOUCHER'][innerItem]) == Num)):
                    print(innerItem+": "+item['VOUCHER'][innerItem])
                    # pass

        json_data = json.dumps(data_dict)

        with open("data.json", "w") as json_file:
            json_file.write(json_data)
            json_file.close()

        res = req.text.encode("UTF-8")
        print("Data Received.")
        sheetCall()

        # return res


def get_payload(r_type, from_dt, to_dt):
    # Select $Date,$Reference,$VouchertypeName,$PartyLedgerName,$$CollectionField:$Amount:1:LedgerEntries from RTSAllVouchers where $$IsSales:$VoucherTypeName
    print("Payload is Creating....")

    xml = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST>"
    xml += "<TYPE>DATA</TYPE><ID>" + r_type + "</ID></HEADER><BODY>"
    xml += "<DESC><STATICVARIABLES><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>"
    xml += "<SVFROMDATE Type='DATE'>" + from_dt + \
        "</SVFROMDATE><SVTODATE Type='DATE'>" + to_dt
    xml += "</SVTODATE></STATICVARIABLES></DESC></BODY></ENVELOPE>"

    # xml = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST>"
    # xml += "<TYPE>OBJECT</TYPE><SUBTYPE>"+r_type+"</SUBTYPE><ID TYPE=\"Name\">Sale A/c</ID></HEADER><BODY>"
    # xml += "<DESC><STATICVARIABLES><SVEXPORTFORMAT>$$SysName:JSON</SVEXPORTFORMAT>"
    # xml += "<SVFROMDATE Type='DATE'>" + from_dt + "</SVFROMDATE><SVTODATE Type='DATE'>" + to_dt
    # xml += "</SVTODATE></STATICVARIABLES></DESC></BODY></ENVELOPE>"

    print("Payload is Created")

    return xml


title = "Day book"
from_dt = "1-4-2022"
to_dt = "30-4-2022"

response = get_data(get_payload(title, from_dt, to_dt))
# print(response)
xml = Et.fromstring(response)


bill_fixed = []
bill_closing = []
bill_due = []
bill_days = []

# for data2 in xml:
#     print(data2.items())
# for data3 in data2:
#     print(data3.text)


# for data in xml.findall("./BILLFIXED"):
#     bill_fixed.append(BillsFixed(data.find("./BILLDATE").text,
#                       data.find("./BILLREF").text, data.find("./BILLPARTY").text))
# for data2 in xml.findall("./ALLINVENTORYENTRIES.LIST"):
#     for data3 in data2:
#         print(data3.text)
#     bill_closing.append(data2.text)

# for data3 in xml.findall("./BILLDUE"):
#     bill_due.append(data3.text)

# for data4 in xml.findall("./BILLOVERDUE"):
#     bill_days.append(data4.text)


# print(bill_fixed)
# print(bill_fixed)
# print(bill_closing)
# print(bill_due)
# print(bill_days)

# +
#
#
#
#
#  return { Name=title, from_dt=from_dt, to_dt=to_dt, bill_fix=bill_fixed, bill_cl=bill_closing, bill_due=bill_due, bill_days=bill_days}
