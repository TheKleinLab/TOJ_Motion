__author__ = "Austin Hurst"
from klibs.KLIndependentVariable import IndependentVariableSet

TOJ_Motion_ind_vars = IndependentVariableSet()

# Define project variables and variable types

# NOTE: an SOA of 0 indicates that the trial will be a color probe trial (which are 1/3 of trials)
flip = 1000/60.0 # Time required per refresh of the screen
soa_list = [(flip, 3), (flip*3, 2), (flip*6, 2), (flip*9, 2), (flip*16, 1), (0, 5)]

TOJ_Motion_ind_vars.add_variable("t1_location", str, ["left", "right"])
TOJ_Motion_ind_vars.add_variable("t1_shape", str, ["a", "b"])
TOJ_Motion_ind_vars.add_variable("toj_type", str, ["motion", "stationary"])
TOJ_Motion_ind_vars.add_variable("upper_target", str, ["t1", "t2"])
TOJ_Motion_ind_vars.add_variable("t1_t2_soa", float, soa_list)