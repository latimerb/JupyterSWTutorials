from neuron import h
from matplotlib import pyplot
import CellTemplate
import ConfigParser
h.load_file("stdgui.hoc")


def set_source_params(src, src_interval=10, src_number=5, src_start=10, src_noise=0):
    src.interval = src_interval
    src.number = src_number
    src.start = src_start
    src.noise = src_noise


# ----- Open Config File -----
config = ConfigParser.RawConfigParser()
config.read('SimpleSynapse.cfg')

# ----- Define all variables -----
v_init = config.getint('Simulation Parameters', 'v_init')
tstop = config.getint('Simulation Parameters', 'tstop')
dt = config.getfloat('Simulation Parameters', 'dt')
steps_per_ms = 1/config.getfloat('Simulation Parameters', 'dt')
interval = config.getint('Stimulation Parameters', 'interval')
number = config.getint('Stimulation Parameters', 'number')
start = config.getint('Stimulation Parameters', 'start')
noise = config.getint('Stimulation Parameters', 'noise')

# ----- Create Single Cell -----
simpleCell = CellTemplate.Cell()

# ----- Simulation Parameters -----
h.v_init = v_init
h.tstop = tstop
h.dt = dt
h.steps_per_ms = steps_per_ms

# ----- Stimulation Parameters -----
exp_syn = h.Exp2Syn(simpleCell.dend(0.5))

# ----- Create Netstim -----
net_stimulation = h.NetStim(0.5)
set_source_params(net_stimulation, interval, number, start, noise)

# ----- Connect Synapse to Stimulation Source -----
nc_stim_expsyn = h.NetCon(net_stimulation, exp_syn, 1, 0, 1)

# ----- Create Vectors to Record Plotting Parameters -----
t_vec = h.Vector()
v_vec = h.Vector()
exp_syn_vec = h.Vector()
il_leak_vec = h.Vector()
ikd_kdr_vec = h.Vector()
ina_na_vec = h.Vector()
i_pas_vec = h.Vector()

# ----- Create Recording for Each Parameter -----
t_vec.record(h._ref_t)
v_vec.record(simpleCell.soma(0.5)._ref_v)
exp_syn_vec.record(exp_syn._ref_g)
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
plot_exc, = pyplot.plot(t_vec, exp_syn_vec, 'r', label='syn_exc.g')
pyplot.xlim(0, h.tstop)
pyplot.ylabel('Siemens/cm^2')
pyplot.legend(handles=[plot_exc])
pyplot.title('Excitatory Synapse')
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
figure.savefig('SimpleSynapse.png')
# pyplot.show()
