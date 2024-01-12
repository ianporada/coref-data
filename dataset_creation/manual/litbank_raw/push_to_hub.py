"""
Write the litbank dataset to the HuggingFace Hub.
"""

import csv
import glob
import os

from conll_coref_transform import conll_transform
from datasets import Dataset, DatasetDict

COREF_DIR = "coref/conll/" # .conll CoNLL-2012 Shared Task format
ENTITY_DIR = "entities/tsv/" # .tsv [word, BIO, BIO, BIO, BIO] where BIO is TAG-TYPE e.g. B-PER
EVENT_DIR = "events/tsv/" # .tsv [word, TAG] where TAG is O or EVENT
TEXT_DIR = "original/" # .txt original text
QUOTATIONS = "quotations/tsv/" # .tsv see https://github.com/dbamman/litbank/blob/master/quotations/README.md

TOKEN_COLUMN = 3

META_INFO = """
|Gutenberg ID|Date|Author|Title|
|---|---|---|---|
|514|1868|Alcott, Louisa May|Little Women|
|18581|1904|Alger, Horatio, Jr.|Adrift in New York: Tom and Florence Braving the World|
|5348|1868|Alger, Horatio, Jr.|Ragged Dick, Or, Street Life in New York with the Boot-Blacks|
|158|1815|Austen, Jane|Emma|
|105|1818|Austen, Jane|Persuasion|
|1342|1813|Austen, Jane|Pride and Prejudice|
|1206|1914|Bower, B. M.|The Flying U Ranch|
|969|1848|Brontë, Anne|The Tenant of Wildfell Hall|
|1260|1847|Brontë, Charlotte|Jane Eyre: An Autobiography|
|768|1847|Brontë, Emily|Wuthering Heights|
|2095|1853|Brown, William Wells|Clotelle: A Tale of the Southern States|
|113|1911|Burnett, Frances Hodgson|The Secret Garden|
|6053|1778|Burney, Fanny|Evelina, Or, the History of a Young Lady's Entrance into the World|
|62|1912|Burroughs, Edgar Rice|A Princess of Mars|
|78|1912|Burroughs, Edgar Rice|Tarzan of the Apes|
|2084|1903|Butler, Samuel|The Way of All Flesh|
|11|1865|Carroll, Lewis|Alice's Adventures in Wonderland|
|24|1913|Cather, Willa|O Pioneers!|
|44|1915|Cather, Willa|The Song of the Lark|
|472|1900|Chesnutt, Charles W. (Charles Waddell)|The House Behind the Cedars|
|1695|1908|Chesterton, G. K. (Gilbert Keith)|The Man Who Was Thursday: A Nightmare|
|160|1899|Chopin, Kate|The Awakening, and Selected Short Stories|
|1155|1922|Christie, Agatha|The Secret Adversary|
|155|1868|Collins, Wilkie|The Moonstone|
|219|1899|Conrad, Joseph|Heart of Darkness|
|974|1907|Conrad, Joseph|The Secret Agent: A Simple Tale|
|940|1826|Cooper, James Fenimore|The Last of the Mohicans; A narrative of 1757|
|73|1895|Crane, Stephen|The Red Badge of Courage: An Episode of the American Civil War|
|876|1861|Davis, Rebecca Harding|Life in the Iron-Mills; Or, The Korl Woman|
|521|1719|Defoe, Daniel|The Life and Adventures of Robinson Crusoe|
|1023|1852|Dickens, Charles|Bleak House|
|766|1849|Dickens, Charles|David Copperfield|
|1400|1861|Dickens, Charles|Great Expectations|
|730|1838|Dickens, Charles|Oliver Twist|
|1661|1892|Doyle, Arthur Conan|The Adventures of Sherlock Holmes|
|2852|1902|Doyle, Arthur Conan|The Hound of the Baskervilles|
|233|1900|Dreiser, Theodore|Sister Carrie: A Novel|
|15265|1911|Du Bois, W. E. B. (William Edward Burghardt)|The Quest of the Silver Fleece: A Novel|
|145|1871|Eliot, George|Middlemarch|
|550|1861|Eliot, George|Silas Marner|
|12677|1914|Ferber, Edna|Personality Plus: Some Experiences of Emma McChesney and Her Son, Jock|
|6593|1749|Fielding, Henry|History of Tom Jones, a Foundling|
|9830|1922|Fitzgerald, F. Scott (Francis Scott)|The Beautiful and Damned|
|805|1920|Fitzgerald, F. Scott (Francis Scott)|This Side of Paradise|
|2775|1915|Ford, Ford Madox|The Good Soldier|
|2641|1908|Forster, E. M. (Edward Morgan)|A Room with a View|
|2891|1910|Forster, E. M. (Edward Morgan)|Howards End|
|4276|1855|Gaskell, Elizabeth Cleghorn|North and South|
|32|1915|Gilman, Charlotte Perkins|Herland|
|502|1913|Grey, Zane|Desert Gold|
|3457|1919|Grey, Zane|The Man of the Forest|
|711|1887|Haggard, H. Rider (Henry Rider)|Allan Quatermain|
|2166|1885|Haggard, H. Rider (Henry Rider)|King Solomon's Mines|
|27|1874|Hardy, Thomas|Far from the Madding Crowd|
|110|1891|Hardy, Thomas|Tess of the d'Urbervilles: A Pure Woman|
|77|1851|Hawthorne, Nathaniel|The House of the Seven Gables|
|33|1850|Hawthorne, Nathaniel|The Scarlet Letter|
|95|1894|Hope, Anthony|The Prisoner of Zenda|
|41|1820|Irving, Washington|The Legend of Sleepy Hollow|
|208|1879|James, Henry|Daisy Miller: A Study|
|432|1903|James, Henry|The Ambassadors|
|209|1898|James, Henry|The Turn of the Screw|
|367|1896|Jewett, Sarah Orne|The Country of the Pointed Firs|
|2807|1899|Johnston, Mary|To Have and to Hold|
|4217|1916|Joyce, James|A Portrait of the Artist as a Young Man|
|2814|1914|Joyce, James|Dubliners|
|4300|1922|Joyce, James|Ulysses|
|217|1913|Lawrence, D. H. (David Herbert)|Sons and Lovers|
|543|1920|Lewis, Sinclair|Main Street|
|215|1903|London, Jack|The Call of the Wild|
|351|1915|Maugham, W. Somerset (William Somerset)|Of Human Bondage|
|11231|1853|Melville, Herman|Bartleby, the Scrivener: A Story of Wall-Street|
|2489|1851|Melville, Herman|Moby Dick; Or, The Whale|
|45|1908|Montgomery, L. M. (Lucy Maud)|Anne of Green Gables|
|41286|1866|Oliphant, Mrs. (Margaret)|Miss Marjoribanks|
|60|1905|Orczy, Emmuska Orczy, Baroness|The Scarlet Pimpernel|
|932|1839|Poe, Edgar Allan|The Fall of the House of Usher|
|1064|1842|Poe, Edgar Allan|The Masque of the Red Death|
|4051|1915|Praed, Campbell, Mrs.|Lady Bridget in the Never-Never Land: a story of Australian life|
|3268|1794|Radcliffe, Ann Ward|The Mysteries of Udolpho|
|434|1908|Rinehart, Mary Roberts|The Circular Staircase|
|171|1791|Rowson, Mrs.|Charlotte Temple|
|271|1877|Sewell, Anna|Black Beauty|
|84|1823|Shelley, Mary Wollstonecraft|Frankenstein; Or, The Modern Prometheus|
|120|1883|Stevenson, Robert Louis|Treasure Island|
|345|1897|Stoker, Bram|Dracula|
|829|1726|Swift, Jonathan|Gulliver's Travels into Several Remote Nations of the World|
|8867|1918|Tarkington, Booth|The Magnificent Ambersons|
|599|1848|Thackeray, William Makepeace|Vanity Fair|
|76|1884|Twain, Mark|Adventures of Huckleberry Finn|
|74|1876|Twain, Mark|The Adventures of Tom Sawyer|
|1327|1898|Von Arnim, Elizabeth|Elizabeth and Her German Garden|
|238|1915|Webster, Jean|Dear Enemy|
|5230|1897|Wells, H. G. (Herbert George)|The Invisible Man: A Grotesque Romance|
|36|1897|Wells, H. G. (Herbert George)|The War of the Worlds|
|541|1920|Wharton, Edith|The Age of Innocence|
|174|1890|Wilde, Oscar|The Picture of Dorian Gray|
|2005|1919|Wodehouse, P. G. (Pelham Grenville)|Piccadilly Jim|
|16357|1788|Wollstonecraft, Mary|Mary: A Fiction|
|1245|1919|Woolf, Virginia|Night and Day|
"""

def read_tsv(fname):
    with open(fname) as f:
        csv_reader = csv.reader(f, delimiter='\t')
        return [row for row in csv_reader]


docs = []
for doc_fname in glob.glob(os.path.join(TEXT_DIR, "*.txt")):
    doc_name = os.path.basename(doc_fname).replace(".txt", "")

    # read conll data
    conll_fname = os.path.join(COREF_DIR, doc_fname + '.conll')
    docs = conll_transform.read_file(conll_fname)
    assert len(docs.values()) == 1, f"{doc_fname} conll file should have only one doc"
    sentences = docs.values()[0]
    coref_chains = conll_transform.compute_chains(sentences)
    tokens = [[row[TOKEN_COLUMN] for row in s] for s in sentences]

    # read entity data
    entity_fname = os.path.join(ENTITY_DIR, doc_fname + '.tsv')
    entity_rows = read_tsv(entity_fname) # [word, BIO, BIO, BIO, BIO] where BIO is TAG-TYPE e.g. B-PER
    entities = []
    for row in entity_rows:
        token = row[0]
        bio_tags = row[1:]
        entities.append({
            "token": token,
            "bio_tags": bio_tags,
        })
    
    # read event data
    event_fname = os.path.join(EVENT_DIR, doc_fname + '.tsv')
    event_rows = read_tsv(event_fname) # [word, TAG] where TAG is O or EVENT
    events = []
    for row in event_rows:
        token = row[0]
        is_event = row[1] == "EVENT"
        events.append({
            "token": token,
            "is_event": is_event,
        })

    # read text data
    text_fname = os.path.join(TEXT_DIR, doc_fname + '.txt')
    with open(doc_fname) as f:
        original_text = f.read()

    # read quotation data
    quotation_fname = os.path.join(QUOTATIONS, doc_fname + '.tsv')
    quotation_rows = read_tsv(quotation_fname)
    quotes = {}
    attributions = {}
    for row in quotation_rows:
        if row[0] == "QUOTE":
            quote_id, sent_start, token_start, sent_end, token_end, quotation = row[1:]
            quotes[quote_id] = {
                "quote_id": quote_id,
                "start": {"sent_id": sent_start, "token_id": token_start},
                "end": {"sent_id": sent_end, "token_id": token_end},
                "quotation": quotation
            }
        elif row[0] == "ATTRIB":
            quote_id, speaker = row[1:]
            attributions[quote_id] = speaker
    for quote_id, speaker in attributions:
        quotes[quote_id]["attribution"] = speaker
    quotes = list(quotes.values)

    doc = {
        "doc_name": doc_name,
        "sentences": tokens,
        "coref_chains": coref_chains,
        "entities": entities,
        "events": events,
        "original_text": original_text,
        "quotes": quotes,
    }


# dataset = DatasetDict({
#     "train": Dataset.from_list(train_docs),
#     "validation": Dataset.from_list(validation_docs),
#     "test": Dataset.from_list(test_docs),
# })

# dataset.push_to_hub("coref-data/gum_raw", private=True)
