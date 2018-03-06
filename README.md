# TOJ_Motion

TOJ_Motion is an experiment program for a study looking at how temporal order judgements (TOJs) differ between contexts where people are asked to judge which of two *stationary* shapes appeared first (or second) on a line, versus when they are asked to judge which of two *moving* shapes touched the line first (or second).

![TOJ_Motion_combined_trial](https://github.com/TheKleinLab/TOJ_Motion/raw/master/toj_motion.gif)


In addition, this experiment program presents colour probes at shape locations on a random third of trials, to verify that attention is being biased to the desired location for that block.

## Requirements

TOJ_Motion is programmed in Python 2.7 using the [KLibs framework](https://github.com/a-hurst/klibs). It has been developed and tested on macOS (10.9 through 10.13), but should also work with minimal hassle on computers running [Ubuntu](https://www.ubuntu.com/download/desktop) or [Debian](https://www.debian.org/distrib/) Linux. It is not currently compatible with any version of Windows, nor will it run under the [Windows Subsystem for Linux](https://msdn.microsoft.com/en-us/commandline/wsl/install_guide).

## Getting Started

### Installation

First, you will need to install the KLibs framework by following the instructions [here](https://github.com/a-hurst/klibs).

Then, you can then download and install the experiment program with the following commands (replacing `~/Downloads` with the path to the folder where you would like to put the program folder):

```
cd ~/Downloads
git clone https://github.com/TheKleinLab/TOJ_Motion.git
```

### Running the Experiment

TOJ_Motion is a KLibs experiment, meaning that it is run using the `klibs` command at the terminal (running the 'experiment.py' file using python directly will not work).

To run the experiment, navigate to the TOJ_Motion folder in Terminal and run `klibs run [screensize]`,
replacing `[screensize]` with the diagonal size of your display in inches (e.g. `klibs run 24` for a 24-inch monitor). If you just want to test the program out for yourself and skip demographics collection, you can add the `-d` flag to the end of the command to launch the experiment in development mode.

#### Optional Settings

The experiment program allows you to choose whether participants should be asked to judge which shape was **first** or which shape was **second**. To specify which condition to run, launch the experiment with the `--condition` or `-c` flag, followed by `first` or `second`. For example, if you wanted to run the experiment asking which shape was second on a computer with a 20-inch monitor, you would run 

```
klibs run 20 --condition second
```

If no condition is manually specified, the experiment program defaults to asking which shape was **first**.

Additionally, by default, responses in TOJ\_Motion are made using the '8' and '2' keys on the keyboard numpad. If you want to test out TOJ\_Motion on a computer that doesn't have a numpad (e.g. most laptops), you can open the experiment's parameters file (`ExpAssets/Config/TOJ_Motion_params.py`) and change the value of the variable `use_numpad` from 'True' to 'False'. This will map the TOJ response keys to the number row '8' and '2' instead.
