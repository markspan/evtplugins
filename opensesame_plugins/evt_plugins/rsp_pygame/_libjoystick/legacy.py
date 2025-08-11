# -*- coding:utf-8 -*-

"""
Created on 25-05-2012

Author: Edwin Dalmaijer

This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.

"""
from libopensesame.py3compat import *
import pygame
from .basejoystick import BaseJoystick


class Legacy(BaseJoystick):

    def __init__(self, experiment, device=0, joybuttonlist=None, timeout=None):
        """See _libjoystick.basejoystick"""
        self.js = pygame.joystick.Joystick(device)
        self.js.init()
        self.experiment = experiment
        self.set_joybuttonlist(joybuttonlist)
        self.set_timeout(timeout)
        pygame.event.set_blocked(pygame.JOYAXISMOTION)
        pygame.event.set_blocked(pygame.JOYHATMOTION)
        pygame.event.set_blocked(pygame.JOYBALLMOTION)

    def get_joybutton(self, joybuttonlist=None, timeout=None):
        """See _libjoystick.basejoystick"""
        if joybuttonlist is None or joybuttonlist == []:
            joybuttonlist = self._joybuttonlist
        if timeout is None:
            timeout = self.timeout
        start_time = pygame.time.get_ticks()
        time = start_time
        while timeout is None or time - start_time <= timeout:
            time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.experiment.pause()
                if event.type == pygame.JOYBUTTONDOWN:
                    if (
                            joybuttonlist is None or
                            event.button + 1 in joybuttonlist
                    ):
                        bpress = event.button + 1
                        return bpress, time
        return None, time

    def get_joyaxes(self, timeout=None):
        """See _libjoystick.basejoystick"""
        pygame.event.set_allowed(pygame.JOYAXISMOTION)
        if timeout is None:
            timeout = self.timeout
        pos = []
        start_time = pygame.time.get_ticks()
        time = start_time
        while timeout is None or time - start_time < timeout:
            time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.experiment.pause()
                if event.type == pygame.JOYAXISMOTION:
                    for axis in range(self.js.get_numaxes()):
                        pos.append(self.js.get_axis(axis))
                    pygame.event.set_blocked(pygame.JOYAXISMOTION)
                    return pos, time
        pygame.event.set_blocked(pygame.JOYAXISMOTION)
        return None, time

    def get_joyballs(self, timeout=None):
        """See _libjoystick.basejoystick"""
        pygame.event.set_allowed(pygame.JOYBALLMOTION)
        if timeout is None:
            timeout = self.timeout
        ballpos = []
        start_time = pygame.time.get_ticks()
        time = start_time
        while timeout is None or time - start_time < timeout:
            time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.experiment.pause()
                if event.type == pygame.JOYBALLMOTION:
                    for ball in range(self.js.get_numballs()):
                        ballpos.append(self.js.get_ball(ball))
                    pygame.event.set_blocked(pygame.JOYBALLMOTION)
                    return ballpos, time
        pygame.event.set_blocked(pygame.JOYBALLMOTION)
        return None, time

    def get_joyhats(self, timeout=None):
        """See _libjoystick.basejoystick"""
        pygame.event.set_allowed(pygame.JOYHATMOTION)
        if timeout is None:
            timeout = self.timeout
        hatpos = []
        start_time = pygame.time.get_ticks()
        time = start_time
        while timeout is None or time - start_time < timeout:
            time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.experiment.pause()
                if event.type == pygame.JOYHATMOTION:
                    for hat in range(self.js.get_numhats()):
                        hatpos.append(self.js.get_hat(hat))
                    pygame.event.set_blocked(pygame.JOYHATMOTION)
                    return hatpos, time
        pygame.event.set_blocked(pygame.JOYHATMOTION)
        return None, time

    def get_joyinput(self, joybuttonlist=None, timeout=None):
        """See _libjoystick.basejoystick"""
        pygame.event.set_allowed(pygame.JOYHATMOTION)
        pygame.event.set_allowed(pygame.JOYAXISMOTION)
        pygame.event.set_allowed(pygame.JOYBALLMOTION)
        if joybuttonlist is None or joybuttonlist == []:
            joybuttonlist = self._joybuttonlist
        if timeout is None:
            timeout = self.timeout
        pos = []
        ballpos = []
        hatpos = []
        eventtype = None
        start_time = pygame.time.get_ticks()
        time = start_time
        while timeout is None or time - start_time <= timeout:
            time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.experiment.pause()
                if event.type == pygame.JOYBUTTONDOWN:
                    if (
                            joybuttonlist is None or
                            event.button + 1 in joybuttonlist
                    ):
                        eventtype = u'joybuttonpress'
                        bpress = event.button + 1
                        pygame.event.set_blocked(pygame.JOYHATMOTION)
                        pygame.event.set_blocked(pygame.JOYAXISMOTION)
                        pygame.event.set_blocked(pygame.JOYBALLMOTION)
                        return eventtype, bpress, time
                if event.type == pygame.JOYAXISMOTION:
                    eventtype = u'joyaxismotion'
                    for axis in range(self.js.get_numaxes()):
                        pos.append(self.js.get_axis(axis))
                    pygame.event.set_blocked(pygame.JOYHATMOTION)
                    pygame.event.set_blocked(pygame.JOYAXISMOTION)
                    pygame.event.set_blocked(pygame.JOYBALLMOTION)
                    return eventtype, pos, time
                if event.type == pygame.JOYBALLMOTION:
                    eventtype = u'joyballmotion'
                    for ball in range(self.js.get_numballs()):
                        ballpos.append(self.js.get_ball(ball))
                    pygame.event.set_blocked(pygame.JOYHATMOTION)
                    pygame.event.set_blocked(pygame.JOYAXISMOTION)
                    pygame.event.set_blocked(pygame.JOYBALLMOTION)
                    return eventtype, ballpos, time
                if event.type == pygame.JOYHATMOTION:
                    eventtype = u'joyhatmotion'
                    for hat in range(self.js.get_numhats()):
                        hatpos.append(self.js.get_hat(hat))
                    pygame.event.set_blocked(pygame.JOYHATMOTION)
                    pygame.event.set_blocked(pygame.JOYAXISMOTION)
                    pygame.event.set_blocked(pygame.JOYBALLMOTION)
                    return eventtype, hatpos, time
        pygame.event.set_blocked(pygame.JOYHATMOTION)
        pygame.event.set_blocked(pygame.JOYAXISMOTION)
        pygame.event.set_blocked(pygame.JOYBALLMOTION)
        return eventtype, None, time

    def input_options(self):
        """See _libjoystick.basejoystick"""
        ninputs = [
            self.js.get_numbuttons(),
            self.js.get_numaxes(),
            self.js.get_numballs(),
            self.js.get_numhats()
        ]
        return ninputs

    def flush(self):
        """See _libjoystick.basejoystick"""
        joyinput = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.experiment.pause()
            if event.type in (
                    pygame.JOYBUTTONDOWN,
                    pygame.JOYAXISMOTION,
                    pygame.JOYBALLMOTION,
                    pygame.JOYHATMOTION
            ):
                joyinput = True
        return joyinput
