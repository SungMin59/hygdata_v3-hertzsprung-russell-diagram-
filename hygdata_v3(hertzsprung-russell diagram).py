import matplotlib.pyplot as plt
import numpy as np
import csv

fs=open('/content/hygdata_v3-abridged.csv', '', encoding='UTF8')
data=csv.reader(fs)

# codejump
next(data)
for k in range(0):
  next(data)

# hex to int
def Ox_int(arg:any):
  return int(arg,16)

# int to hex
def int_Ox(arg:any):
  value = hex(arg).replace('0x','')
  if len(value) == 1:
    return '0'+value
  else:
    return value

# arr
colorArr=('#ff0000','#ff8000','#ffff00','#ffff80','#ffffff','#8080ff','#0000ff')
scaleArr=(0.07, 0.09, 0.06, 0.047, 0.04, 0.06, 0.08)
constArr=(0,3500, 5000, 6000, 7500, 10000, 28000,110000)

# code
count = 0
for info in data:
  count += 1
  if count%500 == 0:
    print(count)
  if info[15] != '' and info[-1] != '':
    T, absmag = float(info[-1]), float(info[15])
    for op in range(6):
      TMin, TMax = constArr[op], constArr[op+1]
      CMin, CMax = colorArr[op].replace('#',''), colorArr[op+1].replace('#','')
      if TMin < T and T <= TMax:
        TLerp = (TMax - TMin)/10
        sMin = np.array([ Ox_int(CMin[0:2]), Ox_int(CMin[2:4]), Ox_int(CMin[4:6]) ])
        sMax = np.array([ Ox_int(CMax[0:2]), Ox_int(CMax[2:4]), Ox_int(CMax[4:6]) ])
        spect = abs((sMax - sMin)//10)
        spectLerp = np.array([0,0,0])
        for sp in range(10):
          if TLerp*(sp)+TMin < T and T <= TLerp*(sp+1)+TMin:
            for i in range(3):
              if sMin[i] > sMax[i]:
                spectLerp[i] = sMin[i] - (spect[i])*sp
              elif sMin[i] < sMax[i]:
                spectLerp[i] = sMin[i] + (spect[i])*sp
              else:
                spectLerp[i] = sMin[i]
            #print(spectLerp)
            color = '#' + str(int_Ox(spectLerp[0])) + str(int_Ox(spectLerp[1])) + str(int_Ox(spectLerp[2]))
            plt.scatter(T,absmag,scaleArr[op],c=color)

plt.xlim(22500, 0)
plt.ylim(20, -10)
plt.gca().set_facecolor('#000000')
plt.figure(figsize=(50,50))
plt.show()
