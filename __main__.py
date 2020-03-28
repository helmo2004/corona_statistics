import csv
import collections
import numpy
import re
from datetime import datetime
from matplotlib import pyplot as plt
import urllib

csv_source = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"
treshold = 100


def process_country(country, data_dict, image_file_name):
    print "process country {}".format(country)
    dates_dict = {}

    # filter data
    for k, v in data_dict.iteritems():
        if (re.match('\d+/\d+/\d+', k) and float(v) > treshold):
            date_time = datetime.strptime(k, '%m/%d/%y')
            dates_dict[date_time] = float(v)

    # sort data
    dates_dict = collections.OrderedDict(sorted(dates_dict.items()))

    lists = sorted(dates_dict.items())
    d, number_of_deseases = zip(*lists)
    number_of_new_deseases = [0] + list(numpy.diff(number_of_deseases))

    # calculate doubling rate
    rate = numpy.divide(number_of_deseases[1:], number_of_deseases[:-1])
    log2_vector = numpy.full((len(rate)), numpy.log(2))
    doubling_rate = [0.0] + list(numpy.divide(log2_vector, numpy.log(rate)))

    labelx = -0.12

    # total number of deseases
    ax1 = plt.subplot(411)
    plt.title(country + " (Source: Johns Hopkins)")
    plt.ylabel("Number of corona")
    plt.grid(True)
    plt.plot(d, number_of_deseases)
    plt.gcf().autofmt_xdate()
    ax1.yaxis.set_label_coords(labelx, 0.5)

        # total number of deseases
    ax2 = plt.subplot(412)
    plt.grid(True)
    plt.yscale("log")
    plt.plot(d, number_of_deseases)
    plt.gcf().autofmt_xdate()
    ax2.yaxis.set_label_coords(labelx, 0.5)

    # new deseases
    ax3 = plt.subplot(413, sharex=ax1)
    plt.ylabel("Delta")
    plt.grid(True)
    plt.bar(d, number_of_new_deseases, width=0.4)
    plt.gcf().autofmt_xdate()
    ax3.yaxis.set_label_coords(labelx, 0.5)

    # doubling rate
    ax4 = plt.subplot(414, sharex=ax1)
    plt.ylabel("Doubling Rate")
    plt.grid(True)
    plt.bar(d, doubling_rate, width=0.4)
    plt.gcf().autofmt_xdate()
    ax4.yaxis.set_label_coords(labelx, 0.5)

    plt.savefig(image_file_name)
    plt.clf()


if __name__ == "__main__":
    file_name = "data.csv"
    print "get {}".format(file_name)
    urllib.urlretrieve(csv_source, filename=file_name)
    with open(file_name) as csvfile:
        dict_reader = csv.DictReader(csvfile, delimiter=',')
        countries = ['Austria', 'Italy', 'Germany', 'Spain', 'Turkey']
        processed_countries = []
        for data_dict in dict_reader:
            current_country = data_dict['Country/Region']
            if current_country in countries:
                image_file_name = current_country + ".png"
                process_country(current_country, data_dict, image_file_name)
                processed_countries.append(current_country)
    if sorted(countries) != sorted(processed_countries):
        print "Error: could not process all countries. Not found: {}".format(list(set(countries) - set(processed_countries)))
    print "done"