"""CME Python Workshop: Compute for each user the one other user with the  
   highest positive correlation (PCC closest to 1.0)
"""
import math as math

# Take filename and return data structure
def loadFile(filename):
    f = open(filename)
    users = {}          # create dictionary
    userid = 0
    movieid = 0
    rating = 0
    for line in f:
        fields = line.split()
        userid = int(fields[0])
        movieid = int(fields[1])
        rating = int(fields[2]) 
        if userid in users:
            users[userid][1][movieid] = rating
        else:
            users[userid] = [0, {movieid:rating}]
    # Compute average
    f.close()
    for userid in users:
        ratingsum = 0.0
        for key in users[userid][1]:
            ratingsum = ratingsum + (users[userid][1][key])
        users[userid][0]= ratingsum/float(len(users[userid][1]))
    return users
        
# Pass in the lists for the two users
def computePCC(user1,user2):
    num = 0.0
    den1 = 0.0
    den2 = 0.0
    common_movies = set(user1[1].keys()) & set(user2[1].keys())
    for movie in common_movies:
        num +=  (user1[1][movie]-user1[0])*(user2[1][movie]-user2[0])
        den1 += (user1[1][movie]-user1[0])**2
        den2 += (user2[1][movie]-user2[0])**2
    if (den1*den2 == 0):
        PCC = 0.0
    else:
        PCC = num/math.sqrt(den1*den2)
    return PCC, len(common_movies)

def computeAllCorrelations():    
    users = loadFile("test.data")
    threshold = 6
    f = open("output_test.txt","w")
    for user1 in sorted(users.keys()):
        bestCorrelation = (user1,-2.0,0)
        for user2 in users:
            if user1 == user2:
                continue
            PCC, ncommon = computePCC(users[user1],users[user2])
            if (PCC > bestCorrelation[1]) and (ncommon >= threshold):
                bestCorrelation = (user2,PCC,ncommon)
        if (bestCorrelation[1] >= -1.0):
            f.write("%d (%d,%.2f,%d)\n"
            % (user1,bestCorrelation[0],bestCorrelation[1],bestCorrelation[2]))
        else:
            f.write("%d\n" % user1)
    f.close()

computeAllCorrelations()