#!/usr/bin/env python
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#
##

##
# Import Modules
#
import os
import sys
import subprocess
import errno
import shutil
import argparse
import multiprocessing

def prep_env (workspace):
    edk2source = workspace
    os.chdir(edk2source)
    if os.name == 'posix':
        toolchain = 'GCC49'
        gcc_ver = subprocess.Popen(['gcc', '-dumpversion'], stdout=subprocess.PIPE)
        (gcc_ver, err) = subprocess.Popen(['sed', 's/\\..*//'], stdin=gcc_ver.stdout, stdout=subprocess.PIPE).communicate()
        if int(gcc_ver) > 4:
            toolchain = 'GCC5'

        os.environ['PATH'] = os.environ['PATH'] + ':' + os.path.join(edk2source, 'BaseTools/BinWrappers/PosixLike')
    elif os.name == 'nt':
        toolchain = ''
        os.environ['PATH'] = os.environ['PATH'] + ';' + os.path.join(edk2source, 'BaseTools\\Bin\\Win32')
        os.environ['PATH'] = os.environ['PATH'] + ';' + os.path.join(edk2source, 'BaseTools\\BinWrappers\\WindowsLike')
        os.environ['PYTHONPATH'] = os.path.join(edk2source, 'BaseTools', 'Source', 'Python')
        vs_ver_list = [
            ('2015', 'VS140COMNTOOLS', '81', '8.1'),
            ('2013', 'VS120COMNTOOLS', '8',  '8.0'),
            ('2012', 'VS110COMNTOOLS', '71', 'v7.1A'),
            ('2010', 'VS100COMNTOOLS', '7',  'v7.0A'),
            ('2008', 'VS90COMNTOOLS',  '',   'v6.0A'),
            ('2005', 'VS80COMNTOOLS',  '',   '')
        ]
        for vs_ver, vs_tool, sdkv, sdkd in vs_ver_list:
            if vs_tool in os.environ:
                toolchain='VS%s%s' % (vs_ver, 'x86')
                toolchainprefix = 'VS%s_PREFIX' % (vs_ver)
                os.environ[toolchainprefix] = os.path.join(os.environ[vs_tool], '..//..//')
                break
        if not toolchain:
            print ("Could not find supported Visual Studio version !")
            sys.exit(1)

        os.environ['WINSDK%s_PREFIX'    % sdkv] = "c:/Program Files/Windows Kits/%s/bin/" % (sdkd)
        os.environ['WINSDK%sx86_PREFIX' % sdkv] = "c:/Program Files (x86)/Windows Kits/%s/bin/" % (sdkd)

        if 'NASM_PREFIX' not in os.environ:
            os.environ['NASM_PREFIX'] = "C:\\Nasm\\"
        if 'OPENSSL_PATH' not in os.environ:
            os.environ['OPENSSL_PATH'] = "C:\\Openssl\\"
        if 'IASL_PREFIX' not in os.environ:
            os.environ['IASL_PREFIX'] = "C:\\ASL\\"
    else:
        print ("Unsupported operating system !")
        sys.exit(1)

    # Update Environment vars
    #os.environ['EDK2PLT_SOURCE']  = os.path.join(workspace, 'PldPlatform')
    os.environ['EDK2_SOURCE']     = edk2source
    os.environ['EDK_TOOLS_PATH']  = os.path.join(edk2source, 'BaseTools')
    os.environ['BASE_TOOLS_PATH'] = os.path.join(edk2source, 'BaseTools')
    os.environ['WORKSPACE']       = workspace
    os.environ['CONF_PATH']       = os.path.join(os.environ['WORKSPACE'], 'Conf')
    os.environ['TOOL_CHAIN']      = toolchain

def rebuild_basetools ():
    ret = 0
    edk2source = os.environ['EDK2_SOURCE']
    if os.name == 'posix':
        genffs_exe_path = os.path.join(edk2source, 'BaseTools', 'Source', 'C', 'bin', 'GenFfs')
        genffs_exist = os.path.exists(genffs_exe_path)
        if not genffs_exist:
            ret = subprocess.call(['make', '-C', 'BaseTools'])

    elif os.name == 'nt':
        os.environ['PYTHON_HOME'] = sys.exec_prefix
        os.environ['PYTHON_COMMAND'] = sys.executable
        genffs_exe_path = os.path.join(edk2source, 'BaseTools', 'Bin', 'Win32', 'GenFfs.exe')
        genffs_exist = os.path.exists(genffs_exe_path)

        if not genffs_exist:
            print ("Could not find pre-built BaseTools binaries, try to rebuild BaseTools ...")
            ret = subprocess.call(['BaseTools\\toolsetup.bat', 'forcerebuild'])

    if ret:
        print ("Build BaseTools failed, please check required build environment and utilities !")
        sys.exit(1)

        genffs_exist = os.path.exists(genffs_exe_path)
        if not genffs_exist:
                print ("Build python executables failed !")
                sys.exit(1)


def clone_repo(repo_name, branch, target_dir, work_dir):
    sys.stdout.flush()

    repo_dir = os.path.join(work_dir, target_dir)
    if not os.path.exists(repo_dir + '/.git'):
        print ('Cloning repo ... %s', repo_name)
        cmd = 'git clone --recursive %s %s' % (repo_name, target_dir)
        ret = subprocess.call(cmd.split(' '), cwd=work_dir)
        if ret:
            print ('Failed to clone to directory %s !' % work_dir)
            sys.exit(1)
        print ('Done\n')
    else:
        output = subprocess.check_output(['git', 'tag', '-l'], cwd=repo_dir).decode()
        if branch not in output:
            ret = subprocess.call(['git', 'fetch', '--all'], cwd=repo_dir)
            if ret:
                print ('Failed to fetch all tags !')
                sys.exit(1)

    print ('Checking out branch (%s)...' % branch)
    cmd = 'git checkout -f ' + branch
    ret = subprocess.call(cmd.split(' '), cwd=repo_dir)
    if ret:
        print ('Failed to check out branch !')
        sys.exit(1)

    print ('Checking out submodules ...')
    cmd = 'git submodule update --init'
    ret = subprocess.call(cmd.split(' '), cwd=repo_dir)
    if ret:
        print ('Failed to check out submodules !')
        sys.exit(1)

    print ('Done\n')

def build_uefi_payload (target_dir, coreboot, release, arch64):
    prep_env (target_dir)
    rebuild_basetools()

    # create conf and build folder if not exist
    if not os.path.exists(os.path.join(target_dir, 'Conf')):
        os.makedirs(os.path.join(target_dir, 'Conf'))
    for name in ['target', 'tools_def', 'build_rule']:
        txt_file = os.path.join(target_dir, 'Conf/%s.txt' % name)
        if not os.path.exists(txt_file):
            shutil.copy (
                os.path.join(target_dir, 'BaseTools/Conf/%s.template' % name),
                os.path.join(target_dir, 'Conf/%s.txt' % name))

    dsc_file = os.path.join(target_dir, 'UefiPayloadPkg', 'UefiPayloadPkg.dsc')
    if not os.path.exists(dsc_file):
        print ("DSC file %s could not be found!" % dsc_file)
        sys.exit(1)

    build_cmd  = "build"        if os.name == 'posix' else "build.bat"
    build_cmd += " -b RELEASE"  if release            else " -b DEBUG"
    build_cmd += " -a X64"      if arch64             else " -a IA32 -a X64"
    build_cmd += " -p %s"  % dsc_file
    build_cmd += " -t %s"  % os.environ['TOOL_CHAIN']
    build_cmd += " -n %s"  % str(multiprocessing.cpu_count())
    build_cmd += " -y Report.log"
    build_cmd += " -Y PCD"
    build_cmd += " -Y FLASH"
    build_cmd += " -Y LIBRARY"
    build_cmd += " -D PLATFORM_ARCH=X64"
    build_cmd += " -D BOOTLOADER=COREBOOT"  if coreboot else " -D BOOTLOADER=SBL"

    # Run build
    print (build_cmd)
    x = subprocess.call(build_cmd, cwd=target_dir, shell=True)
    return x

def build_sbl (target_dir, release, arch64):
    os.environ.pop('EDK2_SOURCE')
    os.environ.pop('EDK_TOOLS_PATH')
    os.environ.pop('BASE_TOOLS_PATH')
    os.environ.pop('WORKSPACE')
    os.environ.pop('CONF_PATH')
    build_cmd = ['python', 'BuildLoader.py', 'build', 'qemu', '-p', 'OsLoader.efi:LLDR:Lz4;UefiPld.fd:UEFI:Lzma', '-k']
    if release:
        build_cmd.extend(['-r'])
    if arch64:
        build_cmd.extend(['-a', 'x64'])
    print (build_cmd)
    print (target_dir)
    ret = subprocess.call(build_cmd, cwd=target_dir)
    if ret:
        print ('Failed to build slim bootloader!')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r',    '--release',     action='store_true', help='Release build')
    parser.add_argument('-cb',   '--coreboot',    action='store_true', help='Build UEFI payload with coreboot,  by default with Slim Bootloader')
    parser.add_argument('-x64',  '--arch64',      action='store_true', help='Build bootloader and payload for 64bit bootloader. by default for 32bit.')
    args = parser.parse_args()
    print(args)

    tool_dir = os.path.dirname (os.path.realpath(__file__))
    work_dir = os.path.join(tool_dir, 'codeworkspace')
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    if args.coreboot:
        print ("coreboot support is not ready yet!")
        sys.exit(1)
    else:
        clone_repo ('https://github.com/gdong1/slimbootloader.git', 'universal_payload_api', 'slimbootloader', work_dir)

    clone_repo ('https://github.com/gdong1/edk2.git', 'universal_payload_api', 'edk2', work_dir)

    print ('\n\nbuild UEFI payload....')
    ret = build_uefi_payload (os.path.join(work_dir, 'edk2'), args.coreboot, args.release, args.arch64)
    if ret:
        print ("build UEFI payload error")
        sys.exit(1)

    # copy payload binary to bootloader repo
    pld_file = os.path.join(work_dir, 'edk2', 'Build', 'UefiPayloadPkgX64', '%s_%s' % ('RELEASE' if args.release else 'DEBUG', os.environ['TOOL_CHAIN']), 'FV', 'UEFIPAYLOAD.fd')
    dst_dir  = os.path.join(work_dir, 'slimbootloader', 'Platform', 'QemuBoardPkg', 'Binaries')
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    shutil.copy(pld_file, os.path.join(dst_dir, 'UefiPld.fd'))

    print ('\n\nbuild Slim bootloader with UEFI payload....')
    build_sbl(os.path.join(work_dir, 'slimbootloader'), args.release, args.arch64)

    # copy the final binary to workspace folder
    final_file = os.path.join(work_dir, 'slimbootloader', 'Outputs', 'qemu', 'SlimBootloader.bin')
    shutil.copy(final_file, os.path.join(work_dir, 'SlimBootloader.bin'))

if __name__ == '__main__':
    sys.exit(main())
