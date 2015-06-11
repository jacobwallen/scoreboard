#!/usr/bin/python


from datetime import datetime
import random


init_run = False

today = datetime.today()
today = today.strftime("%Y-%m-%d")

location = None
date = None

rules = None
base_rounds = 1

pilots = ['1',
          '2',
          '3',
          '4',
          '5',
          '6',
          '7',
          '8',
          '9',
          '10',
          '11',
          '12',
          '13',
          '14',
          ]

startlists = []
rounds = []
contest_scores = []


def init():
    """"""
    cls()
    print "Setup Contest"
    global init_run
    global location
    global date
    global rules

    if location is None:
        location = raw_input("Location: ")

    if date is None:
        date = raw_input("Date: (%s)" % today)
        if date is "":
            date = today

    valid = ("WW2", "WW1")
    while rules not in valid:
        rules = raw_input("Rules: (WW2)")
        if rules is "":
            rules = "WW2"
    init_run = True
    return


def menu():
    """Menu representation"""
    if not init_run:
        init()

    opt = ""
    valid = ("1", "2", "3", "4", "5", "7", "8", "9", "q")
    while opt not in valid:
        cls()
        print "### %s %s %s ###" % (location, date, rules)
        print "    %s rounds + final" % base_rounds
        print ""
        print "1. Add Pilot (%s added)" % len(pilots)
        print "2. Remove Pilot"
        print "3. Show Pilots"
        print "4. Report Score"
        print "5. dump score array"
        print ""
        print "7. Randomize Heat Lists"
        print "8. Show Heat Lists"
        print "9. Set Number of Base Rounds"
        print "q. Quit\n"
        opt = raw_input("What do you want to do? ")

        if opt is "1":
            add_pilot()
            opt = ""
        elif opt is "2":
            remove_pilot()
            opt = ""
        elif opt is "3":
            show_pilots()
            any_key()
            opt = ""
        elif opt is "4":
            report_score()
            opt = ""
        elif opt is "5":
            print_contest_scores()
            opt = ""
        elif opt is "7":
            randomize_heats()
            opt = ""
        elif opt is "8":
            show_heats()
            any_key()
            opt = ""
        elif opt is "9":
            set_rounds()
            opt = ""
        elif opt is "q":
            if confirm("exit"):
                exit()
            opt = ""


def cls():
    """"""
    print(chr(27) + "[2J")


def any_key():
    """"""
    raw_input("\nPress any key to contine...")
    return


def add_pilot():
    """"""
    global pilots
    cls()
    new_pilot = raw_input("New Pilot: ")

    pilots.append(new_pilot)
    return


def confirm(msg):
    """"""
    global pilots
    valid = ["yes", "y"]
    confirm = ""
    while confirm not in valid:
        confirm = raw_input("Confirm %s (y/N) " % msg)
        if confirm in valid:
            return True
        else:
            return False


def remove_pilot():
    """"""
    global pilots
    show_pilots()
    remove_id = int(raw_input("\nID of pilot to remove: "))
    if confirm("delete %s" % pilots[remove_id - 1]):
        del pilots[remove_id - 1]


def show_pilots():
    """"""
    global pilots
    cls()
    print "-- Pilot List --"
    i = 1
    for pilot in pilots:
        print "%s %s" % (i, pilot)
        i += 1


def report_score():
    global pilots
    global contest_scores
    cls()
    show_pilots()
    pilot_id = int(raw_input("Pilot ID: "))
    pilot = pilots[pilot_id - 1]
    rnumber = raw_input("Round: ")
    print "%s Round %s:" % (pilot, rnumber)

    valid = range(0, 7)
    minutes = 99
    while int(minutes) not in valid:
        minutes = int(raw_input("Minutes: "))

    valid = range(0, 60)
    seconds = 99
    while int(seconds) not in valid:
        seconds = int(raw_input("Seconds: "))

    cuts = int(raw_input("How Many Cuts? "))
    streamer = bool(raw_input("Streamer OK? "))
    non_eng = bool(raw_input("Non-Engagement? "))
    safety = bool(raw_input("Safety?"))

    roundscore = [pilot, rnumber, minutes, seconds, cuts, streamer,
                  non_eng, safety]
    print roundscore
    print calc_heat_score(minutes, seconds, cuts, streamer, non_eng, safety)

    contest_scores.append(roundscore)
    any_key()


def print_contest_scores():
    global contest_scores
    cls()
    print contest_scores
    any_key()


def make_round(l, n):
    """ Yield successive n-sized chunks from l.
    """
    ret = []
    for i in xrange(0, len(l), n):
        ret.append(l[i:i+n])
    return ret


def scramble(orig):
    """Scramble a list"""
    dest = orig[:]
    random.shuffle(dest)
    return dest


def show_heats():
    """Show heat lists"""
    cls()
    global rounds
    print "\n### HEAT LIST ###\n"
    i_r = 1  # round iterator
    i_h = 1  # heat iterator
    for _round in rounds:
        print "\n== ROUND %s ==" % i_r
        for heat in _round:
            print "\n--HEAT %s--" % i_h
            for p in heat:
                print "  %s" % p
            i_h += 1
        print "\n------------"
        i_r += 1
        i_h = 1
    i_r = 1


def randomize_heats():
    global pilots
    global startlists
    global rounds
#    global base_rounds
    if len(startlists) > 0:
        answ = raw_input(" Warning startlists already made, "
                         "generate new overwriting old? (y)")
        if answ is "y":
            startlists = []
            rounds = []
        else:
            return
    cls()
    print "%s pilots registred" % len(pilots)
    mpph = raw_input("Max Pilots per heat (7): ")
    if mpph is "":
        mpph = 7
    else:
        mpph = int(mpph)
    cls()

    i = 1
    while i <= base_rounds:
        _round = make_round(scramble(pilots), mpph)
        rounds.append(_round)
        for startlist in _round:
            startlists.append(startlist)  # store who meet who
        i += 1
    show_heats()
    any_key()


def set_rounds():
    """"""
    global base_rounds
    cls()
    base_rounds = int(raw_input("Set number of base_rounds: "))
    return


def calc_heat_score(mins, secs, cuts,
                    streamer=False, non_eng=False, safety=False):
    """R"""
    time = (mins * 60 + secs) / 3
    cuts = cuts * 100
    if streamer:
        streamer = 50
    if non_eng:
        non_eng = -50
    if safety:
        safety = -200
    return time + cuts + streamer + non_eng + safety

menu()
