######################################
# title: jiaoliqing论文里的走滑实验模拟
# date: 2022-05-11
# authors: 张召
# E-mail: 1034860292@qq.com
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
GLINE P1 (   100.0,  10000.0 ) P2 (  18500.0, 10000.0 ) r 80.0 color blue GROUP bom_wall
GLINE P1 (   100.0,  30000.0 ) P2 (  18500.0, 30000.0 ) r 80.0 color blue GROUP top_wall
GLINE P1 (   100.0,  10000.0 ) P2 (    100.0, 30000.0 ) r 80.0 color blue GROUP left_wall
GLINE P1 ( 18500.0,  10000.0 ) P2 (  18500.0, 30000.0 ) r 80.0 color blue GROUP right_wall

fix x y spin range group bom_wall
fix x y spin range group top_wall
fix x y spin range group left_wall
fix x y spin range group right_wall

WALL nodes (  9250.0,  10000.0 ) (  9250.0, 30000.0 ) kn= 11.2e9 ks=11.2e9 fric 0.00 GROUP fault

set large
set dt 1e-6
set gravity 0.0 -10.0
set damp 0.8

ini xvel 0.0 yvel 0.0 range x 100.0 18500.0 y 10000.0 30000.0

# 双向压缩
ini xvel -0.05 yvel 0.0 range group left_wall
ini xvel 0.05 yvel 0.0 range group right_wall

hist id 1 xvel 9250.0 20000.0
hist id 2 yvel 9250.0 20000.0
hist id 3 xdisp 9250.0 20000.0
hist id 4 ydisp 9250.0 20000.0

hist id 5 xvel 9249.0 20000.0
hist id 6 yvel 9249.0 20000.0
hist id 7 xdisp 9249.0 20000.0
hist id 8 ydisp 9249.0 20000.0

hist id 9 xvel 9251.0 20000.0
hist id 10 yvel 9251.0 20000.0
hist id 11 xdisp 9251.0 20000.0
hist id 12 ydisp 9251.0 20000.0

hist id 13 xforce range group fault
hist id 14 yforce range group fault

hist id 15 unbal

# 压缩阶段
step 500000

# 保存压缩后状态
save compress.sav

# 剪切阶段
ini xvel 0.0 yvel 0.0 range x 100.0 18500.0 y 10000.0 30000.0
ini xvel 0.0 yvel -0.05 range group bom_wall
ini xvel 0.0 yvel 0.05 range group top_wall

step 1000000

save shear.sav
quit
