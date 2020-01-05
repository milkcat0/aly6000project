
import pprint as pp
import matplotlib.pyplot as plt
import pandas as pd
import xlrd
import numpy as np

import plotly
import plotly.graph_objs as go
plotly.offline.init_notebook_mode(connected=True)

class UsPopulation:
    """
        A module used to help conducting US car statistical analysis
    """
    def __init__(self, filename: object = 'uspopulation.xlsx', debug_mode: object = True) -> object:
        self._debug_mode = debug_mode
        self.filename = filename
        self.population_stats = {}

    def extract(self):
        """
            A helper function to load/ import raw data
        """
        book = xlrd.open_workbook(filename=self.filename)
        sheet = book._sheet_list[0]

        self.raw_data = sheet._cell_values
        if self._debug_mode:
            print("Loaded raw data with %s rows in raw data" % len(self.raw_data))

        return self

    def transform(self):
        """
            A helper function to manipulate raw data and convert
            them into useful data structure for downstream analytics

            population stats dict schema:
            |- state
                |- city
                    |- 2017 US Population
                    |- Net Domestic Migration
                    |- Domestic Migration Rate
                    |- International Migration Rate
                    |- Natural Change
        """
        # Hard code and only take useful header item
        self.header = [item for item in self.raw_data.pop(0) if item][2:]
        for row in self.raw_data:
            city = row[2].split(', ')[0]
            state = row[2].split(', ')[1]
            stats = [row[3], row[4], row[5], row[6],row[7],row[8]]

            # Add state if not exist
            if state not in self.population_stats:
                self.population_stats[state] = {}

            # Add city if state is present but not city
            if state in self.population_stats and city not in self.population_stats[state]:
                self.population_stats[state][city] = {}

            # If both city and state are presented, add detail information
            if state in self.population_stats and city in self.population_stats[state]:
                for i, key in enumerate(self.header):
                    self.population_stats[state][city][key] = stats[i]

            # Print stats
            if self._debug_mode:
                self.print_dict()

        return self

    def us_top_10_states_2017(self):
        """
            Top 10 states with the highest population 2017
        """
        targeted_key = self.header[0]  # 2017 Us Population
        top_10_states_2017 = {}
        # Find the state and state dic
        state_count = 0
        city_count = 0
        # through the state level
        for state, state_lvl_dict in self.population_stats.items():
            state_count += 1
            total_state_population = 0
            # Find city and city dic
            for city, city_lvl_dict in state_lvl_dict.items():
                total_state_population += city_lvl_dict.get(targeted_key, 0)
                city_count  += 1

            top_10_states_2017[state] = total_state_population
            # print('state: %s, city: %s, %s: %s' %(state, city, self.header[2], city_lvl_dict[self.header[2]]))
        return sorted(top_10_states_2017.items(), key=lambda x: x[1], reverse=True)[:10]

    # def qq(self):
    #     domestic_migration_rate = []
    #     cities=[]
    #     targeted_key = self.header[2]  # 2017 domestic_migration rate
    #     # Find the state and state dic
    #     for state, state_lvl_dict in self.population_stats.items():
    #         for city, city_lvl_dict in state_lvl_dict.items():
    #             a = city_lvl_dict.get(targeted_key, 0)
    #             domestic_migration_rate.append(a)
    #     return cities, domestic_migration_rate

    def domestic_migration(self, func):

        self.domestic_migration_rate_list = []
        cities = []
        targeted_key = self.header[2] # 2017 domestic_migration rate
        for state, state_lvl_dict in self.population_stats.items():
            for city, city_lvl_dict in state_lvl_dict.items():
                b = city_lvl_dict.get(targeted_key, 0)
                self.domestic_migration_rate_list.append(b)
        # Find the range
        max_num = max(self.domestic_migration_rate_list)
        min_num = min(self.domestic_migration_rate_list)
        num_of_records = len(self.domestic_migration_rate_list)
        diff = max_num - min_num
        num_of_bins = 10
        increment = diff / 10
        # Find the bins
        index = min_num
        freq_interval_dict = {}
        key_list = []

        for i in range(num_of_bins):
            freq_interval_dict[index] = {'occurance': 0}
            key_list.append(index)
            index = index + increment

        freq_interval_dict = func(
            increment=increment, key_list=key_list, domestic_migration_rate_list=self.domestic_migration_rate_list, freq_interval_dict=freq_interval_dict)
        for k, v in freq_interval_dict.items():
            freq_interval_dict[k]['frequency']=v['occurance'] / num_of_records

        if self._debug_mode:
            pp.pprint(num_of_records)

        return freq_interval_dict

    def a(self, increment, key_list, domestic_migration_rate_list, freq_interval_dict):

        # Iterate through the list of numbers
        for num in domestic_migration_rate_list:
            for i, value in enumerate(key_list):
                if num - value < increment and (num - value) >= 0:
                    freq_interval_dict[key_list[i]]['occurance'] += 1
        return freq_interval_dict

    def b(self, increment, key_list, domestic_migration_rate_list, freq_interval_dict):
        for num in domestic_migration_rate_list:
            for i, value in enumerate(key_list):
                if num - value < increment:
                    freq_interval_dict[key_list[i]]['occurance'] += 1
        return freq_interval_dict


    def domestic_migration_table(self):
        """
            Get table
        """
        domestic_migration_rate_list = []
        cities = []
        targeted_key = self.header[2] # 2017 domestic_migration rate

        for state, state_lvl_dict in self.population_stats.items():
            for city, city_lvl_dict in state_lvl_dict.items():
                b = city_lvl_dict.get(targeted_key, 0)
                domestic_migration_rate_list.append(b)
        return cities, domestic_migration_rate_list

    def get_domestic_migration_rates(self):
        """
            Get table
        """
        domestic_migration_rate_list = []
        targeted_key = self.header[2] # 2017 domestic_migration rate

        for state, state_lvl_dict in self.population_stats.items():
            for city, city_lvl_dict in state_lvl_dict.items():
                b = city_lvl_dict.get(targeted_key, 0)
                domestic_migration_rate_list.append(b)
        return domestic_migration_rate_list

    def get_international_migration_rates(self):
        """
            Get table
        """
        international_migration_rate_list = []
        targeted_key = self.header[4] # 2017 domestic_migration rate

        for state, state_lvl_dict in self.population_stats.items():
            for city, city_lvl_dict in state_lvl_dict.items():
                b = city_lvl_dict.get(targeted_key, 0)
                international_migration_rate_list.append(b)
        return international_migration_rate_list



    # def household_with_car_2016(self):
    #     """
    #         get info from household with car 2016
    #     """
    #     has_car_2016_list = []
    #     cities = []
    #     targeted_key = self.header[3] # 2016 household with cars
    #
    #     for state, state_lvl_dict in self.car_stats.items():
    #         for city, city_lvl_dict in state_lvl_dict.items():
    #             has_car_2016 = city_lvl_dict.get(targeted_key, 0)
    #             has_car_2016_list.append(has_car_2016)
    #             cities.append(city)
    #     if self._debug_mode:
    #         print(has_car_2016_list)
    #
    #     return cities, has_car_2016_list





    # graph
    def plot_histogram_chart(self,data, rate, x,y,title):

        # cf.set_config_file(offline=False, world_readable=True, theme='pearl')

        trace = go.Histogram(
            x=rate,
            y=[v['frequency'] for k, v in data.items()],
            histnorm='probability'
        )

        data = [trace]
        layout = go.Layout(
            title='Relative Frequency of Dometic Migration Rate',
            yaxis=dict(title='Relative Frequency'),
            xaxis=dict(title='Domestic Migration Rate')
        )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig)


    def plot_scatter_chart(self, x, y, x_value, y_value, title):

        plt.scatter(x_value, y_value, marker='.', c='b')
        plt.xlabel(x, fontsize=16)
        plt.ylabel(y, fontsize=16)
        plt.title(title, fontsize=20)
        plt.show()


    def plot_bar_chart(self,data,x,y,title):
        df = pd.DataFrame({
            x:[round(key, 4) for key in data.keys()] ,
            y: [v['frequency'] for k, v in data.items()]
        })
        # df = pd.Series(df)
        # df.plot(kind='bar', x=x, y=y, legend=None, title=title)
        df.plot(kind='bar' , x=x, y=y, title=title)
        plt.show()

    # Plot line chart
    def line_chart(self, data,x,y,title):
        df = pd.DataFrame({
            x:[round(key, 4) for key in data.keys()],
            y:[v['occurance'] for k, v in data.items()]})
        df.plot(kind='line', x=x, y=y, legend=None, title=title)
        plt.show()

    def plot_pareto_chart(self, data, x, y, title, show_pct_y=False, pct_format='{0:.0%}'):
        """
            Serve as a baseline util for graphing
        """
        states = []
        population = []

        for (state, total) in data:
            states.append(state)
            population.append(total)

        df = pd.DataFrame({
            x: states,
            y: population
        })

        xlabel = x
        ylabel = y
        tmp = df.sort_values(y, ascending=False)
        x = tmp[x].values
        y = tmp[y].values
        weights = y / y.sum()
        cumsum = weights.cumsum()

        fig, ax1 = plt.subplots()
        ax1.bar(x, y)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)

        ax2 = ax1.twinx()
        ax2.plot(x, cumsum, '-ro', alpha=0.5)
        ax2.set_ylabel('', color='r')
        ax2.tick_params('y', colors='r')

        vals = ax2.get_yticks()
        ax2.set_yticklabels(['{:,.2%}'.format(x) for x in vals])

        # hide y-labels on right side
        if not show_pct_y:
            ax2.set_yticks([])

        formatted_weights = [pct_format.format(x) for x in cumsum]
        for i, txt in enumerate(formatted_weights):
            ax2.annotate(txt, (x[i], cumsum[i]), fontweight='heavy')

        if title:
            plt.title(title)

        plt.tight_layout()
        plt.show()

    # create table chart
    def de_chart(self,y):
        d = {
             'Domestic Migration Rate Table': pd.Series(y)}

        # Create a DataFrame
        df = pd.DataFrame(d)

        self.df = df
        # return df


    # def print_dict(self):
    #     for state, state_lvl_info in self.car_stats.items():
    #         print("\n\n--------------------------\nState: %s\n--------------------------" % state)
    #
    #         for city, city_lvl_info in state_lvl_info.items():
    #             print("City: %s" % city)
    #             print(city_lvl_info)






if __name__ == "__main__":
    c = UsPopulation(debug_mode=False)
    c.extract()
    c.transform()
    c.us_top_10_states_2017()


    # Question 1
    # top_10_states = c.us_top_10_states_2017()
    # print(top_10_states)
    # c.plot_pareto_chart(data=top_10_states, x='States', y='Population',
    # title = 'Top 10 States with The Highest Population in 2017.')

    #Question 2
    # q=c.domestic_migration(func=c.a)

    # data = c.domestic_migration(func=c.a)
    # pp.pprint(data)
    # c.plot_histogram_chart(data= data, rate=c.domestic_migration_rate_list, x='Bins', y='Relative Freq', title='Relative Frequency domestic migration rate')


    # Question 3:
    # q=c.domestic_migration(func=c.b)
    # data = c.domestic_migration(func=c.b)
    # c.line_chart(data=data, x='Bins', y='Cumulative Frequency', title=' Cumulative Frequency of Domestic Migration Rate”')

    # Question 4
    # q=c.domestic_migration_table()
    # cities, domestic_migration_rate_list = q
    # c.de_chart(y=domestic_migration_rate_list)
    # print(c.df.describe())
    # print('median: %s' % c.df.median())
    # print('variance: %s' % c.df.var())
    # print('skew: %s' % c.df.skew())
    # print('kurtosis: %s' % c.df.kurtosis())
    # print('mode: %s' % c.df.mode())




    # Question 5
    """
    For the “Domestic Migration Rate” for all counties, determine whether there are any
    outliers. Comment on the states to which the outliers belong.
    """
    # Q3 = 1.6
    # Q1 =0.2
    #
    # IQR = Q3 - Q1
    #
    # max = Q3 + 1.5 * IQR
    # min = Q1 - 1.5 * IQR
    # print('Max: %s' % max)
    # print('Min: %s' % min)
    #
    # outliers = []
    #
    # for state, state_lvl_dict in c.population_stats.items():
    #     for city, city_lvl_dict in state_lvl_dict.items():
    #         rate = city_lvl_dict[c.header[4]]
    #         if rate > max or rate < min:
    #             outliers.append((state, city, rate))
    #
    # print('Number of outliers: %s' % len(outliers))
    #
    # small_outliers = [(s, c, r) for s, c, r in outliers if r > max]
    # large_outliers = [(s, c, r) for s, c, r in outliers if r < min]
    #
    # print('Number of outliers greater than max: %s' % len(small_outliers))
    # print('Number of outliers smaller than min: %s' % len(large_outliers))
    #
    # pp.pprint('Small outliers: %s\n' % [s for s, _, _ in small_outliers])
    # pp.pprint('Large outliers: %s\n' % [s for s, _, _ in large_outliers])
    # pp.pprint(outliers)

    # # Question 7
    # """
    # #Create a scatter plot of the (“International Migration Rate” versus “Domestic
    # Migration Rate”. Use the scatter plot to describe whether there exists a correlation
    # between the two quantities above. Interpret their correlation in words.

    # dmr = c.get_domestic_migration_rates()
    # imr = c.get_international_migration_rates()
    #
    # c.plot_scatter_chart(
    #     x='International Migration Rate', y='Domestic Migration Rate', x_value=imr, y_value=dmr,
    #     title='"International Migration Rate" versus "Domestic Migration Rate"')





