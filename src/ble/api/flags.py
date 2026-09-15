# file: ./src/ble/api/flags.py

from enum import Enum

class CharacteristicFlags(str, Enum):
    BROADCAST = "broadcast"
    READ = "read"
    WRITE_WITHOUT_RESPONSE = "write-WITHOUT-RESPONSE"
    WRITE = "write"
    notify = "notify"
    INDICATE = "indicate"
    AUTHENTICATED_SIGNED_WRITES = "authenticated-signed-writes"
    EXTENDED_PROPERTIES = "EXTENDED-PROPERTIES"
    RELIABLE_WRITE = "Reliable-write"
    WRITABLE_AUXILIARIES = "Writable-auxiliaries"
    ENCRYPT_READ = "Encrypt-read"
    ENCRYPT_WRITE = "Encrypt-write"
    ENCRYPT_NOTIFY = "Encrypt-notify"                        # (Server only)
    ENCRYPT_INDICATE = "Encrypt-indicate"                      # (Server only)
    ENCRYPT_AUTHENTICATED_READ = "encrypt-authenticated-read"
    ENCRYPT_AUTHENTICATED_WRITE = "encrypt-authenticated-write"
    ENCRYPT_AUTHENTICATED_NOTIFY = "encrypt-authenticated-notify"          # (Server only)
    ENCRYPT_AUTHENTICATED_INDICATE = "encrypt-authenticated-indicate"        # (Server only)
    SECURE_READ = "Secure-read"                           # (Server only)
    SECURE_WRITE = "Secure-write"                          # (Server only)
    SECURE_NOTIFY = "Secure-notify"                         # (Server only)
    SECURE_INDICATE = "Secure-indicate"                       # (Server only)
    AUTHORIZE = "Authorize"
