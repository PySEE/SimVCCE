"""
The vapor-compression refrigeration cycle simulator for education in Python
VCRCycle: the Simulator class of VCR Cycle  
"""

import time
import getpass
from platform import os

from components.node import Node
from components import compdict


class VCRCycle:

    def __init__(self, dictcycle):
        """
          dictcycle={"name":namestring,
                     "nodes":[{node1},{node2},...],
                     "comps":[{component1},{component2},...]
                     }
          TO:           
             self.nodes : dict of all node objects:
                {node id:node object}
             self.comps : dict of all component objects:
                {device name:device obiect}
        """
        self.name = dictcycle["name"]
        dictnodes = dictcycle["nodes"]
        dictcomps = dictcycle["comps"]

        # 1 convert dict to the dict of node objects {node id:node object}
        self.nodes = {}
        for curnode in dictnodes:
            self.nodes[curnode["id"]] = Node(curnode)

        # 2 convert dict to the dict of device objects: {device name:device obiect}
        self.comps = {}
        for curdev in dictcomps:
            self.comps[curdev['name']] = compdict[curdev['devtype']](
                curdev, self.nodes)

    def ComponentState(self):
        for key in self.comps:
            self.comps[key].state()

        for key in self.nodes:
            if self.nodes[key].stateok == False:
                self.nodes[key].state()

    def ComponentBalance(self):
        for curdev in self.comps:
            self.comps[curdev].balance()

    def simulator(self):
        self.ComponentState()
        self.ComponentBalance()

        self.Wc = 0
        self.Qlow = 0

        for key in self.comps:
            if self.comps[key].energy == "CompressionWork":
                self.Wc += self.comps[key].Wc
            elif self.comps[key].energy == "RefrigerationCapacity":
                self.Qlow += self.comps[key].Qlow

        self.cop = self.Qlow / self.Wc
        self.Qlow = self.Qlow*60*(1/211)

    def __setformatstr(self, formatstr, result):
        result += formatstr.format('Compression Work(kW): ', self.Wc)
        result += formatstr.format('Refrigeration Capacity(ton): ', self.Qlow)
        result += formatstr.format('The coefficient of performance: ', self.cop)
        return result

    def __str__(self):
        str_curtime = time.strftime(
            "%Y/%m/%d %H:%M:%S", time.localtime(time.time()))
        result = "\nRefrigeration Cycle: {} (Time: {} by {} on {})\n".format(
            self.name, str_curtime,getpass.getuser(),os.popen('hostname').read())
        try:
            formatstr = "{:>35} {:>6.3f}\n"
            result = self.__setformatstr(formatstr, result)
        except:
            formatstr = "{} {}\n"
            result = self.__setformatstr(formatstr, result)
        return result
