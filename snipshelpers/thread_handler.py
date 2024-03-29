# -*-: coding utf-8 -*-
""" Thread handler. """

import threading
import time

class Singleton:
    """ Singleton class. """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """ Initialisation. """
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class ThreadHandler(Singleton):
    """ Thread handler. """

    def __init__(self):
        """ Initialisation. """
        self.thread_pool = []
        self.run_events = []

    def run(self, target, args=()):
        """ Run a function in a separate thread.

        :param target: the function to run.
        :param args: the parameters to pass to the function.
        """
        run_event = threading.Event()
        run_event.set()
        thread = threading.Thread(target=target, args=args + (run_event, ))
        thread.daemon = True
        self.thread_pool.append(thread)
        self.run_events.append(run_event)
        thread.start()

    def start_run_loop(self):
        """ Start the thread handler, ensuring that everything stops property
            when sending a keyboard interrupt.
        """
        try:
            while 1:
                time.sleep(.1)
        except (KeyboardInterrupt, SystemExit):
            self.stop()

    def stop(self):
        """ Stop all functions running in the thread handler."""
        for run_event in self.run_events:
            run_event.clear()

        for thread in self.thread_pool:
            thread.join()
