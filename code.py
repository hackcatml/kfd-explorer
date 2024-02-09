import platform

import frida
from PySide6 import QtCore
from PySide6.QtCore import QObject

MESSAGE = ""
ERRMESSAGE = ""


def clean_message():
    global MESSAGE
    MESSAGE = ''


class Instrument(QObject):
    attachsig = QtCore.Signal(int)

    def __init__(self, script_text, target):
        super().__init__()
        self.name = None
        self.sessions = []
        self.script = None
        self.script_text = script_text
        self.device = None
        self.device = frida.get_usb_device(1)
        self.attachtarget = target

    def __del__(self):
        for session in self.sessions:
            session.detach()

    def is_attached(self, attached: bool):
        self.attachsig.emit(1) if attached is True else self.attachsig.emit(0)

    def on_destroyed(self):
        self.attachsig.emit(0)

    # frida script에서 send 함수로 보내는 메시지는 on_message에서 처리됨
    def on_message(self, message, data):
        # print(message)
        global MESSAGE
        if 'payload' in message and message['payload'] is not None:
            MESSAGE = message['payload']
        if message['type'] == 'error':
            ERRMESSAGE = message['description']
            ERRMESSAGE += message['stack']
            print("[hackcatml] errmessage: ", ERRMESSAGE)

    def read_frida_js_source(self):
        # on Windows should open frida script with encoding option('cp949 issue')
        with open(self.script_text, 'r', encoding="UTF8") if platform.system() == 'Windows' \
                else open(self.script_text, "r") as f:
            return f.read()

    def instrument(self, caller):
        session = self.device.attach(self.attachtarget)
        self.name = self.attachtarget
        session.on('detached', self.is_attached)    # register is_attached callback func for a session's on detach event
        self.sessions.append(session)
        self.script = session.create_script(self.read_frida_js_source())
        self.script.on('message', self.on_message)
        self.script.on('destroyed', self.on_destroyed)
        self.script.load()
        self.is_attached(True)

    def get_agent(self):
        return self.script.exports_sync

    # just dummy func for checking script is destroyed or not
    def dummy_script(self):
        self.script.exports.dummy()
        return MESSAGE

    def arch(self):
        self.script.exports.arch()
        return MESSAGE

    def platform(self):
        self.script.exports.platform()
        return MESSAGE

    def list_modules(self):
        self.script.exports.listmodules()
        return MESSAGE

    def mem_enumerate_ranges(self, prot):
        enumranges = self.script.exports.enumerateranges(prot)
        return enumranges

    def get_kernel_slide(self):
        return self.script.exports.get_kernel_slide()

    def get_vm_kernel_link_addr(self):
        return self.script.exports.get_vm_kernel_link_addr()

    def get_kernel_base(self):
        return int(self.get_vm_kernel_link_addr()) + int(self.get_kernel_slide())

    def get_kern_version(self):
        return self.script.exports.get_kern_version()

    def get_offsets(self):
        clean_message()
        self.script.exports.get_offsets()
        return MESSAGE

    def get_kfd(self):
        clean_message()
        self.script.exports.get_kfd()
        return MESSAGE

    def get_all_proc(self, pid):
        return self.script.exports.get_all_proc(pid)

    def get_vnode_at_path(self, filePath):
        clean_message()
        self.script.exports.get_vnode_at_path(filePath)
        return MESSAGE

    def unsign_kptr(self, pac_kaddr):
        return self.script.exports.unsign_kptr(pac_kaddr)

    def read_kmem_offset(self, offset):
        if offset == "0x0":
            kaddr = self.get_kernel_base()
            self.script.exports.k_hex_dump(kaddr, None)
        else:
            kaddr = str(int(self.get_kernel_base()) + int(offset, 16))
            self.script.exports.k_hex_dump(kaddr, None)
        return MESSAGE

    def read_kmem_addr(self, kaddr, size):
        clean_message()
        self.script.exports.k_hex_dump(kaddr, size)
        return MESSAGE

    def write_kmem_addr(self, arg):
        for target in arg:
            targetAddr = target[0]
            targetPatchCode = target[1]
            self.script.exports.write_kmem_addr(targetAddr, targetPatchCode)

    def read_mem_addr(self, addr, size):
        clean_message()
        self.script.exports.hexdumpaddr(addr, size)
        return MESSAGE

    def write_mem_addr(self, arg):
        for target in arg:
            targetAddr = target[0]
            targetPatchCode = target[1]
            targetProt = target[3]
            self.script.exports.writememaddr(targetAddr, targetPatchCode, targetProt)


