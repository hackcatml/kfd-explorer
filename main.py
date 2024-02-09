import collections
import inspect
import platform
import re

from PySide6 import QtGui
from PySide6.QtCore import QThread, Slot, Qt, QEvent, QPoint
from PySide6.QtGui import QPixmap, QTextCursor, QShortcut, QKeySequence, QIcon, QPalette
from PySide6.QtWidgets import QLabel, QMainWindow, QMessageBox, QApplication

import code
import globvar
import ui
from disasm import DisassembleWorker
from history import HistoryViewClass


def set_mem_range(prot):
    try:
        result = globvar.fridaInstrument.mem_enumerate_ranges(prot)
        # print("[hackcatml] mem_enumerate_ranges result: ", result)
    except Exception as e:
        print(e)
        return
    # enumerateRanges --> [(base, base + size - 1, prot, size), ... ]
    globvar.enumerateRanges.clear()
    for i in range(len(result)):
        globvar.enumerateRanges.append(
            (result[i]['base'], hex(int(result[i]['base'], 16) + result[i]['size'] - 1), result[i]['protection'],
             result[i]['size']))
    # print("[hackcatml] globvar.enumerateRanges: ", globvar.enumerateRanges)


def hex_calculator(s):
    """ https://leetcode.com/problems/basic-calculator-ii/solutions/658480/Python-Basic-Calculator-I-II-III-easy
    -solution-detailed-explanation/comments/881191/"""

    def twos_complement(input_value: int, num_bits: int) -> int:
        mask = 2 ** num_bits - 1
        return ((input_value ^ mask) + 1) & mask

    def replace(match):
        num = int(match.group(0), 16)
        return "- " + hex(twos_complement(num, 64))

    # multiply, divide op are not supported
    if re.search(r"[*/]", s):
        return False

    # find negative hex value which starts with ffffffff and replace it with "- 2's complement"
    pattern = re.compile(r'[fF]{8}\w*')
    s = pattern.sub(replace, s)
    s = s.replace('0x', '')

    num, op, arr, stack = '', "+", collections.deque(s + "+"), []
    while sym := arr.popleft() if arr else None:
        if str.isdigit(sym):
            num += sym
        elif re.search(r"[a-zA-F]", sym):
            num += sym
        elif sym in ('+', '-'):
            if num == '':
                num = '0'
            stack += int(op + num, 16),
            op, num = sym, ''

    return hex(sum(stack))


def process_read_kmem_result(result: str) -> str:
    remove_target = '0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF\n'
    result = result.replace(result[result.find('\n') + 1:result.find(remove_target)], '')
    result = result.replace(remove_target, '')
    # remove any residual whitespace
    result = result.strip()
    return result


class WindowClass(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.statusBar()
        self.statusLight = QLabel()
        self.set_status_light()

        self.hexEditShortcut = QShortcut(QKeySequence(Qt.Key.Key_F2), self)

        self.hexViewer.wheelupsig.connect(self.wheelupsig_func)
        self.hexViewer.movesig.connect(self.movesig_func)
        self.hexViewer.refreshsig.connect(self.refreshsig_func)
        self.hexViewer.statusBar = self.statusBar()
        self.defaultcolor = QLabel().palette().color(QPalette.ColorRole.WindowText)

        self.attachtargetname = None    # name to attach. need to provide on the AppList widget
        self.attachedname = None    # main module name after frida attached successfully
        self.refreshCurrentAddressShortcut = QShortcut(QKeySequence(Qt.Key.Key_F3), self)
        self.refreshCurrentAddressShortcut.activated.connect(self.refresh_curr_addr)

        self.attachBtn.clicked.connect(lambda: self.attach_frida("attachBtnClicked"))
        self.detachBtn.clicked.connect(self.detach_frida)
        self.offsetInput.returnPressed.connect(lambda: self.offset_ok_btn_pressed_func("returnPressed"))
        self.offsetOkbtn.pressed.connect(lambda: self.offset_ok_btn_pressed_func("pressed"))
        self.offsetOkbtn.clicked.connect(self.offset_ok_btn_func)

        self.addrInput.returnPressed.connect(lambda: self.addr_btn_pressed_func("returnPressed"))
        self.addrBtn.pressed.connect(lambda: self.addr_btn_pressed_func("pressed"))
        self.addrBtn.clicked.connect(self.addr_btn_func)
        self.tabWidget2.tabBarClicked.connect(self.status_tab_bar_click_func)

        self.hexEditBtn.clicked.connect(self.hex_edit)
        self.hexEditDoneBtn.clicked.connect(self.hex_edit)
        self.hexEditShortcut.activated.connect(self.hex_edit)

        self.refreshBtn.clicked.connect(self.refresh_curr_addr)
        self.moveBackwardBtn.clicked.connect(self.move_backward)
        self.moveForwardBtn.clicked.connect(self.move_forward)

        self.offsetFilter.textChanged.connect(lambda: self.search_offset("offsetFilter"))

        self.disasm_thread = QThread()
        self.disasm_worker = DisassembleWorker()
        self.disasm_worker.hexviewer = self.hexViewer
        self.disasm_worker.hexviewer.wheelsig.connect(self.disasm_worker.hexviewer_wheelsig_func)
        self.disasm_worker.hexviewer.scrollsig.connect(self.disasm_worker.hexviewer_scrollsig_func)
        self.disasm_worker.moveToThread(self.disasm_thread)
        self.disasm_thread.start()
        self.disassemBtnClickedCount = 0
        self.disassemBtn.clicked.connect(self.show_disassemble_result)

        self.history_view = HistoryViewClass()
        self.history_view.historyaddrsig.connect(self.history_addr_sig_func)
        self.historyBtn.clicked.connect(self.show_history)
        self.historyBtnClickedCount = 0

        self.kslide = None
        self.kbase = None
        self.kernversion = None

        self.utilViewer.get_kfd_btn = self.getKfdBtn
        self.utilViewer.get_kfd_btn.clicked.connect(self.utilViewer.get_kfd)

        self.utilViewer.get_pid_list_btn = self.getPidListBtn
        self.utilViewer.get_pid_list_btn.clicked.connect(self.utilViewer.get_pid_list)

        self.utilViewer.get_all_proc_btn = self.getAllProcBtn
        self.utilViewer.get_all_proc_btn.clicked.connect(self.utilViewer.get_all_proc)

        self.utilViewer.get_vnode_at_path_btn = self.getVnodeAtPathBtn
        self.utilViewer.get_vnode_at_path_input = self.getVnodeAtPathInput
        self.utilViewer.get_vnode_at_path_input.returnPressed.connect(self.utilViewer.get_vnode_at_path)
        self.utilViewer.get_vnode_at_path_btn.clicked.connect(self.utilViewer.get_vnode_at_path)

        self.utilViewer.util_viewer_filter = self.utilViewerFilter
        self.utilViewer.util_viewer_filter.textChanged.connect(self.utilViewer.util_viewer_filter_func)

        # install event filter to use tab and move to some input fields
        self.interested_widgets = []
        QApplication.instance().installEventFilter(self)

    @Slot(str)
    def wheelupsig_func(self, wheelupsig: str):
        # print(wheelupsig)
        if self.status_kernel_base.toPlainText() == hex_calculator(f"{wheelupsig}"):
            return
        addr = hex_calculator(f"{wheelupsig} - 10")
        # print(addr)
        self.addrInput.setText(addr)
        self.addr_btn_func()

    @Slot(int)
    def movesig_func(self, movesig: int):
        self.move_backward() if movesig == 0 else self.move_forward()

    @Slot(int)
    def refreshsig_func(self, refreshsig: int):
        if refreshsig:
            self.refresh_curr_addr()

    @Slot(int)
    def fridaattachsig_func(self, attach_sig: int):
        if attach_sig:
            globvar.isFridaAttached = True
        else:
            globvar.isFridaAttached = False
            self.detach_frida()
        self.set_status_light()

    @Slot(str)
    def history_addr_sig_func(self, addr: str):
        self.addrInput.setText(addr)
        self.addr_btn_func()

    def adjust_label_pos(self):
        tc = self.hexViewer.textCursor()
        text_length = len(tc.block().text())
        current_height = self.height()
        self.resize(text_length * 13, current_height)
        if text_length >= 77:
            self.label_3.setIndent(28 + (text_length - 77) * 8)
        else:
            self.label_3.setIndent(28 - (77 - text_length) * 7)

    def attach_frida(self, caller: str):
        if globvar.isFridaAttached is True:
            try:
                # check if script is still alive. if not exception will occur
                globvar.fridaInstrument.dummy_script()
                QMessageBox.information(self, "info", "Already attached")
            except Exception as e:
                self.statusBar().showMessage(f"{inspect.currentframe().f_code.co_name}: {e}", 3000)
                globvar.fridaInstrument.sessions.clear()
            return

        try:
            self.attachtargetname = "Gadget"
            globvar.fridaInstrument = code.Instrument("scripts/default.js",
                                                      self.attachtargetname)
            # connect frida attach signal function
            globvar.fridaInstrument.attachsig.connect(self.fridaattachsig_func)
            msg = globvar.fridaInstrument.instrument(caller)
        except Exception as e:
            self.statusBar().showMessage(f"{inspect.currentframe().f_code.co_name}: {e}", 3000)
            return

        if msg is not None:
            QMessageBox.information(self, "info", msg)
            self.offsetInput.clear()
            return

        set_mem_range('r--')

        try:
            self.platform = globvar.fridaInstrument.platform()
            self.utilViewer.platform = self.platform
            globvar.arch = globvar.fridaInstrument.arch()
            name = globvar.fridaInstrument.list_modules()[0]['name']
            self.attachedname = name
            self.set_status()
        except Exception as e:
            print(e)
            return

    def detach_frida(self):
        if globvar.fridaInstrument is None:
            pass
        else:
            try:
                for session in globvar.fridaInstrument.sessions:
                    session.detach()
                globvar.fridaInstrument.sessions.clear()
                globvar.enumerateRanges.clear()
                globvar.hexEdited.clear()
                globvar.offsets.clear()
                globvar.arch = None
                globvar.isFridaAttached = False
                globvar.fridaInstrument = None
                globvar.visitedAddress.clear()
                if self.history_view is not None:
                    self.history_view.history_window.close()
                    self.history_view.clear_table()
                self.statusBar().showMessage("")
            except Exception as e:
                self.statusBar().showMessage(f"{inspect.currentframe().f_code.co_name}: {e}", 5000)

    def offset_ok_btn_pressed_func(self, caller):
        if caller == "returnPressed":
            self.offset_ok_btn_func()

    def offset_ok_btn_func(self):
        if globvar.isFridaAttached is False:
            QMessageBox.information(self, "info", "Attach first")
            self.offsetInput.clear()
            return

        offset = self.offsetInput.text()
        try:
            offset = hex_calculator(offset)
        except Exception as e:
            self.statusBar().showMessage(f"{inspect.currentframe().f_code.co_name}: {e}", 3000)
            return

        if offset is False:
            self.statusBar().showMessage("can't operate *, /", 3000)
            return

        self.offsetInput.setText(offset)

        try:
            result = globvar.fridaInstrument.read_kmem_offset(offset)
        except Exception as e:
            self.statusBar().showMessage(f"{inspect.currentframe().f_code.co_name}: {e}", 3000)
            if str(e) == globvar.errorType1:
                globvar.fridaInstrument.sessions.clear()
            return

        self.show_mem_result_on_viewer(None, result)

    def addr_btn_pressed_func(self, caller):
        if caller == "returnPressed":
            self.addr_btn_func()

    def addr_btn_func(self):
        if globvar.isFridaAttached is False:
            QMessageBox.information(self, "info", "Attach first")
            self.addrInput.clear()
            return

        addr = self.addrInput.text()
        if addr.strip() == '':
            return
        hex_regex = re.compile(r'(\b0x[a-fA-F0-9]+\b|\b[a-fA-F0-9]{6,}\b)')
        match = hex_regex.match(addr)
        # in case it's not a hex expression on addrInput field. for example "fopen", "sysctl", ...
        if match is None:
            self.statusBar().showMessage(f"Cannot find address for {addr}", 3000)
            return

        try:
            addr = hex_calculator(addr)
        except Exception as e:
            self.statusBar().showMessage(f"{inspect.currentframe().f_code.co_name}: {e}", 3000)
            return

        if addr is False:
            self.statusBar().showMessage("Can't operate *, /")
            return

        self.addrInput.setText(addr)
        # print(f"addr_btn_func: {int(addr, 16)}")
        # return

        try:
            if re.search(r"0x0*[fF]{6,}", addr):
                result = globvar.fridaInstrument.read_kmem_addr(addr, None)
            else:
                result = globvar.fridaInstrument.read_mem_addr(addr, 0x640)
        except Exception as e:
            self.statusBar().showMessage(f"{inspect.currentframe().f_code.co_name}: {e}", 3000)
            if str(e) == globvar.errorType1:
                globvar.fridaInstrument.sessions.clear()
            return

        self.show_mem_result_on_viewer(addr, result)

    def show_mem_result_on_viewer(self, addr, result):
        # empty changed hex list before refresh hexviewer
        globvar.hexEdited.clear()
        # show hex dump result
        hex_dump_result = result[result.find('\n') + 1:]
        self.hexViewer.setPlainText(hex_dump_result)
        # adjust label pos
        self.adjust_label_pos()

        if inspect.currentframe().f_back.f_code.co_name != "offset_ok_btn_func":
            self.set_status()
            # reset address input area
            self.addrInput.clear()
        else:
            self.set_status()
            # reset offset input area
            self.offsetInput.clear()

        # move cursor
        if self.hexViewer.textCursor().positionInBlock() == 0:
            self.hexViewer.moveCursor(QTextCursor.MoveOperation.NextWord)
        # set initial currentFrameStartAddress
        globvar.currentFrameBlockNumber = 0
        globvar.currentFrameStartAddress = "".join(
            ("0x", self.hexViewer.textCursor().block().text()[:self.hexViewer.textCursor().block().text().find(' ')]))
        # print("[hackcatml] currentFrameBlockNumber: ", globvar.currentFrameBlockNumber)
        # print("[hackcatml] currentFrameStartAddress: ", globvar.currentFrameStartAddress)
        self.visited_addr()

        self.disasm_worker.disassemble(globvar.arch, globvar.currentFrameStartAddress, hex_dump_result)

    # remember visited address
    def visited_addr(self):
        if len(inspect.stack()) > 3 and inspect.stack()[3].function == 'wheelupsig_func':
            return

        kaddr = self.status_current_kaddr.toPlainText()
        addr = self.status_current_addr.toPlainText()
        curr_addr = ""
        if kaddr != "" and addr == "":
            curr_addr = kaddr
        elif kaddr == "" and addr != "":
            curr_addr = addr
        match = re.search(r'\(0x[a-fA-F0-9]+\)', curr_addr)
        visited_addr = curr_addr[:match.start()] if match is not None else curr_addr
        if visited_addr != '':
            if len(globvar.visitedAddress) == 0:
                globvar.visitedAddress.append(['last', visited_addr])
            else:
                last_visit_index = None
                for item in globvar.visitedAddress:
                    if item[0] == 'last':
                        last_visit_index = globvar.visitedAddress.index(item)
                if not any(sublist[1] == visited_addr for sublist in globvar.visitedAddress):
                    globvar.visitedAddress.append(['last', visited_addr])
                    if last_visit_index is not None:
                        globvar.visitedAddress[last_visit_index][0] = 'notlast'
                else:
                    revisit_index = None
                    # Find the index of the sublist to modify
                    for idx, sublist in enumerate(globvar.visitedAddress):
                        if sublist[1] == visited_addr and sublist[0] == 'notlast':
                            revisit_index = idx
                            break
                    # Modify the sublist if we found a matching index
                    if revisit_index is not None and (inspect.stack()[3].function != 'move_forward' and inspect.stack()[3].function != 'move_backward'):
                        revisit_addr_mark = globvar.visitedAddress[revisit_index][0]
                        revisit_addr = globvar.visitedAddress[revisit_index][1]
                        globvar.visitedAddress.remove([revisit_addr_mark, revisit_addr])
                        globvar.visitedAddress.append(['last', revisit_addr])
                        for idx, sublist in enumerate(globvar.visitedAddress):
                            if sublist[1] != revisit_addr and sublist[0] == 'last':
                                globvar.visitedAddress[idx][0] = 'notlast'
                                break
                    elif revisit_index is not None and (inspect.stack()[3].function == 'move_forward' or inspect.stack()[3].function == 'move_backward'):
                        globvar.visitedAddress[revisit_index][0] = 'last'
                        if revisit_index != last_visit_index:
                            globvar.visitedAddress[last_visit_index][0] = 'notlast'
            # add visted_addr to the history table
            self.history_view.add_row(visited_addr)

    def show_disassemble_result(self):
        self.disassemBtnClickedCount += 1
        self.disasm_worker.disasm_window.show()
        if self.disassemBtnClickedCount == 1:
            curr_pos = self.disasm_worker.disasm_window.pos()
            new_pos = curr_pos + QPoint(-270, 150)
            self.disasm_worker.disasm_window.move(new_pos)

    def show_history(self):
        self.historyBtnClickedCount += 1
        self.history_view.history_window.show()
        if self.historyBtnClickedCount == 1:
            curr_pos = self.history_view.history_window.pos()
            new_pos = (curr_pos + QPoint(480, -350)) if platform.system() == "Darwin" else (curr_pos + QPoint(490, -360))
            self.history_view.history_window.move(new_pos)

    def status_tab_bar_click_func(self, index):
        # status tab
        if index == 0:
            try:
                if globvar.fridaInstrument is not None:
                    globvar.fridaInstrument.dummy_script()
            except Exception as e:
                if str(e) == globvar.errorType1:
                    globvar.fridaInstrument.sessions.clear()
                self.statusBar().showMessage(f"{inspect.currentframe().f_code.co_name}: {e}", 3000)
                return
        # offsets tab
        elif index == 1:
            text = ""
            result = []
            self.offsetFilter.setText('')
            if globvar.fridaInstrument is not None:
                try:
                    result = globvar.fridaInstrument.get_offsets()
                    globvar.offsets = result
                except Exception as e:
                    if str(e) == globvar.errorType1:
                        globvar.fridaInstrument.sessions.clear()
                    self.statusBar().showMessage(f"{inspect.currentframe().f_code.co_name}: {e}", 3000)
                    return
            if len(result) > 0:
                for key in result:
                    text += f"{key}\t{hex(int(result[key]))}\n"
            self.offsetsViewer.setTextColor(self.defaultcolor)
            self.offsetsViewer.setPlainText(text)

    def hex_edit(self):
        if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Util":
            return
        # print(self.sender().__class__.__name__)
        if self.sender().__class__.__name__ == "QShortcut" or \
                (self.sender().__class__.__name__ != "QShortcut" and self.sender().text() == "Done"):
            if globvar.isHexEditMode is True:
                self.hexViewer.setReadOnly(True)
                if len(globvar.hexEdited) == 0:
                    globvar.isHexEditMode = False
                    return
                elif len(globvar.hexEdited) >= 1:
                    try:
                        globvar.fridaInstrument.write_kmem_addr(globvar.hexEdited)
                    except Exception as e:
                        if str(e) == globvar.errorType1:
                            globvar.fridaInstrument.sessions.clear()
                            globvar.hexEdited.clear()
                        self.statusBar().showMessage(f"{inspect.currentframe().f_code.co_name}: {e}", 3000)
                        return
                print("[hackcatml] hex edited: ", globvar.hexEdited)

                # refresh hex viewer after patching
                tc = self.hexViewer.textCursor()
                finalposlist = []
                for arr in globvar.hexEdited:
                    origpos = arr[4]
                    tc.setPosition(origpos, QTextCursor.MoveMode.MoveAnchor)
                    tc.movePosition(QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.MoveAnchor)
                    if tc.position() not in finalposlist:
                        finalposlist.append(tc.position())

                for finalpos in finalposlist:
                    tc.setPosition(finalpos, QTextCursor.MoveMode.MoveAnchor)
                    # read mem addr after patching
                    result = globvar.fridaInstrument.read_kmem_addr(
                        "".join(("0x", tc.block().text()[:tc.block().text().find(' ')])), 16)
                    # process read mem result
                    result = process_read_kmem_result(result)
                    # replace text
                    tc.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
                    tc.insertText(result)

                self.hexViewer.moveCursor(QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.MoveAnchor)
                self.hexViewer.moveCursor(QTextCursor.MoveOperation.NextWord, QTextCursor.MoveMode.MoveAnchor)
                globvar.isHexEditMode = False
                # empty changed hex list
                globvar.hexEdited.clear()
                # reset current frame block number
                # globvar.currentFrameBlockNumber = 0
                return

        if self.sender().__class__.__name__ == "QShortcut" or (
                self.sender().__class__.__name__ != "QShortcut" and self.sender().text() == "kwrite"):
            if globvar.isHexEditMode is False:
                self.hexViewer.setReadOnly(False)
                self.hexViewer.setTextInteractionFlags(
                    ~Qt.TextInteractionFlag.TextSelectableByKeyboard & ~Qt.TextInteractionFlag.TextSelectableByMouse)
                globvar.isHexEditMode = True

    def refresh_curr_addr(self):
        kaddr = self.status_current_kaddr.toPlainText()
        addr = self.status_current_addr.toPlainText()
        curr_addr = kaddr if kaddr != '' else addr
        if curr_addr == '':
            return
        else:
            match = re.search(r'\(0x[a-fA-F0-9]+\)', curr_addr)
            curr_addr = curr_addr[:match.start()] if match is not None else curr_addr
            self.addrInput.setText(curr_addr)
            self.addr_btn_func()

    def move_backward(self):
        tc = self.hexViewer.textCursor()
        indices = [i for i, x in enumerate(tc.block().text()) if x == " "]
        if len(indices) == 0:
            return
        elif re.search(r"\d+\. 0x[a-f0-9]+, module:", tc.block().text()):
            return

        if len(globvar.visitedAddress) > 0:
            for idx, sublist in enumerate(globvar.visitedAddress):
                if sublist[0] == 'last' and idx > 0:
                    addr_to_visit = globvar.visitedAddress[idx - 1][1]
                    self.addrInput.setText(addr_to_visit)
                    self.addr_btn_func()
                    break

    def move_forward(self):
        tc = self.hexViewer.textCursor()
        indices = [i for i, x in enumerate(tc.block().text()) if x == " "]
        if len(indices) == 0:
            return
        elif re.search(r"\d+\. 0x[a-f0-9]+, module:", tc.block().text()):
            return

        if len(globvar.visitedAddress) > 0:
            for idx, sublist in enumerate(globvar.visitedAddress):
                if sublist[0] == 'last' and idx < len(globvar.visitedAddress) - 1:
                    addr_to_visit = globvar.visitedAddress[idx + 1][1]
                    self.addrInput.setText(addr_to_visit)
                    self.addr_btn_func()
                    break

    def search_offset(self, caller):
        # print(self.offsetFilter.text())
        text_to_find = ''
        viewer = None
        if caller == "offsetFilter":
            text_to_find = self.offsetFilter.text().lower()
            viewer = self.offsetsViewer

        matched = ''
        if len(globvar.offsets) > 0:
            for offset in globvar.offsets:
                if offset.lower().find(text_to_find) != -1:
                    matched += f"{offset}\t{hex(int(globvar.offsets[offset]))}\n"
        viewer.setText(matched)

    def set_status(self):
        # print(inspect.currentframe().f_back.f_code.co_name)
        # print(inspect.stack()[0][3] + ':', name)
        if self.kernversion is None:
            self.kernversion = globvar.fridaInstrument.get_kern_version()
        if self.kslide is None:
            self.kslide = globvar.fridaInstrument.get_kernel_slide()
        if self.kbase is None:
            self.kbase = globvar.fridaInstrument.get_kernel_base()

        self.status_kernel_version.setPlainText(self.kernversion)
        self.status_kernel_base.setPlainText(hex(int(self.kbase)))
        self.status_kernel_slide.setPlainText(hex(int(self.kslide)))

        input = self.offsetInput.text()
        if inspect.stack()[2].function == "addr_btn_func":
            input = self.addrInput.text()

        if input.startswith('0x') is False:
            input = "".join(("0x0", input))

        try:
            if inspect.stack()[2].function == "offset_ok_btn_func":
                addr = hex(int(self.kbase) + int(input, 16))
                current_addr = addr + f"({input})"
                self.status_current_kaddr.setPlainText(current_addr)
                self.status_current_addr.setPlainText("")
            elif inspect.stack()[2].function == "addr_btn_func" and re.search(r"0x0*[fF]{6,}", input):
                addr = input
                if int(addr, 16) >= int(self.kbase):
                    current_addr = addr + f"({hex(int(input, 16) - int(self.kbase))})"
                else:
                    current_addr = addr
                self.status_current_kaddr.setPlainText(current_addr)
                self.status_current_addr.setPlainText("")
            elif inspect.stack()[2].function == "addr_btn_func" and not re.search(r"0x0*[fF]{6,}", input):
                current_addr = input
                self.status_current_kaddr.setPlainText("")
                self.status_current_addr.setPlainText(current_addr)
            # caller function 찾기. https://stackoverflow.com/questions/900392/getting-the-caller-function-name-inside-another-function-in-python
            elif inspect.currentframe().f_back.f_code.co_name == "attach_frida":
                self.offsetInput.clear()
                self.addrInput.clear()
        except Exception as e:
            print(e)
            pass

    def set_status_light(self):
        onicon = QPixmap("icon/greenlight.png").scaledToHeight(13)
        officon = QPixmap("icon/redlight.png").scaledToHeight(13)

        self.statusLight.setPixmap(officon)
        if globvar.isFridaAttached is True:
            self.statusLight.setPixmap(onicon)

        self.statusBar().removeWidget(self.statusLight)
        self.statusBar().addPermanentWidget(self.statusLight)
        self.statusLight.show()

    def eventFilter(self, obj, event):
        self.interested_widgets = [self.offsetInput, self.addrInput]
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Tab:
            try:
                if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "Util":
                    self.interested_widgets = [self.getVnodeAtPathInput, self.utilViewerFilter]
                # Get the index of the currently focused widget in our list
                index = self.interested_widgets.index(self.focusWidget())

                # Try to focus the next widget in the list
                self.interested_widgets[(index + 1) % len(self.interested_widgets)].setFocus()
            except ValueError:
                # The currently focused widget is not in our list, so we focus the first one
                self.interested_widgets[0].setFocus()

            # We've handled the event ourselves, so we don't pass it on
            return True

        # For other events, we let them be handled normally
        return super().eventFilter(obj, event)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.disasm_worker is not None:
            self.disasm_worker.disasm_window.close()
            self.disasm_worker.thread().quit()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon/kfd-explorer.png'))
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec())
