# import pyvisa # PyVisa info @ http://PyVisa.readthedocs.io/en/stable/
import serial.tools.list_ports
import serial
import time


def range_check(val, min, max, val_name):
    if val > max:
        print(f"Wrong {val_name}: {val}. Max output should be less then {max} V")
        val = max
    if val < min:
        print(f"Wrong {val_name}: {val}. Should be >= {min}")
        val = min
    return val


# def ch_list_from_range(is_req, min, max, add_space=1, channels_num=20 ):
#     channels_34901A = 20  # 34901A 20 Channel Multiplexer (2/4-wire) Module
#     channels_34902A = 16  # 34902A 16 Channel Multiplexer (2/4-wire) Module
#     channels_34902A = 40  # 34908A 40 Channel Single-Ended Multiplexer Module
#     req_txt = "?" if is_req == 1 else ""
#     space_txt = " " if add_space == 1 else ""
#     channels = channels_num
#     slot_id = int(min/100)
#     slot_id = range_check(slot_id,1,3,"slot ID")
#     min = range_check(min, (slot_id*100+1), (slot_id*100+channels), " channels number")
#     max = range_check(max, (slot_id*100+1), (slot_id*100+channels), " channels number")
#     txt = f"{min},"
#     l = [f"{min},"]
#     for z in range(0, (max - min)):
#         l.append(f'{min + z + 1},')
#     txt = "".join(l)
#     txt = txt[:-1]
#     txt = f"{req_txt}{space_txt}(@{txt})"
#     return txt


# def ch_list_from_list(is_req, *argv):
#     req_txt = "?" if is_req == 1 else ""
#     txt = ""
#     for items in argv:
#         txt = f'{txt}{items},'
#     txt = txt[:-1]
#     txt = f'{req_txt} (@{txt})'
#     return txt


def ch_list_from_list2(*argv):
    txt = ""
    for items in argv:
        txt = f'{txt}{items},'
    txt = txt[:-1]
    return f'(@{txt})'


def ch_list_from_range2(min, max, channels_num=20):
    channels_34901A = 20  # 34901A 20 Channel Multiplexer (2/4-wire) Module
    channels_34902A = 16  # 34902A 16 Channel Multiplexer (2/4-wire) Module
    channels_34902A = 40  # 34908A 40 Channel Single-Ended Multiplexer Module
    channels = channels_num
    slot_id = int(min / 100)
    slot_id = range_check(slot_id, 1, 3, "slot ID")
    min = range_check(min, (slot_id * 100 + 1), (slot_id * 100 + channels), " channels number")
    max = range_check(max, (slot_id * 100 + 1), (slot_id * 100 + channels), " channels number")
    txt = f"{min},"
    l = [f"{min},"]
    for z in range(0, (max - min)):
        l.append(f'{min + z + 1},')
    txt = "".join(l)
    txt = txt[:-1]
    return f"(@{txt})"


class com_interface():
    def __init__(self):
        # Commands Subsystem
        # this is the list of Subsystem commands
        # super(communicator, self).__init__(port="COM10",baudrate=115200, timeout=0.1)
        print("communicator init")
        self.cmd = None
        self.ser = None

    def init(self, com_port, baudrate_var=115200):
        com_port_list = [comport.device for comport in serial.tools.list_ports.comports()]
        if com_port not in com_port_list:
            print("COM port is not found")
            print("Please ensure that USB is connected")
            print(f"Please check COM port Number. Currently it is {com_port} ")
            print(f'Founded COM ports:{com_port_list}')
            return False
        else:
            self.ser = serial.Serial(
                port=com_port,
                baudrate=baudrate_var,
                timeout=0.1
            )
            if not self.ser.isOpen():
                self.ser.open()

            txt = '*IDN?'

            read_back = self.query(txt)
            print(f"Connected to: {read_back}")
            return True

    def send(self, txt):
        # will put sending command here
        txt = f'{txt}\r\n'
        # print(f'Sending: {txt}')
        self.ser.write(txt.encode())

    def query(self, cmd_srt):
        txt = f'{cmd_srt}\r\n'
        self.ser.reset_input_buffer()
        self.ser.write(txt.encode())
        # print(f'Query: {txt}')
        return_val = self.ser.readline().decode()
        return return_val

    def close(self):
        self.ser.close()
        self.ser = None


class str_return:
    def __init__(self):
        self.cmd = None

    def str(self):
        # will put sending command here
        return self.cmd

    def req(self):
        return self.cmd + "?"

    def ch_list(self, is_req, *argv):
        ch_list_txt = ch_list_from_list(is_req, *argv)
        txt = f'{self.cmd}{ch_list_txt}'
        return txt

    def ch_range(self, is_req, min, max, channels_num=20):
        ch_list_txt = ch_list_from_range(is_req, min, max, channels_num)
        txt = f"{self.cmd}{ch_list_txt}"
        return txt


class str:
    def __init__(self):
        self.cmd = None

    def str(self):
        # will put sending command here
        return self.cmd


class req2(str):
    def __init__(self, prefix):
        self.prefix = prefix + "?"
        self.cmd = self.prefix
        self.ch = select_channel2(self.prefix + " ")


class conf2(str):
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix
        self.ch = select_channel2(self.prefix)


class select_channel2():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix

    def list(self, *argv):
        ch_list_txt = ch_list_from_list2(*argv)
        txt = f'{self.cmd}{ch_list_txt}'
        return txt

    def range(self, min, max, channels_num=20):
        ch_list_txt = ch_list_from_range2(min, max, channels_num)
        txt = f"{self.cmd}{ch_list_txt}"
        return txt


class req:
    def __init__(self):
        self.cmd = None

    def req(self):
        return self.cmd + "?"

class req3:
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix

    def req(self):
        return self.cmd + "?"



class str3:
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix

    def str(self, ):
        return self.cmd


class str_and_req:
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix

    def str(self, ):
        return self.cmd

    def req(self):
        return self.cmd + "?"


class sel_ch_with_param():
    def __init__(self, prefix, min, max):
        self.prefix = prefix
        self.cmd = self.prefix
        self.max = max
        self.min = min

    def list(self,var, *argv):
        var = range_check(var, self.min, self.max, self.cmd)
        ch_list_txt = ch_list_from_list2(*argv)
        txt = f'{self.cmd} {var},{ch_list_txt}'
        return txt

    def range(self, var, ch_min, ch_max, ch_num=20):
        var = range_check(var, self.min, self.max, self.cmd)
        ch_list_txt = ch_list_from_range2(ch_min, ch_max, ch_num)
        txt = f"{self.cmd} {var},{ch_list_txt}"
        return txt

# class conf_with_param(str):
#     def __init__(self, prefix):
#         self.prefix = prefix
#         self.cmd = self.prefix
#         self.ch = select_channel2(self.prefix)

class dig_param:
    def __init__(self):
        self.cmd = None  # this value to be inherited for high order class
        self.max = None  # this value to be inherited for high order class
        self.min = None  # this value to be inherited for high order class

    def val(self, count=0):
        count = range_check(count, self.min, self.max, "MAX count")
        txt = f'{self.cmd} {count}'
        return txt

class dig_param3:
    def __init__(self, prefix, min, max):
        self.prefix = prefix
        self.cmd = self.prefix
        self.max = max
        self.min = min

    def val(self, count=0):
        count = range_check(count, self.min, self.max, "MAX count")
        txt = f'{self.cmd} {count}'
        return txt



class ch_single:
    def __init__(self):
        self.cmd = None

    def ch_single(self, ch_num, max_ch_number=20):
        channels_34901A = 20  # 34901A 20 Channel Multiplexer (2/4-wire) Module
        channels_34902A = 16  # 34902A 16 Channel Multiplexer (2/4-wire) Module
        channels_34902A = 40  # 34908A 40 Channel Single-Ended Multiplexer Module
        channels = max_ch_number
        slot_id = int(ch_num / 100)
        slot_id = range_check(slot_id, 1, 3, "slot ID")
        ch_num = range_check(ch_num, (slot_id * 100 + 1), (slot_id * 100 + channels), " channels number")
        txt = f'{self.cmd} (@{ch_num})'
        return txt


class select_channel:
    def __init__(self):
        self.cmd = None

    def ch_list(self, *argv):
        ch_list_txt = ch_list_from_list(0, *argv)
        txt = f'{self.cmd}{ch_list_txt}'
        return txt

    def ch_range(self, min, max, channels_num=20):
        ch_list_txt = ch_list_from_range(0, min, max, channels_num)
        txt = f"{self.cmd}{ch_list_txt}"
        return txt

    # def ch_list(self, is_req, *argv):
    #     ch_list_txt = ch_list_from_list(is_req, *argv)
    #     txt = f'{self.cmd}{ch_list_txt}'
    #     return txt
    #
    # def ch_range(self, is_req, min, max, channels_num=20):
    #     ch_list_txt = ch_list_from_range(is_req, min, max, channels_num)
    #     txt = f"{self.cmd}{ch_list_txt}"
    #     return txt


# class select_channel_2params:
#     def __init__(self, cmd):
#         self.cmd = None
#
#     def ch_list(self, range, resolution,  *argv):
#         ch_list_txt = ch_list_from_list(0, *argv)
#         txt = f'{self.cmd}{ch_list_txt}'
#         return txt
#
#     def ch_range(self, range, resolution, min, max, channels_num=20):
#         ch_list_txt = ch_list_from_range(0,min,max,channels_num)
#         txt = f"{self.cmd}{ch_list_txt}"
#         return txt
#     def __get_range


class storage():
    def __init__(self):
        self.cmd = None
        self.prefix = None
        # super(communicator, self).__init__()
        # super(storage,self).__init__()
        # communicator.init(self, "COM10")
        # this is the list of Subsystem commands
        # self.calculate = calculate()
        # self.calibration = calibration()
        self.configure = configure()
        # self.data = data()
        # self.diagnostic = diagnostic()
        # self.display = display()
        # self.fformat = fformat()
        # self.ieee-488.2 = ieee-488.2()
        # self.instrument = instrument()
        self.measure = measure()
        # self.memory = memory()
        # self.mmemory = mmemory()
        # self.output = output()
        self.sense = sense()
        self.source = source()
        self.status = status()
        # self.system = system()
        self.trigger = trigger()
        self.route = route()
        self.abort = str3("ABORt")
        self.fetch = req3("FETCh")
        self.init = str3("INITiate")
        self.read = req2("READ")
        self.r = dig_param3("R?", 1, 50000)
        self.unit_temperature = unit_temperature()
        self.input_impedance_auto = input_impedance_auto()


class configure(req):
    # availanle commands for CONFigure
    # * CONFigure?
    # * CONFigure:CURRent:AC
    # * CONFigure:CURRent:DC
    # * CONFigure:DIGital:BYTE
    # * CONFigure:FREQuency
    # * CONFigure:FRESistance
    # *  CONFigure:PERiod
    # * CONFigure:RESistance
    # *  CONFigure:TEMPerature
    # * CONFigure:TOTalize
    # * CONFigure:VOLTage:AC
    # * CONFigure:VOLTage:DC
    def __init__(self):
        print("INIT CONFIGURE")
        super(configure, self).__init__()
        self.prefix = "CONFigure"
        self.cmd = "CONFigure"
        self.current = current(self.prefix)
        self.voltage = voltage(self.prefix)
        self.digital_byte = digital_byte(self.prefix)
        self.frequency = frequency(self.prefix)
        self.period = period(self.prefix)
        self.temperature = temperature(self.prefix)
        self.resistance = resistance(self.prefix)
        self.fresistance = fresistance(self.prefix)
        self.totalize = totalize(self.prefix)


class measure:
    # command list :
    # MEASure:CURRent:AC?
    # MEASure:CURRent:DC?
    # MEASure:DIGital:BYTE?
    # MEASure:FREQuency?
    # MEASure:FRESistance?
    # MEASure:PERiod?
    # MEASure:RESistance?
    # MEASure:TEMPerature?
    # MEASure:TOTalize?
    # MEASure:VOLTage:AC?
    # MEASure:VOLTage:DC?

    def __init__(self):
        print("INIT Measure")
        self.cmd = "MEASure"
        self.prefix = "MEASure"
        self.current = current(self.prefix)
        self.voltage = voltage(self.prefix)
        self.digital_byte = digital_byte(self.prefix)
        self.frequency = frequency(self.prefix)
        self.period = period(self.prefix)
        self.temperature = temperature(self.prefix)
        self.resistance = resistance(self.prefix)
        self.fresistance = fresistance(self.prefix)
        self.totalize = totalize(self.prefix)


class sense:
    # AC Current
    # [SENSe:]CURRent:AC:BANDwidth
    # [SENSe:]CURRent:AC:BANDwidth?
    # [SENSe:]CURRent:AC:RANGe
    # [SENSe:]CURRent:AC:RANGe?
    # [SENSe:]CURRent:AC:RANGe:AUTO
    # [SENSe:]CURRent:AC:RANGe:AUTO
    # [SENSe:]CURRent:AC:RESolution
    # [SENSe:]CURRent:AC:RESolution?
    # DC Current
    # [SENSe:]CURRent:DC:APERture
    # [SENSe:]CURRent:DC:APERture?
    # [SENSe:]CURRent:DC:NPLC
    # [SENSe:]CURRent:DC:NPLC?
    # [SENSe:]CURRent:DC:RANGe
    # [SENSe:]CURRent:DC:RANGe?
    # [SENSe:]CURRent:DC:RANGe:AUTO
    # [SENSe:]CURRent:DC:RANGe:AUTO
    # [SENSe:]CURRent:DC:RESolution
    # [SENSe:]CURRent:DC:RESolution?
    # AC Voltage
    # [SENSe:]VOLTage:AC:RANGe
    # [SENSe:]VOLTage:AC:RANGe?
    # [SENSe:]VOLTage:AC:RANGe:AUTO
    # [SENSe:]VOLTage:AC:RANGe:AUTO?
    # [SENSe:]VOLTage:AC:BANDwidth
    # [SENSe:]VOLTage:AC:BANDwidth?
    # DC Current
    # [SENSe:]VOLTage:DC:APERture
    # [SENSe:]VOLTage:DC:APERture?
    # [SENSe:]VOLTage:DC:NPLC
    # [SENSe:]VOLTage:DC:NPLC?
    # [SENSe:]VOLTage:DC:RANGe
    # [SENSe:]VOLTage:DC:RANGe?
    # [SENSe:]VOLTage:DC:RANGe:AUTO
    # [SENSe:]VOLTage:DC:RANGe:AUTO?
    # [SENSe:]VOLTage:DC:RESolution
    # [SENSe:]VOLTage:DC:RESolution?
    # 2-Wire Resistance
    # [SENSe:]RESistance:APERture
    # [SENSe:]RESistance:APERture?
    # [SENSe:]RESistance:NPLC
    # [SENSe:]RESistance:NPLC?
    # [SENSe:]RESistance:OCOMpensated
    # [SENSe:]RESistance:OCOMpensated?
    # [SENSe:]RESistance:RANGe
    # [SENSe:]RESistance:RANGe?
    # [SENSe:]RESistance:RANGe:AUTO
    # [SENSe:]RESistance:RANGe:AUTO?
    # [SENSe:]RESistance:RESolution
    # [SENSe:]RESistance:RESolution?
    # 4-Wire Resistance
    # [SENSe:]FRESistance:APERture
    # [SENSe:]FRESistance:APERture?
    # [SENSe:]FRESistance:NPLC
    # [SENSe:]FRESistance:NPLC?
    # [SENSe:]FRESistance:OCOMpensated
    # [SENSe:]FRESistance:OCOMpensated?
    # [SENSe:]FRESistance:RANGe
    # [SENSe:]FRESistance:RANGe?
    # [SENSe:]FRESistance:RANGe:AUTO
    # [SENSe:]FRESistance:RANGe:AUTO?
    # [SENSe:]FRESistance:RESolution
    # [SENSe:]FRESistance:RESolution?
    # Frequency
    # [SENSe:]FREQuency:APERture
    # [SENSe:]FREQuency:APERture?
    # [SENSe:]FREQuency:RANGe:LOWer
    # [SENSe:]FREQuency:RANGe:LOWer?
    # [SENSe:]FREQuency:VOLTage:RANGe
    # [SENSe:]FREQuency:VOLTage:RANGe?
    # [SENSe:]FREQuency:VOLTage:RANGe:AUTO
    # [SENSe:]FREQuency:VOLTage:RANGe:AU
    # Miscellaneous
    # [SENSe:]FUNCtion
    # [SENSe:]FUNCtion?
    # [SENSe:]ZERO:AUTO
    # [SENSe:]ZERO:AUTO?
    def __init__(self):
        print("INIT Sense")
        self.cmd = "SENSe"
        self.prefix = "SENSe"
        self.current = current(self.prefix)
        self.voltage = voltage(self.prefix)
        self.digital_byte = digital_data(self.prefix)
        self.frequency = frequency(self.prefix)
        self.period = period(self.prefix)
        self.temperature = temperature(self.prefix)
        self.resistance = resistance(self.prefix)
        self.fresistance = fresistance(self.prefix)
        self.totalize = totalize(self.prefix)
        self.func = sence_func(self.prefix)
        self.zero = zero(self.prefix)


class route:
    # Command Summary
    # ROUTe:CHANnel:ADVance:SOURce
    # ROUTe:CHANnel:ADVance:SOURce?
    # ROUTe:CHANnel:DELay
    # ROUTe:CHANnel:DELay?
    # ROUTe:CHANnel:DELay:AUTO
    # ROUTe:CHANnel:DELay:AUTO?
    # ROUTe:CHANnel:FWIRe
    # ROUTe:CHANnel:FWIRe?
    # ROUTe:CLOSe
    # ROUTe:CLOSe?
    # ROUTe: CLOSe:EXCLusive
    # ROUTe: DONE?
    # ROUTe: MONitor
    # ROUTe: MONitor?
    # ROUTe: MONitor:DATA?
    # ROUTe: MONitor:STATe
    # ROUTe: MONitor:STATe?
    # ROUTe: OPEN
    # ROUTe: OPEN?
    # ROUTe: SCAN
    # ROUTe: SCAN?
    # ROUTe: SCAN:SIZE?
    def __init__(self):
        print("INIT ROUTE")
        self.cmd = "ROUTe"
        self.prefix = "ROUTe"
        # self.channel = route_channel(self.prefix)
        self.close = close_channel(self.prefix)
        self.done = req3(self.prefix + ":DONE")
        self.monitor = monitor(self.prefix)
        self.open = open_channel(self.prefix)
        self.scan = scan(self.prefix)


# **********  UNIT:TEMPerature *************
class unit_temperature:
    def __init__(self):
        print("INIT Read")
        self.prefix = "UNIT:TEMPerature"
        self.cmd = "UNIT:TEMPerature"
        self.req = req2(self.prefix)
        self.conf_f = conf2(self.prefix + " F,")
        self.conf_c = conf2(self.prefix + " C,")
        self.conf_k = conf2(self.prefix + " K,")


class input_impedance_auto:
    def __init__(self):
        print("INIT INPut:IMPedance:AUTO")
        self.prefix = "INPut:IMPedance:AUTO"
        self.cmd = "INPut:IMPedance:AUTO"
        self.req = req2(self.prefix)
        self.conf_on = conf2(self.prefix + " ON ")
        self.conf_off = conf2(self.prefix + " OFF ")


# part of ROUTE class
class scan(str_return):
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "SCAN"
        self.cmd = self.prefix
        self.size = size(self.prefix)


# part of ROUTE: SCAN class
class size(req):
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "SIZE"
        self.cmd = self.prefix


# part of ROUTE class
class open_channel(str_return):
    # This command opens the specified channels on a multiplexer or switch
    # module.
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "OPEN"
        self.cmd = self.prefix
        self.size = size(self.prefix)


# part of ROUTE class
class close_channel(str_return):
    # This command closes the specified channels on a multiplexer or switch
    # module. On the multiplexer modules, if any channel on the module is
    # defined to be part of the scan list, attempting to send this command will
    # result in an error.
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "CLOSe"
        self.cmd = self.prefix
        self.exclusive = exclusive(self.prefix)


class exclusive(str_return):
    # This command opens all channels on a multiplexer or switch module and
    # then closes the specified channels. On the multiplexer modules, if any
    # channel on the module is defined to be part of the scan list, attempting to
    # send this command will result in an error.
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "EXCLusive"
        self.cmd = self.prefix


class done(req):
    # This queries the status of all relay operations on cards not involved in the
    # scan and returns a 1 when all relay operations are finished (even during
    # a scan). ONLY -> ROUTe:DONE?
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "DONE"
        self.cmd = self.prefix


class monitor(req, ch_single):
    # This command/query selects the channel to be displayed on the front
    # panel. Only one channel can be monitored at a time.
    # ROUTe:MONitor
    # ROUTe:MONitor?
    # ROUTe:MONitor:DATA?
    # ROUTe:MONitor:STATe
    # ROUTe:MONitor:STATe?
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "MONitor"
        self.cmd = self.prefix
        self.data = data(self.prefix)
        self.state = state(self.prefix)


class data(req):
    # This query reads the monitor data from the selected channel. It returns
    # the reading only; the units, time, channel, and alarm information are not
    # returned (the FORMat:READing commands do not apply to monitor
    # readings).
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "DATA"
        self.cmd = self.prefix


class state(req):
    # This query reads the monitor data from the selected channel. It returns
    # the reading only; the units, time, channel, and alarm information are not
    # returned (the FORMat:READing commands do not apply to monitor
    # readings).
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "STATe"
        self.cmd = self.prefix

    def mode_on(self):
        return self.prefix + " 1"

    def mode_off(self):
        return self.prefix + " 0"


class zero():
    # This queries the status of all relay operations on cards not involved in the
    # scan and returns a 1 when all relay operations are finished (even during
    # a scan). ONLY -> ROUTe:DONE?
    def __init__(self, prefix):
        # super(zero, self).__init__()
        self.prefix = prefix + ":" + "ZERO"
        self.cmd = self.prefix
        self.auto = auto(self.prefix)


class sence_func():
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "FUNC"
        self.cmd = self.prefix
        self.req = req2(self.prefix)
        self.temperature = conf2(self.prefix + ' "TEMPerature",')
        self.volt_dc = conf2(self.prefix + ' "VOLTage",')
        self.volt_ac = conf2(self.prefix + ' "VOLTage:AC",')
        self.resistance = conf2(self.prefix + ' "RESistance",')
        self.fresistance = conf2(self.prefix + ' "FRESistance",')
        self.current_dc = conf2(self.prefix + ' "CURRent",')
        self.current_ac = conf2(self.prefix + ' "CURRent:AC",')
        self.frequency = conf2(self.prefix + ' "FREQuency",')
        self.period = conf2(self.prefix + ' "PERiod",')


class auto():
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "AUTO"
        self.cmd = self.prefix
        self.req = req2(self.prefix)
        self.on = conf2(self.prefix + " ON,")
        self.off = conf2(self.prefix + " OFF,")
        self.once = conf2(self.prefix + " ONCE,")


class voltage():
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "VOLTage"
        self.ac = ac(self.prefix)
        self.dc = dc(self.prefix)
        if (self.prefix.find(":FREQuency:") != -1) or self.prefix.find(":PERiod:") != -1:
            self.Range = Range(self.prefix)


class current():
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "Current"
        self.ac = ac(self.prefix)
        self.dc = dc(self.prefix)


class digital_byte():
    # This command configures the instrument to scan the specified digital
    # input channels on the multifunction module as byte data, but does not
    # initiate the scan. This command redefines the scan list.
    # The digital input channels are numbered "s01" (LSB) and "s02"
    # (MSB), where s is the first digit of the slot number.
    # example: CONF:DIG:BYTE (@101:102)
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "DIG:BYTE"
        self.cmd = self.prefix
        if self.prefix.find("CONFigure:") != -1:
            self.conf = conf2(self.prefix + " ")
        if self.prefix.find("MEASure:") != -1:
            self.req = req2(self.prefix)


class digital_data():
    # This command configures the instrument to scan the specified digital
    # input channels on the multifunction module as byte data, but does not
    # initiate the scan. This command redefines the scan list.
    # The digital input channels are numbered "s01" (LSB) and "s02"
    # (MSB), where s is the first digit of the slot number.
    # example: CONF:DIG:BYTE (@101:102)
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "DIGital:DATA:"
        self.cmd = self.prefix
        self.req_byte = req2(self.prefix + "BYTE")
        self.req_word = req2(self.prefix + "WORD")
        if self.prefix.find("SOURce:") != -1:
            self.conf_byte = sel_ch_with_param(self.prefix + "BYTE", 0, 255)
            self.conf_word = sel_ch_with_param(self.prefix + "WORD", 0, 65535)



class frequency(select_channel):
    # These commands configure the channels for frequency or period
    # measurements, but they do not initiate the scan.
    # The CONFigure command does not place the instrument in the "wait-fortrigger"
    # state. Use the INITiate or READ? command in conjunction with
    # CONFigure to place the instrument in the "wait-for-trigger" state.
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "FREQuency"
        self.cmd = self.prefix
        if self.prefix.find("CONFigure:") != -1:
            self.conf = conf2(self.prefix + " ")
        if self.prefix.find("MEASure:") != -1:
            self.req = req2(self.prefix)
        if self.prefix.find("SENSe:") != -1:
            self.Range_lower_req = req2(self.prefix + ":RANGe:LOWer")
            self.Range_lower_conf = conf2(self.prefix + ":RANGe:LOWer")
            self.Volt_range_req = req2(self.prefix + ":VOLTage:RANGe")
            self.Volt_range_conf = conf2(self.prefix + ":VOLTage:RANGe")
            self.voltage = voltage(self.prefix)
            # self.Volt_range_auto_on_conf = conf2(self.prefix + ":VOLTage:RANGe:AUTO ON,")
            # self.Volt_range_auto_off_conf = conf2(self.prefix + ":VOLTage:RANGe:AUTO OFF,")
            # self.Volt_range_auto_req = req2(self.prefix + ":VOLTage:RANGe:AUTO")
            self.Aperture = Aperture(self.prefix)


class period(select_channel):
    # These commands configure the channels for frequency or period
    # measurements, but they do not initiate the scan.
    # The CONFigure command does not place the instrument in the "wait-fortrigger"
    # state. Use the INITiate or READ? command in conjunction with
    # CONFigure to place the instrument in the "wait-for-trigger" state.
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "PERiod"
        self.cmd = self.prefix
        if self.prefix.find("CONFigure:") != -1:
            self.conf = conf2(self.prefix + " ")
        if self.prefix.find("MEASure:") != -1:
            self.req = req2(self.prefix)


class temperature(select_channel):
    # These commands configure the channels for temperature measurements
    # but do not initiate the scan. If you omit the optional <ch_list> parameter,
    # this command applies to the currently defined scan list.
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "TEMPerature"
        self.cmd = self.prefix
        if self.prefix.find("CONFigure:") != -1:
            self.conf = conf2(self.prefix + " ")
        if self.prefix.find("MEASure:") != -1:
            self.req = req2(self.prefix)
        if self.prefix.find("SENSe:") != -1:
            self.rjunction = req2(self.prefix + ":" + "RJUNction")
            self.transducer = transduser(self.prefix)


class resistance(select_channel):
    # These commands configure the channels for 2-wire (RESistance)
    # resistance measurements but do not initiate the scan.
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "RESistance"
        self.cmd = self.prefix
        self.prefix = self.cmd
        if self.prefix.find("CONFigure:") != -1:
            self.conf = conf2(self.prefix + " ")
        if self.prefix.find("MEASure:") != -1:
            self.req = req2(self.prefix)
        if self.prefix.find("SENSe:") != -1:
            self.Bandwidth = Bandwidth(self.prefix)
            self.Range = Range(self.prefix)
            self.Resolution = Resolution(self.prefix)
            self.Aperture = Aperture(self.prefix)
            self.NPLC = NPLC(self.prefix)
            self.Ocompensated = Ocompensated(self.prefix)


class fresistance(select_channel):
    # These commands configure the channels for  4-wire (FRESistance) resistance
    # measurements but do not initiate the scan.
    def __init__(self, prefix):
        self.prefix = prefix + ":" + "FRESistance"
        self.cmd = self.prefix
        self.prefix = self.cmd
        if self.prefix.find("CONFigure:") != -1:
            self.conf = conf2(self.prefix + " ")
        if self.prefix.find("MEASure:") != -1:
            self.req = req2(self.prefix)
        if self.prefix.find("SENSe:") != -1:
            self.Bandwidth = Bandwidth(self.prefix)
            self.Range = Range(self.prefix)
            self.Resolution = Resolution(self.prefix)
            self.Aperture = Aperture(self.prefix)
            self.NPLC = NPLC(self.prefix)
            self.Ocompensated = Ocompensated(self.prefix)


class totalize():
    # This command configures the instrument to read the specified totalizer
    # channels on the multifunction module but does not initiate the scan. To
    # read the totalizer during a scan without resetting the count, set the
    # <mode> to READ. To read the totalizer during a scan and reset the count
    # to 0 after it is read, set the <mode> to RRESet (this means "read and
    # reset").
    # CONFigure:TOTalize <mode: READ|RRESet>,(@<scan_list>)

    def __init__(self, prefix):
        self.prefix = prefix + ":" + "TOTalize"
        self.cmd = self.prefix
        if self.prefix.find("CONFigure:") != -1:
            self.conf_read = conf2(self.prefix + " READ,")
            self.conf_rres = conf2(self.prefix + " RRES,")
        # probably it will be better to use conf2 class
        if self.prefix.find("MEASure:") != -1:
            self.req_read = conf2(self.prefix + "?" + " READ,")
            self.req_rres = conf2(self.prefix + "?" + " RRES,")


class ac(select_channel):
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "AC"
        self.prefix = self.cmd
        if self.prefix.find("CONFigure:") != -1:
            self.conf = conf2(self.prefix + " ")
        if self.prefix.find("MEASure:") != -1:
            self.req = req2(self.prefix)
        if self.prefix.find("SENSe:") != -1:
            self.Bandwidth = Bandwidth(self.prefix)
            self.Range = Range(self.prefix)
            self.Resolution = Resolution(self.prefix)


class dc(select_channel):
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "DC"
        self.prefix = self.cmd
        if self.prefix.find("CONFigure:") != -1:
            self.conf = conf2(self.prefix + " ")
        if self.prefix.find("MEASure:") != -1:
            self.req = req2(self.prefix)
        if self.prefix.find("SENSe:") != -1:
            self.Range = Range(self.prefix)
            self.Resolution = Resolution(self.prefix)
            self.Aperture = Aperture(self.prefix)
            self.NPLC = NPLC(self.prefix)


class Bandwidth():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "BANDwidth"
        self.prefix = self.cmd
        self.conf_3 = conf2(self.prefix + " 3,")
        self.conf_20 = conf2(self.prefix + " 20,")
        self.conf_200 = conf2(self.prefix + " 200,")
        self.req = req2(self.prefix)


class Range(str_return):
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "RANGe"
        self.prefix = self.cmd
        self.auto = auto(self.prefix)
        self.conf = conf2(self.prefix + " ")
        self.req = req2(self.prefix)
        self.conf_min = conf2(self.prefix + " MIN,")
        self.conf_max = conf2(self.prefix + " MAX,")


class Resolution(str_return):
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "RESolution"
        self.prefix = self.cmd
        self.conf = conf2(self.prefix + " ")
        self.req = req2(self.prefix)


class Aperture(str_return):
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "APERture"
        self.prefix = self.cmd
        self.req = req2(self.prefix)
        self.conf_min = conf2(self.prefix + " 400E-6,")
        self.conf_10ms = conf2(self.prefix + " 10E-3,")
        self.conf_100ms = conf2(self.prefix + " 100E-3,")
        self.conf_500ms = conf2(self.prefix + " 500E-3,")
        self.conf_max = conf2(self.prefix + " 1,")


class NPLC(str_return):
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "NPLC"
        self.prefix = self.cmd
        self.conf = conf2(self.prefix + " ")
        self.req = req2(self.prefix)
        self.conf_min = conf2(self.prefix + " 0.02,")
        self.conf_02 = conf2(self.prefix + " 0.2,")
        self.conf_1 = conf2(self.prefix + " 1,")
        self.conf_2 = conf2(self.prefix + " 2,")
        self.conf_10 = conf2(self.prefix + " 10,")
        self.conf_20 = conf2(self.prefix + " 20,")
        self.conf_100 = conf2(self.prefix + " 100,")
        self.conf_max = conf2(self.prefix + " 200,")


class Ocompensated():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "OCOMpensated"
        self.prefix = self.cmd
        self.conf_on = conf2(self.prefix + " ON,")
        self.conf_off = conf2(self.prefix + " OFF,")
        self.req = req2(self.prefix)


class transduser():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "TRANsducer"
        self.prefix = self.cmd
        self.rtd = rtd(self.prefix)
        self.frtd = frtd(self.prefix)
        self.tcouple = tcouple(self.prefix)
        self.thermistor = thermistor(self.prefix)


class rtd():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "RTD"
        self.prefix = self.cmd
        self.Ocompensated = Ocompensated(self.prefix)
        self.type = rtd_type(self.prefix)
        self.resistance = resistance_ref(self.prefix)


class frtd():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "FRTD"
        self.prefix = self.cmd
        self.Ocompensated = Ocompensated(self.prefix)
        self.type = rtd_type(self.prefix)
        self.resistance = resistance_ref(self.prefix)


class rtd_type():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "TYPE"
        self.prefix = self.cmd
        self.conf_85 = conf2(self.prefix + " 85,")
        self.conf_91 = conf2(self.prefix + " 91,")
        self.req = req2(self.prefix)


class resistance_ref():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "RESistance:REFerence"
        self.prefix = self.cmd
        self.conf_49 = conf2(self.prefix + " 49,")
        self.conf_2100 = conf2(self.prefix + " 2100,")
        self.req = req2(self.prefix)


class tcouple():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "TCouple"
        self.prefix = self.cmd
        self.check = tcouple_check(self.prefix)
        self.rjunction = tcouple_rjunction(self.prefix)
        self.type = tcouple_type(self.prefix)


class tcouple_check():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "CHECk"
        self.prefix = self.cmd
        self.conf_on = conf2(self.prefix + " ON,")
        self.conf_off = conf2(self.prefix + " OFF,")
        self.req = req2(self.prefix)


class tcouple_rjunction():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "RJUNction"
        self.prefix = self.cmd
        self.req = req2(self.prefix)
        self.conf_m20C = conf2(self.prefix + " -20,")
        self.conf_80C = conf2(self.prefix + " 80,")
        self.type = junction_type(self.prefix)


class junction_type():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "TYPE"
        self.prefix = self.cmd
        self.req = req2(self.prefix)
        self.conf_internal = conf2(self.prefix + " INTernal,")
        self.conf_external = conf2(self.prefix + " EXTernal,")
        self.conf_fixed = conf2(self.prefix + " FIXed,")


class tcouple_type():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "TYPE"
        self.prefix = self.cmd
        self.req = req2(self.prefix)
        self.conf_B = conf2(self.prefix + " B,")
        self.conf_E = conf2(self.prefix + " E,")
        self.conf_J = conf2(self.prefix + " J,")
        self.conf_K = conf2(self.prefix + " K,")
        self.conf_N = conf2(self.prefix + " N,")
        self.conf_R = conf2(self.prefix + " R,")
        self.conf_S = conf2(self.prefix + " S,")
        self.conf_T = conf2(self.prefix + " T,")


class thermistor():
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + ":THERmistor:TYPE"
        self.prefix = self.cmd
        self.req = req2(self.prefix)
        self.conf_type_2252 = conf2(self.prefix + " 2252,")
        self.conf_type_5000 = conf2(self.prefix + " 5000,")
        self.conf_type_10000 = conf2(self.prefix + " 10000,")


class trigger():
    # TRIGger:COUNt
    # TRIGger:COUNt?
    # TRIGger:SOURce
    # TRIGger:SOURce?
    # TRIGger:TIMer
    # TRIGger:TIMer?
    def __init__(self):
        print("INIT Trigger")
        self.cmd = "TRIGger"
        self.prefix = "TRIGger"
        self.count = trig_count(self.prefix)
        self.source = trig_source(self.prefix)
        self.timer = trig_timer(self.prefix)


class trig_count(dig_param):
    # This command specifies the number of times to sweep through the scan
    # list. A sweep is one pass through the scan list. The scan stops when the
    # number of specified sweeps has occurred.
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "COUNt"
        self.prefix = self.cmd
        self.req = req2(self.prefix)
        self.min = 0
        self.max = 500000


class trig_source():
    # Select the trigger source to control the onset of each sweep through the
    # scan list (a sweep is one pass through the scan list). The instrument will
    # accept a software (bus) command, an immediate (continuous) scan
    # trigger, an external TTL trigger pulse, an alarm-initiated action, or an
    # internally paced timer.
    # IMMediate=Continuous scan trigger
    # BUS =Software trigger
    # EXTernal =An external TTL pulse trigger
    # ALARm = Trigger on an alarm
    # TIMer =Internally paced timer trigger
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "SOURce"
        self.prefix = self.cmd
        self.req = req2(self.prefix)
        self.conf_bus = str3(self.prefix + " BUS")
        self.conf_immediate = str3(self.prefix + " IMMediate")
        self.conf_alarm1 = str3(self.prefix + " ALARm1")
        self.conf_alarm2 = str3(self.prefix + " ALARm2")
        self.conf_alarm3 = str3(self.prefix + " ALARm3")
        self.conf_alarm4 = str3(self.prefix + " ALARm4")
        self.conf_timer = str3(self.prefix + " TIMer")


class trig_timer(dig_param):
    # This command sets the trigger-to-trigger interval (in seconds) for
    # measurements on the channels in the present scan list. This command
    # defines the time from the start of one trigger to the start of the next
    # trigger, up to the specified trigger count (see TRIGger:COUNt
    # command).
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "TIMer"
        self.prefix = self.cmd
        self.req = req2(self.prefix)
        self.min = 0
        self.max = 0.359999

class source():
    # SOURce:DIGital:DATA[:{BYTE|WORD}]
    # SOURce:DIGital:DATA[:{BYTE|WORD}]?
    # This command outputs a digital pattern as an 8-bit byte or 16-bit word to
    # the specified digital output channels.
    #
    # SOURce:DIGital:STATe?
    # This command returns the status (input or output) of the specified digital
    # channels.
    #
    # SOURce:VOLTage
    # SOURce:VOLTage?
    def __init__(self):
        print("INIT SOURce")
        self.cmd = "SOURce"
        self.prefix = "SOURce"
        self.digital_data = digital_data(self.prefix)
        self.digital_state_req = req2(self.prefix + ":DIGital:STATe")
        self.voltage = source_voltage(self.prefix)


class source_voltage():
    # This command sets the output voltage level for the specified DAC
    # channels on the 34907A Multifunction Module.
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix + ":" + "VOLTage"
        self.prefix = self.cmd
        self.min = -12
        self.max = 12
        self.req = req2(self.prefix)
        self.conf = sel_ch_with_param(self.prefix, self.min, self.max)

class status():
    # *ESE
    # *ESE?
    # *ESR?
    # *SRE
    # *STB?
    # STATus:ALARm:CONDition?
    # STATus:ALARm:ENABle
    # STATus:ALARm:ENABle?
    # STATus:ALARm[:EVENt]?
    # STATus:OPERation:CONDition?
    # STATus:OPERation:ENABle
    # STATus:OPERation:ENABle?
    # STATus:OPERation[:EVENt]?
    # STATus:PRESet
    # STATus:QUEStionable:CONDition?
    # STATus:QUEStionable:ENABle
    # STATus:QUEStionable:ENABle?
    # STATus:QUEStionable[:EVENt]?
    def __init__(self):
        print("INIT Status")
        self.cmd = "STATus"
        self.prefix = "STATus"
        self.ese = str_and_req("*ESE")
        self.esr = req3("*ESR")
        self.sre = str3("*SRE")
        self.stb = req3("*STB")
        self.preset = str3(self.prefix + ":" + "PRESet")
        self.alarm = st_com(self.prefix + ":" + "ALARm" )
        self.operation = st_com(self.prefix + ":" + "OPERation" )
        self.questionable = st_com(self.prefix + ":" + "QUEStionable")

class st_com():
    # This command sets the output voltage level for the specified DAC
    # channels on the 34907A Multifunction Module.
    def __init__(self, prefix):
        self.prefix = prefix
        self.cmd = self.prefix
        self.prefix = self.cmd
        self.condition = req3(self.prefix + ":" + "CONDition")
        self.enable_conf = dig_param3(self.prefix + ":ENABle", 0, 65535)
        self.enable_req = req3(self.prefix + ":ENABle")
        self.event = req3(self.prefix + ":" + "EVENt")



if __name__ == '__main__':
    # dev = LOG_34970A()
    # dev.init("COM10")
    # dev.send("COM10 send")
    cmd = storage()
    print("")
    print("TOP LEVEL")
    print("*" * 150)
    print(cmd.abort.str())
    print(cmd.fetch.req())
    print(cmd.r.val(100))
    print(cmd.init.str())

    print(cmd.read.str())
    print(cmd.read.ch.range(102, 105))

    print(cmd.r.val(1000))

    print(cmd.unit_temperature.req.str())
    print(cmd.unit_temperature.req.ch.range(102, 110))
    print(cmd.unit_temperature.conf_c.ch.range(110, 115))
    print(cmd.unit_temperature.conf_f.ch.range(110, 115))
    print(cmd.unit_temperature.conf_k.ch.range(110, 115))

    print(cmd.input_impedance_auto.req.str())
    print(cmd.input_impedance_auto.req.ch.range(109, 112))
    print(cmd.input_impedance_auto.conf_on.ch.range(101, 108))
    print(cmd.input_impedance_auto.conf_off.ch.list(101, 108))

    print("")
    print("Configure")
    print("*" * 150)
    print(cmd.configure.req())

    print(cmd.configure.voltage.ac.conf.ch.range(101, 108))
    print(cmd.configure.voltage.dc.conf.ch.range(101, 108))

    print(cmd.configure.current.ac.conf.ch.range(101, 108))
    print(cmd.configure.current.dc.conf.ch.range(101, 108))

    print(cmd.configure.digital_byte.conf.ch.range(101, 110))

    print(cmd.configure.resistance.conf.ch.range(101, 107))
    print(cmd.configure.fresistance.conf.ch.range(101, 107))

    print(cmd.configure.frequency.conf.ch.range(101, 110))
    print(cmd.configure.period.conf.ch.range(101, 110))

    print(cmd.configure.resistance.conf.ch.range(101, 110))

    print(cmd.configure.temperature.conf.ch.range(101, 110))
    print(cmd.configure.totalize.conf_read.ch.range(101, 110))

    print("")
    print("MEASURE")
    print("*" * 150)
    print(cmd.measure.voltage.ac.req.ch.range(109, 115))
    print(cmd.measure.current.dc.req.ch.range(109, 115))
    print(cmd.measure.digital_byte.req.ch.range(101, 120))
    print(cmd.measure.frequency.req.ch.range(101, 120))
    print(cmd.measure.period.req.ch.range(101, 120))
    print(cmd.measure.temperature.req.ch.range(101, 120))
    print(cmd.measure.totalize.req_read.ch.range(101, 120))
    print(cmd.measure.totalize.req_rres.ch.range(101, 120))
    print(cmd.measure.resistance.req.ch.range(101, 120))
    print(cmd.measure.fresistance.req.ch.range(101, 120))

    print("")
    print("sense")
    print("*" * 150)

    print(cmd.sense.current.ac.Bandwidth.conf_200.ch.list(102, 105))
    print(cmd.sense.current.ac.Bandwidth.conf_3.ch.list(101))
    print(cmd.sense.current.ac.Range.req.ch.range(102, 105))
    print(cmd.sense.current.ac.Range.auto.req.ch.range(102, 105))
    print(cmd.sense.current.ac.Range.auto.off.ch.range(102, 105))
    print(cmd.sense.current.ac.Resolution.conf.ch.range(101, 102))
    print(cmd.sense.current.ac.Bandwidth.req.ch.range(102, 105))
    print(cmd.sense.current.dc.NPLC.conf_10.ch.range(101, 103))

    print(cmd.sense.current.ac.Range.req.ch.range(102, 105))
    print(cmd.sense.current.ac.Range.auto.req.ch.range(102, 105))
    print(cmd.sense.current.ac.Resolution.conf.ch.range(101, 102))
    print(cmd.sense.current.ac.Bandwidth.req.ch.range(102, 105))

    print(cmd.sense.digital_byte.req_byte.ch.range(101, 105))
    print(cmd.sense.digital_byte.req_word.ch.range(101, 105))

    print(cmd.sense.frequency.voltage.Range.auto.off.ch.list(101))

    print(cmd.sense.zero.auto.off.ch.list(102))
    print(cmd.sense.func.req.ch.list(120))
    print(cmd.sense.func.temperature.ch.range(101, 104))
    print(cmd.sense.temperature.rjunction.ch.range(101, 105))
    print(cmd.sense.temperature.transducer.rtd.type.conf_85.ch.range(103, 108))
    print(cmd.sense.temperature.transducer.frtd.type.conf_91.ch.range(103, 108))
    print(cmd.sense.temperature.transducer.rtd.resistance.conf_49.ch.list(101))
    print(cmd.sense.temperature.transducer.tcouple.type.conf_K.ch.list(102, 110))
    print(cmd.sense.temperature.transducer.thermistor.conf_type_5000.ch.list(120))

    print("")
    print("TRIGER")
    print("*" * 150)
    print(cmd.trigger.timer.val(0.001))
    print(cmd.trigger.count.val(100))
    print(cmd.trigger.source.conf_alarm1.str())
    print(cmd.trigger.source.conf_timer.str())

    print("")
    print("SOURCE")
    print("*" * 150)
    print(cmd.source.voltage.req.ch.list(102))
    print(cmd.source.voltage.conf.list(10, 101, 102))
    print(cmd.source.voltage.conf.range(8.000, 101, 115))
    print(cmd.source.digital_state_req.ch.range(101, 102))
    print(cmd.source.digital_data.conf_byte.list(100, 101))
    print(cmd.source.digital_data.conf_word.range(65540, 101, 110))

    print("")
    print("STATUS")
    print("*" * 150)
    print(cmd.status.ese.req())
    print(cmd.status.ese.str())
    print(cmd.status.sre.str())
    print(cmd.status.alarm.condition.req())
    print(cmd.status.alarm.enable_conf.val(10))
    print(cmd.status.alarm.enable_req.req())
    print(cmd.status.operation.enable_conf.val(100))
    print(cmd.status.questionable.condition.req())
    #
    # print("*" * 30)
    # print(cmd.sense.voltage.ac.Range.combine())
    # print(cmd.sense.voltage.ac.Resolution.combine())
    # print(cmd.sense.voltage.ac.Bandwidth.combine())
    #
    # print("*" * 30)
    # print(cmd.sense.current.dc.Aperture.combine())
    # print(cmd.sense.current.dc.NPLC.combine())
    # print(cmd.sense.current.dc.Range.combine())
    # print(cmd.sense.current.dc.Range.Auto.combine())
    # print(cmd.sense.current.dc.Resolution.combine())
    #
    # print("*" * 30)
    # print(cmd.sense.resistance.Aperture.combine())
    # print(cmd.sense.resistance.NPLC.combine())
    # print(cmd.sense.resistance.Ocompensated.combine())
    # print(cmd.sense.resistance.Range.combine())
    # print(cmd.sense.resistance.Range.Auto.combine())
    # print(cmd.sense.resistance.Resolution.combine())
    #
    # print("*" * 30)
    # print(cmd.sense.fresistance.Aperture.combine())
    # print(cmd.sense.fresistance.NPLC.combine())
    # print(cmd.sense.fresistance.Ocompensated.combine())
    # print(cmd.sense.fresistance.Range.combine())
    # print(cmd.sense.fresistance.Range.Auto.combine())
    # print(cmd.sense.fresistance.Resolution.combine())

    # print("*" * 30)
    # print(cmd.route.scan.str())
    # print(cmd.route.scan.size.req())
    # print(cmd.route.scan.ch_range(0, 301, 320))
    # print(cmd.route.close.exclusive.str())
    # print(cmd.route.close.exclusive.ch_range(0,110,120))
    # print(cmd.route.open.req())
    # print(cmd.route.scan.size.req())
    # print(cmd.route.done.req())
    # print(cmd.route.monitor.req())
    # print(cmd.route.monitor.ch_single(320))
    # print(cmd.route.monitor.state.mode_on())
    # print(cmd.route.monitor.state.mode_off())
    # print(cmd.route.monitor.state.req())
