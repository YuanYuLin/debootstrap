import ops
import iopc

pkg_path = ""
output_dir = ""
arch = ""
do_debootstrap = ""
base_rootfs_dir = ""
base_rootfs_tarball = ""

def set_global(args):
    global pkg_path
    global output_dir
    global arch
    global do_debootstrap
    global base_rootfs_dir
    global base_rootfs_tarball
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    arch = ops.getEnv("ARCH_ALT")
    do_debootstrap = ops.getEnv("DO_DEBOOTSTRAP")
    pkg_args = args["pkg_args"]
    base_rootfs_tarball = ops.path_join(pkg_path, pkg_args["version"])
    if arch == "armhf":
        base_rootfs_dir = ops.path_join(output_dir, "debian_jessie_armhf")
    elif arch == "armel":
        base_rootfs_dir = ops.path_join(output_dir, "debian_jessie_armel")
    elif arch == "x86_64":
        base_rootfs_dir = ops.path_join(output_dir, "base_rootfs")
    else:
        sys.exit(1)

    print base_rootfs_tarball

def MAIN_ENV(args):
    set_global(args)

    ops.exportEnv(ops.setEnv("BASE_ROOTFS_DIR", base_rootfs_dir))
    ops.exportEnv(ops.setEnv("BASE_ROOTFS_TARBALL", base_rootfs_tarball))
    return False

def MAIN_EXTRACT(args):
    set_global(args)
    CMD = []
    if do_debootstrap != "Y":
        ops.unTarXzSUDO(base_rootfs_tarball, output_dir)
    else:
        if arch == "armhf": # hard flot
            output_path=ops.pkg_mkdir(output_dir, "debian_jessie_armhf")
            download_url = 'ftp://ftp.debian.org/debian/'
            CMD=["qemu-debootstrap", "--arch=armhf", "jessie", output_path, download_url]
        elif arch == "armel": # soft flot
            output_path=ops.pkg_mkdir(output_dir, "debian_jessie_armel")
            download_url = 'ftp://ftp.debian.org/debian/'
            #CMD=["qemu-debootstrap", "--arch=" + arch, "jessie", output_path, download_url]
            CMD=["qemu-debootstrap", "--arch=armel", "stable", "--variant=minbase", output_path, download_url]
        elif arch == "x86_64":
            output_path=ops.pkg_mkdir(output_dir, "debian_base_rootfs")
            download_url = 'ftp://ftp.debian.org/debian/'
            CMD=["qemu-debootstrap", "--arch=amd64", "stable", "--variant=minbase", output_path, download_url]

        res = ops.execCmd(CMD, output_path, False, None)

    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(output_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)
    return False

def MAIN_BUILD(args):
    set_global(args)
    return False

def MAIN_INSTALL(args):
    set_global(args)
    return False

def MAIN_SDKENV(args):
    set_global(args)
    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)
    return False

def MAIN(args):
    set_global(args)

