from utils import levenshtein
from typing import Optional


existing_vendor_list = [
  {
    "id": "101",
    "vendor_name": "Apple Inc.",
    "vendor_email": "cook@apple.com",
    "alias": [
      "Apple", 
      "Apple Computers", 
      "Apple Inc",
    ],
    "vendor_address": "One Infinite Loop, Cupertino, CA 95014",
  },

  {
    "id": "102",
    "vendor_name": "Alphabet Inc.",
    "vendor_email": "billing@google.com",
    "alias": [
      "Google", 
      "Google Inc", 
      "Alphabet",
      "Alphabet Inc",
    ],
    "vendor_address": "1600 Amphitheatre Parkway Mountain View, CA 94043",
  },

  {
    "id": "103",
    "vendor_name": "Auditoria.ai",
    "vendor_email": "billing@auditoria.ai",
    "alias": [
      "Auditoria", 
      "Auditoria.ai", 
      "Auditoria.ai Inc.",
      "Auditoria Inc.",
    ],
    "vendor_address": "2445 Augustine Dr Suite 150, Santa Clara, CA 95054",
  },
]


def check_vendor(vendor_name, vendor_email) -> Optional[str]:
  for vr in existing_vendor_list:
    vn = vr["vendor_name"]
    if vn not in vr["alias"]:
      vr["alias"].append(vn)
    for v in vr["alias"]:
      if levenshtein(vendor_name, v, ignore_case=True) < 2:
        return vn
  return


def get_vendor_record(vendor_name, vendor_email) -> Optional[dict]:
  for vr in existing_vendor_list:
    vn = vr["vendor_name"]
    if vn not in vr["alias"]:
      vr["alias"].append(vn)
    for v in vr["alias"]:
      if levenshtein(vendor_name, v, ignore_case=True) < 2:
        return vr
  return
