"""
File with helper methods.
"""

from itertools import repeat
import js2xml
import csv
import re


def parse_script(script):
  """
  Parses HTML <script> tag contents and pulls out x and y values.
  """

  parsed = js2xml.parse(script)
  data = [d.xpath(".//array/number/@value") 
    for d in parsed.xpath("//property[@name='data']")]

  categories = parsed.xpath("//property[@name='categories']//string/text()")

  return list(zip(repeat(categories), data))


def store_data(soup, script_id, csv_file, params):
  """
  Pulls x and y values and stores them in a CSV file.
  """

  try:
    script = soup.find("script", text=re.compile(script_id)).contents[0]
    parsed_script = parse_script(script)[0]
    rows = zip(parsed_script[0], list(map(int, parsed_script[1])))
  except AttributeError:
    country = csv_file.rsplit('/', 1)[-1]
    print(f"Weird JS structure/name for {country}")
    return

  with open(csv_file, "w") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(params)
    for row in rows:
      csv_writer.writerow(row)
