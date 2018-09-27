from neuron import h


# Define a Class for Cell
class Cell(object):
    # Create an initialization function that runs when a cell is created
    # Create sections of the cell, connect cell sections, and create functions to initialize each section
    def __init__(self):
        self.soma = soma = h.Section(name='soma', cell=self)
        self.dend = dend = h.Section(name='dend', cell=self)
        self.dend.connect(self.soma(1), 0)
        self.section_names = ["soma", "dend"]
        self.all = h.SectionList()
        self.init_section_list()
        self.init_soma()
        self.init_dend()

    # Function that defines the section soma's geometry and biophysics
    def init_soma(self):
        soma = self.soma
        h.pt3dclear(sec=soma)
        h.pt3dadd(0, 0, 0, 1, sec=soma)
        h.pt3dadd(15, 0, 0, 1, sec=soma)
        soma.L = 50
        soma.diam = 50
        soma.nseg = 1
        soma.Ra = 150
        soma.cm = 1
        soma.insert('leak')
        soma.glbar_leak = 1/3333.33
        soma.el_leak = -70
        soma.insert('kdr')
        soma.gkdrbar_kdr = 0.036
        soma.insert('na')
        soma.gnabar_na = 0.12

    # Function that defines the section dend's geometry and biophysics
    def init_dend(self):
        dend = self.dend
        h.pt3dclear(sec=dend)
        h.pt3dadd(0, 0, 0, 1, sec=dend)
        h.pt3dadd(-59, 0, 0, 1, sec=dend)
        dend.L = 150
        dend.diam = 10
        dend.nseg = 1
        dend.Ra = 150
        dend.cm = 1
        dend.insert('pas')

    # Function to define all section lists
    def init_section_list(self):
        self.all.append(sec=self.soma)
        self.all.append(sec=self.dend)
