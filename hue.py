import requests
import time
import urllib3
import math
import argparse
import random
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 192.168.1.4/debug/clip.html
BRIDGE_IP = "192.168.1.4"
USERNAME = "TGaYkrLuo0zVWNzQVWuj8gJl1-PfvWw84POPJFyi"

def make_request(light_number, hue="0", brightness="254", is_on=True):
    url = "http://{}/api/{}/lights/{}/state".format(BRIDGE_IP, USERNAME, light_number)
    body = "{{\"on\":{}, \"sat\":254, \"bri\":{}, \"hue\":{}}}".format("true" if is_on else "false", brightness, hue)

    try:
        r = requests.put(url, data=body, verify=False, timeout=5)
        print(r)
        print(r.json())
        print(body)

    except requests.exceptions.ConnectTimeout:
        print("Timeout")
        exit(1)



def practice_range():
    return [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]

def full_spectrum_step_size(step_size):
    return range(0, 65535, step_size)

def degrees_for_spectrum(start, end, step=1):
    return [x * 182 for x in range(start, end, step)]

def full_spectrum_degrees():
    return degrees_for_spectrum(0, 360)

def reds():
    return degrees_for_spectrum(60, 0, -1) + degrees_for_spectrum(360, 300, -1)

def greens():
    return degrees_for_spectrum(60, 180)

def blues():
    return degrees_for_spectrum(180, 320)

def offset_blues():
    # return degrees_for_spectrum(300, 330) + degrees_for_spectrum(190, 299) ------- too jarring
    return degrees_for_spectrum(210, 360)

def parse_input_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--period', type=float, default=0.5, help='Period between colour change requests')
    parser.add_argument('-s', '--step', type=int, default=1, help='Steps in degrees that we jump through the hue wheel')
    parser.add_argument('-c', '--cycle', action='store_true', help='Cycle through entire colour spectrum')
   # parser.add_argument('-q', '--quiet', action='store_false', help='Disable logging')
    return parser.parse_args()

def cycle():

    sign = 1
    args = parse_input_args()
    period = args.period
    step = args.step
    # QUIET=args.quiet

    brightness = random.randrange(180, 254, 5)

    r = degrees_for_spectrum(0, 360, 1) if args.cycle else blues()
    l = degrees_for_spectrum(0, 360, 1) if args.cycle else reds()

    j = -1
    while 1:
        if j > 1023:
            j = 0

        j += 1

        print(j)
        sign = -1 if j % 2 == 0 else 1
        for i in range(1, min(len(r), len(l)) - step):

            is_even = True # i % 2 == 0
            index = i * sign
            hue_3 = r[index + step] if is_even else l[index + step]
            hue_4 = l[index + (step - 2)] if is_even else r[index + (step - 2)]

            if i % 10 == 0:
                brightness = random.randrange(180, 254, 5)
            
            print("sign: {}".format(sign))
            print("index: {}".format(i))
            #print("array index 3: {}".format(index_3))
            #print("array index 4: {}".format(index_4))
            print("light #3 hue: {}".format(hue_3))
            print("light #4 hue: {}".format(hue_4))

            make_request("3", hue_3, brightness)
            time.sleep(period)

            make_request("4", hue_4, brightness)

            print("sleep")
            time.sleep(period)


    print(str)


def all_on():
    make_request("3", is_on=True)
    make_request("4", is_on=True)

def all_off():
    make_request("3", is_on=False)
    make_request("4", is_on=False)

if __name__ == '__main__':

    # all_off()
    # all_on()
    cycle()


##########################################################################################
##### TODO
##########################################################################################

# Add arg parser
# modes/funcs

##########################################################################################
##### Nice to have
##########################################################################################

# GUI

