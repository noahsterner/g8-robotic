import random

from bluezero import async_tools
from bluezero import peripheral
from bluezero import adapter

CPU_TMP_SRVC = '12341000-1234-1234-1234-123456789abc'
# https://www.bluetooth.com/specifications/assigned-numbers/
# Bluetooth SIG adopted UUID for Temperature characteristic

CPU_TMP_CHRC = '2A6E'
# Bluetooth SIG adopted UUID for Characteristic Presentation Format
CPU_FMT_DSCP = '2904'

def read_value():
    """
    Example read callback. Value returned needs to a list of bytes/integers
    in little endian format.

    This one does a mock reading CPU temperature callback.
    Return list of integer values.
    Bluetooth expects the values to be in little endian format and the
    temperature characteristic to be an sint16 (signed & 2 octets) and that
    is what dictates the values to be used in the int.to_bytes method call.

    :return: list of uint8 values
    """
    cpu_value = random.randrange(3200, 5310, 10) / 100
    return list(int(cpu_value * 100).to_bytes(2,
                                              byteorder='little', signed=True))


def update_value(characteristic):
    """
    Example of callback to send notifications

    :param characteristic:
    :return: boolean to indicate if timer should continue
    """
    # read/calculate new value.
    new_value = read_value()
    # Causes characteristic to be updated and send notification
    characteristic.set_value(new_value)
    # Return True to continue notifying. Return a False will stop notifications
    # Getting the value from the characteristic of if it is notifying
    return characteristic.is_notifying


def notify_callback(notifying, characteristic):
    """
    Noitificaton callback example. In this case used to start a timer event
    which calls the update callback ever 2 seconds

    :param notifying: boolean for start or stop of notifications
    :param characteristic: The python object for this characteristic
    """
    if notifying:
        async_tools.add_timer_seconds(2, update_value, characteristic)

adapter_address = list(adapter.Adapter.available())[0].address

periph = peripheral.Peripheral(adapter_address, local_name='MyRobot', appearance=1344)
periph.add_service(srv_id=1, uuid=CPU_TMP_SRVC, primary=True)


periph.publish() #start sendin packages
