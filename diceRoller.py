#!/usr/bin/env python3

import random

def parse_roll(msg):
    rolls = msg.split(',')
    if len(rolls) == 1:
        return " rolled {}: `{}`".format(msg,roll(rolls[0]))
    else:
        answer = " rolled: "
        for r in rolls:
            answer += "`{}`, ".format(roll(r))
        return answer[:-2]

def roll(dice):
    # print("{}".format(dice))
    dice = dice.split('+')
    if len(dice) > 1 or "d" in dice[0]:
        print(dice)
    n = 0
    for die in dice:
        param = die.split('d')
        if(len(param) == 1):
            n += int(param[0].strip('()'))
        else:
            print("Rolling: " + ' dice of '.join(param))
            amount = roll(param[0].strip('()'))
            faces = roll(param[1].strip('()'))
            for i in range(0,amount):
                n += random.randint(1,faces)
                print("Rolled {}".format(n))
    return n
