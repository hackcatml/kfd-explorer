/*
 * Copyright (c) 2023 Félix Poulin-Bélanger. All rights reserved.
 */

import SwiftUI
import os

struct ContentView: View {
    init() {
    }
    
    @State private var kfd: UInt64 = 0
    @State private var isGadgetLoaded: Bool = false

    private var puaf_pages_options = [16, 32, 64, 128, 256, 512, 1024, 2048]
    @State private var puaf_pages_index = 7
    @State private var puaf_pages = 0

    private var puaf_method_options = ["physpuppet", "smith", "landa"]
    @State private var puaf_method = 2

    private var kread_method_options = ["kqueue_workloop_ctl", "sem_open"]
    @State private var kread_method = 1

    private var kwrite_method_options = ["dup", "sem_open"]
    @State private var kwrite_method = 1

    var body: some View {
        NavigationView {
            Form {
                Section {
                    Picker(selection: $puaf_pages_index, label: Text("puaf pages:")) {
                        ForEach(0 ..< puaf_pages_options.count, id: \.self) {
                            Text(String(self.puaf_pages_options[$0]))
                        }
                    }.disabled(kfd != 0)
                }
                Section {
                    Picker(selection: $puaf_method, label: Text("puaf method:")) {
                        ForEach(0 ..< puaf_method_options.count, id: \.self) {
                            Text(self.puaf_method_options[$0])
                        }
                    }.disabled(kfd != 0)
                }
                Section {
                    Picker(selection: $kread_method, label: Text("kread method:")) {
                        ForEach(0 ..< kread_method_options.count, id: \.self) {
                            Text(self.kread_method_options[$0])
                        }
                    }.disabled(kfd != 0)
                }
                Section {
                    Picker(selection: $kwrite_method, label: Text("kwrite method:")) {
                        ForEach(0 ..< kwrite_method_options.count, id: \.self) {
                            Text(self.kwrite_method_options[$0])
                        }
                    }.disabled(kfd != 0)
                }
                Section {
                    HStack {
                        Button("kopen") {
                            puaf_pages = puaf_pages_options[puaf_pages_index]
                            
                            kfd = do_kopen(UInt64(puaf_pages), UInt64(puaf_method), UInt64(kread_method), UInt64(kwrite_method))
                            do_fun()
                        }.disabled(kfd != 0).frame(minWidth: 0, maxWidth: .infinity)
                        Button("kclose") {
                            do_kclose()
                            puaf_pages = 0
                            kfd = 0
                            isGadgetLoaded = false
                        }.disabled(kfd == 0).frame(minWidth: 0, maxWidth: .infinity)
                    }.buttonStyle(.bordered)
                }.listRowBackground(Color.clear)
                if kfd != 0 {
                    Section {
                        VStack {
                            Text("Success!").foregroundColor(.green)
                            Text("Look at output in Xcode")
                        }.frame(minWidth: 0, maxWidth: .infinity)
                    }.listRowBackground(Color.clear)
                }
                if isGadgetLoaded {
                    Section {
                        VStack {
                            Text("frida-gadget loaded!").foregroundColor(.red)
                        }.frame(minWidth: 0, maxWidth: .infinity)
                    }.listRowBackground(Color.clear)
                }
            }
            .navigationBarTitle(Text("kfd"), displayMode: .inline)
            .onChange(of: kfd) { kfd in
                if kfd != 0 {
                    let resourceUrl = Bundle.main.resourceURL
                    let fridaGadgetURL = resourceUrl!.appendingPathComponent("frida-gadget-16.1.11.dylib")
                    if access(fridaGadgetURL.path.cString(using: .utf8), F_OK) == 0 {
                        var thread = Thread(block: {
                            fridaGadgetThread()
                        })
                        thread.start()
                    }
                }
            }
        }
    }
    
    func fridaGadgetThread() -> Void {
        let resourceUrl = Bundle.main.resourceURL
        let fridaGadgetURL = resourceUrl!.appendingPathComponent("frida-gadget-16.1.11.dylib")
        let handle: UnsafeMutableRawPointer? = dlopen(fridaGadgetURL.path, RTLD_LAZY)
        if handle != nil {
            os_log("[hackcatml] frida-gadget loaded")
            isGadgetLoaded = true
        } else {
            os_log("[hackcatml] fail to load frida-gadget")
        }
    }
}

//struct ContentView_Previews: PreviewProvider {
//    static var previews: some View {
//        ContentView()
//    }
//}
