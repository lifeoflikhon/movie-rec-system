# importing modules
import csv
import operator
from prettytable import from_csv

# getting csv file from disk
filename = "movie_1000.csv"

# opening file for read
file = open(filename, newline='')
reader = csv.reader(file)

# separating header from other rows
header = next(reader)

# creating empty list to store data later
listByRating = []
listByYear = []
listByDuration = []

# storing data by rating, year, and duration
for row in reader:
    # [director_name, duration, genres, movie_title, title_year, imdb_score]
    movieTitle = str(row[3])
    genres = str(row[2])
    if row[1] == '':
        row[1] = '0'
    duration = int(row[1])
    directorName = str(row[0])
    if row[4] == '':
        row[4] = '0'
    titleYear = int(row[4])
    imdbScore = float(row[5])
    listByRating.append([movieTitle, genres, directorName, imdbScore])
    listByYear.append([movieTitle, genres, directorName, titleYear])
    listByDuration.append([movieTitle, genres, directorName, duration])

# sorting every list in descending order
sortedRating = sorted(listByRating, key=operator.itemgetter(3), reverse=True)
sortedYear = sorted(listByYear, key=operator.itemgetter(3), reverse=True)
sortedDuration = sorted(listByDuration, key=operator.itemgetter(3), reverse=True)

# getting category from user
def get_category():
    try:
        print("Leave it empty to see all category")
        category = str(input("Enter category: ")).title()
        return category
    except ValueError:
        print("Please enter a valid category.")
        get_category()


# getting sorting criteria from user
def get_sorting_criteria():
    try:
        print("\n1. Rating\t2. Duration\t3. Year")
        sc = int(input("How you want to sort movies?[1/2/3]: "))
        if sc == 1:
            return 'Rating'
        elif sc == 2:
            return 'Duration'
        elif sc == 3:
            return 'Year'
        else:
            print("Please select between 1-3")
            get_sorting_criteria()
    except ValueError:
        print("Please enter a valid value between 1-3")
        get_sorting_criteria()

# showing data to user as they want
def show_data(category, base, list):
    # creating new file to store the sorted data
    with open(".sorted_file.csv", 'w', newline='') as sortedFile:

        # writing header
        writer = csv.DictWriter(sortedFile, fieldnames=['Serial', 'Movie', 'Genres', 'Director', base])
        writer.writeheader()

        # initializing counter to track the serial
        count = 1
        for i in list:

            # checking if the genre row contains the given category or not
            if i[1].__contains__(category):
                writer.writerow({'Serial': count, 'Movie': i[0], 'Genres': i[1], 'Director': i[2], base: i[3]})

                # limiting the data to 20 for simplifying to user
                if count == 20:
                    break
                count = count + 1

    # displaying the data in tabular form
    x = from_csv(open('.sorted_file.csv', newline=''))
    print(x)


# executing the app until user close it
while True:
    # getting category from user
    category = get_category()

    # getting criteria from user
    base = get_sorting_criteria()

    # displaying data as user wanted to see
    if base == 'Rating':
        show_data(category, base, sortedRating)
    elif base == 'Duration':
        show_data(category, base, sortedDuration)
    else:
        show_data(category, base, sortedYear)
