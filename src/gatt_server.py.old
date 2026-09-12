from bluezero import peripheral #för Linux


SERVICE_UUID = "65231bdd-d17d-48c3-80fa-53d8be7efca6"
CHARACTERISTIC_UUID = "a58001d3-df0a-4b44-a828-bf9fedcf7e3b"

def data_received(value, options):
    message = bytes(value).decode("utf-8")
    print("Recived:", message)

#skapar BLE-enheten
ble_server = peripheral.Peripheral(
    adapter_address= None,
    local_name="MyApp"
)

#skapar GATT servicen
ble_server.add_service(
    srv_id=1,
    uuid=SERVICE_UUID,
    primary=True
)
ble_server.add_characteristic(
    srv_id=1,
    chr_id=1,
    uuid=CHARACTERISTIC_UUID,
    value=[],
    notifying=False,
    flags=["write"],
    write_callback=data_received,
)
print("Starting BLE GATT server...")
print("Device name: MyApp")
print("Service UUID:", SERVICE_UUID)
print("Characteristic UUID:", CHARACTERISTIC_UUID)

ble_server.publish()
