import requests
import time
from datetime import datetime, timedelta, time as time2

from audiobookshelfapi import api, Config
import Objects as ob
import json
import audiobookshelfenums

#Settings
NUM_BOOKS_TO_ENCODE = Config.Number_of_books_to_encode
TIME_BETWEEN_CHECKS = Config.Time_between_checks
START_TIME = Config.StartTime
END_TIME = Config.EndTime


IP = Config.URL
APITOKEN = Config.APIToken
LIBRARYNAME = Config.LibraryName

# functions for time conversions
def sec_to_time_str(seconds):
    hours = seconds // 3600
    if hours < 10:
        hours = f"0{hours}"
    else:
        hours = str(hours)

    minutes = (seconds // 60) % 60
    if minutes < 10:
        minutes = f"0{minutes}"
    else:
        minutes = str(minutes)

    seconds = seconds % 60
    if seconds < 10:
        seconds = f"0{seconds}"
    else:
        seconds = str(seconds)

    time = f"{hours}:{minutes}:{seconds}"
    return time


def is_hour_between(start_hour, end_hour, target_hour):
    # Convert start_hour, end_hour, and target_hour to time objects
    start_time = time2(start_hour, 0)
    end_time = time2(end_hour, 0)
    target_time = time2(target_hour, 0)

    # If start time is before end time, check if target time is between them
    if start_time <= end_time:
        return start_time <= target_time <= end_time
    # If start time is after end time, check if target time is not between them
    else:
        return not (end_time < target_time < start_time)


def time_to_seconds(t):
    return t.hour * 3600 + t.minute * 60 + t.second


def seconds_between_now_and_start(start_hour):
    # Get current time
    current_time = datetime.now().time()

    # Convert start_hour to a time object
    start_time = time2(start_hour, 0)

    # Convert current time and start time to seconds
    current_seconds = time_to_seconds(current_time)
    start_seconds = time_to_seconds(start_time)

    # Calculate the difference
    if current_seconds <= start_seconds:
        return start_seconds - current_seconds
    else:
        # If start time is after current time, calculate the remaining seconds until the start time of the next day
        return (24 * 3600 - current_seconds) + start_seconds


# conditions for when a book is no longer encoding
def can_encode(lib_item):
    return (not lib_item.isMissing) and (not lib_item.isInvalid) and lib_item.media.numAudioFiles > 1


def encode_books(a, lib):
    # Get the initial count of multitrack books
    books = a.get_all_library_items(lib.id)
    # Remove any books that are not multitrack
    books = [book for book in books if book.media.numAudioFiles > 1]

    converted_ids = []
    encoding_books_time = []

    while len(books) > 0:
        # if outside of time to update books then wait
        if not is_hour_between(START_TIME, END_TIME, datetime.now().hour):
            sleep_time = seconds_between_now_and_start(START_TIME)
            print(f"\nSleeping until {START_TIME}, {sleep_time} seconds")
            time.sleep(sleep_time)

        print("\n-----------------------------------------------------------------------------")
        # get the list books that are multitrack and sort them by duration
        books = a.get_all_library_items(lib.id)
        total_books = len(books)
        books = [book for book in books if book.media.numAudioFiles > 1 and book.id not in converted_ids]
        books.sort(key=lambda x: x.media.duration)

        # print status of the library
        print(f"Total Books: {total_books}, Multitrack books: {str(len(books))},"
              f" Books converted: {str(len(converted_ids))}")

        # Fill the encoding_books list until full or there are no books left
        while len(books) > 0 and len(encoding_books_time) < NUM_BOOKS_TO_ENCODE:
            new_multitrack_book = books.pop(0)
            encoding_books_time.append((new_multitrack_book, datetime.now()))
            print(f'Starting encode of {new_multitrack_book.media.metadata['title']},'
                  f' Duration: {str(timedelta(seconds=new_multitrack_book.media.duration))} at {datetime.now()}')
            a.post_encode_m4b(new_multitrack_book.id)
            converted_ids.append(new_multitrack_book.id)

        while len(encoding_books_time) == NUM_BOOKS_TO_ENCODE:
            # Wait between checking on the books
            time.sleep(TIME_BETWEEN_CHECKS)

            # update the list of books
            server_books = a.get_all_library_items(lib.id)
            multitrack_books_ids = [book.id for book in server_books if book.media.numAudioFiles > 1]

            # check if each book being encoded is not in the list of multitrack books
            completed_book_time = []
            progress_str = '\r\033[KCurrent Books Encoding'
            for i, book_time in enumerate(encoding_books_time):
                time_elapsed = (datetime.now() - book_time[1]).seconds
                if book_time[0].id not in multitrack_books_ids:
                    print(f"\r\033[KSuccessfully encoded! Book: {book_time[0].media.metadata['title']},"
                          f" Time encoding: {sec_to_time_str(time_elapsed)}", end="\n")
                else:
                    progress_str += (f", Book: {book_time[0].media.metadata['title']},"
                                     f" Time encoding: {sec_to_time_str(time_elapsed)}")

            # remove books that have been converted
            encoding_books_time = [book_time for book_time in encoding_books_time if book_time[0].id in multitrack_books_ids]

            # print the updated if there are any books being updated
            if len(progress_str) > 30:
                print(progress_str, end='')



def main():

    # initialize the api
    a = api.AudiobookshelfAPI(IP, APITOKEN)
    library = None

    # get larry's library
    for lib in a.get_all_libraries():
        if lib.name == LIBRARYNAME:
            library = lib
            print('lib id: ' + library.id)

    if library is None:
        print("No Library found with name: ", LIBRARYNAME)
        exit()

    encode_books(a, library)


if __name__ == "__main__":
    main()
