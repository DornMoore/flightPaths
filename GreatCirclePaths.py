import math
from geojson import LineString

def calc_dist(lat1,lon1,lat2,lon2):
        """Calculate the distance between two coordinates using great circle calculation."""
        #Convert the coordinates to radians (make sure it knows the inputs are float)
        lat1=math.radians(float(lat1))
        lat2=math.radians(float(lat2))
        lon1=math.radians(float(lon1))
        lon2=math.radians(float(lon2))
        
        # Great circle distance in radians
        d = math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2))

        # Multiply radians by 6300km to get distance in km
        dist = 6371 * d
        
        return dist

def createPaths(latitude1, longitude1, latitude2, longitude2):
        ptlon1 = longitude1
        ptlat1 = latitude1
        ptlon2 = longitude2
        ptlat2 = latitude2

        # Dynamically set the segments based on one each degree
        numberofsegments= int(calc_dist(ptlat1,ptlon1,ptlat2,ptlon2)/111.3)

        #numberofsegments = num_of_segments
        onelessthansegments = numberofsegments - 1
        fractionalincrement = (1.0/onelessthansegments)

        ptlon1_radians = math.radians(ptlon1)
        ptlat1_radians = math.radians(ptlat1)
        ptlon2_radians = math.radians(ptlon2)
        ptlat2_radians = math.radians(ptlat2)

        distance_radians=2*math.asin(math.sqrt(math.pow((math.sin((ptlat1_radians-ptlat2_radians)/2)),2) + math.cos(ptlat1_radians)*math.cos(ptlat2_radians)*math.pow((math.sin((ptlon1_radians-ptlon2_radians)/2)),2)))
        # 6371.009 represents the mean radius of the earth
        # shortest path distance
        distance_km = 6371.009 * distance_radians

        mylats = []
        mylons = []

        # write the starting coordinates
        mylats.append([])
        mylons.append([])
        mylats[0] = ptlat1
        mylons[0] = ptlon1 

        f = fractionalincrement
        icounter = 1

        while (icounter <  onelessthansegments):
                icountmin1 = icounter - 1
                mylats.append([])
                mylons.append([])
                # f is expressed as a fraction along the route from point 1 to point 2
                A=math.sin((1-f)*distance_radians)/math.sin(distance_radians)
                B=math.sin(f*distance_radians)/math.sin(distance_radians)
                x = A*math.cos(ptlat1_radians)*math.cos(ptlon1_radians) + B*math.cos(ptlat2_radians)*math.cos(ptlon2_radians)
                y = A*math.cos(ptlat1_radians)*math.sin(ptlon1_radians) +  B*math.cos(ptlat2_radians)*math.sin(ptlon2_radians)
                z = A*math.sin(ptlat1_radians) + B*math.sin(ptlat2_radians)
                newlat=math.atan2(z,math.sqrt(math.pow(x,2)+math.pow(y,2)))
                newlon=math.atan2(y,x)
                newlat_degrees = math.degrees(newlat)
                newlon_degrees = math.degrees(newlon)
                mylats[icounter] = newlat_degrees
                mylons[icounter] = newlon_degrees
                icounter += 1
                f = f + fractionalincrement

        # write the ending coordinates
        mylats.append([])
        mylons.append([])
        mylats[onelessthansegments] = ptlat2
        mylons[onelessthansegments] = ptlon2

        # Now, the array mylats[] and mylons[] have the coordinate pairs for intermediate points along the geodesic
        # My mylat[0],mylat[0] and mylat[num_of_segments-1],mylat[num_of_segments-1] are the geodesic end points

        # write a kml of the results
        zipcounter = 0

        out=open("path.kml","wt")
        json_out=open("path.geojson","wt")

        kmlheader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><kml xmlns=\"http://www.opengis.net/kml/2.2\"><Document><name>LineString.kml</name><open>1</open><Placemark><name>unextruded</name><LineString><extrude>1</extrude><tessellate>1</tessellate><coordinates>"
        #print kmlheader
        out.write(kmlheader+"\n")
        geojson_line =""
        while (zipcounter < numberofsegments):
                geojson_pairs = geojson_line + ", [" + repr(mylons[zipcounter]) + "," + repr(mylats[zipcounter]) + "]"
                outputstuff = repr(mylons[zipcounter]) + "," + repr(mylats[zipcounter]) + ",0 "
                out.write(outputstuff+"\n")
                #print outputstuff
                zipcounter += 1
        geojson_line=geojson_pairs[2:]        
        json_out.write(geojson_line)
        #json_out.write(LineString([geojson_line]))
        kmlfooter = "</coordinates></LineString></Placemark></Document></kml>"
        #print kmlfooter
        out.write(kmlfooter)
        out.close
        json_out.close

createPaths(43.1398791,-89.3375045, -43.1398791, 89.3375045)