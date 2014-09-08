import web
import json
import soco
from soco import SoCo


class SonosDevice:
	def __init__(self, name, ip):
		self.name = name
		self.ip = ip

	def toJSON(self):
		return dict(name=self.name, ip=self.ip)



urls = (
'/', 'index',
'/play', 'play',
'/list', 'listDevices',
'/device', 'deviceStatus'

)

class index:
	def GET(self):
		return "SoCo webapi"

class listDevices:
	def GET(self):

		web.header('Content-Type', 'application/json')
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		deviceList = []
		for zone in soco.discover():
			o = SonosDevice(zone.player_name, zone.ip_address)
			deviceList.append(o)
		
		return json.dumps([item.toJSON() for item in deviceList])
class play:
	def GET(self):
		web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Credentials', 'true')

		data = web.input(uri="no", player="no")
		sonos = SoCo('192.168.1.105')
                sonos.play_uri(data.uri)
		track = sonos.get_current_track_info()
                return track['title'] + " - " + data.player

		
class deviceStatus:
	def GET(self):

		web.header('Content-Type', 'application/json')
		web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Credentials', 'true')
		

		data = web.input(player="blank")
		sonos = SoCo(data.player)
		
		track = sonos.get_current_track_info()
		
		

		
		return json.dumps(track)


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
