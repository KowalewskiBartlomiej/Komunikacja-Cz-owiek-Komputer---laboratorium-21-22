import matplotlib.pyplot as plt
__author__ = 'student'


def loadfile(path):
    arr = []
    with open(path) as f:
        for line in f.readlines()[1:]:
            arr.append(line.split(',')[1:])
    return arr


def prepare_x_axis(arr):
    output = []
    for item in arr:
        if float(len(item)) > 0:
            output.append(float(item[0]) / 1000.0)
    return output


def prepare_y_axis(arr):
    output = []
    for item in arr:
        sum = 0
        for i in item[1:]:
            sum += float(i)
        count = float(len(item) - 1)
        output.append(sum / count * 100.0) # multiplied by 100 to make it percent value.
    return output

def prepare_y_axis_box(arr):
    output = []
    for i in arr[-1][1:]:
        output.append(float(i) * 100.0)
    return output


def main():
    # Load data from files.
    ceov2 = loadfile('ceov2.csv')
    ceov2_rs = loadfile('ceov2_rs.csv')
    ceov1 = loadfile('ceov1.csv')
    ceov1_rs = loadfile('ceov1_rs.csv')
    evol1_rs = loadfile('evol1_rs.csv')

    plots = plt.figure(figsize=(10, 7))

    # Succes main plot.
    succ = plots.add_subplot(121)

    succ.plot(prepare_x_axis(evol1_rs), prepare_y_axis(evol1_rs),
              label="1-Evol-RS", color='blue',
              marker='o', markersize=7, markevery=25)
    succ.plot(prepare_x_axis(ceov1_rs), prepare_y_axis(ceov1_rs),
              label="1-Coev-RS", color='green',
              marker='v', markersize=7, markevery=25)
    succ.plot(prepare_x_axis(ceov2_rs), prepare_y_axis(ceov2_rs),
              label="2-Coev-RS", color='red',
              marker='D', markersize=7, markevery=25)
    succ.plot(prepare_x_axis(ceov1), prepare_y_axis(ceov1),
              label="1-Coev", color='black',
              marker='s', markersize=7, markevery=25)
    succ.plot(prepare_x_axis(ceov2), prepare_y_axis(ceov2),
              label="2-Coev", color='magenta',
              marker='d', markersize=7, markevery=25)

    # Set labels and limits.
    succ.set_xlabel("Rozegranych gier (x1000)")
    succ.set_ylabel("Odsetek wygranych gier [%]")
    xmin = 0
    xmax = 500
    succ.set_xlim(xmin, xmax)

    # Succes plot top x axis.
    top_succ = plt.twiny()
    top_succ.set_xlim(0, 200)
    top_succ.set_xticks([0, 100, 200, 300, 400, 500])
    top_succ.set_xticklabels(["0", "40", "80", "120", "160", "200"])
    top_succ.set_xlabel("Pokolenie")

    succ.legend(loc=4)
    succ.grid()

    # Box plot.
    box = plots.add_subplot(122)

    # Set labels.
    box_labels = ["1-Evol-RS",
                  "1-Coev-RS", "2-Coev-RS",
                  "1-Coev", "2-Coev"]

    x_ticks = [.1, .3, .5, .7, .9]
    box.set_xticks(x_ticks)
    box.set_xticklabels(box_labels, rotation=20)

    # Configure Y axis.
    box.set_ylim(60, 100)
    box.set_xlim(0, 1)
    box.yaxis.tick_right()
    box.yaxis.set_label_position("right")

    # Set correct data.
    box_data = [prepare_y_axis_box(evol1_rs),
                prepare_y_axis_box(ceov1_rs), prepare_y_axis_box(ceov2_rs),
                prepare_y_axis_box(ceov1), prepare_y_axis_box(ceov2)]

    box.boxplot(box_data, notch=True)
    box.grid()

    # Add averages.
    box_averages = [sum(prepare_y_axis_box(evol1_rs)) / len(prepare_y_axis_box(evol1_rs)),
                    sum(prepare_y_axis_box(ceov1_rs)) / len(prepare_y_axis_box(ceov1_rs)),
                    sum(prepare_y_axis_box(ceov2_rs)) / len(prepare_y_axis_box(ceov2_rs)),
                    sum(prepare_y_axis_box(ceov1)) / len(prepare_y_axis_box(ceov1)),
                    sum(prepare_y_axis_box(ceov2)) / len(prepare_y_axis_box(ceov2))]

    box.scatter([1, 2, 3, 4, 5], box_averages)

    plt.savefig('plot.pdf')
    plt.close()
if __name__ == '__main__':
    main()
