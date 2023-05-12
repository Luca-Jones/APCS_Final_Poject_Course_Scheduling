count = 0
idArr = []
studentArr = [[0 for i in range(23)] for j in range(23)]
test = []
try:
       f=open("python.txt","r")
       while True:
                count = count + 1
                line=f.readline()
                test = line.split(",", 1)
              
                if test[0] == 'ID':
                    count = 0
                    for i in range(len(test)):
                        if test[i] == 'ID':    
                            test[i] = test[i+1]
                            test[i+1] == ""
                            idArr.append(test[i])
                elif test[0] != 'Course':
                    studentArr[len(idArr) -1][count -1] = test[0]
                
                if line=='':
                    break
                
except FileNotFoundError:
       print ("File is not found")
else:
       f.close()


for i in range(23):
    for j in range(23):
      if j == 0:
           print(idArr[i])
      if studentArr[i][j] != 0:
        print(studentArr[i][j] , end = ' ' )
      if j == 22:
           print(" ")
           print(" ")
           print(" ")