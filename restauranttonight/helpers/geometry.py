import math


#copied from http://stackoverflow.com/questions/238260/how-to-calculate-the-bounding-box-for-a-given-lat-lng-location
# degrees to radians
def deg2rad(degrees):
	return math.pi * float(degrees)/180.0
# radians to degrees
def rad2deg(radians):
	return 180.0*radians/math.pi

# Semi-axes of WGS-84 geoidal reference  
WGS84_a = 6378137.0  # Major semiaxis [m]
WGS84_b = 6356752.3  # Minor semiaxis [m]

# Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
def WGS84EarthRadius(lat):
	# http://en.wikipedia.org/wiki/Earth_radius
	An = WGS84_a*WGS84_a * math.cos(lat)
	Bn = WGS84_b*WGS84_b * math.sin(lat)
	Ad = WGS84_a * math.cos(lat)
	Bd = WGS84_b * math.sin(lat)
	return math.sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) )

# Bounding box surrounding the point at given coordinates,
# assuming local approximation of Earth surface as a sphere
# of radius given by WGS84
def boundingBox(latitudeInDegrees, longitudeInDegrees, halfSideInKm):
	lat = deg2rad(latitudeInDegrees)
	lon = deg2rad(longitudeInDegrees)
	halfSide = 1000*halfSideInKm

	# Radius of Earth at given latitude
	radius = WGS84EarthRadius(lat)
	# Radius of the parallel at given latitude
	pradius = radius*math.cos(lat)

	latMin = lat - halfSide/radius
	latMax = lat + halfSide/radius
	lonMin = lon - halfSide/pradius
	lonMax = lon + halfSide/pradius

	return (rad2deg(latMin), rad2deg(lonMin), rad2deg(latMax), rad2deg(lonMax))


def distance_on_unit_sphere(lat1, long1, lat2, long2):	
	#
	# Convert latitude and longitude to 
	# spherical coordinates in radians.
	degrees_to_radians = math.pi/180.0	    
	#
	# phi = 90 - latitude
	phi1 = (90.0 - lat1)*degrees_to_radians
	phi2 = (90.0 - lat2)*degrees_to_radians
	#
	# theta = longitude
	theta1 = long1*degrees_to_radians
	theta2 = long2*degrees_to_radians
	#
	# Compute spherical distance from spherical coordinates.
	# For two locations in spherical coordinates 
	# (1, theta, phi) and (1, theta, phi)
	# cosine( arc length ) = 
	#    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
	# distance = rho * arc length
	cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
	       math.cos(phi1)*math.cos(phi2))
	arc = math.acos( cos )
	#
	# Remember to multiply arc by the radius of the earth 
	# in your favorite set of units to get length.
	return arc

EARTH_RADIUS = 6372.797

def findDistance(lat1, long1, lat2, long2) :
	try:
		return 6372.797 * distance_on_unit_sphere(float(lat1), float(long1), float(lat2), float(long2))
	except : return 0
	
def findDistanceFromArr(latLngArr) :		
	distance = 0
	for i in range(len(latLngArr)-1):
		try:
			lat1 = latLngArr[i][0]
			long1 = latLngArr[i][1]
			lat2 = latLngArr[i+1][0]
			long2 = latLngArr[i+1][1]
			distance += 6372.797 * distance_on_unit_sphere(float(lat1), float(long1), float(lat2), float(long2))
		except : 
			pass	
	return distance

if __name__ == '__main__':
	print findDistanceFromArr([(-16.9181420,145.7744550),(-25.3599120,131.0173380)])
	print findDistance(-16.9181420,145.7744550,-25.3599120,131.0173380)