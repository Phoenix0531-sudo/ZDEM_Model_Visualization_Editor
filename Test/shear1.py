
######################################
# title: Strike-slip experiment simulation
# date: 2022-05-11
# authors: Project Contributors
# E-mail: project.contributors@example.com
# note:
# 括号内参数可根据模型大小及个人需要修改
# 脚本命令不区分大小写
# 用12个核心，实际用时<3小时
# more info, see www.geovbox.com
# 用的竖起来的40*20的模型，删除右侧颗粒达到40*8.5
# 采用T1*0.5的参数 双向压缩，速度为0.05  距离为2000 
# save 1000改为save 500
# 先存断层宽度500减为250 dpi改为由默认600改为200
# prop fric 0.3 ebmod 2e8 gbmod 2e8 tstrength 1e7 sstrength 2e7 老师让整体乘以0.5########二分之一T1
#######################################


load ini_xyr.dat
prop group ball_rand

set disk 0
log on
BOX left 1.0 right 70001.0 bottom 1.0 height 39999.0 kn= 11.2e9 ks=11.2e9 fric 0.00

# 删除x=18500线右侧的颗粒，使模型宽度达到要求
DEL RANGE y 18500.0 999000.0

# GLINE P1 (   10000.0,  10000.0 ) P2 (  20001.0, 10000.0 ) r 80.0 color blue GROUP bom_wall
# GLINE P1 (   10000.0,   9840.0 ) P2 (  10000.0,  5000.0 ) r 80.0 color blue GROUP bom_wall1
# GLINE P1 (   20000.0,   9840.0 ) P2 (  20000.0,  5000.0 ) r 80.0 color blue GROUP bom_wall2
# prop group bom_move1 range x (15000.0 20001.0) y ( 9999.0 10001.0) 
# fix x y spin range group bom_move1
# fix x y spin range group bom_wall
# fix x y spin range group bom_wall1
# fix x y spin range group bom_wall2

# GLINE P1 (   10000.0, 30000.0 ) P2 (  20001.0, 30000.0 ) r 80.0 color blue GROUP top_wall
# GLINE P1 (   10000.0, 30160.0 ) P2 (  10000.0, 40000.0   ) r 80.0 GROUP top_wall1
# GLINE P1 (   20000.0, 30160.0 ) P2 (  20000.0, 40000.0  ) r 80.0 GROUP top_wall2
# prop group top_move1 range x (15000.0 20001.0) y (29999.0 30001.0) 
# fix x y spin range group top_move1
# prop color blue range group top_wall1
# prop color blue range group top_wall2
# fix x y spin range group top_wall
# fix x y spin range group top_wall1
# fix x y spin range group top_wall2


# GLINE P1 (    9840.0, 8000.0 ) P2 (     9840.0, 35000.0 ) r 80.0 GROUP lef_wall
# GLINE P1 (   20160.0, 8000.0 ) P2 (    20160.0, 35000.0 ) r 80.0 GROUP rig_wall
# prop color red range group lef_wall
# prop color red range group rig_wall
# fix x y spin range group lef_wall
# fix x y spin range group rig_wall

# prop fric 0.0 ebmod 2e8 gbmod 2e8 tstrength 1e100 sstrength 1e100 rubber range group lef_wall
# prop fric 0.0 ebmod 2e8 gbmod 2e8 tstrength 1e100 sstrength 1e100 rubber range group rig_wall
#ini  xp   10e6 range group lef_wall
#ini  xp  -10e6 range group rig_wall
#free x  range group lef_wall
#free x  range group rig_wall 
#fix x y spin range x  3839.9 3840.1  y    0.0  3000.0
#fix x y spin range x  3839.9 3840.1  y 15000.0 18000.0
#fix x y spin range x 12159.9 12160.1  y    0.0  3000.0
#fix x y spin range x 12159.9 12160.1  y 15000.0 18000.0

prop color mg  group left range y 10000.0 12250.0, x 0.0  10160.0
prop color mg  group left range y 10000.0 10160.0, x 10160.0  49840.0
prop color mg  group left range y 10000.0 16250.0, x 49840.0  60000.0

prop color blue  group right range y 12250.0 18500.0, x 0.0  10160.0
prop color blue  group right range y 18340.0 18500.0, x 10160.0  49840.0
prop color blue  group right range y 16250.0 18500.0, x 49840.0  60000.0

fix x y spin range group left
fix x y spin range group right

PROP fric 0.0 den 2.5e3, shear 2.9e9, poiss 0.2, damp 0.7 hertz

# prop color lg     range x 9920.1 30079.9, y 10001.0  12000.0
# prop color green  range x 9920.1 30079.9, y 15000.0  20000.0
# prop color yellow range x 9920.1 30079.9, y 20000.0  25000.0
# prop color red    range x 9920.1 30079.9, y 25000.0  30000.0
# prop color white  range x 9920.1 30079.9, y 30000.0  35000.0
# prop color black  range x 9920.1 30079.9, y 35000.0  40000.0
# prop color mg     range x 9920.1 30079.9, y 40000.0  45000.0
# prop color blue   range x 9920.1 30079.9, y 45000.0  50000.0
# prop color gb     range x 9920.1 30079.9, y 50000.0  60000.0


#prop color red    range x 9920.1 30079.9, y 10000.0  10200.0
prop color yellow    range y 10160.0 18500.0, x 20000.0  20200.0
prop color yellow    range y 10160.0 18500.0, x 30000.0  30200.0
prop color yellow    range y 10160.0 18500.0, x 40000.0  40200.0

prop color mg  range group left
prop color blue  range group right

#prop color blue   range x 15000.0 15200.0, y 10001.0  29999.0
#prop color blue   range x 20000.0 20200.0, y 10001.0  29999.0

set dt 5e-2, Gravity 0.0 0.0
;set damp lsm 1e5
prop damp 0.7
set save 50000
set print 50000
set ps 10000
set stepbar 100
draw interval 100 -bline bfill bondc wall


CYC 1000
#pause

# prop fric 0.3 ebmod 2e8 gbmod 2e8 tstrength 1e7 sstrength 2e7 老师让整体乘以0.5########
prop fric 0.15 ebmod 1e8 gbmod 1e8 tstrength 0.5e7 sstrength 1e7  

#设置先存断层
prop group presturct range P4 (10500.0, 12125.0) (10600.0, 12225.0) (19980.0 14375.0) (19980.0 14475.0)
prop group presturct range P4 (19980.0, 14375.0) (20080.0, 14475.0) (29080.0 15375.0) (29180.0 15475.0)
prop group presturct range P4 (29080.0, 15125.0) (29180.0, 15225.0) (48920.0 16375.0) (49020.0 16475.0)
prop color red range group presturct
bond break range group presturct

# HIST ID 1 INTERVAL 1 , gstress group top_wall 
# HIST ID 2 INTERVAL 1 , gstrain group top_wall|bom_wall 
# ;HIST ID 1 INTERVAL 10 , wall id 3 ystress
# ;HIST ID 2 INTERVAL  10 , ystrain wall 0|3

# !HIST ID 1 INTERVAL 10 , kinetic 
# ;HIST ID 2 INTERVAL 10 , step
# plot hist 2 1


ini  xv -0.05 range group left
ini  xv 0.05 range group right

WALL id 0 nodes ( 1000.0, 14250.0 )   ( 1000.0, 18500.0 ) kn=2e3 ks=2e3 fric=0.00 color=1
WALL ID 0 xv 0.05
imple wall id 0 xm 500.0 save 500.0 print 500.0 ps 500.0
stop

