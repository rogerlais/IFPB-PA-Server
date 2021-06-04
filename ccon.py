#!/usr/bin/env python3

from threading import enumerate, RLock
from base64 import b64encode, b64decode
import socket, traceback
from io import StringIO
import sys, os, select
import logging

ThreadLock = RLock()

#!from getargs import GetArgs
GetArgs = None



#class ccon(GetArgs):
class ClientSession():
    def __init__(self, conn, ip, port, active_threads, max_buffer_size = 8192):
        self.conn = conn
        self.ip = ip
        self.port = port
        self.active_threads = active_threads
        self.service_name = "{u}:{p}".format(u=ip, p=port)
        self.max_buffer_size = max_buffer_size

        self.socket_state(True)
        self.force_flag = False

        self.set_lock(True)
        self.socket_has_exited = False
        self.active_threads['connections'][self.port]['state'] = 1
        self.set_lock(False)

        #GetArgs.__init__(self)
        self.run()

    def set_lock(self, lock=False):
        if lock:
            if ThreadLock.acquire():
                return True
            else:
                return False
        else:
            ThreadLock.release()

    def die(self, *args):
        '''Fata error handling function for
        issuing none, one or many warnings before exiting
        '''
        for msg in args:
            logging.error(msg)
        self.stop_socket(True)

    def socket_state(self, state):
        self.running_state = state

    def stop_socket(self, stop=False):
        if stop and self.running_state:
            logging.info("(%s) Service has been marked for shutdown" % self.service_name)
            self.socket_state(False)

        self.report()

    def close_socket(self):
        self.conn.shutdown(socket.SHUT_RDWR)
        self.conn.close()

    def report(self):
        if self.running_state:
            print(
                "INFO: (%s) Service is running:" % self.service_name,
                "\tPort: %s" % self.port,
                "\tBind Address: %s" % self.host)
        elif not self.running_state and not self.socket_has_exited:
            logging.info("(%s) Services has recieved stop signal. Will exit when all tasks are done." % self.service_name)
            logging.info("(%s) Waiting for client to disconnect." % self.service_name)
        else:
            logging.info("(%s) Service has stopped" % self.service_name)

    def com_drop(self):
        logging.error("(%s) Issuing drop transmission now (009x0DT000x0)" % self.service_name)
        self.conn.sendall(b64encode('009x0DT000x0'.encode('utf-8')))
        self.conn.setblocking(False)
        self.com_drop_status = True
        while True:
            clear_socket = select.select([self.conn], [], [], 2)
            if clear_socket[0]:
                try:
                    self.dump_socket_data = self.read_socket()
                    print(self.dump_socket_data)
                    if self.dump_socket_data == '' or self.dump_socket_data == ' ':
                        break
                except:
                    break
            else:
                break

        self.conn.setblocking(True)

    def com_sync(self, syncType):
        logging.debug("(%s) Sending %s " % (self.service_name, syncType))
        prem = syncType.encode('utf-8')
        msg = b64encode(prem)
        self.conn.sendall(msg)
        self.cldata = self.read_socket()
        logging.debug("(%s) Recieved %s" % (self.service_name, self.cldata))
        if self.cldata == syncType:
            return True
        else:
            self.com_drop()
            return False

    def message_com(self, message, buffer=8192):
        logging.debug("(%s) Start of message" % self.service_name)
        if not self.com_sync('01xSOM01x'):
            return False

        logging.debug("(%s) Sending data: %s" % (self.service_name, message))
        self.conn.sendall(b64encode(message.encode('utf-8')))

        self.cldata = self.read_socket(buffer)
        if self.cldata != '01xROM01x':
            self.com_drop()
            return False
        logging.debug("(%s) Received: %s" % (self.service_name, self.cldata))

        logging.debug("(%s) End data" % self.service_name)

        logging.debug("(%s) End of message" % self.service_name)
        return self.com_sync('01xEOM01x')

    def init_transmissionCom(self, data):
        logging.debug("(%s) Start of Transmission 00xSOT00x" % self.service_name)
        self.com_drop_status = False

        if not self.com_sync('00xSOT00x'):
            return False

        if data['key'] == 'text':
            if not self.message_com(data['value'], 8192):
                return False
        else:
            if not self.message_com('Response for request: %s' % self.client_request, 8192):
                return False
            for msg in data['value']:
                if not self.message_com("\t%s" % msg, 8192):
                    return False
            if not self.message_com('-', 8192):
                return False

        logging.debug("(%s) End of Transmission 00xSOT00x" % self.service_name)
        if self.com_drop_status:
            return False

        return self.com_sync('00xEOT00x')

    def init_sync(self):
        #if self.com_sync('00xSOS00xHELLOx00'):
        if self.com_sync('VAGOAMIN-START'):
            logging.debug("(%s) Client synced!" % self.service_name)
        else:
            self.die("(%s) Communication error" % self.service_name)

    def decode_data(self, data):
        ret = b64decode(data).decode('utf-8')
        return  ret

    def read_socket(self, buffer=8192):
        data = self.conn.recv(buffer)
        return self.decode_data(data)

    def init_client_communication(self, data):
        logging.debug("Starting message_com")
        transmission_status = self.init_transmissionCom(data)

        if transmission_status:
            logging.debug("Communication was sucessful")
        else:
            logging.error("Communicating data failed")

    def run(self):
        self.init_sync()

        logging.debug('%s' % enumerate())
        while self.running_state:

            self.set_lock(True)
            if self.active_threads['connections'][self.port]['state'] != 1:
                self.stop_socket(True)
                break

            self.set_lock(False)

            self.cldata = self.read_socket()
            self.client_request = self.cldata

            logging.info("(%s) Server received request: %s" % (self.service_name, self.cldata))
            if not self.cldata:
                logging.info("[-] Server socket thread disconnected for " + self.ip + ":" + str(self.port))
                self.stop_socket(True)
                break

            if self.cldata in ['Exit', 'Quit', 'exit', 'quit', 'q', 'bye', 'Bye']:
                logging.info("Initiating communication stop " + self.ip + ":" + str(self.port))
                retdata = {'key': 'text', 'value': 'Bye'}
                self.init_client_communication(retdata)
                self.stop_socket(True)
                logging.info("[-] Socket Thread has ended for " + self.ip + ":" + str(self.port))
                break

            std_out = StringIO()
            std_err = StringIO()
            sys.stdout = std_out
            sys.stderr = std_err

            if '--help' in self.cldata:
                try:
                    self.args = self.check_args(self.client_request.split())
                except:
                    retdata = {'key': 'text', 'value': str(std_out.getvalue())}
                    self.init_client_communication(retdata)

                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
                continue
            else:
                try:
                    self.args = self.check_args(self.client_request.split())
                except:
                    self.target_clients_err = sys.exc_info()
                    self.message_com("\n" + str(self.target_clients_err))
                    self.message_com("\n" + str(std_out.getvalue()) + "\n")
                    retdata = {'key': 'text', 'value': str(std_err.getvalue())}
                    self.init_client_communication(retdata)

                    sys.stdout = sys.__stdout__
                    sys.stderr = sys.__stderr__

                    continue

            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            try:
                for arg in self.args.keys():
                    if self.args[arg] == 'ls':
                        retdata = {'key': 'dict', 'value': []}
                        for e in os.listdir():
                            retdata['value'].append(e)
                    elif self.args[arg]  == 'cwd':
                        retdata = {'key': 'text', 'value': os.getcwd()}
                    elif self.args[arg]  == 'pwd':
                        retdata = {'key': 'text', 'value': os.path.dirname(os.getcwd())}

                self.init_client_communication(retdata)
            except:
                self.target_clients_err = sys.exc_info()
                logging.error("Execution error: %s" % str(self.target_clients_err))
                retdata = {'key': 'text', 'value': str(self.target_clients_err)}
                self.init_client_communication(retdata)

        self.close_socket()
        self.socket_has_exited = True
        logging.info("(%s) Service has stopped" % self.service_name)