from vendor_management import check_vendor, get_vendor_record
from utils import ifnone
from flask import Flask, request
import json


app = Flask(__name__)


@app.route('/')
def hello_world():
  return "Hello world!"


@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  print(json.dumps(req, indent=2))

  intent_info = req.get("intentInfo")
  fulfillment_info = req.get("fulfillmentInfo")
  session_info = req.get("sessionInfo")
  params = session_info.get("parameters") if session_info.get("parameters") else dict()

  params.update({"vendor_found": False})

  intent = intent_info.get("displayName") if intent_info else ""
  tag = fulfillment_info.get("tag")

  vendor_name = ifnone(params.get("vendor_name"), "")
  vendor_email = ifnone(params.get("vendor_email"), "")

  if tag == "check_vendor":
    vendor_record = check_vendor(vendor_name=vendor_name, vendor_email=vendor_email)
    if vendor_record:
      vendor_found = True
    else:
      vendor_found = False
    params.update(
      {
        "vendor_found": vendor_found,
      }
    )
    if vendor_found:
      fulfillment_response = {
        "fulfillmentResponse": {
          "messages": [
            {
              "text": {
                "text": [f"Looks like we already have {vendor_record} in our system."]
              }
            }
          ],
        },
        "sessionInfo": session_info
      }
    else:
      fulfillment_response = {
        "fulfillmentResponse": {
          "messages": [
            {
              "text": {
                "text": [
                  f"I verified that we don't have {vendor_record} in our system. "
                  "Let's go ahead to onboard them to our system."
                  ]
              }
            }
          ],
        },
        "sessionInfo": session_info
      }

  elif tag == "get_vendor_record":
    vendor_record = get_vendor_record(vendor_name=vendor_name, vendor_email=vendor_email)
    if vendor_record:
      vendor_found = True
    else:
      vendor_found = False
    if vendor_record:
      params.update(
        {
          "vendor_found": vendor_found,
          "vendor_record": vendor_record
        }
      )
    if vendor_record:
      fulfillment_response = {
        "fulfillmentResponse": {
          "messages": [
            {
              "text": {
                "text": [
                  f"This is what I found:\nName: {vendor_record.get('vendor_name')}\n"
                  f"Email: {vendor_record.get('vendor_email')}\n"
                  f"Address: {vendor_record.get('vendor_address')}"
                  ]
              }
            }
          ],
        },
        "sessionInfo": session_info
      }
    else:
      fulfillment_response = {
        "fulfillmentResponse": {
          "messages": [
            {
              "text": {
                "text": [
                  f"Sorry, but I cannot find {vendor_name} in our system."
                  ]
              }
            }
          ],
        },
        "sessionInfo": session_info
      }

  else:
    fulfillment_response = {
      "fulfillmentResponse": {
        "messages": [
          {
            "text": {
              "text": ["Okay..."]
            }
          }
        ],
      },
      "sessionInfo": session_info
    }

  return fulfillment_response

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
Quick 