from machine import I2C,UART,Pin,SPI,PWM
import framebuf
import time
import math

#▼LCD-Code▼
BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9
class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
#▲LCD-Code▲


#▼BLE-Code▼
# Power-on return message
Power_On_Return_Message_OFF        = b"AT+CR00\r\n"
Power_On_Return_Message_ON         = b"AT+CR01\r\n"

#  Restore Factory Defaults
Factory_Reset                      = b"AT+CW\r\n"

# Reset
Reset                              = b"AT+CZ\r\n"

# Set baud rate
Baud_Rate_9600                     = b"AT+CT01\r\n"
Baud_Rate_19200                    = b"AT+CT02\r\n"
Baud_Rate_38400                    = b"AT+CT03\r\n"
Baud_Rate_57600                    = b"AT+CT04\r\n"
Baud_Rate_115200                   = b"AT+CT05\r\n"
Baud_Rate_256000                   = b"AT+CT06\r\n"
Baud_Rate_512000                   = b"AT+CT07\r\n"
Baud_Rate_230400                   = b"AT+CT08\r\n"
Baud_Rate_460800                   = b"AT+CT09\r\n"
Baud_Rate_1000000                  = b"AT+CT10\r\n"
Baud_Rate_31250                    = b"AT+CT11\r\n"
Baud_Rate_2400                     = b"AT+CT12\r\n"
Baud_Rate_4800                     = b"AT+CT13\r\n"
# Query baud rate
Baud_Rate_Query                    = b"AT+QT\r\n"

# Chip low power Settings
Not_Low_Power                      = b"AT+CL00\r\n"
Low_Power                          = b"AT+CL01\r\n"
# Chip low power Query
Low_Power_Query                    = b"AT+QL\r\n"

# Set the bluetooth name and address
Name_BLE_Set                       = b"AT+Blekami\r\n"
Name_SPP_Set                       = b"AT+Sppkami\r\n"
ADD_SET                            = b"AT+BN666666666666\r\n"
# Example Query the name and address of bluetooth
Name_BLE_Query                     = b"AT+TM\r\n"
Name_SPP_Query                     = b"AT+TD\r\n"
ADD_Query                          = b"AT+TN\r\n"

# ON or OFF BLE
BLE_ON                             = b"AT+B401\r\n"
BLE_OFF                            = b"AT+B400\r\n"
# BLE Switch Query
BLE_Switch_Query                   = b"AT+T4\r\n"

# ON or OFF SPP
SPP_ON                             = b"AT+B501\r\n"
SPP_OFF                            = b"AT+B500\r\n"
# SPP Switch Query
SPP_Switch_Query                   = b"AT+T5\r\n"

# ERROR
ERROR_1                            = b"ER+1\r\n"
ERROR_2                            = b"ER+2\r\n"
ERROR_3                            = b"ER+3\r\n"
ERROR_4                            = b"ER+4\r\n"
ERROR_5                            = b"ER+5\r\n"
ERROR_6                            = b"ER+6\r\n"
ERROR_7                            = b"ER+7\r\n"
ERROR_8                            = b"ER+8\r\n"

# Bluetooth connection detection pin
BLE_MODE_PIN = Pin(15 , Pin.IN , Pin.PULL_UP)

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
# uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))
txData = b'RS232 receive test...\r\n'

def Pico_BLE_init():
    key1Flag=0
    if( BLE_MODE_PIN.value() == 0 ):
        pass
        #print("Please connect the device with your mobile phone")
    while(BLE_MODE_PIN.value() == 0):
        icm20948.icm20948_Gyro_Accel_Read()
        icm20948.icm20948MagRead()
        icm20948.icm20948CalAvgValue()
        
        icm20948.imuAHRSupdate(MotionVal[0] * 0.0175, MotionVal[1] * 0.0175,MotionVal[2] * 0.0175,MotionVal[3],MotionVal[4],MotionVal[5],MotionVal[6], MotionVal[7], MotionVal[8])
        pitch = math.asin(-2 * q1 * q3 + 2 * q0* q2)* 57.3
        roll  = math.atan2(2 * q2 * q3 + 2 * q0 * q1, -2 * q1 * q1 - 2 * q2* q2 + 1)* 57.3
        yaw   = math.atan2(-2 * q1 * q2 - 2 * q0 * q3, 2 * q2 * q2 + 2 * q3 * q3 - 1) * 57.3

        if key1Flag==1:
            LCD.fill(0x000000)
            LCD.hline(10,10,220,LCD.blue)
            LCD.hline(10,125,220,LCD.blue)
            LCD.vline(10,10,115,LCD.blue)
            LCD.vline(230,10,115,LCD.blue)
            LCD.text(('AX=%d'%(MotionVal[3])),12,12,LCD.green)
            LCD.text(('AY=%d'%(MotionVal[4])),82,12,LCD.green)
            LCD.text(('AZ=%d'%(MotionVal[5])),152,12,LCD.green)
            LCD.text(('GX=%.2f'%(MotionVal[0]*0.0175)),12,26,LCD.red)
            LCD.text(('GY=%.2f'%(MotionVal[1]*0.0175)),82,26,LCD.red)
            LCD.text(('GZ=%.2f'%(MotionVal[2]*0.0175)),152,26,LCD.red)
            LCD.text(('MX=%d'%(MotionVal[6])),12,40,LCD.blue)
            LCD.text(('MY=%d'%(MotionVal[7])),82,40,LCD.blue)
            LCD.text(('MZ=%d'%(MotionVal[8])),152,40,LCD.blue)
        elif key1Flag==2:
            LCD.fill(0x000000)
            LCD.hline(10,10,220,LCD.blue)
            LCD.hline(10,125,220,LCD.blue)
            LCD.vline(10,10,115,LCD.blue)
            LCD.vline(230,10,115,LCD.blue)
            LCD.text(('Pitch=%.2f' % (pitch)),12,12,LCD.green)
            LCD.text(('roll=%.2f' % (roll)),12,26,LCD.green)
            LCD.text(('yaw=%.2f' % (yaw)),12,40,LCD.green)
        elif key1Flag==3:
            LCD.fill(0x000000)
            LCD.hline(10,10,220,LCD.blue)
            LCD.hline(10,125,220,LCD.blue)
            LCD.vline(10,10,115,LCD.blue)
            LCD.vline(230,10,115,LCD.blue)
            LCD.text(('Qw=%.2f' % (q0)),12,12,LCD.green)
            LCD.text(('Qx=%.2f' % (q1)),12,26,LCD.green)
            LCD.text(('Qy=%.2f' % (q2)),12,40,LCD.green)
            LCD.text(('Qz=%.2f' % (q3)),12,54,LCD.green)
        elif key1Flag==4:
            LCD.fill(0x000000)
            LCD.hline(10,10,220,LCD.blue)
            LCD.hline(10,125,220,LCD.blue)
            LCD.vline(10,10,115,LCD.blue)
            LCD.vline(230,10,115,LCD.blue)
            LCD.text("Wait Bluetooth Link...",45,60,LCD.green)
            key1Flag=0
        if(key1.value() == 0):
            LCD.hline(10,10,220,LCD.white)
            LCD.hline(10,125,220,LCD.white)
            LCD.vline(10,10,115,LCD.white)
            LCD.vline(230,10,115,LCD.white)
            key1Flag=key1Flag+1
        LCD.show()
        time.sleep_ms(100)
        
    while(True):
        #uart.write("Remove the interference")
        time.sleep_ms(20)
        Data_RX = uart.read(6)
        if( Data_RX == b"ER+7\r\n" ):
            pass
            #print("Enable notify on the mobile phone\r\n")
        else:
            pass
            #print("The connection is successful")
            #uart.write("The connection is successful")
            time.sleep_ms(100)
            break
        Data_RX = ''
        time.sleep_ms(1000)
        
    # Querying Basic Information
    Cmd_Process(Baud_Rate_Query)
    time.sleep_ms(100)
    Cmd_Process(Low_Power_Query)
    time.sleep_ms(100)
    Cmd_Process(Name_BLE_Query)
    time.sleep_ms(100)
    Cmd_Process(Name_SPP_Query)
    time.sleep_ms(100)
    Cmd_Process(ADD_Query)
    time.sleep_ms(100)
    Cmd_Process(BLE_Switch_Query)
    time.sleep_ms(100)
    Cmd_Process(SPP_Switch_Query)
    time.sleep_ms(100)

    # Change the name of Bluetooth
    if( Cmd_Process(Name_BLE_Set) ):
        pass
        #print("BLE was successfully renamed to : BLE-Waveshare")
        #uart.write("BLE was successfully renamed to : BLE-Waveshare")
    time.sleep_ms(100)
    if( Cmd_Process(Name_SPP_Set) ):
        pass
        #print("SPP was successfully renamed to : SPP-Waveshare")
        #uart.write("SPP was successfully renamed to : SPP-Waveshare")
    time.sleep_ms(100)

def Cmd_Process(data):
    i = 0
    #uart.write( data )
    time.sleep_ms(20)
    Data_RX = uart.read()
    if( Data_RX == None ):
        return False
    '''
    if( data == Baud_Rate_Query ):
        if( Data_RX[0:3] == b'QT+') :
            i = (Data_RX[3] - 48) * 10 + Data_RX[4] -48
            if( i == 1 ):
                print("Bluetooth baud rate is 9600")
                uart.write("Bluetooth baud rate is 9600")
            elif( i == 2 ):
                print("Bluetooth baud rate is 19200")
                uart.write("Bluetooth baud rate is 19200")
            elif( i == 3 ):
                print("Bluetooth baud rate is 38400")
                uart.write("Bluetooth baud rate is 38400")
            elif( i == 4 ):
                print("Bluetooth baud rate is 57600")
                uart.write("Bluetooth baud rate is 57600")
            elif( i == 5 ):
                print("Bluetooth baud rate is 115200")
                uart.write("Bluetooth baud rate is 115200")
            elif( i == 6 ):
                print("Bluetooth baud rate is 256000")
                uart.write("Bluetooth baud rate is 256000")
            elif( i == 7 ):
                print("Bluetooth baud rate is 512000")
                uart.write("Bluetooth baud rate is 512000")
            elif( i == 8 ):
                print("Bluetooth baud rate is 230400")
                uart.write("Bluetooth baud rate is 230400")
            elif( i == 9 ):
                print("Bluetooth baud rate is 460800")
                uart.write("Bluetooth baud rate is 460800")
            elif( i == 10 ):
                print("Bluetooth baud rate is 1000000")
                uart.write("Bluetooth baud rate is 1000000")
            elif( i == 11 ):
                print("Bluetooth baud rate is 31250")
                uart.write("Bluetooth baud rate is 31250")
            elif( i == 12 ):
                print("Bluetooth baud rate is 2400")
                uart.write("Bluetooth baud rate is 2400")
            elif( i == 13 ):
                print("Bluetooth baud rate is 4800")
                uart.write("Bluetooth baud rate is 4800")
    elif( data == Low_Power_Query ):
        if( Data_RX[0:5] == b'QL+00' ):
            print("Normal operating mode")
            uart.write("Normal operating mode")
        elif( Data_RX[0:5] == b'QL+01' ):
            print("Low power operation mode")
            uart.write("Low power operation mode")
    elif(( data == Name_BLE_Query ) | ( data == Name_SPP_Query ) | ( data == ADD_Query )):
        if( Data_RX[0:3] == b'TM+' ):
            print("BLE name is : ")
            uart.write("BLE name is : ")
            i = 3
            while (chr(Data_RX[i]) != '\r'):
                i = i+1
            print("%s"%Data_RX[3:i])
            uart.write( Data_RX[3:i] )    
        elif( Data_RX[0:3] == b'TD+' ):
            print("SPP name is : ")
            uart.write("SPP name is : ")
            i = 3
            while (chr(Data_RX[i]) != '\r'):
                i = i+1
            print("%s"%Data_RX[3:i])
            uart.write( Data_RX[3:i] )
        elif( Data_RX[0:3] == b'TB+' ):
            print("BLE add is : ")
            uart.write("BLE add is : ")
            i = 3
            while (chr(Data_RX[i]) != '\r'):
                i = i+1
            print("%s"%Data_RX[3:i])
            uart.write( Data_RX[3:i] )
    elif( data == BLE_Switch_Query ) | ( data == SPP_Switch_Query ):
        if( Data_RX[0:5] == b'T4+01' ):
            print("BLE to open up")
            uart.write("BLE to open up")
        elif( Data_RX[0:5] == b'T4+00' ):
            print("BLE to shut down")
            uart.write("BLE to shut down")
        elif( Data_RX[0:5] == b'T5+01' ):
            print("SPP to open up");
            uart.write("SPP to open up")
        elif( Data_RX[0:5] == b'T5+00' ):
            print("SPP to shut down")
            uart.write("SPP to shut down")
    else:
        if( Data_RX[0:2] == b'OK' ): 
#           print("Command executed successfully")
            return True
    if( Data_RX[0:3] == b'ER+' ):
        ERROR_OUT( Data_RX[3] - 48 )
        return False
'''
def ERROR_OUT(data):
    if( data == 1 ):
        print("Incorrect data frame received")
    elif( data == 2 ):
        print("The received command does not exist")
    elif( data == 3 ):
        print("Received AT instruction, carriage return line feed not received")
    elif( data == 4 ):
        print("Sent instructions with parameters that are out of range or in the wrong format. Please check your AT instructions")
    elif( data == 7 ):
        print("The MCU sends data to the mobile phone, but notify is not enabled on the mobile phone. The BLE connection is successfu")
#▲BLE-Code▲

#▼ICM20948-Code▼
Gyro  = [0,0,0]
Accel = [0,0,0]
Mag   = [0,0,0]
pitch = 0.0
roll  = 0.0
yaw   = 0.0
pu8data=[0,0,0,0,0,0,0,0]
U8tempX=[0,0,0,0,0,0,0,0,0]
U8tempY=[0,0,0,0,0,0,0,0,0]
U8tempZ=[0,0,0,0,0,0,0,0,0]
GyroOffset=[0,0,0]
Ki = 1.0
Kp = 4.50
q0 = 1.0
q1=q2=q3=0.0
angles=[0.0,0.0,0.0]
true                                 =0x01
false                                =0x00
# define ICM-20948 Device I2C address
I2C_ADD_ICM20948                     = 0x68
I2C_ADD_ICM20948_AK09916             = 0x0C
I2C_ADD_ICM20948_AK09916_READ        = 0x80
I2C_ADD_ICM20948_AK09916_WRITE       = 0x00
# define ICM-20948 Register
# user bank 0 register
REG_ADD_WIA                          = 0x00
REG_VAL_WIA                          = 0xEA
REG_ADD_USER_CTRL                    = 0x03
REG_VAL_BIT_DMP_EN                   = 0x80
REG_VAL_BIT_FIFO_EN                  = 0x40
REG_VAL_BIT_I2C_MST_EN               = 0x20
REG_VAL_BIT_I2C_IF_DIS               = 0x10
REG_VAL_BIT_DMP_RST                  = 0x08
REG_VAL_BIT_DIAMOND_DMP_RST          = 0x04
REG_ADD_PWR_MIGMT_1                  = 0x06
REG_VAL_ALL_RGE_RESET                = 0x80
REG_VAL_RUN_MODE                     = 0x01 # Non low-power mode
REG_ADD_LP_CONFIG                    = 0x05
REG_ADD_PWR_MGMT_1                   = 0x06
REG_ADD_PWR_MGMT_2                   = 0x07
REG_ADD_ACCEL_XOUT_H                 = 0x2D
REG_ADD_ACCEL_XOUT_L                 = 0x2E
REG_ADD_ACCEL_YOUT_H                 = 0x2F
REG_ADD_ACCEL_YOUT_L                 = 0x30
REG_ADD_ACCEL_ZOUT_H                 = 0x31
REG_ADD_ACCEL_ZOUT_L                 = 0x32
REG_ADD_GYRO_XOUT_H                  = 0x33
REG_ADD_GYRO_XOUT_L                  = 0x34
REG_ADD_GYRO_YOUT_H                  = 0x35
REG_ADD_GYRO_YOUT_L                  = 0x36
REG_ADD_GYRO_ZOUT_H                  = 0x37
REG_ADD_GYRO_ZOUT_L                  = 0x38
REG_ADD_EXT_SENS_DATA_00             = 0x3B
REG_ADD_REG_BANK_SEL                 = 0x7F
REG_VAL_REG_BANK_0                   = 0x00
REG_VAL_REG_BANK_1                   = 0x10
REG_VAL_REG_BANK_2                   = 0x20
REG_VAL_REG_BANK_3                   = 0x30

# user bank 1 register
# user bank 2 register
REG_ADD_GYRO_SMPLRT_DIV              = 0x00
REG_ADD_GYRO_CONFIG_1                = 0x01
REG_VAL_BIT_GYRO_DLPCFG_2            = 0x10  # bit[5:3]
REG_VAL_BIT_GYRO_DLPCFG_4            = 0x20  # bit[5:3]
REG_VAL_BIT_GYRO_DLPCFG_6            = 0x30  # bit[5:3]
REG_VAL_BIT_GYRO_FS_250DPS           = 0x00  # bit[2:1]
REG_VAL_BIT_GYRO_FS_500DPS           = 0x02  # bit[2:1]
REG_VAL_BIT_GYRO_FS_1000DPS          = 0x04  # bit[2:1]
REG_VAL_BIT_GYRO_FS_2000DPS          = 0x06  # bit[2:1]
REG_VAL_BIT_GYRO_DLPF                = 0x01  # bit[0]
REG_ADD_ACCEL_SMPLRT_DIV_2           = 0x11
REG_ADD_ACCEL_CONFIG                 = 0x14
REG_VAL_BIT_ACCEL_DLPCFG_2           = 0x10  # bit[5:3]
REG_VAL_BIT_ACCEL_DLPCFG_4           = 0x20  # bit[5:3]
REG_VAL_BIT_ACCEL_DLPCFG_6           = 0x30  # bit[5:3]
REG_VAL_BIT_ACCEL_FS_2g              = 0x00  # bit[2:1]
REG_VAL_BIT_ACCEL_FS_4g              = 0x02  # bit[2:1]
REG_VAL_BIT_ACCEL_FS_8g              = 0x04  # bit[2:1]
REG_VAL_BIT_ACCEL_FS_16g             = 0x06  # bit[2:1]
REG_VAL_BIT_ACCEL_DLPF               = 0x01  # bit[0]

# user bank 3 register
REG_ADD_I2C_SLV0_ADDR                = 0x03
REG_ADD_I2C_SLV0_REG                 = 0x04
REG_ADD_I2C_SLV0_CTRL                = 0x05
REG_VAL_BIT_SLV0_EN                  = 0x80
REG_VAL_BIT_MASK_LEN                 = 0x07
REG_ADD_I2C_SLV0_DO                  = 0x06
REG_ADD_I2C_SLV1_ADDR                = 0x07
REG_ADD_I2C_SLV1_REG                 = 0x08
REG_ADD_I2C_SLV1_CTRL                = 0x09
REG_ADD_I2C_SLV1_DO                  = 0x0A

# define ICM-20948 Register  end

# define ICM-20948 MAG Register
REG_ADD_MAG_WIA1                     = 0x00
REG_VAL_MAG_WIA1                     = 0x48
REG_ADD_MAG_WIA2                     = 0x01
REG_VAL_MAG_WIA2                     = 0x09
REG_ADD_MAG_ST2                      = 0x10
REG_ADD_MAG_DATA                     = 0x11
REG_ADD_MAG_CNTL2                    = 0x31
REG_VAL_MAG_MODE_PD                  = 0x00
REG_VAL_MAG_MODE_SM                  = 0x01
REG_VAL_MAG_MODE_10HZ                = 0x02
REG_VAL_MAG_MODE_20HZ                = 0x04
REG_VAL_MAG_MODE_50HZ                = 0x05
REG_VAL_MAG_MODE_100HZ               = 0x08
REG_VAL_MAG_MODE_ST                  = 0x10
# define ICM-20948 MAG Register  end

MAG_DATA_LEN                         =6

class ICM20948(object):#initialization
  def __init__(self,address=I2C_ADD_ICM20948):
    self._address = address
    self._bus = I2C(1)
    bRet=self.icm20948Check()#Multiple initializations will return an error (temporarily turned off)
    # while true != bRet:
    #   print("ICM-20948 Error\n" )
    #   time.sleep(0.5)
    # print("ICM-20948 OK\n" )
    time.sleep(0.5)                       #We can skip this detection by delaying it by 500 milliseconds
    # user bank 0 register 
    self._write_byte( REG_ADD_REG_BANK_SEL , REG_VAL_REG_BANK_0)
    self._write_byte( REG_ADD_PWR_MIGMT_1 , REG_VAL_ALL_RGE_RESET)
    time.sleep(0.1)
    self._write_byte( REG_ADD_PWR_MIGMT_1 , REG_VAL_RUN_MODE)  
    #user bank 2 register
    self._write_byte( REG_ADD_REG_BANK_SEL , REG_VAL_REG_BANK_2)
    self._write_byte( REG_ADD_GYRO_SMPLRT_DIV , 0x07)
    self._write_byte( REG_ADD_GYRO_CONFIG_1 , REG_VAL_BIT_GYRO_DLPCFG_6 | REG_VAL_BIT_GYRO_FS_1000DPS | REG_VAL_BIT_GYRO_DLPF)
    self._write_byte( REG_ADD_ACCEL_SMPLRT_DIV_2 ,  0x07)
    self._write_byte( REG_ADD_ACCEL_CONFIG , REG_VAL_BIT_ACCEL_DLPCFG_6 | REG_VAL_BIT_ACCEL_FS_2g | REG_VAL_BIT_ACCEL_DLPF)
    #user bank 0 register
    self._write_byte( REG_ADD_REG_BANK_SEL , REG_VAL_REG_BANK_0) 
    time.sleep(0.1)
    self.icm20948GyroOffset()
    self.icm20948MagCheck()
    self.icm20948WriteSecondary( I2C_ADD_ICM20948_AK09916|I2C_ADD_ICM20948_AK09916_WRITE,REG_ADD_MAG_CNTL2, REG_VAL_MAG_MODE_20HZ)
  def icm20948_Gyro_Accel_Read(self):
    self._write_byte( REG_ADD_REG_BANK_SEL , REG_VAL_REG_BANK_0)
    data =self._read_block(REG_ADD_ACCEL_XOUT_H, 12)
    self._write_byte( REG_ADD_REG_BANK_SEL , REG_VAL_REG_BANK_2)
    Accel[0] = (data[0]<<8)|data[1]
    Accel[1] = (data[2]<<8)|data[3]
    Accel[2] = (data[4]<<8)|data[5]
    Gyro[0]  = ((data[6]<<8)|data[7]) - GyroOffset[0]
    Gyro[1]  = ((data[8]<<8)|data[9]) - GyroOffset[1]
    Gyro[2]  = ((data[10]<<8)|data[11]) - GyroOffset[2]
    if Accel[0]>=32767:             #Solve the problem that Python shift will not overflow
      Accel[0]=Accel[0]-65535
    elif Accel[0]<=-32767:
      Accel[0]=Accel[0]+65535
    if Accel[1]>=32767:
      Accel[1]=Accel[1]-65535
    elif Accel[1]<=-32767:
      Accel[1]=Accel[1]+65535
    if Accel[2]>=32767:
      Accel[2]=Accel[2]-65535
    elif Accel[2]<=-32767:
      Accel[2]=Accel[2]+65535
    if Gyro[0]>=32767:
      Gyro[0]=Gyro[0]-65535
    elif Gyro[0]<=-32767:
      Gyro[0]=Gyro[0]+65535
    if Gyro[1]>=32767:
      Gyro[1]=Gyro[1]-65535
    elif Gyro[1]<=-32767:
      Gyro[1]=Gyro[1]+65535
    if Gyro[2]>=32767:
      Gyro[2]=Gyro[2]-65535
    elif Gyro[2]<=-32767:
      Gyro[2]=Gyro[2]+65535
  def icm20948MagRead(self):
    counter=20
    while(counter>0):
      time.sleep(0.01)
      self.icm20948ReadSecondary( I2C_ADD_ICM20948_AK09916|I2C_ADD_ICM20948_AK09916_READ , REG_ADD_MAG_ST2, 1)
      if ((pu8data[0] & 0x01)!= 0):
        break
      counter-=1
    if counter!=0:
      for i in range(0,8):
        self.icm20948ReadSecondary( I2C_ADD_ICM20948_AK09916|I2C_ADD_ICM20948_AK09916_READ , REG_ADD_MAG_DATA , MAG_DATA_LEN)
        U8tempX[i] = (pu8data[1]<<8)|pu8data[0]
        U8tempY[i] = (pu8data[3]<<8)|pu8data[2]
        U8tempZ[i] = (pu8data[5]<<8)|pu8data[4]
      Mag[0]=(U8tempX[0]+U8tempX[1]+U8tempX[2]+U8tempX[3]+U8tempX[4]+U8tempX[5]+U8tempX[6]+U8tempX[7])/8
      Mag[1]=-(U8tempY[0]+U8tempY[1]+U8tempY[2]+U8tempY[3]+U8tempY[4]+U8tempY[5]+U8tempY[6]+U8tempY[7])/8
      Mag[2]=-(U8tempZ[0]+U8tempZ[1]+U8tempZ[2]+U8tempZ[3]+U8tempZ[4]+U8tempZ[5]+U8tempZ[6]+U8tempZ[7])/8
    if Mag[0]>=32767:            #Solve the problem that Python shift will not overflow
      Mag[0]=Mag[0]-65535
    elif Mag[0]<=-32767:
      Mag[0]=Mag[0]+65535
    if Mag[1]>=32767:
      Mag[1]=Mag[1]-65535
    elif Mag[1]<=-32767:
      Mag[1]=Mag[1]+65535
    if Mag[2]>=32767:
      Mag[2]=Mag[2]-65535
    elif Mag[2]<=-32767:
      Mag[2]=Mag[2]+65535
  def icm20948ReadSecondary(self,u8I2CAddr,u8RegAddr,u8Len):
    u8Temp=0
    self._write_byte( REG_ADD_REG_BANK_SEL,  REG_VAL_REG_BANK_3) #swtich bank3
    self._write_byte( REG_ADD_I2C_SLV0_ADDR, u8I2CAddr)
    self._write_byte( REG_ADD_I2C_SLV0_REG,  u8RegAddr)
    self._write_byte( REG_ADD_I2C_SLV0_CTRL, REG_VAL_BIT_SLV0_EN|u8Len)

    self._write_byte( REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0) #swtich bank0
    
    u8Temp = self._read_byte(REG_ADD_USER_CTRL)
    u8Temp |= REG_VAL_BIT_I2C_MST_EN
    self._write_byte( REG_ADD_USER_CTRL, u8Temp)
    time.sleep(0.01)
    u8Temp &= ~REG_VAL_BIT_I2C_MST_EN
    self._write_byte( REG_ADD_USER_CTRL, u8Temp)
    
    for i in range(0,u8Len):
      pu8data[i]= self._read_byte( REG_ADD_EXT_SENS_DATA_00+i)

    self._write_byte( REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3) #swtich bank3
    
    u8Temp = self._read_byte(REG_ADD_I2C_SLV0_CTRL)
    u8Temp &= ~((REG_VAL_BIT_I2C_MST_EN)&(REG_VAL_BIT_MASK_LEN))
    self._write_byte( REG_ADD_I2C_SLV0_CTRL,  u8Temp)
    
    self._write_byte( REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0) #swtich bank0
  def icm20948WriteSecondary(self,u8I2CAddr,u8RegAddr,u8data):
    u8Temp=0
    self._write_byte( REG_ADD_REG_BANK_SEL,  REG_VAL_REG_BANK_3) #swtich bank3
    self._write_byte( REG_ADD_I2C_SLV1_ADDR, u8I2CAddr)
    self._write_byte( REG_ADD_I2C_SLV1_REG,  u8RegAddr)
    self._write_byte( REG_ADD_I2C_SLV1_DO,   u8data)
    self._write_byte( REG_ADD_I2C_SLV1_CTRL, REG_VAL_BIT_SLV0_EN|1)

    self._write_byte( REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0) #swtich bank0

    u8Temp = self._read_byte(REG_ADD_USER_CTRL)
    u8Temp |= REG_VAL_BIT_I2C_MST_EN
    self._write_byte( REG_ADD_USER_CTRL, u8Temp)
    time.sleep(0.01)
    u8Temp &= ~REG_VAL_BIT_I2C_MST_EN
    self._write_byte( REG_ADD_USER_CTRL, u8Temp)

    self._write_byte( REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3) #swtich bank3

    u8Temp = self._read_byte(REG_ADD_I2C_SLV0_CTRL)
    u8Temp &= ~((REG_VAL_BIT_I2C_MST_EN)&(REG_VAL_BIT_MASK_LEN))
    self._write_byte( REG_ADD_I2C_SLV0_CTRL,  u8Temp)

    self._write_byte( REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0) #swtich bank0
  def icm20948GyroOffset(self):
    s32TempGx = 0
    s32TempGy = 0
    s32TempGz = 0
    for i in range(0,32):
      self.icm20948_Gyro_Accel_Read()
      s32TempGx += Gyro[0]
      s32TempGy += Gyro[1]
      s32TempGz += Gyro[2]
      time.sleep(0.01)
    GyroOffset[0] = s32TempGx >> 5
    GyroOffset[1] = s32TempGy >> 5
    GyroOffset[2] = s32TempGz >> 5
  def _read_byte(self,cmd):
    rec=self._bus.readfrom_mem(int(self._address),int(cmd),1)
    return rec[0]
  def _read_block(self, reg, length=1):
    rec=self._bus.readfrom_mem(int(self._address),int(reg),length)
    return rec
  def _read_u16(self,cmd):
    LSB = self._bus.readfrom_mem(int(self._address),int(cmd),1)
    MSB = self._bus.readfrom_mem(int(self._address),int(cmd)+1,1)
    return (MSB[0] << 8) + LSB[0]

  def _write_byte(self,cmd,val):
    self._bus.writeto_mem(int(self._address),int(cmd),bytes([int(val)]))
    time.sleep(0.0001)
  def imuAHRSupdate(self,gx, gy,gz,ax,ay,az,mx,my,mz):    
    norm=0.0
    hx = hy = hz = bx = bz = 0.0
    vx = vy = vz = wx = wy = wz = 0.0
    exInt = eyInt = ezInt = 0.0
    ex=ey=ez=0.0 
    halfT = 0.024
    global q0
    global q1
    global q2
    global q3
    q0q0 = q0 * q0
    q0q1 = q0 * q1
    q0q2 = q0 * q2
    q0q3 = q0 * q3
    q1q1 = q1 * q1
    q1q2 = q1 * q2
    q1q3 = q1 * q3
    q2q2 = q2 * q2   
    q2q3 = q2 * q3
    q3q3 = q3 * q3          

    norm = float(1/math.sqrt(ax * ax + ay * ay + az * az))     
    ax = ax * norm
    ay = ay * norm
    az = az * norm

    norm = float(1/math.sqrt(mx * mx + my * my + mz * mz))      
    mx = mx * norm
    my = my * norm
    mz = mz * norm

    # compute reference direction of flux
    hx = 2 * mx * (0.5 - q2q2 - q3q3) + 2 * my * (q1q2 - q0q3) + 2 * mz * (q1q3 + q0q2)
    hy = 2 * mx * (q1q2 + q0q3) + 2 * my * (0.5 - q1q1 - q3q3) + 2 * mz * (q2q3 - q0q1)
    hz = 2 * mx * (q1q3 - q0q2) + 2 * my * (q2q3 + q0q1) + 2 * mz * (0.5 - q1q1 - q2q2)         
    bx = math.sqrt((hx * hx) + (hy * hy))
    bz = hz     

    # estimated direction of gravity and flux (v and w)
    vx = 2 * (q1q3 - q0q2)
    vy = 2 * (q0q1 + q2q3)
    vz = q0q0 - q1q1 - q2q2 + q3q3
    wx = 2 * bx * (0.5 - q2q2 - q3q3) + 2 * bz * (q1q3 - q0q2)
    wy = 2 * bx * (q1q2 - q0q3) + 2 * bz * (q0q1 + q2q3)
    wz = 2 * bx * (q0q2 + q1q3) + 2 * bz * (0.5 - q1q1 - q2q2)  

    # error is sum of cross product between reference direction of fields and direction measured by sensors
    ex = (ay * vz - az * vy) + (my * wz - mz * wy)
    ey = (az * vx - ax * vz) + (mz * wx - mx * wz)
    ez = (ax * vy - ay * vx) + (mx * wy - my * wx)

    if (ex != 0.0 and ey != 0.0 and ez != 0.0):
      exInt = exInt + ex * Ki * halfT
      eyInt = eyInt + ey * Ki * halfT  
      ezInt = ezInt + ez * Ki * halfT

      gx = gx + Kp * ex + exInt
      gy = gy + Kp * ey + eyInt
      gz = gz + Kp * ez + ezInt

    q0 = q0 + (-q1 * gx - q2 * gy - q3 * gz) * halfT
    q1 = q1 + (q0 * gx + q2 * gz - q3 * gy) * halfT
    q2 = q2 + (q0 * gy - q1 * gz + q3 * gx) * halfT
    q3 = q3 + (q0 * gz + q1 * gy - q2 * gx) * halfT  

    norm = float(1/math.sqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3))
    q0 = q0 * norm
    q1 = q1 * norm
    q2 = q2 * norm
    q3 = q3 * norm
  def icm20948Check(self):
    bRet=false
    if REG_VAL_WIA == self._read_byte(REG_ADD_WIA):
      bRet = true
    return bRet
  def icm20948MagCheck(self):
    self.icm20948ReadSecondary( I2C_ADD_ICM20948_AK09916|I2C_ADD_ICM20948_AK09916_READ,REG_ADD_MAG_WIA1, 2)
    if (pu8data[0] == REG_VAL_MAG_WIA1) and ( pu8data[1] == REG_VAL_MAG_WIA2) :
        bRet = true
        return bRet
  def icm20948CalAvgValue(self):
    MotionVal[0]=Gyro[0]/32.8
    MotionVal[1]=Gyro[1]/32.8
    MotionVal[2]=Gyro[2]/32.8
    MotionVal[3]=Accel[0]
    MotionVal[4]=Accel[1]
    MotionVal[5]=Accel[2]
    MotionVal[6]=Mag[0]
    MotionVal[7]=Mag[1]
    MotionVal[8]=Mag[2]
#▲ICM20948-Code▲

#▼Main-Code▼
if __name__ == '__main__':
    print("\nSense HAT Test Program ...\n")
    
    key1 = Pin(17,Pin.IN,Pin.PULL_DOWN)#Only this button,other not use.
    
    key1Flag=0
    
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch14()
    #color BRG
    #LCD.fill(LCD.white)
    #LCD.show()
    LCD.text("Wait Bluetooth Link...",45,60,LCD.green)
    LCD.hline(10,10,220,LCD.blue)
    LCD.hline(10,125,220,LCD.blue)
    LCD.vline(10,10,115,LCD.blue)
    LCD.vline(230,10,115,LCD.blue)
    LCD.show()
    
    
    MotionVal=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    icm20948=ICM20948()
    Pico_BLE_init()
    
    LCD.fill(0x000000)
    LCD.text("Linking...",80,60,LCD.green)
    LCD.hline(10,10,220,LCD.blue)
    LCD.hline(10,125,220,LCD.blue)
    LCD.vline(10,10,115,LCD.blue)
    LCD.vline(230,10,115,LCD.blue)
    LCD.show()
    
    time.sleep(2)
    
    LCD.fill(0x000000)
    LCD.text("Welcome~!!",80,60,LCD.green)
    LCD.hline(10,10,220,LCD.blue)
    LCD.hline(10,125,220,LCD.blue)
    LCD.vline(10,10,115,LCD.blue)
    LCD.vline(230,10,115,LCD.blue)
    LCD.show()
    
    time.sleep(2)
    
    LCD.fill(0x000000)
    LCD.text("-Gyro System-",75,60,LCD.green)
    LCD.hline(10,10,220,LCD.blue)
    LCD.hline(10,125,220,LCD.blue)
    LCD.vline(10,10,115,LCD.blue)
    LCD.vline(230,10,115,LCD.blue)
    LCD.show()

    
    
    while True:
        icm20948.icm20948_Gyro_Accel_Read()
        icm20948.icm20948MagRead()
        icm20948.icm20948CalAvgValue()
        time.sleep(0.1)
        icm20948.imuAHRSupdate(MotionVal[0] * 0.0175, MotionVal[1] * 0.0175,MotionVal[2] * 0.0175,MotionVal[3],MotionVal[4],MotionVal[5],MotionVal[6], MotionVal[7], MotionVal[8])
        pitch = math.asin(-2 * q1 * q3 + 2 * q0* q2)* 57.3
        roll  = math.atan2(2 * q2 * q3 + 2 * q0 * q1, -2 * q1 * q1 - 2 * q2* q2 + 1)* 57.3
        yaw   = math.atan2(-2 * q1 * q2 - 2 * q0 * q3, 2 * q2 * q2 + 2 * q3 * q3 - 1) * 57.3

        #print out
        #print("\r\n /-------------------------------------------------------------/ \r\n")
        #print('\r\n Roll = %.2f , Pitch = %.2f , Yaw = %.2f\r\n'%(roll,pitch,yaw))
        #print('\r\nAcceleration:  X = %d , Y = %d , Z = %d\r\n'%(Accel[0],Accel[1],Accel[2]))  
        #print('\r\nGyroscope:     X = %d , Y = %d , Z = %d\r\n'%(Gyro[0],Gyro[1],Gyro[2]))
        #print('\r\nMagnetic:      X = %d , Y = %d , Z = %d'%((Mag[0],Mag[1],Mag[2]))
        #print('%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f' % (pitch,roll,yaw,q0,q1,q2,q3))

        #BLE out
        uart.write('%.3f    %.3f    %.3f    %.3f    %.3f    %.3f    %.3f    %.3f    %.3f    %.3f    %.3f    %.3f    %.3f    %.3f    %.3f    %.3f\n' %
                   (MotionVal[3], MotionVal[4], MotionVal[5], MotionVal[0]* 0.0175,MotionVal[1]* 0.0175,MotionVal[2]* 0.0175,MotionVal[6], MotionVal[7], MotionVal[8],pitch,roll,yaw,q0,q1,q2,q3))

        if key1Flag==1:
            LCD.fill(0x000000)
            LCD.hline(10,10,220,LCD.blue)
            LCD.hline(10,125,220,LCD.blue)
            LCD.vline(10,10,115,LCD.blue)
            LCD.vline(230,10,115,LCD.blue)
            LCD.text(('AX=%d'%(Accel[0])),12,12,LCD.green)
            LCD.text(('AY=%d'%(Accel[1])),82,12,LCD.green)
            LCD.text(('AZ=%d'%(Accel[2])),152,12,LCD.green)
            LCD.text(('GX=%.2f'%(MotionVal[0]*0.0175)),12,26,LCD.red)
            LCD.text(('GY=%.2f'%(MotionVal[1]*0.0175)),82,26,LCD.red)
            LCD.text(('GZ=%.2f'%(MotionVal[2]*0.0175)),152,26,LCD.red)
            LCD.text(('MX=%d'%(MotionVal[6])),12,40,LCD.blue)
            LCD.text(('MY=%d'%(MotionVal[7])),82,40,LCD.blue)
            LCD.text(('MZ=%d'%(MotionVal[8])),152,40,LCD.blue)
        elif key1Flag==2:
            LCD.fill(0x000000)
            LCD.hline(10,10,220,LCD.blue)
            LCD.hline(10,125,220,LCD.blue)
            LCD.vline(10,10,115,LCD.blue)
            LCD.vline(230,10,115,LCD.blue)
            LCD.text(('Pitch=%.2f' % (pitch)),12,12,LCD.green)
            LCD.text(('roll=%.2f' % (roll)),12,26,LCD.green)
            LCD.text(('yaw=%.2f' % (yaw)),12,40,LCD.green)
        elif key1Flag==3:
            LCD.fill(0x000000)
            LCD.hline(10,10,220,LCD.blue)
            LCD.hline(10,125,220,LCD.blue)
            LCD.vline(10,10,115,LCD.blue)
            LCD.vline(230,10,115,LCD.blue)
            LCD.text(('Qw=%.2f' % (q0)),12,12,LCD.green)
            LCD.text(('Qx=%.2f' % (q1)),12,26,LCD.green)
            LCD.text(('Qy=%.2f' % (q2)),12,40,LCD.green)
            LCD.text(('Qz=%.2f' % (q3)),12,54,LCD.green)
        elif key1Flag==4:
            LCD.fill(0x000000)
            LCD.hline(10,10,220,LCD.blue)
            LCD.hline(10,125,220,LCD.blue)
            LCD.vline(10,10,115,LCD.blue)
            LCD.vline(230,10,115,LCD.blue)
            LCD.text("-Gyro System-",75,60,LCD.green)
            key1Flag=0
        
        if(key1.value() == 0):
            LCD.hline(10,10,220,LCD.white)
            LCD.hline(10,125,220,LCD.white)
            LCD.vline(10,10,115,LCD.white)
            LCD.vline(230,10,115,LCD.white)
            key1Flag=key1Flag+1
        LCD.show()
#▲Main-Code▲


