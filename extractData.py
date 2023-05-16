count = 0
alt = 0
idArr = []
studentArr = [[0 for i in range(838)] for j in range(20)]
test = []
studentlist = [[] for j in range(838)]
altlist = [[] for j in range(838)]
alternate = [[0 for i in range(838)] for j in range(20)]
courselist = []
numStudents = []
numClasses = []

try:
       f=open("python.txt","r")
       while True:
                count = count + 1
                line=f.readline()
                test = line.split(",", 16)
                if line=='':
                    break
                
                if test[0] == 'ID':
                    count = 0
                    alt = 0
                    for i in range(len(test)):
                        if test[i] == 'ID':    
                            test[i] = test[i+1]
                            test[i+1] == ""
                            idArr.append(test[i])
                elif test[0] != 'Course':
                    if test[11] == 'Y':
                        count = count - 1
                        alternate[len(idArr) -1][alt] = test[0]
                        alt = alt + 1
                    else:    
                        studentArr[len(idArr) -1][count -1] = test[0]        
except FileNotFoundError:
       print ("File is not found")
else:
       f.close()



try:
       fi=open("py.txt","r")
       while True:
                
                line=fi.readline()
                test = line.split(",", 16)
                if line=='':
                    break
                courselist.append(test[0])
                numStudents.append(test[9])
                numClasses.append(test[14])
                




               
                
            
                     
              
except FileNotFoundError:
       print ("File is not found")
else:
       f.close()

print (numClasses)
for i in range(23):
    for j in range(23):
      if j == 0:
           print(idArr[i])
      if studentArr[i][j] != 0:
        studentlist[i].append(studentArr[i][j])
      if alternate[i][j] != 0:
        altlist[i].append(alternate[i][j])
      
    if i == 22:
        print(studentlist)
        print(" ")
        print(" ")
        print(" ")
        print(altlist)
