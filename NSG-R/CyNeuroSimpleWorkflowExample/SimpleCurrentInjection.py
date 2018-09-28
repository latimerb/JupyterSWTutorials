from neuron import h
from matplotlib import pyplot
import CellTemplate
import ConfigParser
h.load_file("stdgui.hoc")


def update_iclamp(i_clamp, i_delay, i_dur, i_amp):
    i_clamp.delay = float(i_delay)  # in ms
    i_clamp.dur = float(i_dur)  # in ms
    i_clamp.amp = float(i_amp)  # in nA


# ----- Open Config File -----
config = ConfigParser.RawConfigParser()
config.read('SimpleCurrentInjection.cfg')

# ----- Define all variables -----
v_init = config.getint('Simulation Parameters', 'v_init')
tstop = config.getint('Simulation Parameters', 'tstop')
dt = config.getfloat('Simulation Parameters', 'dt')
steps_per_ms = 1/config.getfloat('Simulation Parameters', 'dt')
delay = config.getint('Stimulation Parameters', 'delay')
duration = config.getint('Stimulation Parameters', 'duration')
amplitude = config.getfloat('Stimulation Parameters', 'amplitude')

# ----- Create Single Cell -----
simpleCell = CellTemplate.Cell()

# ----- Simulation Parameters -----
h.v_init = v_init
h.tstop = tstop
h.dt = dt
h.steps_per_ms = steps_per_ms

# ----- Stimulation Parameters -----
ccl = h.IClamp(simpleCell.soma(0.5))
update_iclamp(ccl, delay, duration, amplitude)

# ----- Create Vectors to Record Plotting Parameters -----
t_vec = h.Vector()
v_vec = h.Vector()
ccl_vec = h.Vector()
il_leak_vec = h.Vector()
ikd_kdr_vec = h.Vector()
ina_na_vec = h.Vector()
i_pas_vec = h.Vector()

# ----- Create Recording for Each Parameter -----
t_vec.record(h._ref_t)
v_vec.record(simpleCell.soma(0.5)._ref_v)
ccl_vec.record(ccl._ref_i)
il_leak_vec.record(simpleCell.soma(0.5)._ref_il_leak)
ikd_kdr_vec.record(simpleCell.soma(0.5)._ref_ikd_kdr)
ina_na_vec.record(simpleCell.soma(0.5)._ref_ina_na)
i_pas_vec.record(simpleCell.dend(0.5)._ref_i_pas)

# ----- Run the Model -----
h.run()

# ----- Create Plots to Visualize Results -----
figure = pyplot.figure(figsize=(12, 8))
pyplot.subplot(221)
plot_v, = pyplot.plot(t_vec, v_vec, 'b', label='soma.v')
pyplot.xlim(0, h.tstop)
pyplot.ylabel('mV')
pyplot.legend(handles=[plot_v])
pyplot.title('Soma Voltage')
pyplot.subplot(222)
plot_ccl, = pyplot.plot(t_vec, ccl_vec, 'r', label='ccl.i')
pyplot.xlim(0, h.tstop)
pyplot.ylabel('nA')
pyplot.legend(handles=[plot_ccl])
pyplot.title('Current Clamp')
pyplot.subplot(223)
plot_leak, = pyplot.plot(t_vec, il_leak_vec, 'r', label='soma.il_leak')
plot_k, = pyplot.plot(t_vec, ikd_kdr_vec, 'b', label='soma.ikd_kdr')
plot_na, = pyplot.plot(t_vec, ina_na_vec, 'g', label='soma.ina_na')
pyplot.xlim(0, h.tstop)
pyplot.ylabel('nA')
pyplot.legend(handles=[plot_leak, plot_k, plot_na])
pyplot.title('Sodium, Potassium, and Leak Currents')
pyplot.subplot(224)
plot_pas, = pyplot.plot(t_vec, i_pas_vec, 'r', label='dend.pas')
pyplot.xlim(0, h.tstop)
pyplot.ylabel('nA')
pyplot.legend(handles=[plot_pas])
pyplot.title('Dendrite Passive Current')
pyplot.subplots_adjust(left=0.065, bottom=0.075, right=0.98, top=0.95, wspace=0.2, hspace=0.25)
figure.savefig('SimpleCurrentInjection.png')
# pyplot.show()
