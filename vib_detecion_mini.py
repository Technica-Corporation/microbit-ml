print("started")
import radio
from microbit import accelerometer,sleep
from gc import collect
train_runs=5
train_runs_std=5
wndw_sz=80
z_thresh=3
n_thresh=3
n_avgs=[0,0,0,0,0,0,0,0,0]
n_mag=n_mag_sum=0
n_x_frq=n_y_frq=n_z_frq=0
x_frqs,y_frqs,z_frqs=[[]for i in range(3)]
n_v=[0,0,0,0,0,0,0,0,0]
stds=[]
x_maxs,y_maxs,z_maxs,x_avgs,y_avgs,z_avgs,mags=[[]for i in range(7)]
x_mins,y_mins,z_mins=[[]for i in range(3)]
z_scores=[]
print('initialized')
def stdv(old_avg,new_vals):
 sum_diffsquared=0
 for val in new_vals:
  sum_diffsquared+=(val-old_avg)**2
 stddev=((sum_diffsquared)/len(new_vals))**(1/2)
 stds.append(stddev)
def z_score(val,mean,std):
 z_scores.append((val-mean)/std)
 return((val-mean)/std)
def get_n_values(frequency):
 global n_mag_sum,n_v
 vals=(accelerometer.get_values())
 print(vals)
 for w in range(3):
  if vals[w]>n_v[w]:n_v[w]=vals[w]
  elif vals[w]<n_v[w+3]:n_v[w+3]=vals[w]
 n_v[6]+=vals[0]
 n_v[7]+=vals[1]
 n_v[8]+=vals[2]
 n_mag_sum+=(int((vals[0])**2+(vals[1])**2+(vals[2])**2)**.5)
 if frequency==1:
  global n_f
  for q in range(3):
   if(vals[q]-n_f[0][q])*(n_f[2][q]-n_f[0][q])<0:
    n_f[1][q]+=1
  n_f[2][0],n_f[2][1],n_f[2][2]=vals[0],vals[1],vals[2]
 sleep(50)
for i in range(train_runs):
 n_mag_sum=0
 n_v=[0,0,0,0,0,0,0,0,0]
 for z in range(wndw_sz):
  get_n_values(0)
 t=train_runs
 for z in range(6):
  n_avgs[z]+=n_v[z]/t
 for y in range(3):
  n_avgs[y+6]+=(n_v[y+6]/wndw_sz)/t
 n_mag+=(n_mag_sum/wndw_sz)/t
 print('Window '+str(i+1)+' done')
collect()
for i in range(train_runs_std):
 n_v=[0,0,0,0,0,0,0,0,0]
 n_f=[[n_avgs[6],n_avgs[7],n_avgs[8]],[0,0,0],[0,0,0]]
 for z in range(wndw_sz):
  get_n_values(1)
 for t,v in enumerate((x_maxs,y_maxs,z_maxs,x_mins,y_mins,z_mins)):
  v.append(n_v[t])
 mags.append(n_mag/wndw_sz)
 x_avgs.append(n_v[6]/wndw_sz)
 y_avgs.append(n_v[7]/wndw_sz)
 z_avgs.append(n_v[8]/wndw_sz)
 n_x_frq=(n_f[1][0]/wndw_sz)
 n_y_frq=(n_f[1][1]/wndw_sz)
 n_z_frq=(n_f[1][2]/wndw_sz)
 x_frqs.append(n_f[1][0]);y_frqs.append(n_f[1][1]);z_frqs.append(n_f[1][2])
 print('Window '+str(i+1)+' completed')
for i,tup in enumerate((x_maxs,y_maxs,z_maxs,x_mins,y_mins,z_mins,x_avgs,y_avgs,z_avgs)):
 stdv(n_avgs[i],tup)
stdv(n_x_frq,x_frqs);stdv(n_y_frq,y_frqs);stdv(n_z_frq,z_frqs);stdv(n_mag,mags)
print(stds)
del x_maxs,y_maxs,z_maxs,x_avgs,y_avgs,z_avgs,mags,x_mins,y_mins,z_mins
del y_frqs, z_frqs, x_frqs
collect()
for i in range(40):
 n_v=[0,0,0,0,0,0,0,0,0]
 z_scores=[]
 n_f=[[n_avgs[6],n_avgs[7],n_avgs[8]],[0,0,0],[0,0,0]]
 for x in range(wndw_sz):
  get_n_values(1)
 for r in range(6):
  if stds[r]==0.0:stds[r]=.000001
  print(z_score(n_v[r],n_avgs[r],stds[r]))
 for r in range(3):
  n_v[r+6]=n_v[r+6]/wndw_sz
  if stds[r+6]==0.0:stds[r+6]=.000001
  print(z_score(n_v[r+6],n_avgs[r+6],stds[r+6]))
 n_mag_sum=n_mag_sum/wndw_sz
 print(z_score(n_f[1][0],n_x_frq,stds[9]))
 print(z_score(n_f[1][1],n_y_frq,stds[10]))
 print(z_score(n_f[1][2],n_z_frq,stds[11]))
 print(z_score(n_mag_sum,n_mag,stds[12]))
 print(' ----- ')
 thresh=0
 for item in z_scores:
  if abs(item)>z_thresh:
   thresh+=1
 if thresh>=n_thresh:
  radio.on()
  radio.send('flash')
  radio.off()
  continue
