import pywapi, string, urllib, lxml.html, lxml.etree, os
from subprocess import call

def get_fast_lane_price():
    url = urllib.urlopen("https://www.fastlane.co.il/mobile.aspx")
    tree = lxml.html.fromstring(url.read())
    return tree.get_element_by_id("lblPrice").text

home = ("34.80543584", "31.95836138")
amdocs = ("34.88898933", "32.17463171")
mentor = ("34.80878055", "32.16168101")
fastlane1 = ("34.84571", "31.99926")
fastlane2 = ("34.84184", "32.00369")

def get_waze(a, b):
    request = "https://www.waze.com/il-RoutingManager/routingRequest?from=x%3A"+a[0]+"+y%3A"+a[1]+"+bd%3Atrue&to=x%3A"+b[0]+"+y%3A"+b[1]+"+bd%3Atrue&returnXML=true&returnGeometries=false&returnInstructions=false&timeout=60000&nPaths=1&AVOID_TRAILS=false&AVOID_LONG_TRAILS=false"
    url = urllib.urlopen(request)
    data = url.read()
    tree = lxml.etree.fromstring(data)
    time = tree.xpath("/route/summary")[0].get("time")
    return int(time) / 60

weather = pywapi.get_weather_from_weather_com('ISXX0011')
weather_text = weather['current_conditions']['text']
weather_temp = weather['current_conditions']['temperature']

line1 = weather_temp + "c " + weather_text.replace(" ", "")

mentor_time = get_waze(home, mentor)
mentor_time_fastlane = get_waze(home, fastlane1) + get_waze(fastlane2, mentor)
amdocs_time = get_waze(home, amdocs)

if mentor_time_fastlane < mentor_time:
    fastlane_price = get_fast_lane_price()
    line2 = "M:" + str(mentor_time) + "/" + str(mentor_time_fastlane) + "+" + fastlane_price
else:
    line2 = "M:" + str(mentor_time)

line2 = line2 + " A:" + str(amdocs_time)

script_dir = os.path.dirname(os.path.realpath(__file__))
lcd_puts = script_dir + "/" + "lcd_puts"

call([lcd_puts, line1, line2])
