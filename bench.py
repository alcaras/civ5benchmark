import os
import sys
import struct
import ctypes
import uuid
import optparse
import codecs
import signal

import cPickle as pickle


class Civ5FileReader(object):
    """ Some basic functionality for reading data from Civ 5 files. """
    def read_map(self):

        lookup = {
            0 : { # 4 of these
                '\x00' : '0',
                '\x01' : '1',
                '\x02' : '2',
                '\x03' : ' ', 
                },
            1 : { # 7 of these
                '\x00' : '0',
                '\x01' : '1',
                '\x02' : '2',
                '\x03' : '3',
                '\x04' : '4',
                '\x05' : '5',
                '\x06' : ' ',
                },
            2 : { # 25 of these 
                '\n'   : 'n',
                '\r'   : 'r',
                '\t'   : 't',
                '\x00' : '0',
                '\x01' : '1',
                '\x02' : '2',
                '\x03' : '3',
                '\x04' : '4',
                '\x05' : '5',
                '\x06' : '6',
                '\x07' : '7',
                '\x08' : '8',
                '\x0b' : 'b',
                '\x0c' : 'c',
                '\x0f' : 'f',
                '\x10' : ')',
                '\x11' : '!',
                '\x12' : '@',
                '\x13' : '#',
                '\x14' : '$',
                '\x15' : '%',
                '\x16' : '^',
                '\x17' : '&',
                '\x18' : '*',
                '\xff' : ' ',
               

                },
            3 : { # 11 of these
                '\n'   : 'n',
                '\x00' : ' ',
                '\x01' : '1',
                '\x02' : '2',
                '\x03' : '3',
                '\x04' : '4',
                '\x05' : '5',
                '\x06' : '6',
                '\x08' : '8',
                '\x0c' : 'c',
                '\x0e' : 'e',
                },
        }
        unknowns = []

       
        print "now reading map..."

        x = self.read_int()
        y = self.read_int()
        hexes = self.read_int()

        print "map dimensions", x, y, "hexes:", hexes
        assert(x*y==hexes)
        
        map = {}
        for i in range(0, x):
            map[i] = {}
    

        for i in range(0, hexes):
            a = self.read_int() # not sure what these represent yet
            b = self.read_int() # not sure what these represent yet
            c = self.read_int() # not sure what these represent yet
            map[i/y][i%y] = c
            # a seems to always be 1
            # b seems to always be the number of turns
            # if i had to guess, c is terrain + resources
            print a, b, c,

            data=ctypes.create_string_buffer(4)
            struct.pack_into("<i", data, 0, c)
            print list(data)


        for k in range(0, 4):
            print "data", k, "map"
            print


            unknowns = []

            for i in range(0, y):
                for j in range(0, x):
                    data=ctypes.create_string_buffer(4)
                    struct.pack_into("<i", data, 0, map[j][i])
                    if data[k] in lookup[k]:
                        sys.stdout.write(lookup[k][data[k]])
                    else:
                        sys.stdout.write('?')
                        if data[k] not in unknowns:
                            unknowns += data[k]
                sys.stdout.write('\n')

            print unknowns
            print

        return map
                    
      
    def read_header(self):
        histograms = {}
        histogram_labels = {}

        print "now reading header..."

        print self.read_sized_string_list(4)[0] # CIV5
        print self.read_int(), "1?" # 1, not sure what it means, seems consistent
        print self.read_string() # game version
        print self.read_string() # build
        self.r.read(5) # 5 bytes, not sure of what
        our_civ = self.read_string() # our civ
        print "^^^@@@ civ", our_civ
        print "^^^@@@ diff", self.read_string() # Difficulty Level
        print self.read_string() # Starting Era
        print self.read_string() # Ending? Era
        print "^^^@@@ speed", self.read_string() # Game Speed
        print "^^^@@@ size", self.read_string() # World Size
        print "^^^@@@ map", self.read_string() # Map Script
        n_dlcs = self.read_int() # a number, looks to be 10? maybe # of DLCs?
        print n_dlcs, "DLCS loaded:"

        # look for a 01 00 00 00, this is the marker that starts DLCs
        # looks like we're here for DLC's...
        
        for i in range(0, n_dlcs):
            while self.read_int() != 1:
                continue

            print " ", self.read_string()


        n_mods = self.read_int() # number of mods
        print n_mods, "mods loaded:" 
        
        for i in range(0, n_mods):
            print " ", self.read_string() #check sum
            print " ", self.read_int()
            print " ", self.read_string()

        print self.read_int(), "0?"
        print self.read_int(), "0?" # should be 2 zeros
        print self.read_string()

        print self.read_int(), "1?"
        print self.read_int(), "0?" # should be a 1 and a 0
        print self.read_string() # map script again

        print self.read_int(), "3? game options"  # these are almost certainly game options
        print self.read_int(), "0?"
        print self.read_int(), "1?"
        print self.read_int(), "0?"

        print self.read_int(), "3?"
        print self.read_int(), "1?"
        print self.read_int(), "15?"
        print self.read_int(), "5?"

        print self.read_int(), "0"
        print self.read_int(), "1"
        print self.read_int(), "2"
        print self.read_int(), "3"

        print self.read_int(), "4"
        # -1 loss
        # 0 time
        # 1 science
        # 2 diplo
        # 3 culture
        # 4 military

        victory_types = { -1 : "Loss",
                          0  : "Time",
                           1 : "Science",
                           2 : "Diplomatic",
                           3 : "Cultural",
                           4 : "Military" }
        
        vt= self.read_int()
        assert(vt in (-1, 0, 1, 2, 3, 4))
        print "Victory Type:", victory_types[vt], vt


        # guess -- tells how many extra bytes to read        
        unknown_value = self.read_int()
        print unknown_value, "unknown_value"

        self.r.read(9+unknown_value) # 9+unknown_value bytes for what i do not know
        
        print self.read_string(), "end date"
    
        print self.read_int(), "0"

        n_events = self.read_int()
        print n_events, "?"
        entities = self.read_int()
        print entities, "number of entities"
        print self.read_int(),
        print self.read_int(), 
        print self.read_int(), 
        print self.read_int(),

        our_leader = self.read_string()

        # pass this on to mark
        ld = open('our_leader.py', 'w')
        ld.write("our_leader = '" + our_leader + "'")
        ld.close()




        our_civ = self.read_string()

        print "***" + our_leader + "***", 

        print "***" + our_civ + "***",



        ld = open('our_civ.py', 'w')
        ld.write("our_civ = '" + our_civ + "'")
        ld.close()



        print self.read_string(), self.read_string()

        for i in range(1, entities):
            print self.read_int(), self.read_int(), self.read_int(), self.read_int(),
            print self.read_string(), self.read_string(), self.read_string(), self.read_string()


        # oh score, histogram data!

        data_sets = self.read_int()
        print data_sets, "data sets?"

        for i in range(0, data_sets):
            h =  self.read_string()
            print h
            histogram_labels[i] = h
            histograms[i] = {}

        n_ent = self.read_int()


        print n_ent, "civs"

        for i in range(0, n_ent):
            print
            print "histograms for civ #", i
            n_data = self.read_int()
            print n_data, "<-- n_data"
            for j in range(0, n_data):
                histograms[i][j] = {}
                print "histogram data for ", histogram_labels[j], "civ", i
                n_turns = self.read_int()
                print n_turns, "<-- turns", j
                for k in range(0, n_turns):
                    turn = self.read_int()
                    value = self.read_int()
                    print turn, value
                    histograms[i][j][k] = value

                print






        print self.read_int(), "2?"

        n_events = self.read_int()
        print "n_events = ", n_events
                

        print "now at", self.r.tell()

        print histogram_labels

        print "Pickling histograms..."

        jar = open('histograms.pickle', 'wb')
        pickle.dump(histograms, jar)
        jar.close()

        print "Pickled"


        return self.r.tell(), n_events


        # the first bit

    def turn_event(self):
        # event type seems to be one of the following values:
        #  0    general information
        #  1    city founded
        #  2    culture gained 
        #  5    religion founded
        #  6    pantheon founded

        super_type_definitions = {0 : "Announcement",
                                  1 : "City Founding",
                                  2 : "Borders", # not sure on the difference
                                  3 : "Borders", # between these
                                  4 : "Borders", 
                                  5 : "Religion Founded",
                                  6 : "Pantheon Founded",
        }

                                
        turn = self.read_int()
        print "Turn", str(turn)

        super_type= self.read_int()
        print "super_type", super_type,

        if super_type in super_type_definitions:
            print super_type_definitions[super_type]
        elif super_type == 56:
            print "End of parse"
            sys.exit()
        else:
            print "Unknown super_type @", self.r.tell()
            sys.exit()


        count = self.read_int() # number of tiles at play here
        print "count", count 
        for i in range(0, count): # each tile is a short
            print i, self.read_short_int(), self.read_short_int()
    
        team = self.read_int()  # which team is this?
        print "Team", str(team).rjust(3)
        
        text = self.read_string() # any message?
        print text.encode('utf-8')
        
        if text != "": # ignore messages with no content
            print
            print "^^^" + str(turn) + "\t" + str(team) + "\t" + text.encode('utf-8')



        print

        


    def __init__(self, input):
        if isinstance(input, str):
            input = file(input, "rb")
        self.r = input

    def read_short_int(self):
        """ Read a single little endian 2 byte integer """
        # My *guess* is that they're all signed
        t = self.r.read(2)
        if len(t) != 2:
            self.eof = True
            return 0
        return struct.unpack("<h", t)[0]

    def read_int(self):
        """ Read a single little endian 4 byte integer """
        # My *guess* is that they're all signed
        t = self.r.read(4)
        if len(t) != 4:
            self.eof = True
            return 0
        return struct.unpack("<i", t)[0]

    def read_ints(self, count=None, esize=1):
        """ Read count tuples of esize little endian 4 byte integers and return them in a list. If count is omitted, read it as a 4 byte integer first """
        if count is None:
            count = self.read_int()
        list = []
        while count > 0:
            if esize > 1:
                t = []
                for i in range(esize):
                    t.append(self.read_int())
                list.append(tuple(t))
            else:
                list.append(self.read_int())
            count -= 1
        return list

    def read_string(self):
        """ Read an undelimited string with the length given in the first 4 bytes """
        len = self.read_int()
#        print "(read",len, "@", self.r.tell() , ")"
        return self.r.read(len).decode("utf-8")

    def read_terminated_string(self):
        """ Read a nul-terminated string. """
        s = ""
        while True:
            c = self.r.read(1)
            if ord(c) == 0:
                return s.decode("utf-8")
            s += c
    
    def read_terminated_string_list(self):
        """ Read a list of nul-terminated strings, terminated by a zero-length string. """
        l = []
        while True:
            s = self.read_terminated_string().decode("utf-8")
            if s == "":
                return l
            l.append(s)

    def read_sized_string_list(self, size):
        """ Read a block of data with a given size, and split in null-terminated strings. """
        block = self.r.read(size)
        if block.endswith("\0"):
            block = block[:-1]
        return block.split("\0")

            
if __name__ == "__main__":

   
    # set up some command line options
    op = optparse.OptionParser()
    (options, args) = op.parse_args()

    if len(args) == 0:
        print "bench.py <replay-file>"
        sys.exit(1)


    replay = None
    if len(args) > 0:
        print "Replaying: %s" % (args[0],)
        print

    fn = args[0]
    r = file(fn, "rb")
    all = r.read()

   
    cf = Civ5FileReader(fn)

    cf.r.seek(0,0)

    data_starts_at, n_events = cf.read_header()
    
    cf.r.seek(data_starts_at,0)

    print "now reading", n_events, "events..."

    for i in range(n_events): 
        cf.turn_event()

    print "left off", cf.r.tell()

    # now we read the map
    cf.read_map()

    print "left off", cf.r.tell()








    


    
