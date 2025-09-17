#2021-05-29
#李长圣@成都
#走滑

start
set disk 0
log on
BOX left 1.0 right 70001.0 bottom 1.0 height 39999.0 kn= 11.2e9 ks=11.2e9 fric 0.00

GLINE P1 (  10000.0,  10000.0 ) P2 (  10000.0, 30000.0 ) r 80.0 color blue GROUP bom_wall
GLINE P1 (   9840.0,  10000.0 ) P2 (    100.0, 10000.0 ) r 80.0 color blue GROUP bom_wall1
GLINE P1 (   9840.0,  30000.0 ) P2 (    100.0, 30000.0 ) r 80.0 color blue GROUP bom_wall2
fix x y spin range group bom_wall
fix x y spin range group bom_wall1
fix x y spin range group bom_wall2


GLINE P1 (  50000.0,  10000.0 ) P2 (  50000.0, 30000.0 ) r 80.0 color blue GROUP top_wall
GLINE P1 (  50160.0,  10000.0 ) P2 (  60000.0, 10000.0 ) r 80.0 GROUP top_wall1
GLINE P1 (  50160.0,  30000.0 ) P2 (  60000.0, 30000.0 ) r 80.0 GROUP top_wall2
fix x y spin range group top_wall
fix x y spin range group top_wall1
fix x y spin range group top_wall2

WALL nodes (  30000.0,  10000.0 ) (  30000.0, 30000.0 ) kn= 11.2e9 ks=11.2e9 fric 0.00 GROUP fault
WALL nodes (  30000.0,  10000.0 ) (  30000.0, 30000.0 ) kn= 11.2e9 ks=11.2e9 fric 0.00 GROUP fault1

set large
set dt 1e-6
set gravity 0.0 -10.0
set damp 0.8

ini xvel 0.0 yvel 0.0 range x 100.0 50000.0 y 10000.0 30000.0
ini xvel 0.0 yvel 0.0 range x 50160.0 60000.0 y 10000.0 30000.0

ini xvel -0.1 yvel 0.0 range group bom_wall
ini xvel -0.1 yvel 0.0 range group bom_wall1
ini xvel -0.1 yvel 0.0 range group bom_wall2

ini xvel 0.1 yvel 0.0 range group top_wall
ini xvel 0.1 yvel 0.0 range group top_wall1
ini xvel 0.1 yvel 0.0 range group top_wall2

hist id 1 xvel 30000.0 20000.0
hist id 2 yvel 30000.0 20000.0
hist id 3 xdisp 30000.0 20000.0
hist id 4 ydisp 30000.0 20000.0

hist id 5 xvel 29999.0 20000.0
hist id 6 yvel 29999.0 20000.0
hist id 7 xdisp 29999.0 20000.0
hist id 8 ydisp 29999.0 20000.0

hist id 9 xvel 30001.0 20000.0
hist id 10 yvel 30001.0 20000.0
hist id 11 xdisp 30001.0 20000.0
hist id 12 ydisp 30001.0 20000.0

hist id 13 xforce range group fault
hist id 14 yforce range group fault

hist id 15 xforce range group fault1
hist id 16 yforce range group fault1

hist id 17 unbal

step 1000000

save gen.sav
quit
