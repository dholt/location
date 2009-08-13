#!/usr/bin/env python 

import urllib2, urllib, json, cookielib, sys, math

# needed to get by special cookie attributes
class ForgivingCookieJar(cookielib.CookieJar):
	
	def _cookie_from_cookie_tuple(self, tup, request):
		name, value, standard, rest = tup
		version = standard.get("version", None)
		if version is not None:
			# Some servers add " around the version number, this module expects a pure int.
			standard["version"] = version.strip('"')
			return cookielib.CookieJar._cookie_from_cookie_tuple(self, tup,request)

class scraper():

	def __init__(self, email, password):
		self.location = {}
		# handlers
		self.proc = urllib2.HTTPCookieProcessor(ForgivingCookieJar())
		self.opener = urllib2.build_opener(self.proc)
		urllib2.install_opener(self.opener)
	
		# login form values
		self.body = urllib.urlencode({'username': email,
					 'password': password,
					 'returnURL': "aHR0cHM6Ly9zZWN1cmUubWUuY29tL3dvL1dlYk9iamVjdHMvRG9ja1N0YXR1cy53b2Evd2EvdHJhbXBvbGluZT9kZXN0aW5hdGlvblVybD0vYWNjb3VudA%3D%3D",
					 'service': 'DockStatus',
					 'realm': 'primary-me',
					 'cancelURL': 'http://www.me.com/mail',
					 'formID': 'loginForm',
					 'reauthorize': 'Y',
					 'destinationUrl': '/account'})
	
	def locate(self):
		try:
			# log in
			self.opener.open('https://auth.apple.com/authenticate',  self.body)
		except urllib2.HTTPError,msg:
			print "Error: ", msg
			exit(1)
	
		# get secure cookie value
		secureCookie = ''
		for i in self.proc.cookiejar:
			if i.name == 'isc-secure.me.com':
				secureCookie = i.value
	
		# build headers
		headers = [ ("Content-Type", "application/json"),
			    ("Accept","text/javascript, text/html, application/xml, text/xml, */*"),
			    ("X-Requested-With", "XMLHttpRequest"),
			    ("X-Prototype-Version", "1.6.0.3"),
			    ("X-Mobileme-Version", "1.0"),
			    ("X-Mobileme-Isc", secureCookie) ]
		self.opener.addheaders = headers
		
		try:
			# get device (only one for now)
			data = self.opener.open('https://secure.me.com/wo/WebObjects/DeviceMgmt.woa/?lang=en').read()
			start = int(data.find("DeviceMgmt.deviceIdMap"))
			start = int(data.find('=',start))+2
			end = int(data.find(';',start))
			deviceId = data[start:end].strip("'")
		
			# configure post data
			post = "postBody=%s" % json.dumps( {
			'deviceId': deviceId,
			'deviceOsVersion': "7A341",
			} )
		
			# get location
			data = self.opener.open('https://secure.me.com/wo/WebObjects/DeviceMgmt.woa/wa/LocateAction/locateStatus', post)
			self.location = json.load(data)
			return self.location
		except urllib2.HTTPError,msg:
			print "Error: ", msg
			exit(1)

<<<<<<< HEAD
if __name__ == '__main__':
	from config import *
	s = scraper(username, password)
=======
	def distanceFrom(self, point):
		lon2 = point['longitude']
		lat2 = point['latitude']
		if len(self.location) == 0:
			self.locate()
		lat1 = self.location['latitude']
		lon1 = self.location['longitude']
		nauticalMilePerLat = 60.00721
		nauticalMilePerLongitude = 60.10793
		rad = math.pi / 180.0
		milesPerNauticalMile = 1.15078
		yDistance = (lat2 - lat1) * nauticalMilePerLat
		xDistance = (math.cos(lat1 * rad) + math.cos(lat2 * rad)) * (lon2 - lon1) * (nauticalMilePerLongitude / 2)
		distance = math.sqrt( yDistance**2 + xDistance**2 )
		return distance * milesPerNauticalMile

if __name__ == '__main__':
	s = scraper('username@me.com', 'password')
>>>>>>> e7a592bee74fa3f908592fdce8b253f4d25294fe
	location = s.locate()

	if 'noLocation' in location and location['noLocation']:
		print "Location unavailable"
		exit(0)

	print location['date'], location['time']
	print "loc:", location['latitude'], location['longitude']
	
<<<<<<< HEAD
=======
	'''
	work = {'latitude': 48.937663,
		'longitude': -123.939734}
	home = {'latitude': 58.030730,
		'longitude': -130.983230}

	distWork = round(float(s.distanceFrom(work)), 2)
	distHome = round(float(s.distanceFrom(home)), 2)

	print distWork, distHome
	'''
>>>>>>> e7a592bee74fa3f908592fdce8b253f4d25294fe
