import cv2
import datetime
from simple_facerec import SimpleFacerec
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def json_serial(obj):
    try:
        return obj.isoformat()
    except:
        return obj

def calcSlot(name):
    timein=dataset[index][2]
    timeout=dataset[index][3]
    p=(timeout.hour - timein.hour)*60+(timeout.minute - timein.minute)
    s=timein.hour*60+timein.minute


    # if x.hour*60+x.minute-1<=s<=x.hour*60+x.minute+1:
    #     time_in_slot=min(p,x.hour*60+x.minute+1-s)
    #     dataset[index][4]=time_in_slot
    #     p-=time_in_slot
    #     if p<=0:
    #         return 
    #     else:
    #         s=x.hour*60+x.minute+2


    # if x.hour*60+x.minute+2<=s<=x.hour*60+x.minute+6: 
    #     time_in_slot=min(2,p)
    #     dataset[index][5]=time_in_slot
    #     p-=time_in_slot 
    #     if p<=0:
    #         return

    if 530<=s<=580:
        time_in_slot=min(p,580-s)
        dataset[index][4]+=time_in_slot
        p-=time_in_slot
        if p<=0:
            return 
        else:
            s=580
    if 580<=s<=630:  #upper limit should be 630 deal with 10 min break
        time_in_slot=min(p,630-s)
        dataset[index][5]+=time_in_slot
        p-=time_in_slot 
        if p<=0:
            return 
        else:
            s=630
    if 630<=s<=640:
        time_in_slot=min(p,640-s)
        dataset[index][6]+=time_in_slot
        p-=time_in_slot 
        if p<=0:
            return 
        else:
            s=640

    if 640<=s<=690:
        time_in_slot=min(p,690-s)
        dataset[index][7]+=time_in_slot
        p-=time_in_slot
        if p<=0:
            return 
        else:
            s=690
    if 690<=s<=740:
        time_in_slot=min(740-s,p)
        dataset[index][8]+=time_in_slot
        p-=time_in_slot
        if p<=0:
            return 
        else:
            s=730
    if 740<=s<=790:
        time_in_slot=min(790-s,p)
        dataset[index][9]+=time_in_slot
        p-=time_in_slot
        if p<=0:
            return 
        else:
            s=780
    if 790<=s<=870:
        time_in_slot=min(870-s,p)
        dataset[index][10]+=time_in_slot
        p-=time_in_slot
        if p<=0:
            return 
        else:
            s=870
    if 870<=s<=920:
        time_in_slot=min(920-s,p)
        dataset[index][11]+=time_in_slot
        p-=time_in_slot
        if p<=0:
            return 
        else:
            s=920
    if 920<=s<=970:
        time_in_slot=min(970-s,p)
        dataset[index][12]+=time_in_slot
        p-=time_in_slot
        if p<=0:
            return 
        else:
            s=970
    if 970<=s<=1020:
        time_in_slot=min(1020-s,p)
        dataset[index][13]+=time_in_slot
        p-=time_in_slot
        if p<=0:
            return
    return

def calc_distance(target,name):
    img, faces = detector.findFaceMesh(frame,draw=False)
    c=0
    if faces:
        # min=sum(target)
        for i in range(len(faces)):
            face=faces[c]
            c+=1

            pointleft = face[145]
            pointright = face[374]
            cv2.circle(img, pointleft,5, (255,0,255),cv2.FILLED)
            cv2.circle(img, pointright,5, (255,0,255),cv2.FILLED)
            cv2.line(img, pointleft, pointright,(0,200,0),3)
            

            top,right,bottom,left=face[10][1],face[454][0],face[152][1],face[234][0]
            valid=abs(target[0]-top)+abs(target[1]-right)+abs(target[2]-bottom)+abs(target[3]-left)
            if valid<200:
                w,_ = detector.findDistance(pointleft,pointright)
                W = 6.3
                f = 1565
                d = (W*f)/w
                cvzone.putTextRect(img, f'Distance:{int(d)}cm',(face[10][0]-100, face[10][1]-50),scale =2)


                if d<80 and name not in dist_faces:
                    dist_faces.append(name)
def calc_distance2(target,name):
    img, faces = detector.findFaceMesh(frame2,draw=False)
    c=0
    if faces:
        # min=sum(target)
        for i in range(len(faces)):
            face=faces[c]
            c+=1

            pointleft = face[145]
            pointright = face[374]
            cv2.circle(img, pointleft,5, (255,0,255),cv2.FILLED)
            cv2.circle(img, pointright,5, (255,0,255),cv2.FILLED)
            cv2.line(img, pointleft, pointright,(0,200,0),3)
            

            top,right,bottom,left=face[10][1],face[454][0],face[152][1],face[234][0]
            valid=abs(target[0]-top)+abs(target[1]-right)+abs(target[2]-bottom)+abs(target[3]-left)
            if valid<200:

                w,_ = detector.findDistance(pointleft,pointright)
                W = 6.3
                f = 1565
                d = (W*f)/w
                cvzone.putTextRect(img, f'Distance:{int(d)}cm',(face[10][0]-100, face[10][1]-50),scale =2)

                if d<55 and name not in dist_faces2:
                    dist_faces2.append(name)

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

x=datetime.datetime.now()
hourly_update = datetime.datetime.now()

cred = ServiceAccountCredentials.from_json_keyfile_name("/Users/varun/Desktop/untitled_folder/desktop/ANOKHA/important/attendanceanokha.json",scopes = scope)

file = gspread.authorize(cred)

workbook = file.open("attendace_anokha")
sheet = workbook.sheet1


cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

detector = FaceMeshDetector(maxFaces=4)
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")
dataset = sheet.get_all_values()
inside=[]
names=[]
for i in dataset:
    if i[14]!="0":
        inside.append(i[1])
    names.append(i[1])
    i[4:14]=0,0,0,0,0,0,0,0,0,0

while True:
    dist_faces = []
    dist_faces2 = []
    isphone = 0
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()
    try:
        face_locations, face_names = sfr.detect_known_faces(frame)
        face_locations2, face_names2 = sfr.detect_known_faces(frame2)
    except:
        continue
    

    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,200), 4)
        calc_distance(list(face_loc),name)
        # print(dist_face

    for face_loc, name in zip(face_locations2, face_names2):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        cv2.putText(frame2, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2)
        cv2.rectangle(frame2, (x1, y1), (x2, y2), (0,0,200), 4)
        calc_distance2(list(face_loc),name)

    
    if len(dist_faces)!=0:

        # print("Yes1")
        for j in dist_faces:
            if j not in inside and j!="Unknown":
                inside.append(j)
                index=names.index(j)
                dataset[index][2]=datetime.datetime.now()
                dataset[index][14]=1
                print(dataset[index])
    if len(dist_faces2)!=0:
        # print("Yes2")
        for j in dist_faces2:
            if j in inside and j!="Unknown":
                inside.remove(j)
                index=names.index(j)
                dataset[index][3]=datetime.datetime.now()
                calcSlot(index)
                dataset[index][14]=0
                print(dataset[index])


    cv2.imshow("Inside", frame)
    cv2.imshow("Outside", frame2)

    curr_time=datetime.datetime.now()
    if curr_time.minute - hourly_update.minute == 2:
        hourly_update=curr_time
        print("Inside")
        print(inside)
        for i in inside:
            index=names.index(i)
            if i=="name":
                continue
            for j in range(2,15):
                if (j==2 or j==3) and dataset[index][j]!='' :
                    sheet.update_cell(index+1,j+1,json_serial(dataset[index][j]))
                else:
                    sheet.update_cell(index+1,j+1,dataset[index][j])

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cap2.release()



