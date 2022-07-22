import time
import serial


class TestController:
    AX_START = 255
    AX_WRITE_DATA = 3
    AX_ID = 3
    AX_MOVE_DATA_LENGTH = 5
    AX_CHANGE_ID_DATA_LENGTH = 4
    AX_CHANGE_BR_DATA_LENGTH = 4
    BR_AD = 4


    def __init__(self):
        self.port = serial.Serial()
        # self.port.baudrate = 1000000
        self.port.baudrate = 57600
        self.port.port = "COM6"
        self.port.xonxoff = False
        self.port.rtscts = False
        self.port.dsrdtr = False
        self.port.timeout = 0.5
        self.port.open()


    def setReg(self, id, reg, pos):
        p = [pos&0xFF, pos>>8]
        checksum = (~(id + TestController.AX_MOVE_DATA_LENGTH + TestController.AX_WRITE_DATA + reg + p[0] + p[1]))&0xFF
        outData = bytes([
            TestController.AX_START, TestController.AX_START, id,
            TestController.AX_MOVE_DATA_LENGTH, TestController.AX_WRITE_DATA,
            reg, p[0], p[1], checksum])
        self.port.write(outData)
        print(outData)


    def test_move(self, id):
        self.setReg(id, 30, 0)
        time.sleep(1)
        self.setReg(id, 30, 300)
        time.sleep(1)


    def change_id(self, curr_id, new_id):
        checksum = (~(curr_id + TestController.AX_CHANGE_ID_DATA_LENGTH \
                    + TestController.AX_WRITE_DATA + TestController.AX_ID + new_id))&0xFF

        outData = bytes([
            TestController.AX_START, TestController.AX_START, curr_id,
            TestController.AX_CHANGE_ID_DATA_LENGTH, TestController.AX_WRITE_DATA,
            TestController.AX_ID, new_id, checksum])
        self.port.write(outData)

    def changeBR(self, id, br):
        checksum = (~(id + TestController.AX_CHANGE_BR_DATA_LENGTH + TestController.AX_WRITE_DATA + TestController.BR_AD + br))&0xFF

        outData = bytes([
            TestController.AX_START, TestController.AX_START, id, TestController.AX_CHANGE_BR_DATA_LENGTH, TestController.AX_WRITE_DATA, TestController.BR_AD, br, checksum])

        self.port.write(outData)

def main():
    test_controller = TestController()
    # test_controller.changeBR(254, 34)
    test_controller.test_move(254)



if __name__ == '__main__' :
    main()
