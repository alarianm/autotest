import numpy as np
import os

# Change directory to the location of the file
os.chdir('/home/arianaverges/catkin_ws/src/PuSHR-Noetic-main/mushr_pixelart_mpc/bags/ex2/TA+NHTTC')

data = np.load('output_raw.npy')

ones_count_row1 = 0
zeros_count_row1 = 0
ones_count_row2 = 0
zeros_count_row2 = 0
ones_count_row7 = 0
zeros_count_row7 = 0

averages = []

for row_idx, row in enumerate(data):
    if row_idx == 0:
        ones_count_row1 += np.sum(row == 1)
        zeros_count_row1 += np.sum(row == 0)
    elif row_idx == 1:
        ones_count_row2 += np.sum(row == 1)
        zeros_count_row2 += np.sum(row == 0)
    elif row_idx == 6:
        ones_count_row7 += np.sum(row == 1)
        zeros_count_row7 += np.sum(row == 0)
    else:
       
        row_average = np.mean(row)
        averages.append(row_average)


print("Success", ones_count_row1)
print("Failure:", zeros_count_row1)
print("We had collision", ones_count_row2)
print("No collision", zeros_count_row2)
print("Deadlock occured", ones_count_row7)
print("No deadlock", zeros_count_row7)

for idx, avg in enumerate(averages, start=2):
    
    if idx == 2:
        print("CTE list:", avg)
    elif idx == 3:
        print("Block dist list:", avg)
    elif idx == 4:
        print("Time list:", avg)
    elif idx == 5:
        print("Min dist list:", avg)
    elif idx == 7:
        print("Block angle list:", avg)