__author__ = "Austin Hurst"

# Import required KLibs classes and functions
import klibs
from klibs.KLConstants import TK_S, TK_MS, RC_KEYPRESS, RC_COLORSELECT
from klibs import P
from klibs.KLUtilities import deg_to_px, flush
from klibs.KLUserInterface import any_key, ui_request
from klibs.KLKeyMap import KeyMap
from klibs.KLTime import CountDown
from klibs.KLGraphics import fill, blit, flip
from klibs.KLGraphics import KLDraw as kld
from klibs.KLCommunication import message, slack_message
from klibs.KLEventInterface import TrialEventTicket as ET
from klibs.KLResponseCollectors import ResponseCollector

# Import additional required libraries
from math import sqrt
import random
import time
import sdl2

# Define colours for the experiment
WHITE = [255, 255, 255, 255]
BLACK = [0, 0, 0, 255]


class TOJ_Motion(klibs.Experiment):

    def __init__(self, *args, **kwargs):
        super(TOJ_Motion, self).__init__(*args, **kwargs)

    def setup(self):
        
        # Stimulus Sizes
        
        target_size = deg_to_px(3.0)
        diamond_size = sqrt(target_size**2/2.0)
        probe_diameter = deg_to_px(1.0)
        wheel_diameter = deg_to_px(16.0)
        
        # Stimulus Drawbjects
        
        self.line_a = kld.Rectangle(width=P.screen_x/2, height=2, fill=WHITE)
        self.line_b = kld.Rectangle(width=P.screen_x/2, height=2, fill=BLACK)
        self.diamond_a = kld.Rectangle(diamond_size, fill=WHITE, rotation=45)
        self.diamond_b = kld.Rectangle(diamond_size, fill=BLACK, rotation=45)
        self.probe = kld.Ellipse(probe_diameter, fill=None)
        self.wheel = kld.ColorWheel(wheel_diameter)
        
        self.line_a.render()
        self.line_b.render()
        self.diamond_a.render()
        self.diamond_b.render()
        
        # Layout
        
        self.left_x = P.screen_x/4
        self.right_x = 3*P.screen_x/4
        self.probe_positions = {
            "left": (self.left_x, P.screen_c[1]),
            "right": (self.right_x, P.screen_c[1])
        }
    
        self.start_baseline = P.screen_y/4
        self.end_offset = deg_to_px(5.0)
        self.left_start = [self.left_x, P.screen_y/4]
        self.right_start = [self.right_x, 3*P.screen_y/4]
        self.left_end = [self.left_x, P.screen_c[1]+self.end_offset]
        self.right_end = [self.right_x, P.screen_c[1]-self.end_offset]
        
        # Timing
        
        self.motion_duration = 1.5 # seconds
        
        # Experiment Messages
        
        if not P.condition:
            P.condition = P.default_condition
            
        toj_string = "Which shape {0} {1}?\n(White = 8   Black = 2)"
        stationary_string = toj_string.format("appeared", P.condition)
        motion_string = toj_string.format("touched the line", P.condition)
        self.toj_prompts = {
            'stationary': message(stationary_string, align="center", blit_txt=False),
            'motion': message(motion_string, align="center", blit_txt=False)
        }
        
        # Initialize ResponseCollector keymaps

        if P.use_numpad:
            keysyms = [sdl2.SDLK_KP_8, sdl2.SDLK_KP_2]
        else:
            keysyms = [sdl2.SDLK_8, sdl2.SDLK_2]

        self.toj_keymap = KeyMap(
            "toj_responses", # Name
            ['8', '2'], # UI labels
            ['white', 'black'], # Data labels
            keysyms # SDL2 Keysyms
        )

        # Initialize second ResponseCollector object for colour wheel responses

        self.wheel_rc = ResponseCollector()
        
        # Generate practice blocks
        
        default_soas = self.trial_factory.exp_factors['t1_t2_soa']
        toj_soas = [soa for soa in default_soas if soa!=0.0]
        toj_only = {"t1_t2_soa": toj_soas}
        probe_only = {"t1_t2_soa": [0.0]}
        
        if P.run_practice_blocks:
            num = P.trials_per_practice_block
            self.insert_practice_block(1, trial_counts=num, factor_mask=toj_only)
            self.insert_practice_block((2,4), trial_counts=num, factor_mask=probe_only)
        self.trial_factory.dump()


    def block(self):
        
        # Determine probe bias for block and generate list of probe locs accordingly
        
        if P.block_number > 3:
            self.probe_bias = "left"
            nonbiased_loc = "right"
        else:
            self.probe_bias = "right"
            nonbiased_loc = "left"
        loc_list = [self.probe_bias]*4 + [nonbiased_loc]
        self.probe_locs = loc_list * int(P.trials_per_block/float(len(loc_list))+1)
        random.shuffle(self.probe_locs)
        
        # At the start of each block, display a start message (block progress if experimental block,
        # practice message if practice block). After 3000ms, keypress will start first trial.
        
        probe_msg = (
            "During this block, the colour target will appear more often on the "
            "{0} and less often on the {1}.".format(self.probe_bias, nonbiased_loc)
        )
        header = "Block {0} of {1}".format(P.block_number, P.blocks_per_experiment)
        if P.practicing:
            header = "This is a practice block. ({0})".format(header)
        if P.block_number > 1:
            msg = message(header+"\n"+probe_msg, align="center", blit_txt=False)
        else:
            msg = message(header, blit_txt=False)

        message_interval = CountDown(1)
        while message_interval.counting():
            ui_request() # Allow quitting during loop
            fill()
            blit(msg, 8, (P.screen_c[0], P.screen_y*0.4))
            flip()
        flush()
        
        fill()
        blit(msg, 8, (P.screen_c[0], P.screen_y*0.4))
        message("Press any key to start.", registration=5, location=[P.screen_c[0], P.screen_y*0.6])
        flip()
        any_key()

        # When running participants, send halfway point and last-block notifications to researcher via Slack

        if not P.development_mode:
            if P.block_number == 3: # If participant is halfway done
                slack_message("Halfway done ({0}/{1})".format(P.block_number, P.blocks_per_experiment))
        
        
    def setup_response_collector(self):
        
        # Determine what type of trial it is before setting up response collector
        
        self.probe_trial = self.t1_t2_soa == 0
        
        # Set up Response Collector to get keypress responses

        self.rc.uses(RC_KEYPRESS)
        self.rc.terminate_after = [3500, TK_MS] # response period times out after 3500ms
        self.rc.keypress_listener.interrupts = True

        if self.probe_trial:
            self.wheel_rc.uses(RC_COLORSELECT)
            self.wheel_rc.terminate_after = [10, TK_S]
            self.wheel_rc.display_callback = self.wheel_callback
            self.wheel_rc.color_listener.interrupts = True
            self.wheel_rc.color_listener.color_response = True
            self.wheel_rc.color_listener.set_wheel(self.wheel)
            self.wheel_rc.color_listener.set_target(self.probe)
        else:
            self.rc.keypress_listener.key_map = self.toj_keymap
            self.rc.display_callback = None


    def trial_prep(self):
        
        # Determing the starting locations of the two target shapes
    
        if self.t1_location == "left":
            t1_x = self.left_x
            t2_x = self.right_x
        else:
            t1_x = self.right_x
            t2_x = self.left_x
            
        # Set shapes for t1 and t2
        
        if self.t1_shape == "a":
            self.t1 = self.diamond_a
            self.t2 = self.diamond_b
            self.t1_line = self.line_b
            self.t2_line = self.line_a
        else:
            self.t1 = self.diamond_b
            self.t2 = self.diamond_a
            self.t1_line = self.line_a
            self.t2_line = self.line_b
        
        self.t1_pos = (t1_x, P.screen_c[1])
        self.t2_pos = (t2_x, P.screen_c[1])

        # Initialize start/end positions and animation paths
        
        if self.toj_type == "motion":
            self.start_offset = P.screen_y/4 + deg_to_px(random.uniform(-2, 2))
            end_offset = deg_to_px(5.0)
            
            if self.upper_target == "t2":
                self.start_offset *= -1
                end_offset *= -1
                self.t1_reg = 8
                self.t2_reg = 2
            else:
                self.t1_reg = 2
                self.t2_reg = 8
                
            t1_start = (t1_x, P.screen_c[1]-self.start_offset)
            t1_end = (t1_x, P.screen_c[1]+end_offset)
            self.t1_path = Animation(t1_start, t1_end, self.motion_duration)
            
            t2_offset = self.t1_path.motion_per_ms[1] * self.t1_t2_soa
            t2_start = (t2_x, P.screen_c[1]+self.start_offset+t2_offset)
            t2_end = (t2_x, P.screen_c[1]-end_offset+t2_offset)
            self.t2_path = Animation(t2_start, t2_end, self.motion_duration)
            
            print(self.upper_target, self.t1_location, self.t1_t2_soa, self.start_offset, t2_offset)
            print("t1 start: {0} end: {1}".format(t1_start, t1_end))
            print("t2 start: {0} end: {1}".format(t2_start, t2_end))

        # Set up colour probe and colour wheel

        self.wheel.rotation = random.randrange(0, 360, 1)
        self.wheel.render()
        self.probe.fill = self.wheel.color_from_angle(random.randrange(0, 360, 1))
        self.probe.render()
        
        # Determine the probe location for the trial
        
        self.probe_location = self.probe_locs.pop()
        self.probe_pos = self.probe_positions[self.probe_location]
        
        # Calculate when t1 onset and t2 off are going to be based on motion
        
        if self.toj_type == "motion":
            self.t1_on = (1/self.t1_path.motion_per_ms[1])*self.start_offset
            self.t2_off = (1/self.t1_path.motion_per_ms[1])*(self.start_offset+end_offset)
        else:
            self.t1_on = self.random_interval(700, 1200)
            self.t2_off = self.t1_on + self.t1_t2_soa-1 + 300
        
        # Add timecourse of events to EventManager
        
        events = []
        events.append([self.t1_on, 't1_on'])
        events.append([events[-1][0] + 200, 'probe_off'])
        events.append([events[-2][0] + self.t1_t2_soa-1, 't2_on'])
        events.append([self.t2_off, 't2_off'])
        for e in events:
            self.evm.register_ticket(ET(e[1], e[0]))

    def trial(self):
        
        # Display the stimuli in sequence (which stimuli and in which sequence is
        # determined above in trial_prep).
        
        while self.evm.before('t2_off'):
            ui_request()
            
            fill()
            blit(self.t1_line, 5, self.t1_pos)
            blit(self.t2_line, 5, self.t2_pos)
            
            if self.toj_type == "motion":
                blit(self.t1, self.t1_reg, self.t1_path.position)
                blit(self.t2, self.t2_reg, self.t2_path.position)
            else:
                if self.evm.after('t1_on'):
                    blit(self.t1, 5, self.t1_pos)
                if self.evm.after('t2_on'):
                    blit(self.t2, 5, self.t2_pos)
                
            if self.probe_trial and self.evm.between('t1_on', 'probe_off'):
                blit(self.probe, 5, self.probe_pos)
                
            flip()
        
        # After 2nd target is off, collect either TOJ response or colour wheel response
        # depending on trial type.
        
        if self.probe_trial:
            self.wheel_rc.collect()
        else:
            self.toj_callback()
            self.rc.collect()
        
        # Parse collected response data before writing to the database
        
        if not self.probe_trial:
            toj_response = self.rc.keypress_listener.response(rt=False)
            toj_rt = self.rc.keypress_listener.response(value=False)
            if toj_response == 'NO_RESPONSE':
                toj_response, toj_rt = ['NA', 'timeout']
            response_col, angle_err, wheel_rt = ['NA', 'NA', 'NA']
        else:
            try:
                angle_err, response_col = self.wheel_rc.color_listener.response(rt=False)
                wheel_rt = self.wheel_rc.color_listener.response(value=False)
                response_col = list(response_col) # to be consistent with probe_col
            except ValueError:
                # if no response made (timeout), only one value will be returned
                angle_err, response_col, wheel_rt = ['NA', 'NA', 'timeout']
            toj_response, toj_rt = ['NA', 'NA']

        return {
            "block_num": P.block_number,
            "trial_num": P.trial_number,
            "toj_condition": P.condition,
            "trial_type": 'probe' if self.probe_trial else 'toj',
            "target_type": self.toj_type,
            "t1_location": self.t1_location,
            "t1_type": "white" if self.t1_shape == "a" else "black",
            "upper_target": self.upper_target if self.toj_type == "motion" else 'NA',
            "t1_t2_soa": self.t1_t2_soa,
            "toj_response": toj_response,
            "toj_rt": toj_rt,
            "probe_loc": self.probe_location if self.probe_trial else 'NA',
            "probe_col": str(self.probe.fill_color[:3]) if self.probe_trial else 'NA',
            "response_col": str(response_col[:3]),
            "angle_err": angle_err,
            "wheel_rt": wheel_rt
        }

    def trial_clean_up(self):
        self.wheel_rc.reset()

    def clean_up(self):
        pass
    
    
    def toj_callback(self):
        fill()
        blit(self.toj_prompts[self.toj_type], 5, P.screen_c)
        flip()
    
    def wheel_callback(self):
        fill()
        blit(self.wheel, location=P.screen_c, registration=5)
        flip()
        
    def random_interval(self, lower, upper, refresh=None):

        # utility function to generate random interval respecting the refresh rate of the monitor,
        # since stimuli can only be changed at refreshes. Converts upper/lower bounds in ms to
        # flips per the refresh rate, selects random number of flips, then converts flips back to ms.

        if not refresh:
            refresh = P.refresh_rate
        time_per_flip = 1000.0/refresh
        min_flips = int(round(lower/time_per_flip))
        max_flips = int(round(upper/time_per_flip))
        return random.choice(range(min_flips, max_flips, 1)) * time_per_flip
    
    
    
class Animation(object):
    
    started = False
    start_time = None
    last_time = None
    done = False
    
    def __init__(self, start, end, duration):
        self.start = start
        self.end = end
        self.__diff_x = end[0]-start[0]
        self.__diff_y = end[1]-start[1]
        self.duration = duration
        self.freq = float(sdl2.SDL_GetPerformanceFrequency())
        
    def reset(self):
        self.started = False
        self.done = False
    
    def highres_time(self):
        # Uses SDL2's high res time functions for smoother animations
        return sdl2.SDL_GetPerformanceCounter()/self.freq
    
    @property
    def position(self):
        if self.done == True:
            return self.end
        if not self.started:
            self.start_time = self.highres_time()
            self.started = True
        t = self.highres_time()
        if self.last_time and (t - self.last_time) > 0.017:
            print("refresh time: {0}".format(t - self.last_time))
        movement = (t - self.start_time)/self.duration
        if movement > 1.0:
            self.done = True
            return self.end
        x = int(self.start[0] + (self.__diff_x * movement))
        y = int(self.start[1] + (self.__diff_y * movement))
        return (x, y)
    
    @property
    def motion_per_ms(self):
        movement = 0.001/self.duration
        x = self.__diff_x * movement
        y = self.__diff_y * movement
        return (x, y)
        