from bs4 import BeautifulSoup as bs
import multiprocessing as mp
import httpx
import requests
import re
import concurrent.futures as cf
import time
import asyncio
import aiofiles
from string import ascii_lowercase

NUM_PROCESS = 4
NUM_THREAD = 4
NUM_BATCH_STRING = 250
BATCH_STRING = [None for i in range(NUM_BATCH_STRING)]
ALLOWED_WORD_TYPES = ('noun', 'verb', 'adjective', 'adverb')
ROOT_URL = 'https://dictionary.cambridge.org'
HEADERS = requests.utils.default_headers()
HEADERS.update({'User-Agent': 'UserAgent1'})
WORD_PATTERN = r'^[a-zA-Z]+$'
ERRS = []

async def main():
    root_session = httpx.Client()
    input_queue = mp.Queue(maxsize=1)
    output_queue = mp.Queue(maxsize=5)

    procs = []
    for i in range(NUM_PROCESS):
        procs.append(mp.Process(target=workerProcess, args=(input_queue, output_queue, i)))
        procs[i].start()

    write_coroutine = None
    async with aiofiles.open('dictionary_v2.txt', mode='w') as file_handler:
        for alpha in ascii_lowercase:
        #for alpha in ['a', 'x']:
            #xctr = 0
            web_page_alpha = fetchUrl(ROOT_URL + '/browse/english/' + alpha + '/', root_session)
            if web_page_alpha:
                batch_string_id = 0
                returned_batches = 0

                web_page_alpha = bs(web_page_alpha, 'html.parser')
                words_links = web_page_alpha.findAll(class_='hlh32 hdb dil tcbd')
                for words_link in words_links:
                    #xctr += 1

                    input_queue.put(str(batch_string_id) + '|' + words_link['href'])
                    batch_string_id += 1
                    while not output_queue.empty():
                        returned_batches += getOutput(output_queue)
                    # if xctr > 20:
                    #     break

                while returned_batches < batch_string_id:
                    returned_batches += getOutput(output_queue)
                # for i in range(batch_string_id):
                #     if BATCH_STRING[i] != '':
                #         print(BATCH_STRING[i])
                if write_coroutine is not None:
                    await write_coroutine
                write_coroutine = file_handler.write(''.join(BATCH_STRING[:batch_string_id]))
            else:
                ERRS.append(ROOT_URL + '/browse/english/' + alpha + '/' + '\n')

        if write_coroutine is not None:
            await write_coroutine

    for i in range(NUM_PROCESS):
        input_queue.put('exit')
    while any(proc.is_alive() for proc in procs):
        print('still alive...')
        time.sleep(1)
    print('ERRORS:', len(ERRS))
    for err in ERRS:
        print(err)
    print('finished.')

def workerProcess(input_queue, output_queue, w_id):
    sessions = [httpx.Client() for i in range(NUM_THREAD)]
    words_error_chunks_threads = [None for i in range(NUM_THREAD)]
    
    with cf.ThreadPoolExecutor(max_workers=NUM_THREAD) as executor:
        while True:
            input_ = input_queue.get()
            print('W' + str(w_id), 'DO:', input_)
            if input_ == 'exit':
                break

            words = ''
            error = ''

            batch_string_id, words_link_href = input_.split('|')
            words_page = fetchUrl(words_link_href, sessions[0])
            if words_page:
                words_page = bs(words_page, 'html.parser')
                word_links = words_page.select('.hlh32.han > a')

                words_error_chunks = deployThreads(word_links, sessions, executor, words_error_chunks_threads)

                for w, e in words_error_chunks:
                    words += w
                    error += e
            else:
                error += (words_link_href + '\n')
            output_queue.put(batch_string_id + '|' + words + '|' + error)
            #print('W' + str(w_id), 'FN:', input_)
    return

def deployThreads(word_links, sessions, executor, words_error_chunks_threads):
    num_word_links = len(word_links)
    thread_chunk = num_word_links // NUM_THREAD
    thread_remainder = num_word_links % NUM_THREAD
    start_chunk_id = 0
    for i in range(NUM_THREAD):
        if thread_remainder > 0:
            end_chunk_id = start_chunk_id + thread_chunk + 1
            thread_remainder -= 1
        else:
            end_chunk_id = start_chunk_id + thread_chunk
        words_error_chunks_threads[i] = executor.submit(getWordsChunkThread, word_links[start_chunk_id:end_chunk_id], sessions[i])
        start_chunk_id = end_chunk_id
    cf.wait(words_error_chunks_threads, return_when=cf.ALL_COMPLETED)
    return [t.result() for t in words_error_chunks_threads]

def getWordsChunkThread(word_links_chunk, session):
    words_chunk = ''
    error_chunk = ''
    for word_link in word_links_chunk:
        the_word = word_link.text.strip()
        if bool(re.match(WORD_PATTERN, the_word)):
            words_chunk += (the_word + '\n')
            # word_page = fetchUrl(ROOT_URL + word_link['href'], session)
            # if word_page:
            #     word_types = bs(word_page, 'html.parser')
            #     word_types = word_types.select('.posgram.dpos-g.hdib.lmr-5 > .pos.dpos')
            #     for word_type in word_types:
            #         if word_type.text in ALLOWED_WORD_TYPES:
            #             words_chunk += (the_word + '\n')
            #             break
            # else:
            #     error_chunk += (ROOT_URL + word_link['href'] + '\n')
    return words_chunk, error_chunk

def getOutput(output_queue):
    batch_string_id, response, error = output_queue.get().split('|')
    BATCH_STRING[int(batch_string_id)] = response
    if error != '':
        ERRS.append(error)
    return 1

def fetchUrl(url, session):
    try:
        response = session.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.text
        return None
    except:
        return None

if __name__ == '__main__':
    asyncio.run(main())