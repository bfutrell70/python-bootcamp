import pandas

student_dict = {
    "student": ['Angela', 'James', 'Lily'],
    "score": [56, 76, 98]
}

# for (key, value) in student_dict.items():
#     print(value)


student_data_frame = pandas.DataFrame(student_dict)
# print(student_data_frame)

# # loop through a data frame
# for (key, value) in student_data_frame.items():
#     print(value)

# loop through rows of a data frame
for (index, row) in student_data_frame.iterrows():
    # print(index)
    # print(row.student, row.score)
    if row.student == 'Angela':
        print(row.score)