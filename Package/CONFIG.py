import ops

def MAIN_ENV(args):
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    base_rootfs_dir = output_dir + "/debian_jessie_armhf"
    base_rootfs_tarball = pkg_path + "/debian_jessie_armhf.tar.xz"
    env = ops.setEnv("BASE_ROOTFS_DIR", base_rootfs_dir)
    ops.exportEnv(env)

    env = ops.setEnv("BASE_ROOTFS_TARBALL", base_rootfs_tarball)
    ops.exportEnv(env)
    return False

def MAIN_EXTRACT(args):
    arch = ops.getEnv("ARCH_ALT")
    output_dir = args["output_path"]
    base_rootfs_tarball = ops.getEnv("BASE_ROOTFS_TARBALL")
    if ops.isExist(base_rootfs_tarball):
        ops.unTarXz(base_rootfs_tarball, output_dir)
    else:
        output_path=ops.pkg_mkdir(output_dir, "debian_jessie_armhf")
        download_url = 'ftp://ftp.debian.org/debian/'
        CMD=["qemu-debootstrap", "--arch=" + arch, "jessie", output_path, download_url]
        res = ops.execCmd(CMD, output_path, False, None)
    return True

def MAIN_CONFIGURE(args):
    output_dir = args["output_path"]
    return False

def MAIN_BUILD(args):
    output_dir = args["output_path"]
    return False

def MAIN_INSTALL(args):
    output_dir = args["output_path"]
    return False

def MAIN_CLEAN_BUILD(args):
    output_dir = args["output_path"]
    return False

def MAIN(args):
    output_dir = args["output_path"]

