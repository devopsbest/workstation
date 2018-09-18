import re
import subprocess
import time
from subprocess import Popen

from ptest.plogger import preporter

START_ANDROID_DEVICE_TIMEOUT = 8
INVALID_PROCESS_ID = -1
MAX_RETRY_TIMES = 3
interval = 2
package_name = "com.ef.core.engage.smartenglish"


def kill_process_by_name(process_name):
    preporter.info('kill process {}'.format(process_name))
    run_command_on_shell('killall {}'.format(process_name))


def remove_android_app(package_name):
    preporter.info('remove app {} on emulator'.format(package_name))
    package = run_command_on_shell("adb shell pm list packages | grep {}".format(package_name))
    if not package:
        preporter.info('package {} is not installed on emulator'.format(package_name))
        return
    run_command_on_shell('adb uninstall {}'.format(package_name))
    preporter.info('android app {} is removed from emulator'.format(package_name))


def has_device_running(retry_times=MAX_RETRY_TIMES):
    # TODO: adb devices is not solid solution to determine device is ready for running automation, will figure out another approach to do this check
    i = 0

    while i < retry_times:
        time.sleep(interval)
        device_info = run_command_on_shell('adb devices')

        if len(device_info) > 1:
            for line in device_info:
                preporter.info(line)
            return True

        i += 1

    return False


def run_command_on_shell(command_string):
    """
    this function is used to run command and return output lines
    command
    :param command_string:
    :return:
    """
    process = start_process_by_command(command_string)
    out, error = process.communicate()
    return out.decode().splitlines()


def start_process_by_command(command_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    """
    this function is used to start a process and return Popen instance
    :param command_string:
    :param shell: set to True to be able to use command string exactly like we use on shell
    :param stdout: set to PIPE to be able to write output to pip
    :param stderr: set to PIPE to be able to write error to pip
    :return:
    """
    assert isinstance(command_string, str)

    process = Popen(command_string, shell=shell, stdout=stdout, stderr=stderr)
    return process


def get_process_info_on_port(port):
    result = run_command_on_shell("lsof -i tcp:{}".format(str(port)))

    return result[1:] if len(result) > 1 else result


def get_listening_process_id_on_port(port):
    process_info = get_process_info_on_port(port)

    processes = []

    for process in process_info:
        if process.__contains__(':{} (LISTEN)'.format(port)):
            processes.append(process.split()[1])

    return processes


def kill_listening_process_on_port(port):
    """
    kill the process which listens on the port, it  will also kill all connection to this port
    :param port:
    :return:
    """
    pids = get_listening_process_id_on_port(port)
    if not pids:
        preporter.info('no process listening on port {}'.format(port))
        return

    for pid in pids:
        run_command_on_shell('kill %s' % str(pid))

    pids = get_listening_process_id_on_port(port)

    if not pids:
        preporter.info('process killed on port {}'.format(port))
    else:
        preporter.info('processes {} still running on port {}'.format(pids, port))


def exec_command(cmd):
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (stdoutdata, stderrdata) = result.communicate()
    if (re.search("error", str(stdoutdata))):
        print("error occur during run {}".format(cmd))
    else:
        return stdoutdata


def install_apk(file):
    stdout = exec_command("adb install -r {}".format(file))
    if "Success" in stdout.decode():
        print("install successfully!")
    else:
        print("install fail!")


if __name__ == "__main__":

    if has_device_running:

        remove_android_app(package_name)

        install_apk("/Users/anderson/Downloads/builds/engage-smartenglish-qa-debug.apk")

    else:
        print("please connect devices!")