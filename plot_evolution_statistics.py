import pickle as pkl
from compute_theoretical_limits import get_theoretical_limit
import matplotlib.pyplot as plt

TL = get_theoretical_limit()

logfile_name = 'log2022-12-06 002438.001242.pkl'

with open(logfile_name, 'rb') as logfile:
    logs = pkl.load(logfile)
print('Terminei de ler')
xs_gens = []
ys_maxes = []
ys_means = []
ys_std_ups = []
ys_std_downs = []
ys_mins = []

for log in logs:
    # print(log)
    xs_gens.append(log['gen'])
    ys_maxes.append(log['Max']/TL*100)
    ys_means.append(log['Mean']/TL*100)
    ys_std_ups.append((log['Std'] + log['Mean'])/TL*100)
    ys_std_downs.append((-log['Std'] + log['Mean'])/TL*100)
    ys_mins.append(log['Min']/TL*100)
print(max(ys_maxes))
fig = plt.figure()

ax = fig.add_subplot(1, 1, 1)
ax.plot(xs_gens, ys_maxes, color='tab:red', label='Maior fitness')
ax.plot(xs_gens, ys_means, color='tab:green', label='Fitness média')
ax.plot(xs_gens, ys_mins, color='tab:blue', label='Menor fitness')
#ax.plot(xs_gens, ys_std_ups, color='black')
#ax.plot(xs_gens, ys_std_downs, color='black')

ax.set_xlim([0, 200])
ax.set_ylim([0, 100])

ax.set_title('Fitness ao longo das gerações')
ax.set_xlabel('Número da geração')
ax.set_ylabel('Porcentagem do máximo teórico')


plt.legend()
plt.savefig('lalala.png')

plt.show()

