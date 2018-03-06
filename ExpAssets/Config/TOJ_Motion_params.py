### Klibs Parameter overrides ###

# All of these values can be overridden locally in a file here:
# TOJ_Motion/ExpAssets/Local/TOJ_Motion_params.py
# You will need to create it if it doesn't already exist.

from klibs import P

#########################################
# Runtime Settings
#########################################
collect_demographics = True
manual_demographics_collection = False
manual_trial_generation = False
run_practice_blocks = True
multi_user = False
view_distance = 57 # in centimeters, 57cm = 1 deg of visual angle per cm of screen
slack_messaging = True

#########################################
# Available Hardware
#########################################
eye_tracker_available = False
eye_tracking = False
labjack_available = False
labjacking = False

#########################################
# Environment Aesthetic Defaults
#########################################
default_fill_color = (128, 128, 128, 255)
default_color = (255, 255, 255, 255)
default_font_size = 28
default_font_name = 'Roboto-Medium'

#########################################
# EyeLink Settings
#########################################
manual_eyelink_setup = False
manual_eyelink_recording = False

saccadic_velocity_threshold = 20
saccadic_acceleration_threshold = 5000
saccadic_motion_threshold = 0.15

#########################################
# Experiment Structure
#########################################
multi_session_project = False
trials_per_block = 360
blocks_per_experiment = 2 # practice blocks are appended later in experiment.py
table_defaults = {} 
conditions = ['first', 'second']

#########################################
# Development Mode Settings
#########################################
dm_auto_threshold = True
dm_trial_show_mouse = True
dm_ignore_local_overrides = False
dm_show_gaze_dot = True

#########################################
# Data Export Settings
#########################################
primary_table = "trials"
unique_identifier = "userhash"
default_participant_fields = [[unique_identifier, "participant"], "gender", "age", "handedness"]
default_participant_fields_sf = [[unique_identifier, "participant"], "random_seed", "gender", "age", "handedness"]

#########################################
# PROJECT-SPECIFIC VARS
#########################################
trials_per_practice_block = 40
use_numpad = True # If True, use numpad '2' and '8' instead of regular '2' and '8' for responses
default_condition = 'first' # if no condition specified, default to 'first'