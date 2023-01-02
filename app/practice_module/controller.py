from config import Database
from pymongo import errors, results, cursor
import random
from datetime import datetime

# get a reference to the databases
intera_practice_db = Database.client.intera_practice_db

# get a reference to the collections
try: 
    word_data = intera_practice_db['word_data']
except errors.CollectionInvalid as err:
    print(err)

def create_word_entry(word, url, classified=True):
    word_entry = {'word': word, 'url': url, 'classified': classified}
    result = word_data.insert_one(word_entry)

    if isinstance(result, results.InsertOneResult):
        if result.inserted_id:
            return (1, 'Word {word} created successfully')

    return (0, 'Error creating word {word}')


def retrieve_random_word(self):
    # get random word from mongodb without using aggregate
    count = word_data.count_documents({'classified': True})
    random_index = random.randint(0, count - 1)
    word = word_data.find({'classified': True})[random_index]

    if word is None:
        return (0, 'No classified words found', None)

    return (1, 'success', word)


def get_word_video_url(word):
    word_entry = word_data.find_one({'word': word})

    if word_entry:
        return (1, 'success', word_entry['url'])
    
    return (0, 'Unable to find word {word}', None)


def set_classified_status(word, classified):
    result = word_data.update_one({'word': word}, {'$set': {'classified': classified}})

    if isinstance(result, results.UpdateResult):
        if result.matched_count == 1:
            return (1, 'Word {word} updated successfully')
        else:
            return (0, 'Word {word} not found')
    
    return (0, 'Error updating word {word}')


def delete_word(word):
    result = word_data.delete_one({'word': word})

    if isinstance(result, results.DeleteResult):
        if result.deleted_count == 1:
            return (1, 'Word {word} deleted successfully')

    return (0, 'Word {word} not found')


# get a reference to the collections
try: 
    attempted_words = intera_practice_db['attempted_words']
except errors.CollectionInvalid as err:
    print(err)


def create_attempted_word_entry(word, user_id, classification, correct):
    word_entry = {'word': word, 'user_id': user_id, 'classification': classification, 'correct': correct, 'date_created': datetime.now()}
    result = attempted_words.find_one_and_replace(filter={ '$and': {'word': word, 'user_id': user_id}}, replacement=word_entry, upsert=True)

    if result is not None:
        return (1, 'Word attempt {word} created successfully')

    return (0, 'Error creating word attempt {word}')


def get_attempted_words(user_id):
    words = attempted_words.find({'user_id': user_id}).sort('date_created', -1)

    if words is None:
        return (0, 'No words found', None)
    
    return (1, 'success', list(words))


def get_attempted_word(word, user_id):
    word_entry = attempted_words.find({'$and': {'word': word, 'user_id': user_id}}).sort('date_created', -1)

    if word_entry.count() == 0:
        return (0, 'Word not found', None)
    
    return (1, 'success', list(word_entry)[0])


def delete_attempted_word(word, user_id):
    result = attempted_words.delete_one({'word': word, 'user_id': user_id})

    if isinstance(result, results.DeleteResult):
        if result.deleted_count == 1:
            return (1, 'Word attempt {word} deleted successfully')
    
    return (0, 'Word attempt {word} not found')