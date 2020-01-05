import xlrd


class Project2_Solution(object):
    all_project_data = []
    count_Q = 0
    count_S = 0
    count_C = 0
    count_p0 = 0
    count_p1 = 0
    count_p2 = 0
    count_p3 = 0
    count_p4 = 0
    count_p5 = 0
    count_p6 = 0
    count_p7 = 0

    def __init__(self, file_name=None, sheet=None):
        self.file_name = file_name
        self.sheet = sheet

    def load_data(self):
        excel_data = xlrd.open_workbook(self.file_name)
        all_data = excel_data.sheets()[self.sheet]
        rows = all_data.nrows
        cols = all_data.ncols

        for per_row in range(1, rows):
            per_line = {}
            for per_col in range(cols):
                field = all_data.cell_value(0, per_col)
                val = all_data.cell_value(per_row, per_col)
                per_line[field] = val
            self.all_project_data.append(per_line)

    def print_data(self):
        for per_line in self.all_project_data:
            print(per_line)

    def digger_data(self):
        for per_line in self.all_project_data:
            per_line['Q'] = 0
            per_line['S'] = 0
            per_line['C'] = 0
            if per_line['Quality Score'] > 750:
                per_line['Q'] = 1
                self.count_Q += 1
            if per_line['Process Days'] < 15:
                per_line['S'] = 2
                self.count_S += 1
            if per_line['Project Cost'] < 222000:
                per_line['C'] = 3
                self.count_C += 1

            per_line['Score'] = self.valid_score(per_line['Q'], per_line['S'], per_line['C'])

    def valid_score(self, q, s, c):
        if q != 1 and s != 2 and c != 3:
            self.count_p0 += 1
            return 0
        if q == 1 and s != 2 and c != 3:
            self.count_p1 += 1
            return 1
        if q != 1 and s == 2 and c != 3:
            self.count_p2 += 1
            return 2
        if q != 1 and s != 2 and c == 3:
            self.count_p3 += 1
            return 3
        if q == 1 and s == 2 and c != 3:
            self.count_p4 += 1
            return 4
        if q == 1 and s != 2 and c == 3:
            self.count_p5 += 1
            return 5
        if q != 1 and s == 2 and c == 3:
            self.count_p6 += 1
            return 6
        if q == 1 and s == 2 and c == 3:
            self.count_p7 += 1
            return 7
        return 0


if __name__ == '__main__':
    p2 = Project2_Solution("project2_data.xls", 0)
    p2.load_data()
    p2.print_data()
    p2.digger_data()
    #
    p2.print_data()
    # # Part1
    # print("the count of Q is {}, and the probability is {}".format(p2.count_Q, p2.count_Q / len(p2.all_project_data)))
    # print("the count of S is {}, and the probability is {}".format(p2.count_S, p2.count_S / len(p2.all_project_data)))
    # print("the count of C is {}, and the probability is {}".format(p2.count_C, p2.count_C / len(p2.all_project_data)))
    #
    # # Part2
    # print("the count of Score = 0 is {}, and the probability is {}".format(p2.count_p0,
    #                                                                        p2.count_p0 / len(p2.all_project_data)))
    # print("the count of Score = 1 is {}, and the probability is {}".format(p2.count_p1,
    #                                                                        p2.count_p1 / len(p2.all_project_data)))
    # print("the count of Score = 2 is {}, and the probability is {}".format(p2.count_p2,
    #                                                                        p2.count_p2 / len(p2.all_project_data)))
    # print("the count of Score = 3 is {}, and the probability is {}".format(p2.count_p3,
    #                                                                        p2.count_p3 / len(p2.all_project_data)))
    # print("the count of Score = 4 is {}, and the probability is {}".format(p2.count_p4,
    #                                                                        p2.count_p4 / len(p2.all_project_data)))
    # print("the count of Score = 5 is {}, and the probability is {}".format(p2.count_p5,
    #                                                                        p2.count_p5 / len(p2.all_project_data)))
    # print("the count of Score = 6 is {}, and the probability is {}".format(p2.count_p6,
    #                                                                        p2.count_p6 / len(p2.all_project_data)))
    # print("the count of Score = 7 is {}, and the probability is {}".format(p2.count_p7,
    #                                                                        p2.count_p7 / len(p2.all_project_data)))
    # part3
    # #Abc, aBc, ABc, abC, AbC, aBC, ABC
    #     venn3(subsets=(7, 10, 2, 10, 3, 5, 5), set_labels=('Q', 'S', 'C'))
    #     plt.show()
    # part4

    # a) Of those who satisfied Cost, what percentage also satisfied Speed?
    #  if q != 1 and s != 2 and c == 3:
    #  count_a_1 = 0
    # count_a_2 = 0

    # for per_line in p2.all_project_data:
        # if per_line['C'] == 3:
            # count_a_1 += 1
            # if per_line["S"] == 2:
                # count_a_2 += 1
    # print("the count of a is {}, and the probability is {}".format(count_a_2, count_a_2 / count_a_1))

    # b) Of those who satisfied Quality, what percentage also satisfied Cost?

    # count_b_1 = 0
    # count_b_2 = 0

    # for per_line in p2.all_project_data:
        # if per_line['Q'] == 1:
            # count_b_1 += 1
            # if per_line["C"] == 3:
                # count_b_2 += 1
    # print("the count of b is {}, and the probability is {}".format(count_b_2, count_b_2 / count_b_1))

    # c) Of those who satisfied Quality, what percentage also satisfied Speed but did not satisfy the Cost?

    count_c_1 = 0
    count_c_2 = 0

    for per_line in p2.all_project_data:
        if per_line['Q'] == 1:
            count_c_1 += 1
            if per_line["C"] != 3 and per_line["S"] == 2:
                count_c_2 += 1
    print("the count of c is {}, and the probability is {}".format(count_c_2, count_c_2 / count_c_1))

    # d) Of those who satisfied Cost, what percentage also satisfied Speed but did not satisfy the Quality?

    count_d_1 = 0
    count_d_2 = 0

    for per_line in p2.all_project_data:
        if per_line['C'] == 3:
            count_d_1 += 1
            if per_line["Q"] != 1 and per_line["S"] == 2:
                count_d_2 += 1
    print("the count of d is {}, and the probability is {}".format(count_d_2, count_d_2 / count_d_1))
    # e) Of those who did not satisfy Speed, what percentage satisfied Quality and Cost?

    count_e_1 = 0
    count_e_2 = 0

    for per_line in p2.all_project_data:
        if per_line['S'] != 2:
            count_e_1 += 1
            if per_line["Q"] == 1 and per_line["C"] == 3:
                count_e_2 += 1
    print("the count of e is {}, and the probability is {}".format(count_e_2, count_e_2 / count_e_1))

    # f) What percentage satisfied exactly two of the three criteria?

    count_f_1 = len(p2.all_project_data)
    count_f_2 = p2.count_p4+p2.count_p5+p2.count_p6
    print("the count of f is {}, and the probability is {}".format(count_f_2, count_f_2 / count_f_1))


    # g) Of those who satisfied at least one of the three criteria, what percentage satisfied exactly one criterion?

    count_g_1 = len(p2.all_project_data)-p2.count_p0
    count_g_2 = p2.count_p1+p2.count_p2+p2.count_p3
    print("the count of g is {}, and the probability is {}".format(count_g_2, count_g_2 / count_g_1))

    # h) Of those who did not satisfy Cost, what percentage satisfied the Speed criterion?

    count_h_1 = 0
    count_h_2 = 0

    for per_line in p2.all_project_data:
        if per_line['C'] != 3:
            count_h_1 += 1
            if per_line["S"] == 2:
                count_h_2 += 1
    print("the count of h is {}, and the probability is {}".format(count_h_2, count_h_2 / count_h_1))

