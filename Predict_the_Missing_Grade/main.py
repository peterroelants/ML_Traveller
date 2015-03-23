import json
import numpy as np
import fileinput
import pickle
import zlib
import base64
import sklearn.linear_model


serialized_model="""eNp9U02P0zAQvc/PWCTay1Z2viMh9rBoUTn0QJE4UBQ5jpMNmybGdndbCfHbeZMsLBc4uHbefL15
M9V6spfKmY7wo6fRB3fSYXJkBa21fxiMcuNm6Efc1XFqzLDxYdL3yodeV51TTW/GQPv37z6azhnv
OVSSrqr61A+hH6uKpvqb0YFsRLtgY/poE1o3NqX96km5Y+WDcmFFNqOtEOT3q2HyHt85HIz1/TCN
VT96M/o+9I8GloK9bvEo6U5u5hh/f2rbgY1S/M7zaFw9+RmTwBhq+4BcwThtLNeUEQySLc+VGItJ
j6ejvWz05MzmeEIbyjl1Ia/VoLg/NLC4UBMu1gBJaY3sBYdzH7SVFKzM0awsaL2N0csbNpa02+22
1+BzPXMKNhJU71eHsxD/O4iNOGUUIWUUzzLxaPqxq5wK3GSUoEg/PjJLwIyk7Af10DB/gtmMWDOq
IVwYYpGHiF+zqHZ6Mq5iZSJoKzZLBqfGZpoHNReKBe2Ahorfku7yJCnzbJmDCYq5xhFHL8oOkhn2
E8Mxw3JOqgZ7rxhLqGNBOwi1X6XqcC7KL+L14Vy2b9mcous4Q9dxzmF6Mu1cuPjXlP5eZPiVf2Y1
NouDTbDbs/aJRMka2ZKIv+bdBBUMb70tGUmJafE+7a9upQE38GswERMfznV5A5YA6gwGHA2wKa/x
U8OigNTF4SwbAO0HII1muM2B40icMsLNGRpYhEaKHFGNwT60CNUF4Fb9/LEUlYJt8OY8JR6cSqZg
k+CO8WhiDsj6pbrQ3x9gzIAVoNbWcEh3X1/hym6u0HXGPeZUe16c538Fi5sU1LFw3YtSJXWzSKmA
SKl8FolXMo1eRFpJkJZXn1DffAZHUKpbJExjdkxQqd78AixwWC8=
"""

# Courses:
# Create a list that holds the courses
course_list = [
    'Mathematics', # 0
    'English', # 1
    'Physics', # 2
    'Chemistry', # 3
    'ComputerScience', # 4
    'Hindi', # 5
    'Biology', # 6
    'PhysicalEducation', # 7
    'Economics', # 8
    'Accountancy', # 9
    'BusinessStudies' # 10
]
# Create dictionary to hold index values so that these can easily be found when needed.
index_dict = dict()
for i in xrange(len(course_list)):
    index_dict[course_list[i]] = i
number_of_courses = len(index_dict)

# Mathematics needs to be predicted
# Hindi has never a grade in the training set
# English is always present
# There are 8 remaining classes, of which each time 3 are chosen

# Define the course columns to extract for the X matrix
# Mathematics needs to be predicted
# Hindi doesnt have any grades in the test set
X_columns = [1,2,3,4,6,7,8,9,10]


def get_json_courses(sample_line):
    """
    Function to extract a json object with grades from sample_line.
    Get each course from this json object and return as a vector
    """
    x = np.zeros((number_of_courses,), dtype=np.int)
    sample = json.loads(sample_line)
    for course, grade in sample.iteritems():
        if course != 'serial':
            x[index_dict[course]] = grade
    return x


def predict_integer_grade(model, x):
    """
    Make predictions for x with the given model.
    """
    output = model.predict(x)
    output = np.round(output).astype(int)
    # make sure the output is between 1, and 8.
    # since an error of 1 can be made, the minimum prediction is 2, maximum is 7
    output[output < 2] = 2
    output[output > 7] = 7
    return output


def main():
    # Get the model
    model = pickle.loads(zlib.decompress(base64.decodestring(serialized_model)))

    # Read the input and make predictions
    inp = fileinput.input()
    nb_of_samples = int(next(inp))
    XY = np.zeros((nb_of_samples, number_of_courses), dtype=np.int)
    for idx, line in enumerate(inp):
        x = get_json_courses(line)
        XY[idx, :] = x
    X_test = XY[:, X_columns]
    # Make and print predictions
    output = predict_integer_grade(model, X_test)
    for p in output:
        print p

if __name__ == '__main__':
    main()