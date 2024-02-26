\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  y[0] + y[1] + y[2]
Subject To
 R0: x[0] + x[1] - 2 y[0] >= 0
 R1: x[2] - y[1] >= 0
 R2: x[4] + x[5] - 2 y[2] >= 0
 R3: 6 y[0] <= 6
 R4: x[3] + 6 y[1] <= 6
 R5: x[2] + 6 y[2] <= 6
Bounds
Binaries
 x[0] x[1] x[2] x[3] x[4] x[5] y[0] y[1] y[2]
End
