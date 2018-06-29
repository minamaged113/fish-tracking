"""
Python3 module
provided by the University of Oulu in collaboration with
LUKE-OY. The software is intended to be an open-source.

author: Mina Ghobrial.
date:   April 19th, 2018.

References: 
#   https://github.com/SoundMetrics
#   https://github.com/EminentCodfish/pyARIS

"""
import struct
import json
import aris_utils.utils as utils
import numpy as np 
import aris_utils.error_description as err


class ARIS_Frame:
    FRAME_DATA = None
    BEAM_COUNT = None
    Tmatrix = None
    def __init__(self, filename, frameIndexInp, frameSize):
        frameIndex = frameIndexInp - 1
        try:
            with open(filename, "rb") as fhand:
                frameoffset = (1024+(frameIndex*(1024+(frameSize))))
                fhand.seek(frameoffset, 0)
                self.frameIndex = struct.unpack(
                    utils.cType["uint64_t"], fhand.read(utils.c("uint64_t")))[0]
                self.frameTime = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.version = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.status = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.sonarTimeStamp = struct.unpack(
                    utils.cType["uint64_t"], fhand.read(utils.c("uint64_t")))[0]
                self.TS_Day = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.TS_Hour = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.TS_Minute = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.TS_Second = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.TS_Hsecond = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.transmitMode = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.windowStart = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.windowLength = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.threshold = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.intensity = struct.unpack(
                    utils.cType["int32_t"], fhand.read(utils.c("int32_t")))[0]
                self.receiverGain = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.degC1 = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.degC2 = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.humidity = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.focus = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.battery = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.userVal1 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.userVal2 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.userVal3 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.userVal4 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.userVal5 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.userVal6 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.userVal7 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.userVal8 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.velocity = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.depth = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.altitude = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.pitch = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.pitchRate = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.roll = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.rollRate = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.heading = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.headingRate = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.compassHeading = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.compassPitch = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.compassRoll = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.latitude = struct.unpack(
                    utils.cType["double"], fhand.read(utils.c("double")))[0]
                self.longitude = struct.unpack(
                    utils.cType["double"], fhand.read(utils.c("double")))[0]
                self.sonarPosition = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.configFlags = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.beamTilt = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.targetRange = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.targetBearing = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.targetPresent = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.firmwareRev = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.flags = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.sourceFrame = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.waterTemp = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.timerPeriod = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.sonarX = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.sonarY = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.sonarZ = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.sonarPan = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.sonarTilt = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.sonarRoll = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.panPNNL = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.tiltPNNL = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.rollPNNL = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.vehicleTime = struct.unpack(
                    utils.cType["double"], fhand.read(utils.c("double")))[0]
                self.timeGGK = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.dateGGK = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.qualityGGK = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.numStatsGGK = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.DOPGGK = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.EHTGGK = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.heaveTSS = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.yearGPS = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.monthGPS = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.dayGPS = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.hourGPS = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.minuteGPS = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.secondGPS = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.HSecondGPS = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.sonarPanOffset = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.sonarTiltOffset = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.sonarRollOffset = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.sonarXOffset = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.sonarYOffset = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.sonarZOffset = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix1 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix2 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix3 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix4 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix5 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix6 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix7 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix8 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix9 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix10 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix11 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix12 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix13 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix14 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix15 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.Tmatrix16 = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.sampleRate = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.accelX = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.accelY = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.accelZ = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.pingMode = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.freq = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.pulseWidth = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.cyclePeriod = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.samplePeriod = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.transmitEnable = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.frameRate = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.soundSpeed = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.samplesPerBeam = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.enable150V = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.sampleStartDelay = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.largeLens = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.systemType = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.sonarSerialNumber = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.reservedEK = struct.unpack(
                    utils.cType["uint64_t"], fhand.read(utils.c("uint64_t")))[0]
                self.ARISErrorFlags = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.missedPackets = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.ARISAppVersion = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.available2 = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.reordered = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.salinity = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.pressure = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.batteryVoltage = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.mainVoltage = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.switchVoltage = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.focusMotorMoving = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.voltageChanging = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.focusTimeoutFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.focusOverCurrentFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.focusNotFoundFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.focusStalledFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.FPGATimeoutFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.FPGABusyFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.FPGAStuckFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.CPUTempFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.PSUTempFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.waterTempFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.humidityFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.pressureFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.voltageReadFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.voltageWriteFault = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.focusCurrentPosition = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.targetPan = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.targetTilt = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.targetRoll = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.panMotorErrorCode = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.tiltMotorErrorCode = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.rollMotorErrorCode = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.panAbsPos = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.tiltAbsPos = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.rollAbsPos = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.panAccelX = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.panAccelY = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.panAccelZ = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.tiltAccelX = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.tiltAccelY = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.tiltAccelZ = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.rollAccelX = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.rollAccelY = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.rollAccelZ = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.appliedSett = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.constrainedSett = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.invalidSett = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.enableInterpacketDelay = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.interpacketDelayPeriod = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.uptime = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.ARISAppVersionMajor = struct.unpack(
                    utils.cType["uint16_t"], fhand.read(utils.c("uint16_t")))[0]
                self.ARISAppVersionMinor = struct.unpack(
                    utils.cType["uint16_t"], fhand.read(utils.c("uint16_t")))[0]
                self.goTime = struct.unpack(
                    utils.cType["uint64_t"], fhand.read(utils.c("uint64_t")))[0]
                self.panVelocity = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.tiltVelocity = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.rollVelocity = struct.unpack(
                    utils.cType["float"], fhand.read(utils.c("float")))[0]
                self.GPSTimeAge = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.systemVariant = struct.unpack(
                    utils.cType["uint32_t"], fhand.read(utils.c("uint32_t")))[0]
                self.padding = struct.unpack(
                    utils.cType["char[288]"], fhand.read(utils.c("char[288]")))[0]


                self.BEAM_COUNT = self.getBeamsFromPingMode(self.pingMode)
                self.FRAME_DATA = self.readData(frameoffset, fhand)
                

        except:
            err.print_error(err.frameReadError)
            raise
        pass

    def getBeamsFromPingMode(self, pingmode):
        """This function takes a class variable pingMode
        `self.pingMode` and returns the Number of beams
        across the image in the horizontal dimension;
        this is derived from the ping mode used. Beam
        count can be 48, 64, 96, or 128 depending on
        the model of ARIS that produced the data.

        if it returns false, it means that the file being
        read is corrupted.
        
        Arguments:
            pingmode {[integer]} -- [please look up `frame_headers_info.json`
                                    for `pingMode`]
        
        Returns:
            [integer] -- [Number of beams across the image in the horizontal dimension]
        """

        if pingmode in [1, 2]:
            return 48
        elif pingmode in [3,4,5]:
            return 96
        elif pingmode in [6,7,8]:
            return 64
        elif pingmode in [9,10,11,12]:
            return 128
        else:
            return False


    def readData(self, frameOffset , fileHandle):
        data = np.empty( [self.samplesPerBeam, self.BEAM_COUNT] , dtype=float)
        # print(self.samplesPerBeam, " x ", self.BEAM_COUNT)
        # print(data.size)
        fileHandle.seek(frameOffset+1024, 0)
        for rows in range(len(data)):
            for cols in range(len(data[rows])):
                data[rows][cols] = struct.unpack(utils.cType["uint8_t"] , fileHandle.read(1))[0]

        data = np.fliplr(data)
        return data


    def getTransformationMatrix(self, t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16):

        pass

    def __len__(self):
        pass
