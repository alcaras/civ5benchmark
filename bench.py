import os
import sys
import struct
import uuid
import optparse
import codecs
import signal


known_types = { 1: "Founding",
                2: "Culture",
                6: "Religion", }

class Civ5FileReader(object):
    """ Some basic functionality for reading data from Civ 5 files. """

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
        print text
        
        if text != "": # ignore messages with no content
            print
            print "^^^" + str(turn) + "\t" + str(team) + "\t" + text



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
        print "(read",len, "@", self.r.tell() , ")"
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

# we're going to look for "is founded" and then roll back to the start to
# find the start
# then extract all messages

    bp = all.find("is founded")
    
    # since i am always playing poland, it is always going to be warsaw
    # so hard coding to -7
    # event format
    # 0xff 0xff 0xff 0xff 0x00 0x00 (four bytes, length of the string after)
    # (string) (four bytes, turn number)
    
    cf = Civ5FileReader(fn)
    
#    cf.r.seek(bp-39, 0) # not 11, not 79
    cf.r.seek(bp-79, 0) # not 11, not 79


    while True:
        cf.turn_event()






    


    



    


# Messages are <string> with a turn # byte




    
