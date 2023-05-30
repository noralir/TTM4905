import matplotlib.pyplot as plt


def changing_parameters():
    plt.figure(figsize=(5, 4) )
    #ax = plt.axes()
    #ax.set_facecolor("#fffcf5")

    color_two_green = ['#7fc97f','#1b9e77']
    color_two_pink = ['#f4cae4', '#e7298a']
    color_two_blue = ['#cbd5e8', '#8da0eb']

    x = [0,10000,10000, 20000, 20000,30000, 30000, 40000,40000, 50000]
    y1 = [0.015, 0.015,0.025, 0.025, 0.045,0.045,  0.015, 0.015,0.025,0.025]
    y2 = [1/12]*10
    y3 = [1/6, 1/6,1/10, 1/10,1/16,1/16, 1/6, 1/6,1/10,1/10]

    plt.plot([10000,10000],[0,0.18], color="#AAA", ls="--")
    plt.plot([20000,20000],[0,0.18], color="#AAA", ls="--")
    plt.plot([30000,30000],[0,0.18], color="#AAA", ls="--")
    plt.plot([40000,40000],[0,0.18], color="#AAA", ls="--")


    #plt.plot(x,y2, color="#e7298a", label = r"$\mu$")
    plt.plot(x,y3, color="#ff7f00", label = r"$\mu$")
    plt.plot(x,y1, color="#1b9e77", label = r"$\lambda$")




    plt.xlabel(r"$Packet #$")
    plt.ylabel(r"$Parameter$")

    plt.yticks([0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18])
    plt.margins(x=0,y=0)

    a=0.6
    plt.axvspan(00000, 10000, facecolor='#7fc97f', alpha=a)
    plt.axvspan(10000, 20000, facecolor='#f4cae4', alpha=a)
    plt.axvspan(20000, 30000, facecolor='#cbd5e8', alpha=a)
    plt.axvspan(30000, 40000, facecolor='#7fc97f', alpha=a)
    plt.axvspan(40000, 50000, facecolor='#f4cae4', alpha=a)

    plt.legend()

    plt.show() 

changing_parameters()