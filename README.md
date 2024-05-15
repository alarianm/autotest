# Testing PuSHR 

This tutorial provides a comprehensive guide to testing PuSHR configurations. 

## Introduction 
Available test configurations are as follows: 
| Test Configuration | Code  |
|--------------------|-------|
| TA+CLCBS+MPC      | PuSHR |
| CLCBS+MPC         | GP-CA |
| CLCBS+PP          | GP    |
| NHTTC             | LC    |
| TA+NHTTC          | LC-TA |

## NHTTC 
Follow instructions [here](https://github.com/prl-mushr/nhttc_ros) to download NHTTC

## Autotest Set up

To initiate the autotest setup, follow these steps:

  1. Modify the paths in the .yaml file located at ~/catkin_ws/src/PuSHR-Noetic/mushr_pixelart_mpc/config/autotest.yaml to match your system configuration.
  2. Adjust the num_iterations parameter to specify the number of iterations for each test configuration.
  3. Update the bench_name to reflect the name of the file you're currently using for testing.
  4. Modify the autotest.py script located at ~/catkin_ws/src/PuSHR-Noetic/mushr_pixelart_mpc/scripts/autotest_mpc.py to match your setup.

```bash
for i in range(6):
    test = autotest("/home/stark/catkin_mushr/src/mushr_pixelart_mpc/config/autotest.yaml", "ex" + str(i + 1))
    test.run_autotest()
```

Make sure to modify the file path to match your set up. As is shown above, autotest.py will run the scenarios included in `~/catkin_ws/src/PuSHR-Noetic/mushr_pixelart_mpc/benchmarks`.

For running a single scenario, use:
```bash
for i in range(1):
    test = autotest("/your/file/path/src/mushr_pixelart_mpc/config/autotest.yaml", "your_file_name")
    test.run_autotest()
```

To make your own configuration of test scenarios, follow the same format of the .yaml files included in` ~/catkin_ws/src/PuSHR-Noetic/mushr_pixelart_mpc/benchmarks`



## Results Set up

Organize the results of your tests by creating folders in the following format for each test scenario run:

~/catkin_ws/src/PuSHR-Noetic/mushr_pixelart_mpc/bags/test_file_name/test_configuration

For example, when running ex1 and testing all configurations, create folders like:

    ~/catkin_ws/src/PuSHR-Noetic/mushr_pixelart_mpc/bags/ex1/TA+CLCBS+MPC
    ~/catkin_ws/src/PuSHR-Noetic/mushr_pixelart_mpc/bags/ex1/CLCBS+MPC
    ~/catkin_ws/src/PuSHR-Noetic/mushr_pixelart_mpc/bags/ex1/CLCBS+PP
    ~/catkin_ws/src/PuSHR-Noetic/mushr_pixelart_mpc/bags/ex1/NHTTC
    ~/catkin_ws/src/PuSHR-Noetic/mushr_pixelart_mpc/bags/ex1/TA+NHTTC
This step must be completed before running autotest.

## Data Collection of Results 

After simulations, results are stored in matrices (refer to lines 414-420 in autotest.py). To view these results, utilize data.py included in ` ~/catkin_ws/src/PuSHR-Noetic/mushr_pixelart_mpc/scripts` and adjust the file paths accordingly. The results will be displayed on the screen.


## Visualizing with rviz

In a terminal:

```bash
rviz -d ~/catkin_ws/src/clcbs_ros/rviz/clcbs.rviz
```

Make sure to start rviz before launching `init_clcbs.launch`.

