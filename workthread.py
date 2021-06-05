#!/usr/bin/env python3

from threading import Thread, enumerate, RLock
from clientsession import ClientSession
import socket, traceback
import sys, select
#import yaml
import json
import logging

if 'debug' in sys.argv[:]:
    log_level = logging.DEBUG
else:
    log_level = logging.INFO

proc_log = logging.getLogger()

proc_log= logging.basicConfig(level=log_level, format='%(levelname)s (%(threadName)-9s) %(message)s',)

ThreadLock = RLock()

active_threads = {
    'connections': {},
}

class WorkThread():
    def __init__(self, port=8421, host="0.0.0.0"):
        self._host = host
        self._port = port
        self.ServiceState(True)

    def ServiceState(self, state):
        self.running_state = state

    def StopService(self, stop=False):
        if stop and self.running_state:
            logging.info("Service has been marked for shutdown")
            self.ServiceState(False)
            self.CloseSocket()
            self.StopConnectedClients()
        elif stop and not self.running_state:
            logging.info("Waiting for all active clients to disconnect.")

        self.report()

    def StopConnectedClients(self):
        for c in active_threads['connections'].keys():
            if active_threads['connections'][c]['thread'].is_alive():
                logging.info("Sending stop signal at - \t%s:%s" % (active_threads['connections'][c]['ip'], c))
                ThreadLock.acquire()
                active_threads['connections'][c]['state'] = 2
                ThreadLock.release()

    def report(self):
        if self.running_state:
            print(
                "INFO Service is running:",
                "\tPort: %s" % self._port,
                "\tBind Address: %s" % self._host)
        else:
            logging.info("Service has stopped")

    def CloseSocket(self):
        self.soc.shutdown(socket.SHUT_RDWR)
        self.soc.close()

    def run(self):
        try:
            logging.info("Defining Socket Server")
            logging.info("Address, protocol Family and socket type")
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            logging.info("Binding socket {h} {p}".format(h=self._host, p=self._port))
            self.soc.bind((self._host, self._port))
            logging.info("Socket created successfully.")
        except:
            logging.error("Socket Creation Failed: " + str(sys.exc_info()))
            self.CloseSocket()
            sys.exit(1)

        self.soc.listen(5)
        logging.info("Socket now listening at {p}".format(p=self._port))

        while self.running_state:
            self.conn, self.address = self.soc.accept()
            self.ip, self._port = str(self.address[0]), str(self.address[1])
            logging.info("Client {i} has been connected at {p} port".format(i=self.ip, p=self._port))

            try:
                self.new_sock = Thread(
                    target=ClientSession,
                    args=(
                        self.conn,
                        self.ip,
                        self._port,
                        active_threads,
                    ),
                    daemon=False
                )

                ThreadLock.acquire()
                active_threads['connections'][self._port] = {
                    'thread': self.new_sock,
                    'ip': self.ip,
                    'state': 0
                }

                ThreadLock.release()

                self.new_sock.start()

                logging.info("Currently Active Clients:")

                ThreadLock.acquire()
                for c in active_threads['connections'].keys():
                    if active_threads['connections'][c]['thread'].is_alive():
                        logging.info("Client - \t%s:%s" % (active_threads['connections'][c]['ip'], c))
                ThreadLock.release()
            except:
                logging.info("WARN: Could not serve new thread for client {i}.".format(i=self.ip))
                self.client_conerr = sys.exc_info()
                logging.error(str(self.client_conerr))
                # traceback.print_exc()

        self.CloseSocket()
        print("Socket server has stopped")


#todo remover lixo abaixo
"""
if __name__ == "__main__":
    try:
        srv = srvprime()
        srv.run()
    except KeyboardInterrupt:
        srv.StopService(True)
"""