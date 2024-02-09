import re

import frida
from PySide6 import QtGui
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QTextBrowser, QTextEdit, QLineEdit, QPushButton, QCheckBox

import globvar


class UtilViewerClass(QTextEdit):
    def __init__(self, args):
        super(UtilViewerClass, self).__init__(args)

        self.platform = None
        self.statusBar = None
        self.pid_list = None
        self.proc_list = None

        self.get_kfd_btn = QPushButton(None)
        self.get_pid_list_btn = QPushButton(None)
        self.get_all_proc_btn = QPushButton(None)
        self.get_vnode_at_path_input = QLineEdit(None)
        self.get_vnode_at_path_btn = QPushButton(None)

        self.util_viewer_filter = QLineEdit(None)

    def get_kfd(self):
        try:
            if globvar.fridaInstrument is None:
                return
            kfd = globvar.fridaInstrument.get_kfd()
            if kfd is not None:
                # Find the maximum key length for alignment
                max_key_length = max(len(key) for key in kfd) + 1  # +1 for extra space before value
                kfd_text = ""
                for key in kfd:
                    # Right-align the value with calculated padding
                    padding = max_key_length - len(key)
                    kfd_text += f"{key}{' ' * padding}\t\t{kfd[key]}\n"
                self.setText(f"{kfd_text}")
        except Exception as e:
            print(e)
            return

    def get_pid_list(self):
        self.setPlainText('')
        try:
            device = frida.get_usb_device(1)
            enumeration_function = device.enumerate_processes
        except Exception as e:
            print(e)
            return

        self.pid_list = [app for app in enumeration_function()]
        pid_list_text = ''
        for app in self.pid_list:
            pid_list_text += f"{str(app.pid)}\t{app.name}\n"

        self.setText(pid_list_text)

    def get_all_proc(self):
        try:
            if globvar.fridaInstrument is None:
                return
            device = frida.get_usb_device(1)
            enumeration_function = device.enumerate_processes
        except Exception as e:
            print(e)
            return

        self.pid_list = [app for app in enumeration_function()]
        self.proc_list = [[app.pid, app.name, globvar.fridaInstrument.get_all_proc(app.pid)] for app in self.pid_list]
        proc_list_text = ''
        for proc in self.proc_list:
            proc_list_text += f"pid: {proc[0]}\tname: {proc[1]}\tproc: {hex(int(proc[2]))}\n"

        self.setPlainText('')
        self.setText(proc_list_text)

    def get_vnode_at_path(self):
        try:
            if globvar.fridaInstrument is None:
                return
            if (path := self.get_vnode_at_path_input.text()) != '':
                vnode = globvar.fridaInstrument.get_vnode_at_path(path)
                if vnode != '':
                    vnode_text = f"path: {path}\n" \
                                 f"vnode: {hex(int(vnode['vnode']))}\n" \
                                 f"usecount: {vnode['usecount']}, iocount: {vnode['iocount']}\n" \
                                 f"flag: {hex(int(vnode['flag']))}"
                    self.setPlainText('')
                    self.setText(vnode_text)
            else:
                self.get_vnode_at_path_input.setFocus()
        except Exception as e:
            print(e)
            return

    def util_viewer_filter_func(self):
        text_to_find = self.util_viewer_filter.text().lower()

        matched = ''
        if self.pid_list is not None and len(self.pid_list) > 0 and re.search(r"^\d+\t.*", self.toPlainText()):
            for app in self.pid_list:
                pid_list_text = f"{str(app.pid)}\t{app.name}\n"
                if pid_list_text.lower().find(text_to_find) != -1:
                    matched += pid_list_text
        elif self.proc_list is not None and len(self.proc_list) > 0 and re.search(r"^pid: \d+\tname: .*\tproc: .*", self.toPlainText()):
            for proc in self.proc_list:
                proc_list_text = f"pid: {proc[0]}\tname: {proc[1]}\tproc: {hex(int(proc[2]))}\n"
                if proc_list_text.lower().find(text_to_find) != -1:
                    matched += proc_list_text

        if matched != '':
            self.setText(matched)

    # def contextMenuEvent(self, e: QtGui.QContextMenuEvent) -> None:
    #     menu = super(UtilViewerClass, self).createStandardContextMenu()  # Get the default context menu
    #     select_all_action = next((action for action in menu.actions() if "Select All" in action.text()), None)
    #
    #     if select_all_action:
    #         # parse more on __got, __la_symbol_ptr tables
    #         selected_text = self.textCursor().selectedText()
    #         if self.platform == 'linux':
    #             detail_section = ['.dynsym', '.rela.plt', '.got.plt', '.symtab']
    #             for item in detail_section:
    #                 if item in self.textCursor().block().text():
    #                     selected_text = item
    #         regex = re.compile(r'(\b__got\b|\b__la_symbol_ptr\b|\.dynsym|\.rela.plt|\.got\.plt|\.symtab)')
    #         match = regex.match(selected_text)
    #         is_selected = bool(selected_text)
    #
    #         def create_action(text, enabled, func):
    #             action = QAction(text, self)
    #             action.setEnabled(enabled)
    #             action.triggered.connect(func)
    #             return action
    #
    #         if match and is_selected:
    #             detail_action = create_action(f"Parse {selected_text}", True, lambda: self.detail(selected_text))
    #             menu.insertAction(select_all_action, detail_action)
    #
    #     menu.exec(e.globalPos())




