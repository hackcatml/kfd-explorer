import inspect
import re

from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QAction, QCursor
from PySide6.QtWidgets import QTextEdit, QApplication, QWidget, QVBoxLayout

import globvar


class HexViewerClass(QTextEdit):
    wheelupsig = QtCore.Signal(str)
    wheelsig = QtCore.Signal(str)
    scrollsig = QtCore.Signal(int)
    movesig = QtCore.Signal(int)
    refreshsig = QtCore.Signal(int)

    def __init__(self, args):
        super(HexViewerClass, self).__init__(args)
        self.hitcount = 0
        self.verticalScrollBar().sliderMoved.connect(self.setScrollBarPos)
        self.statusBar = None
        self.result_widget = ResultWidget()
        # hexviewer text changed event
        self.textChanged.connect(self.text_changed_event)

    def setScrollBarPos(self, value):
        # print("[hackcatml] slidermoved: ", value)
        self.scrollsig.emit(value)
        globvar.currentFrameBlockNumber = round(value / 15)

    # wheelevent https://spec.tistory.com/449
    def wheelEvent(self, e: QtGui.QWheelEvent) -> None:
        delta = e.angleDelta().y()
        # wheel down
        if delta < 0:
            globvar.currentFrameBlockNumber += -1 * delta / 120 * 4
        # wheel up
        elif delta > 0 and globvar.currentFrameBlockNumber > 0:
            globvar.currentFrameBlockNumber -= delta / 120 * 4

        tc = self.textCursor()
        tc.movePosition(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor, 1)
        tc.movePosition(QTextCursor.MoveOperation.Down, QTextCursor.MoveMode.MoveAnchor, int(globvar.currentFrameBlockNumber))
        globvar.currentFrameStartAddress = "".join(("0x", tc.block().text()[:tc.block().text().find(' ')]))

        if tc.blockNumber() == 0 and re.search(r"\d+\. 0x[0-9a-f]+, module:", tc.block().text()) is None:
            self.hitcount += 1
            if self.hitcount > 0 and delta > 0:
                self.wheelupsig.emit(globvar.currentFrameStartAddress)
                self.hitcount = 0
        elif re.search(r"\d+\. 0x[0-9a-f]+, module:", tc.block().text()) is None:
            self.wheelsig.emit(globvar.currentFrameStartAddress)
        # print("[hackcatml] globvar.currentFrameBlockNumber: ", globvar.currentFrameBlockNumber)
        # print("[hackcatml] tc.blockNumber(): ", tc.blockNumber())
        # print("[hackcatml] tc.block().text(): ", tc.block().text())
        # print("[hackcatml] globvar.currentFrameStartAddress: ", globvar.currentFrameStartAddress)

        return super(HexViewerClass, self).wheelEvent(e)

    def keyReleaseEvent(self, e: QtGui.QKeyEvent) -> None:
        # if key is hexedit shortcut key then just return. if not hexeditor behavior is weird
        if e.key() == Qt.Key.Key_F2:
            return

        tc = self.textCursor()
        tcx = tc.positionInBlock()
        # print("keyrelease pos: ", tcx)
        indices = [i for i, x in enumerate(tc.block().text()) if x == " "]
        if len(indices) == 0:
            return
        if tcx in range(indices[1]):
            return

        # change color on edited hex as black -> red
        if self.isReadOnly() is False:
            self.moveCursor(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor)
            self.setTextColor(QtGui.QColor("Red"))
            self.moveCursor(QTextCursor.MoveOperation.Right)

        if tcx in range(indices[2], indices[len(indices) - 2] + 3, 3) and e.key() != Qt.Key.Key_Left:
            if tcx == indices[len(indices) - 2]:
                self.moveCursor(QTextCursor.MoveOperation.Down)
                self.moveCursor(QTextCursor.MoveOperation.StartOfLine)
                self.moveCursor(QTextCursor.MoveOperation.NextWord)
                return
            self.moveCursor(QTextCursor.MoveOperation.Right)
            return

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        tc = self.textCursor()
        tcx = tc.positionInBlock()
        tcy = tc.anchor()
        # print("keypress pos: ", tcx, tcy)

        # backspace, delete, enter, left key and space is not allowed
        if e.key() in (
                QtCore.Qt.Key.Key_Backspace, QtCore.Qt.Key.Key_Delete, QtCore.Qt.Key.Key_Return, Qt.Key.Key_Left, Qt.Key.Key_Space
        ): return

        # hexedit 모드에서 ctrl + a, cmd + a (select all), ctrl + v, cmd + v (paste) is not allowed
        # if self.isReadOnly() is False:
        if (e.keyCombination().keyboardModifiers() == QtCore.Qt.KeyboardModifier.MetaModifier or e.keyCombination().keyboardModifiers() == QtCore.Qt.KeyboardModifier.ControlModifier) and e.key() == QtCore.Qt.Key.Key_A:
            # print("ctrl + a, cmd + a is not allowed")
            return
        if (e.keyCombination().keyboardModifiers() == QtCore.Qt.KeyboardModifier.MetaModifier or e.keyCombination().keyboardModifiers() == QtCore.Qt.KeyboardModifier.ControlModifier) and e.key() == QtCore.Qt.Key.Key_V:
            # print("ctrl + v, cmd + v is not allowed")
            return

        # cmd, ctrl, alt, shift + up, right, left, down selection not allowed
        # print(str(e.keyCombination().keyboardModifiers()))
        if str(e.keyCombination().keyboardModifiers()) in ["KeyboardModifier.KeypadModifier|ShiftModifier", "KeyboardModifier.AltModifier", "KeyboardModifier.KeypadModifier|ControlModifier|ShiftModifier", "KeyboardModifier.KeypadModifier|MetaModifier|ShiftModifier","KeyboardModifier.KeypadModifier|AltModifier|ShiftModifier", "KeyboardModifier.KeypadModifier|ControlModifier"]: return

        # editable only hex area. indices => [9, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 59]
        indices = [i for i, x in enumerate(tc.block().text()) if x == " "]
        if (len(indices) > 0) is False:
            return
        if tcx in range(indices[1]) or tcx in range(indices[1] + 3, indices[len(indices) - 2] + 3, 3):
            return

        super(HexViewerClass, self).keyPressEvent(e)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        super(HexViewerClass, self).mousePressEvent(e)
        pos = e.pos()
        tc = self.cursorForPosition(pos)
        tcx = tc.positionInBlock()
        line = tc.block().text()
        # print(tc.block().text())
        # print("mousepress pos: ", tcx, tcy)

        indices = [i for i, x in enumerate(line) if x == " "]
        # memory pattern search 한 결과창에서 마우스 클릭한 경우
        if len(indices) == 0:
            if e.buttons() == QtCore.Qt.MouseButton.XButton1 or e.buttons() == QtCore.Qt.MouseButton.XButton2: return
            for i in range(2): self.moveCursor(QTextCursor.MoveOperation.Up)
            self.moveCursor(QTextCursor.MoveOperation.NextWord)
            return
        # elif line.find(', module:') != -1:
        elif re.search(r"\d+\. 0x[a-f0-9]+, module:", line):
            if e.buttons() == QtCore.Qt.MouseButton.XButton1 or e.buttons() == QtCore.Qt.MouseButton.XButton2: return
            self.moveCursor(QTextCursor.MoveOperation.Down)
            self.moveCursor(QTextCursor.MoveOperation.StartOfBlock)
            self.moveCursor(QTextCursor.MoveOperation.NextWord)
            return

        if e.buttons() == QtCore.Qt.MouseButton.XButton1:
            self.movesig.emit(0)
        elif e.buttons() == QtCore.Qt.MouseButton.XButton2:
            self.movesig.emit(1)

        # mouse left click on non hex editable region at normal hexviewer
        if e.buttons() == QtCore.Qt.MouseButton.LeftButton and len(indices) > 0:
            # ADDRESS region
            if tcx in range(indices[1] + 1):
                self.moveCursor(QTextCursor.MoveOperation.NextWord)
                return
            # ASCII String Region
            if tcx in range(len(line) - 16, len(line) + 1):
                self.moveCursor(QTextCursor.MoveOperation.StartOfLine)
                for i in range(16):
                    self.moveCursor(QTextCursor.MoveOperation.NextWord)
                return
            # if (tcx - 9) % 3 == 0 or (tcx - 9) % 3 == 1:
            if tcx in indices or (tcx + 1) in indices:
                self.moveCursor(QTextCursor.MoveOperation.PreviousWord)
                return

    def contextMenuEvent(self, e: QtGui.QContextMenuEvent) -> None:
        # If in hexedit mode, don't create a context menu on right click
        if not self.isReadOnly():
            return

        tc = self.cursorForPosition(e.pos())
        tcx = tc.positionInBlock()

        menu = super(HexViewerClass, self).createStandardContextMenu()  # Get the default context menu
        select_all_action = next((action for action in menu.actions() if "Select All" in action.text()), None)

        if select_all_action:
            # Check if the selected text matches the hex_regex
            hex_regex = re.compile(r'(\b0x[a-fA-F0-9]+\b|\b[a-fA-F0-9]{6,}\b)')
            match = hex_regex.match(self.textCursor().selectedText())
            is_selected = bool(self.textCursor().selectedText())

            def create_action(text, enabled, func):
                action = QAction(text, self)
                action.setEnabled(enabled)
                action.triggered.connect(func)
                return action

            # Create and insert the actions
            copy_hex_action = create_action("Copy Hex", is_selected and match is None, self.copy_hex)
            disassemble_action = create_action("Hex to Arm", is_selected and match is None, self.request_armconverter)

            copy_pointer_action = None
            unsign_kptr_action = None
            if globvar.fridaInstrument is None:
                self.statusBar.showMessage(f"Attach first", 3000)
                return
            addr_match = hex_regex.match(tc.block().text())
            if addr_match is not None:
                addr_length = len(addr_match[0])
                hex_start = addr_length + 2
                cursor_len_4bytes = 12  # '00 00 00 00 '
                cursor_len_8bytes = 2 * 12
                if globvar.arch == "arm64" and (tcx in [hex_start, hex_start + 1, hex_start + 2] or tcx in [hex_start + cursor_len_8bytes, hex_start + cursor_len_8bytes + 1, hex_start + cursor_len_8bytes + 2]):
                    make_copy_pointer_action = True
                elif globvar.arch == "arm" and (tcx in [hex_start, hex_start + 1, hex_start + 2] or tcx in [hex_start + cursor_len_4bytes, hex_start + cursor_len_4bytes + 1, hex_start + cursor_len_4bytes + 2] or tcx in [hex_start + cursor_len_8bytes, hex_start + cursor_len_8bytes + 1, hex_start + cursor_len_8bytes + 2] or tcx in [hex_start + 3 * cursor_len_4bytes, hex_start + 3 * cursor_len_4bytes + 1, hex_start + 3 * cursor_len_4bytes + 2]):
                    make_copy_pointer_action = True
                else:
                    make_copy_pointer_action = False

                if make_copy_pointer_action:
                    copy_pointer_action = create_action("Copy Pointer", match is None,
                                                        lambda: self.copy_pointer(tc, hex_start))
                    unsign_kptr_action = create_action("Unsign kptr", match is None,
                                                       lambda: self.unsign_kptr(tc, hex_start))

            menu.insertAction(select_all_action, copy_hex_action)
            menu.insertAction(select_all_action, disassemble_action)
            if copy_pointer_action is not None:
                menu.insertAction(select_all_action, copy_pointer_action)
                menu.insertAction(select_all_action, unsign_kptr_action)

        menu.exec(e.globalPos())

    def text_changed_event(self):
        tc = self.textCursor()
        tcx = tc.positionInBlock()
        line = tc.block().text()
        # print("[hackcatml] text changed: " + tc.block().text())

        # if tc.block().text() == "", index out of error occurs
        if line == "": return

        # if changed text is not hex, then refresh the hex viewer
        # print(f"text: {line[len(line) - 66:len(line) - 16]}")
        if re.search(r"[^0-9a-f\s]+", line[len(line) - 66:len(line) - 16]) and not re.search(r"\d+\. 0x[0-9a-f]+, module:", line):
            self.refreshsig.emit(1) if globvar.isFridaAttached else None
            return

        indices = [i for i, x in enumerate(line) if x == " "]
        try:
            hexstart = indices[1] + 1
        except Exception as e:
            print(f"{inspect.currentframe().f_code.co_name}: {e}")
            self.clear()
            return

        # print("[hackcatml] (tcx - hexstart) // 3 = ", (tcx - hexstart) // 3)
        if (tcx - hexstart) // 3 < 0 or (tcx - hexstart) // 3 > 15: return

        addr = hex(int(line[:line.find(" ")], 16) + (tcx - hexstart) // 3)
        # print("[hackcatml] text changed addr: ", addr)

        changed = line[3 * ((tcx - hexstart) // 3) + hexstart: 3 * ((tcx - hexstart) // 3) + hexstart + 2]
        changed = "".join(("0x", changed))
        # print("[hackcatml] changed hex: ", changed)

        pos = tc.position()

        try:
            orig = globvar.fridaInstrument.read_kmem_addr(addr, 1)
            index = orig.find("\n")
            index = index + orig[index:].find(' ') + 2
            orig = orig[index: index + 2]
            orig = "".join(("0x", orig))
            if changed == orig or len(changed.replace('0x', '').strip()) == 1 or re.search(r"(?![0-9a-fA-F]).",
                                                                                           changed.replace('0x', '')):
                return
        except Exception as e:
            if str(e) == globvar.errorType1:
                globvar.fridaInstrument.sessions.clear()
            return

        prot = '---'
        for i in range(len(globvar.enumerateRanges)):
            if int(globvar.enumerateRanges[i][0], 16) <= int(addr, 16) <= int(globvar.enumerateRanges[i][1], 16):
                prot = globvar.enumerateRanges[i][2]

        for i in range(len(globvar.hexEdited)):
            if addr in globvar.hexEdited[i]:
                globvar.hexEdited[i][1] = changed
                globvar.hexEdited[i][2] = orig
                globvar.hexEdited[i][3] = prot
                globvar.hexEdited[i][4] = pos
                return

        globvar.hexEdited.append([addr, changed, orig, prot, pos])
        # print(f"text changed pos: {tcx}")

    def selected_text(self, request_to_armconverter: bool) -> str:
        selected_text = self.textCursor().selectedText()  # gets the currently selected text
        selected_text = selected_text.replace('\u2029', '\n')
        lines = selected_text.strip().split('\n')
        if len(lines) <= 2:
            hex_data = []
            for line in lines:
                matches = re.findall(r'\b[0-9a-fA-F]{2}\b', line)
                hex_data.append(' '.join(matches))
            if request_to_armconverter is False:
                hex_string = '\n'.join(hex_data)
            else:
                hex_string = ''.join(hex_data)
            return hex_string
        elif len(lines) > 2:
            # Determine the length of the second line
            second_line_length = len(lines[1])
            # If the first line is shorter, pad it with spaces at the beginning
            if len(lines[0]) < second_line_length:
                difference = second_line_length - len(lines[0])
                lines[0] = ' ' * difference + lines[0]
            # If the last line is shorter, pad it with spaces at the end
            if len(lines[-1]) < second_line_length:
                difference = second_line_length - len(lines[-1])
                lines[-1] += ' ' * difference
            hex_data = []
            for line in lines:
                # Calculate hex start and end positions
                hex_start = len(line) - 65
                hex_end = len(line) - 16

                # Extract hex part
                hex_part = line[hex_start:hex_end]

                # Extract two-digit hex numbers from the part
                matches = re.findall(r'\b[0-9a-fA-F]{2}\b', hex_part)
                hex_data.append(' '.join(matches))
            # Join hex data into a single string
            if request_to_armconverter is False:
                hex_string = '\n'.join(hex_data)
            else:
                hex_string = ''.join(hex_data)
            return hex_string

    def copy_hex(self):
        hex_string = self.selected_text(False)
        QApplication.clipboard().setText(hex_string)  # copies the hex text to the clipboard

    def request_armconverter(self):
        import requests

        url = 'https://armconverter.com/api/convert'
        hex_string = self.selected_text(True)

        payload = {"hex": hex_string, "offset": "", "arch": [globvar.arch]}
        response = requests.post(url, json=payload)
        data = response.json()

        if data['asm'][globvar.arch][0] is True:
            hex_to_arm_result = data['asm'][globvar.arch][1]
            # Show the copied text in a new widget
            self.new_hex_to_arm_widget = NewHexToArmWidget(hex_to_arm_result)
            cursor_pos = QCursor.pos()
            # Move the widget to the cursor position
            self.new_hex_to_arm_widget.move(cursor_pos)
            self.new_hex_to_arm_widget.show()
        else:
            print("Fail to hex to arm convert")

    def hex_code_at_pos(self, tc, hex_start):
        tcx = tc.positionInBlock()
        cursor_len_4bytes = 12
        cursor_len_8bytes = 12 * 2
        hex_code = None

        if tcx in [hex_start, hex_start + 1, hex_start + 2]:
            hex_code = tc.block().text()[
                       hex_start:hex_start + cursor_len_8bytes - 1] if globvar.arch == "arm64" else tc.block().text()[
                                                                                                    hex_start:hex_start + cursor_len_4bytes - 1]
        elif tcx in [hex_start + cursor_len_4bytes, hex_start + cursor_len_4bytes + 1,
                     hex_start + cursor_len_4bytes + 2]:
            hex_code = tc.block().text()[hex_start + cursor_len_4bytes:hex_start + cursor_len_8bytes - 1]
        elif tcx in [hex_start + cursor_len_8bytes, hex_start + cursor_len_8bytes + 1,
                     hex_start + cursor_len_8bytes + 2]:
            hex_code = tc.block().text()[
                       hex_start + cursor_len_8bytes:hex_start + 2 * cursor_len_8bytes - 1] if globvar.arch == "arm64" else tc.block().text()[
                                                                                                                            hex_start + cursor_len_8bytes:hex_start + 3 * cursor_len_4bytes - 1]
        elif tcx in [hex_start + 3 * cursor_len_4bytes, hex_start + 3 * cursor_len_4bytes + 1,
                     hex_start + 3 * cursor_len_4bytes + 2]:
            hex_code = tc.block().text()[hex_start + 3 * cursor_len_4bytes:hex_start + 4 * cursor_len_4bytes - 1]

        return hex_code

    def copy_pointer(self, tc: QTextCursor, hex_start):
        hex_code = self.hex_code_at_pos(tc, hex_start)
        pointer = hex(int(''.join(reversed(hex_code.split(' '))), 16))
        QApplication.clipboard().setText(pointer)

    def unsign_kptr(self, tc: QTextCursor, hex_start):
        hex_code = self.hex_code_at_pos(tc, hex_start)
        pointer = hex(int(''.join(reversed(hex_code.split(' '))), 16))
        result = globvar.fridaInstrument.unsign_kptr(pointer)

        self.result_widget.text_edit.append(hex(int(result)))
        cursorPOS = QCursor.pos()
        self.result_widget.move(cursorPOS)
        self.result_widget.show()


class ResultWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unsign kptr")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  # Make the text edit read-only
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)
        self.resize(250, 100)

    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        self.text_edit.clear()
        self.text_edit.closeEvent(e)
        super().closeEvent(e)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


class NewHexToArmWidget(QWidget):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("HEX to ARM")
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(text)
        self.text_edit.setReadOnly(True)  # Make the text edit read-only
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)




