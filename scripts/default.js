var module_name = "kfd"
var kreadbuf = new NativeFunction(Module.findExportByName(module_name, "kreadbuf"), 'void', ['uint64', 'pointer', 'int']);
var get_kslide = new NativeFunction(Module.findExportByName(module_name, "get_kslide"), 'uint64', []);
var get_vm_kernel_link_addr = new NativeFunction(Module.findExportByName(module_name, "get_vm_kernel_link_addr"), 'uint64', []);
var get_kernversion = new NativeFunction(Module.findExportByName(module_name, "get_kernversion"), 'pointer', []);
var getProc = new NativeFunction(Module.findExportByName(module_name, "getProc"), 'uint64', ['int']);
var getVnodeAtPath = new NativeFunction(Module.findExportByName(module_name, "getVnodeAtPath"), 'uint64', ['pointer']);
var unsign_kptr = new NativeFunction(Module.findExportByName(module_name, "unsign_kptr"), 'uint64', ['uint64']);
var kread8 = new NativeFunction(Module.findExportByName(module_name, "kread8"), 'uint8', ['uint64']);
var kread16 = new NativeFunction(Module.findExportByName(module_name, "kread16"), 'uint32', ['uint64']);
var kread32 = new NativeFunction(Module.findExportByName(module_name, "kread32"), 'uint32', ['uint64']);
var kread64 = new NativeFunction(Module.findExportByName(module_name, "kread64"), 'uint64', ['uint64']);
var kwrite8 = new NativeFunction(Module.findExportByName(module_name, "kwrite8"), 'void', ['uint64', 'uint64']);
var kwrite16 = new NativeFunction(Module.findExportByName(module_name, "kwrite16"), 'void', ['uint64', 'uint64']);
var kwrite32 = new NativeFunction(Module.findExportByName(module_name, "kwrite32"), 'void', ['uint64', 'uint64']);
var kwrite64 = new NativeFunction(Module.findExportByName(module_name, "kwrite64"), 'void', ['uint64', 'uint64']);

// offsets
var offsets = {
    "off_p_list_le_prev": getOffset('off_p_list_le_prev'),
    "off_p_proc_ro": getOffset('off_p_proc_ro'),
    "off_p_ppid": getOffset('off_p_ppid'),
    "off_p_original_ppid": getOffset('off_p_original_ppid'),
    "off_p_pgrpid": getOffset('off_p_pgrpid'),
    "off_p_uid": getOffset('off_p_uid'),
    "off_p_gid": getOffset('off_p_gid'),
    "off_p_ruid": getOffset('off_p_ruid'),
    "off_p_rgid": getOffset('off_p_rgid'),
    "off_p_svuid": getOffset('off_p_svuid'),
    "off_p_svgid": getOffset('off_p_svgid'),
    "off_p_sessionid": getOffset('off_p_sessionid'),
    "off_p_puniqueid": getOffset('off_p_puniqueid'),
    "off_p_pid": getOffset('off_p_pid'),
    "off_p_pfd": getOffset('off_p_pfd'),
    "off_p_textvp": getOffset('off_p_textvp'),
    "off_p_name": getOffset('off_p_name'),
    "off_p_ro_p_csflags": getOffset('off_p_ro_p_csflags'),
    "off_p_ro_p_ucred": getOffset('off_p_ro_p_ucred'),
    "off_p_ro_pr_proc": getOffset('off_p_ro_pr_proc'),
    "off_p_ro_pr_task": getOffset('off_p_ro_pr_task'),
    "off_p_ro_t_flags_ro": getOffset('off_p_ro_t_flags_ro'),
    "off_u_cr_label": getOffset('off_u_cr_label'),
    "off_u_cr_posix": getOffset('off_u_cr_posix'),
    "off_cr_uid": getOffset('off_cr_uid'),
    "off_cr_ruid": getOffset('off_cr_ruid'),
    "off_cr_svuid": getOffset('off_cr_svuid'),
    "off_cr_ngroups": getOffset('off_cr_ngroups'),
    "off_cr_groups": getOffset('off_cr_groups'),
    "off_cr_rgid": getOffset('off_cr_rgid'),
    "off_cr_svgid": getOffset('off_cr_svgid'),
    "off_cr_gmuid": getOffset('off_cr_gmuid'),
    "off_cr_flags": getOffset('off_cr_flags'),
    "off_task_t_flags": getOffset('off_task_t_flags'),
    "off_task_itk_space": getOffset('off_task_itk_space'),
    "off_fd_ofiles": getOffset('off_fd_ofiles'),
    "off_fd_cdir": getOffset('off_fd_cdir'),
    "off_fp_glob": getOffset('off_fp_glob'),
    "off_fg_data": getOffset('off_fg_data'),
    "off_fg_flag": getOffset('off_fg_flag'),
    "off_vnode_v_ncchildren_tqh_first": getOffset('off_vnode_v_ncchildren_tqh_first'),
    "off_vnode_v_ncchildren_tqh_last": getOffset('off_vnode_v_ncchildren_tqh_last'),
    "off_vnode_v_nclinks_lh_first": getOffset('off_vnode_v_nclinks_lh_first'),
    "off_vnode_v_iocount": getOffset('off_vnode_v_iocount'),
    "off_vnode_v_usecount": getOffset('off_vnode_v_usecount'),
    "off_vnode_v_flag": getOffset('off_vnode_v_flag'),
    "off_vnode_v_name": getOffset('off_vnode_v_name'),
    "off_vnode_v_mount": getOffset('off_vnode_v_mount'),
    "off_vnode_v_data": getOffset('off_vnode_v_data'),
    "off_vnode_v_kusecount": getOffset('off_vnode_v_kusecount'),
    "off_vnode_v_references": getOffset('off_vnode_v_references'),
    "off_vnode_v_lflag": getOffset('off_vnode_v_lflag'),
    "off_vnode_v_owner": getOffset('off_vnode_v_owner'),
    "off_vnode_v_parent": getOffset('off_vnode_v_parent'),
    "off_vnode_v_label": getOffset('off_vnode_v_label'),
    "off_vnode_v_cred": getOffset('off_vnode_v_cred'),
    "off_vnode_v_writecount": getOffset('off_vnode_v_writecount'),
    "off_vnode_v_type": getOffset('off_vnode_v_type'),
    "off_vnode_v_id": getOffset('off_vnode_v_id'),
    "off_vnode_vu_ubcinfo": getOffset('off_vnode_vu_ubcinfo'),
    "off_mount_mnt_data": getOffset('off_mount_mnt_data'),
    "off_mount_mnt_fsowner": getOffset('off_mount_mnt_fsowner'),
    "off_mount_mnt_fsgroup": getOffset('off_mount_mnt_fsgroup'),
    "off_mount_mnt_devvp": getOffset('off_mount_mnt_devvp'),
    "off_mount_mnt_flag": getOffset('off_mount_mnt_flag'),
    "off_specinfo_si_flags": getOffset('off_specinfo_si_flags'),
    "off_namecache_nc_dvp": getOffset('off_namecache_nc_dvp'),
    "off_namecache_nc_vp": getOffset('off_namecache_nc_vp'),
    "off_namecache_nc_hashval": getOffset('off_namecache_nc_hashval'),
    "off_namecache_nc_name": getOffset('off_namecache_nc_name'),
    "off_namecache_nc_child_tqe_prev": getOffset('off_namecache_nc_child_tqe_prev'),
    "off_ipc_space_is_table": getOffset('off_ipc_space_is_table'),
    "off_ubc_info_cs_blobs": getOffset('off_ubc_info_cs_blobs'),
    "off_ubc_info_cs_add_gen": getOffset('off_ubc_info_cs_add_gen'),
    "off_cs_blob_csb_pmap_cs_entry": getOffset('off_cs_blob_csb_pmap_cs_entry'),
    "off_cs_blob_csb_cdhash": getOffset('off_cs_blob_csb_cdhash'),
    "off_cs_blob_csb_flags": getOffset('off_cs_blob_csb_flags'),
    "off_cs_blob_csb_teamid": getOffset('off_cs_blob_csb_teamid'),
    "off_cs_blob_csb_validation_category": getOffset('off_cs_blob_csb_validation_category'),
    "off_pmap_cs_code_directory_ce_ctx": getOffset('off_pmap_cs_code_directory_ce_ctx'),
    "off_pmap_cs_code_directory_der_entitlements_size": getOffset('off_pmap_cs_code_directory_der_entitlements_size'),
    "off_pmap_cs_code_directory_trust": getOffset('off_pmap_cs_code_directory_trust'),
    "off_ipc_entry_ie_object": getOffset('off_ipc_entry_ie_object'),
    "off_ipc_object_io_bits": getOffset('off_ipc_object_io_bits'),
    "off_ipc_object_io_references": getOffset('off_ipc_object_io_references'),
    "off_ipc_port_ip_kobject": getOffset('off_ipc_port_ip_kobject'),

    "off_cdevsw": getOffset('off_cdevsw'),
    "off_gPhysBase": getOffset('off_gPhysBase'),
    "off_gPhysSize": getOffset('off_gPhysSize'),
    "off_gVirtBase": getOffset('off_gVirtBase'),
    "off_perfmon_dev_open": getOffset('off_perfmon_dev_open'),
    "off_perfmon_devices": getOffset('off_perfmon_devices'),
    "off_ptov_table": getOffset('off_ptov_table'),
    "off_vn_kqfilter": getOffset('off_vn_kqfilter'),
    "off_proc_object_size": getOffset('off_proc_object_size')
}

function getOffset(name) {
    var exportList = Module.enumerateExportsSync(module_name);
    var found = exportList.find(function(m) { return m.type == 'variable' && m.name == name; });
    if (found) {
        if (name == "off_cdevsw" || name == "off_gPhysBase" || name == "off_gPhysSize" || name == "off_gVirtBase" || name == "off_perfmon_dev_open" || name == "off_perfmon_devices" || name == "off_ptov_table" || name == "off_vn_kqfilter" || name == "off_proc_object_size") {
            return ptr(found.address).readU64();
        }
        return ptr(found.address).readU32();
    }
    return null;
}

rpc.exports = {
    // just dummy function for checking script is alive
    dummy: () => {
        // console.log("muffin")
        send("")
    },
    arch: () => {
        send(Process.arch)
    },
    platform: () => {
        send(Process.platform)
    },
    enumerateranges: (prot) => {
        // send(Process.enumerateRangesSync(prot))
        return Process.enumerateRangesSync(prot)
    },
    listmodules: () => {
        send(Process.enumerateModulesSync())
    },
    getKernelSlide: () => {
        return get_kslide();
    },
    getVmKernelLinkAddr: () => {
        return get_vm_kernel_link_addr();
    },
    getKernVersion: () => {
        return get_kernversion().readUtf8String();
    },
    getOffsets: () => {
        send(offsets);
    },
    getKfd: () => {
        var symbolsList = Module.enumerateSymbolsSync(module_name)
        var found = symbolsList.find(function(m) { return m.name === "_kfd" && m.address != "0x0"; })
        if (found) {
            var _kfd = ptr(found.address)
            var _kfd_struct = _kfd.readPointer()
            var kfd = {
                "kfd": _kfd,
                "kfd->info.env.pid": _kfd_struct.add(0x18).readU32(),
                "kfd->info.env.tid": _kfd_struct.add(0x18).add(0x8).readU64(),
                "kfd->info.env.vid": _kfd_struct.add(0x18).add(0x10).readU64(),
                "kfd->info.env.maxfilesperproc": _kfd_struct.add(0x18).add(0x18).readU64(),
                "kfd->info.kaddr.current_map": _kfd_struct.add(0x38).readPointer(),
                "kfd->info.kaddr.current_pmap": _kfd_struct.add(0x38).add(0x8).readPointer(),
                "kfd->info.kaddr.current_proc": _kfd_struct.add(0x38).add(0x10).readPointer(),
                "kfd->info.kaddr.current_task": _kfd_struct.add(0x38).add(0x18).readPointer(),
                "kfd->info.kaddr.kernel_map": _kfd_struct.add(0x38).add(0x20).readPointer(),
                "kfd->info.kaddr.kernel_pmap": _kfd_struct.add(0x38).add(0x28).readPointer(),
                "kfd->info.kaddr.kernel_proc": _kfd_struct.add(0x38).add(0x30).readPointer(),
                "kfd->info.kaddr.kernel_task": _kfd_struct.add(0x38).add(0x38).readPointer(),
                "kfd->perf.kernel_slide": _kfd_struct.add(0x78).readPointer(),
                "kfd->perf.gVirtBase": _kfd_struct.add(0x78).add(0x8).readPointer(),
                "kfd->perf.gPhysBase": _kfd_struct.add(0x78).add(0x10).readPointer(),
                "kfd->perf.gPhysSize": _kfd_struct.add(0x78).add(0x18).readPointer(),
            }
            send(kfd)
        }
    },
    getAllProc: (pid) => {
        return getProc(pid);
    },
    getVnodeAtPath: (file_path) => {
        var path = Memory.allocUtf8String(file_path);
        var vnode = getVnodeAtPath(path);
        if (ptr(vnode) != '0xffffffffffffffff') {
            var vnode_info = {
                "vnode": vnode,
                "usecount": kread32(vnode.add(0x60)),
                "iocount": kread32(vnode.add(0x64)),
                "flag": kread32(vnode.add(0x54))
            }
            send(vnode_info)
        }
    },
    unsignKptr: (pac_kaddr) => {
        return unsign_kptr(uint64(pac_kaddr));
    },
    kHexDump: (kaddr, size) => {
        // console.log(uint64(kaddr))
        var kdump_size;
        size == null ? kdump_size = 0x640 : kdump_size = size;
        var data = Memory.alloc(kdump_size);
        kreadbuf(uint64(kaddr), data, kdump_size);
        send(hexdump(data, {address: uint64(kaddr), length: kdump_size}));
    },
    writeKmemAddr: (kaddr, code) => {
        kwrite8(uint64(kaddr), uint64(code));
    },
    hexdumpaddr: (addr, size) => {
        send(hexdump(ptr(addr), {offset:0, length:size}))
    },
    writememaddr: (addr, code, prot) => {
        // console.log("mem prot: " + prot)
        var newprot = prot
        if(prot == "r--" || prot == "r-x" || prot == "---") {
            newprot = "rw-"
        }
        Memory.protect(ptr(addr), 4, newprot)
        Memory.writeByteArray(ptr(addr), [code])
        if(prot == "---") return    // if mem protection '---' then remain else back to orig prot
        Memory.protect(ptr(addr), 4, prot)
    },
}
