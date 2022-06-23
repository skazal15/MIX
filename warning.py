import telebot
import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from analis import all_data, m
file1 = open("user.txt","r+")  
lines = file1.read().split(',')
lines=[x for x in lines if x != '']
bot = telebot.TeleBot("1647991895:AAGqPjhkOSbsuSdycrLrikffs7kiR2-JTzM")
for i in range(len(m)):
    print(all_data[i][7])
    if all_data[i][7].lower() == 'emas1':
        per=round(all_data[i][8],2)
        if per >= 70:
            mon=all_data[i][7]
            dat=all_data[i][1]
            df=all_data[i][11]
            mon=str(mon)
            dat=str(dat)
            per=str(per)
            matplotlib.use('Agg')
            plt.ioff()
            plt.style.use("dark_background")
            for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
                plt.rcParams[param] = '0.9'  # very light grey
            for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
                plt.rcParams[param] = '#212946'  # bluish dark grey
            colors = [
                '#08F7FE',  # teal/cyan
                '#FE53BB',  # pink
                '#F5D300',  # yellow
                '#00ff41',  # matrix green
                ]
            fig, ax = plt.subplots()
            df.plot(marker='o', color=colors, ax=ax)
            # Redraw the data with low alpha and slighty increased linewidth:
            n_shades = 10
            diff_linewidth = 1.05
            alpha_value = 0.3 / n_shades
            for n in range(1, n_shades+1):
                df.plot(marker='o',
                        linewidth=2+(diff_linewidth*n),
                        alpha=alpha_value,
                        legend=False,
                        ax=ax,
                        color=colors)
            # Color the areas below the lines:
            for column, color in zip(df, colors):
                ax.fill_between(x=df.index,
                                y1=df.values,
                                color=color,
                                alpha=0.1)
            ax.grid(color='#2A3459')
            ax.set_xlim([ax.get_xlim()[0] - 0.2, ax.get_xlim()[1] + 0.2])  # to not have the markers cut off
            ax.set_ylim(0)
            plt.title('prediction')
            plt.ylabel('%')
            plt.savefig('harga.png')
            img = open('harga.png', 'rb')      
            for t in range(len(lines)):
                bot.send_message(lines[t], 'warning ⚠️ ,utilisasi storage sistem '+ mon +' diprediksi akan mencapai '+ per + ' pada tanggal: '+ dat)
                bot.send_message(lines[t], 'grafik utilisasi storage sistem '+ mon )
                bot.send_photo(lines[t], img)