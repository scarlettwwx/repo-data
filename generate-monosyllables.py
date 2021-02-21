import csv
import json
import pprint
#Notes
# /ɚ/ should probably be removed since it is non-syllabic
#TODO coda appendices
#TODO include /w/ in rhyme???

#VOWELS
peak_vowels   = ['i', 'ɪ', 'ɛ', 'ɑ', 'æ', 'u', 'ʊ', 'oʊ', 'ʌ', 'ɔ', 'aɪ', 'aʊ', 'ɔɪ', 'eɪ', 'ə', 'ɝ', 'ɚ']

peak_T = ['i', 'ɑ', 'u', 'ɔ']
peak_D = ['oʊ', 'aɪ', 'aʊ', 'ɔɪ', 'eɪ']

#CONSONANTS
consonants  = ['p','b','t','d','k','g','f','v','θ','ð','s','z','ʃ','ʒ','h','m','n','ŋ','l','r','w','j','tʃ','dʒ']
consonants_minus_g = ['p','b','t','d','k','f','v','θ','ð','s','z','ʃ','ʒ','h','m','n','ŋ','l','r','w','j','tʃ','dʒ'] # since the 'g' character is wacky
#ONSET
onset_consonants = ['p','b','t','d','k','g','f','v','θ','ð','s','z','ʃ',    'h','m','n',    'l','r','w','j','tʃ','dʒ']
onset_appendices = ['s']
onset_j_clusters = ['pj', 'bj', 'fj', 'vj', 'kj', 'gj', 'hj', 'mj'] #can only occur before 'u'

#CODA
coda_consonants       = ['p','b','t','d','k','ɡ','f','v','θ','ð','s','z','ʃ','ʒ',    'm','n','ŋ','l', 'r', 'w','j','tʃ','dʒ']
coda_R = ['r']
coda_L = ['l']
coda_N = ['n', 'm', 'ŋ']
coda_F = ['f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ']
coda_P = ['p', 'b', 't', 'd', 'k', 'g','tʃ','dʒ']
coda_appendices     = ['t', 'd', 'θ', 's', 'z', 'dʒ']


#ONSET CLUSTERS
onsets_l0 = ['']
onsets_l1 = onset_consonants
onsets_l2 = ['pl','pr','bl','br','fl','fr','tr','tw','dr','dw','θr','θw','sm','sn','sl','sw','ʃm','ʃn','ʃl','ʃr','ʃw','kl','kr','kw','gl','gr','gw','sf','vr'] #note /sf/ and /vr/ and any with /ʃ/
onsets_l3 = ['spl', 'spr', 'str', 'skl', 'skr']

#RHYME - VOWEL + CODA CLUSTERS
rhyme_l1 = peak_T + peak_D
rhyme_l2 = [V + C for V in peak_vowels if V not in peak_D for C in coda_consonants]
rhyme_l3 = [V + C for V in peak_D for C in coda_consonants] \
        + [V + C1 + C2 for V in peak_vowels if V not in peak_D for C1 in coda_R for C2 in coda_consonants if C2 not in coda_R] \
        + [V + C1 + C2 for V in peak_vowels if V not in peak_D for C1 in coda_L for C2 in coda_consonants if C2 not in coda_R or C2 not in coda_L] \
        + [V + C1 + C2 for V in peak_vowels if V not in peak_D for C1 in coda_N for C2 in coda_consonants if C2 in coda_F or C2 in coda_P]

#writing every combination for l4-6. It takes way more memory than if I had followed filters given in the book,
#but the filter dictates a [-son] [-cor] in the X_6 position, preventing generation of a monosyllable like "sixths"
#hopefully the phonotactics scorer will filter out the bulk of bad coda clusters.
rhyme_l4 = [R + A for R in rhyme_l3 for A in coda_appendices]
rhyme_l5 = [R + A for R in rhyme_l4 for A in coda_appendices]
rhyme_l6 = [R + A for R in rhyme_l5 for A in coda_appendices]

#ONSETS AND RHYMES OF ALL LENGTHS
onsets_all = onsets_l0 + onsets_l1 + onsets_l2 + onsets_l3
rhymes_all = rhyme_l1 + rhyme_l2 + rhyme_l3 + rhyme_l4 + rhyme_l5 + rhyme_l6
print("Number of rhymes = " + str(rhymes_all.__len__()) + "\nNumber of onsets = " + str(onsets_all.__len__()))

#For parsing affricates and diphthongs
diph_or_affr_first_char = ['t','d','a','ɔ','o','e']
diph_or_affr_second_char = ['ʃ','ʒ','ɪ','ʊ']

affr_first_char = ['t','d']
affr_second_char = ['ʃ','ʒ']
diph_first_char = ['a','ɔ','o','e']
diph_second_char = ['ɪ','ʊ']

#IPA to ARPAbet dictionary unstressed
with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/ARPAbet-IPA_no_stress.csv", 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    IPA_ARPA_dict = {rows[1]: rows[0] for rows in csv_reader}

#ARPAbet to IPA dictionary unstressed
with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/ARPAbet-IPA_no_stress.csv", 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    ARPA_IPA_dict = {rows[0]: rows[1] for rows in csv_reader}

#cmu dictionary with key/values switched. new format: arpa,ortho
with open('/Users/Graham/Desktop/McGill/Summer2018/dictionary/cmu2/index.json',
          encoding='utf-8') as cmu_file:
    cmu_dict = json.loads(cmu_file.read())
    cmu_dict_switched = {y: x for x, y in cmu_dict.items()}
    cmu_dict_switched_unstressed = {' '.join([char.rstrip('012') for char in word.split(' ')]) : cmu_dict_switched[word] for word in cmu_dict_switched.keys()}
print(cmu_dict_switched_unstressed)
# IPA peter dictionary. format: IPA,peter
with open('/Users/Graham/Desktop/McGill/Summer2018/phonotactics/data/features/peter_to_ipa.tsv') as peter_ipa_file:
    peter_ipa_reader = csv.reader(peter_ipa_file, delimiter=',')
    peter_ipa_dict = {row[1]:row[0] for row in peter_ipa_reader}

with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/ipa-arpa-peter-unstressed.csv", 'r') as ipa_arpa_peter_file:
    arpa_peter_reader = csv.reader(ipa_arpa_peter_file, delimiter=',')
    arpa_peter_dict = {row[1]:row[2] for row in arpa_peter_reader}


def IPA_to_ARPAbet(input_symbol):

        if input_symbol in IPA_ARPA_dict:
            return IPA_ARPA_dict[input_symbol]
        #'g' symbol is different from second 'g' symbol here
        # elif input_symbol == 'g' or input_symbol == 'ɡ':
        #     return 'G'
        elif input_symbol not in consonants_minus_g and input_symbol not in peak_vowels:
            return 'G'
        elif input_symbol == 'ʃ':
            return 'SH'


def ARPAbet_to_IPA(input_symbol):
    if input_symbol in ARPA_IPA_dict:
        return ARPA_IPA_dict[input_symbol]
    # vanna's changes for the blick scorer: AX0 --> AH0, AXR0 --> AX0 R
    elif input_symbol == 'AH0':
        return ARPA_IPA_dict['AX0']
    elif input_symbol == 'AX0 R':
        return ARPA_IPA_dict['AXR0']


def IPA_to_peter(input_symbol):
    if input_symbol in peter_ipa_dict:
        return peter_ipa_dict[input_symbol]
    # 'g' symbol is different from second 'g' symbol here
    # elif input_symbol == 'g' or input_symbol == 'ɡ':
    #     return 'G'
    elif input_symbol not in consonants_minus_g and input_symbol not in peak_vowels:
        return 'CKXtNvo1'
    elif input_symbol == 'ʃ':
        return 'CSXsNfo1'

# def ARPAbet_to_peter(input_symbol):
#     if input_symbol in ['OW1','OW2','OY1','OY2','EY1','EY2','AW1','AW2','AY1','AY2', 'ER1', 'ER2']:
#         #TODO convert diphthongs appropriately
#         exceptions = {
#             'OW1': 'VDUrNvo1_VEWrNvo1',
#             'OW2': 's',
#             'OY1': 's',
#             'OY2', 'EY1', 'EY2', 'AW1', 'AW2', 'AY1', 'AY2', 'ER1', 'ER2' assert False
#         }
#         if input_symbol == 'OW1': return 'VDUrNvo1_VEWrNvo1'
#         if input_symbol == 'OW2': return ''

#This version ignores stress
def ARPAbet_to_peter(input_symbol):
    input_symbol = input_symbol.rstrip('0123')
    if input_symbol == 'OW': return 'VDUrNvo1_VEWrNvo1' # 'oʊ'
    if input_symbol == 'OY': return 'VAWrNvo1_VEYuNvo1' # 'ɔɪ'
    if input_symbol == 'EY': return 'VDZuNvo1_VEYuNvo1' # 'eɪ'
    if input_symbol == 'AW': return 'VAYuNvo1_VEWrNvo1' # 'aʊ'. no 'a' so used 'æ' instead
    if input_symbol == 'AY': return 'VAYuNvo1_VEYuNvo1' # 'aɪ'same thing here
    if input_symbol == 'ER': return 'VBYuNvo1_CRXlNvo1' # 'ɝ'. ER0 is ɚ
    if input_symbol == 'AX': return 'VQXuNvo1' # 'ə'. does not occur in cmu dictionary
    if input_symbol == 'AXR': return 'VQXuNvo1_CRXlNvo1' # 'ɚ'. does not occur in cmu dictionary
    elif input_symbol in arpa_peter_dict: return arpa_peter_dict[input_symbol]
    else: print(input_symbol + " did not match any keys\n"); return ''

#Generates a file that has an (almost, with some reservations about the restricted set of onsets) exhaustive list of
#possible monosyllabic English words based on English phonotactic rules written in the book
#English Phonology: an Introduction (Giegerich 1992)
def write_all_IPA():
    # Generate monosyllables in IPA
    with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/english_monosyllabic_nonce_IPA.csv", 'w') as output_file:

        #most of the monosyllables
        for onset in onsets_all:
            for rhyme in rhymes_all:
                output_file.write(onset + rhyme + "\n")

        #onset clusters with /j/ in the second position
        for j_cluster in onset_j_clusters:
            for rhyme in rhymes_all:
                if rhyme[0] == 'u':
                    output_file.write(j_cluster + rhyme + "\n")


#returns 1 if an inputted string matches a key in the Carnegie Melon University ARPAbet transcribed pronunciation dictionary.
#returns 0 if not.
generated_cmu_words = []
def detect_cmu(word_ARPA):
        if word_ARPA in cmu_dict_switched:
            generated_cmu_words.append(word_ARPA)
            return 1
        else:
            return 0

def detect_cmu_unstressed(word_ARPA):
    if word_ARPA in cmu_dict_switched_unstressed:
        generated_cmu_words.append(word_ARPA)
        return 1
    else:
        return 0
#converts an IPA file to a peter file
#format: column 1: ipa, column 2: peter
def write_peter():
    with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/english_monosyllabic_nonce_IPA1.csv",
              'r') as input_file:
        with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/monosyllabic_nonce_peter_only_no_schwa.csv",
                  'w') as output_file:
            output_file.write("word\n")
            for row in csv.reader(input_file, delimiter='\t'):
                word_IPA = row[0].rstrip()
                word_as_list_IPA = list(word_IPA)
                word_peter = "#"
                guard = False
                #peter has no 'ɝ' or 'ɚ' characters. cmu dictionary has no schwa
                if 'ɝ' in word_IPA or 'ɚ' in word_IPA or 'ə' in word_IPA:
                    continue
                for i in range(0, len(word_as_list_IPA)):
                    # handling diphthongs, affricates which are a 2 character units
                    if guard: guard = False; continue  # skip converting the next char if it made a diphthong/affricate with the previous char
                    if word_as_list_IPA[i] in affr_first_char and i + 1 <= len(word_as_list_IPA) - 1:
                        guard = True
                        first_char = word_as_list_IPA[i]
                        second_char = word_as_list_IPA[i + 1]
                        if second_char in affr_second_char:
                            word_peter += IPA_to_peter(first_char + second_char) + "_"
                        else:
                            word_peter += IPA_to_peter(first_char) + "_" + IPA_to_peter(second_char) + "_"
                    else:
                        word_peter += IPA_to_peter(word_as_list_IPA[i]) + "_"

                word_peter = word_peter.rstrip('_') + "#"
                # print(word_IPA + '\t' + word_peter)
                # output_file.write(word_IPA + '\t' + word_peter +'\n')
                output_file.write(word_peter + '\n')

#Took about 4-5 hours to run this
#generate monosyllables (monosyllabic nonce words) in IPA (column 1), ARPAbet (col 2), and 1 if in the
# Carnegie Melon University (cmu) ARPAbet transcribed pronunciation dictionary or 0 if not.
#Requires write_all_IPA() to be run first since it needs a list of IPA symbols that will be converted to ARPAbet first.
#This could have been avoided by using the body of write_all_IPA() in this function and applying API_to_ARPAbet.
def write_all():

    with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/english_monosyllabic_nonce_IPA1.csv",
              'r') as input_file:
        with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/nonce_forms_ipa_arpa.tsv",
                  'w') as output_file:
            output_file.write('ipa' + '\t' + 'arpa' + '\t'+ 'incmu' + '\n')
            for line in input_file:
                word_IPA = line.rstrip()
                word_as_list_IPA = list(word_IPA)
                word_ARPA = ""
                guard = False

                #ARPAbet version
                for i in range(0, len(word_as_list_IPA)):
                    # handling diphthongs, affricates which are a 2 character units
                    if guard: guard = False; continue #skip converting the next char if it made a diphthong/affricate with the previous char
                    if word_as_list_IPA[i] in diph_or_affr_first_char and i + 1 <= len(word_as_list_IPA) - 1:
                        guard = True
                        first_char = word_as_list_IPA[i]
                        second_char = word_as_list_IPA[i + 1]
                        #if affricate
                        if first_char in affr_first_char:
                            if second_char in affr_second_char:
                                word_ARPA += IPA_to_ARPAbet(first_char + second_char) + " "
                            else:
                                word_ARPA += IPA_to_ARPAbet(first_char) + " " + IPA_to_ARPAbet(second_char) + " "
                        #if diphthong
                        elif first_char in diph_first_char:
                            if second_char in diph_second_char:
                                word_ARPA += IPA_to_ARPAbet(first_char + second_char) + " "
                            else:
                                word_ARPA += IPA_to_ARPAbet(first_char) + " " + IPA_to_ARPAbet(second_char) + " "
                    else:
                        word_ARPA += IPA_to_ARPAbet(word_as_list_IPA[i]) + " "

                word_ARPA = word_ARPA.rstrip()

                #print(word_IPA + '\t' + word_ARPA + '\t' + str(detect_cmu(word_ARPA)))
                #Format: IPA    ARPA    peter   incmu
                output_file.write(word_IPA + '\t' + word_ARPA + '\t' + str(detect_cmu_unstressed(word_ARPA)) + '\n')

def write_mode(input_path="/Users/Graham/Desktop/McGill/Summer2018/python/data/filtered_forms.csv",
               output_path="/Users/Graham/Desktop/McGill/Summer2018/python/data/filtered_forms1.csv"):
    with open(input_path, 'r') as input_file:
        with open(output_path, 'w') as output_file:
            csv_reader = csv.DictReader(input_file, delimiter='\t')
            guard = False
            for line in csv_reader:
                if guard: guard = False; continue
                arpa_word_as_list = line['arpa'].split()
                word_IPA = ""
                for i in range(0, len(arpa_word_as_list)):
                    if arpa_word_as_list[i] == 'AH0':
                        guard = True
                        first_char = arpa_word_as_list[i]
                        second_char = arpa_word_as_list[i+1]
                        # vanna's changes for the blick scorer: AX0 --> AH0, AXR0 --> AX0 R
                        if second_char == 'R':
                            word_IPA += ARPAbet_to_IPA(first_char + " " + second_char)
                            arpa_word_as_list[i] = 'AXR0'
                            arpa_word_as_list[i+1] = ''
                        else:
                            word_IPA += ARPAbet_to_IPA(first_char) + ARPAbet_to_IPA(second_char)
                            arpa_word_as_list[i] = 'AX0'
                    word_IPA += ARPAbet_to_IPA(arpa_word_as_list[i])
                output_file.write(word_IPA + '\t' + line['arpa'] + '\t' +  line['score'] + '\t' + str(detect_cmu_unstressed(line['arpa'])) + '\n')

def main():

    #write_all_IPA()
    #write_all()
    # count=0
    # with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/generated_cmu_words.csv", 'w') as output_file:
    #     for word in generated_cmu_words:
    #         output_file.write(cmu_dict_switched[word] + '\n')
    #         print(cmu_dict_switched[word])
    #         count+=1
    # print(count)
    # write_all()
    strip_cmu()
    #filter()
    # write_mode()
    # pprint.pprint(peter_ipa_dict)
    # rewrite_cmu()

#output file has the following format:
#column 1: peter, column 2: arpabet, column 3: orthography
#rewrites the cmu dictionary to have extra columns.
def rewrite_cmu():
    with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/cmu_dict.csv", 'r') as input_file:
        with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/cmu_dict_peter.csv", 'w') as output_file:
            cmu_reader = csv.reader(input_file, delimiter=',')
            print("word,arpa,ortho")
            for row in cmu_reader:
                word_arpa = row[0]
                word_arpa_as_list = word_arpa.split(" ")
                word_peter = '#'
                for char in word_arpa_as_list:
                    word_peter = word_peter + ARPAbet_to_peter(char) + '_'
                word_peter = word_peter.rstrip('_') + '#'
                output_file.write(word_peter + ',' + row[0] + ',' + row[1] + '\n')

def strip_cmu():
    with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/cmu_dict.csv", 'r') as input_file:
        with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/cmu_dict_no_stress.csv", 'w') as output_file:
            cmu_reader = csv.reader(input_file, delimiter=',')
            output_file.write('arpa,ortho')
            for row in cmu_reader:
                word_arpa = row[0]
                word_arpa_as_list = word_arpa.split(" ")
                word_no_stress = ''
                for char in word_arpa_as_list:
                    if char == char.rstrip('012 '):
                        word_no_stress = word_no_stress + char + ' '
                    else:
                        # word_no_stress = word_no_stress + char.rstrip('012 ') + '1 '
                        word_no_stress = word_no_stress + char.rstrip('012 ') + ' '
                output_file.write(word_no_stress.rstrip() + ',' + row[1] + '\n')

def filter(threshold=9.0, path="/Users/Graham/Desktop/McGill/Summer2018/python/data/fullArpaOnlyList-output.csv"):
    with open(path, 'r') as input_file:
        with open("/Users/Graham/Desktop/McGill/Summer2018/python/data/filtered_forms.csv", 'w') as output_file:
            reader = csv.reader(input_file, delimiter='\t')
            count = 0
            output_file.write("arpa\tscore\n")
            for row in reader:
                if float(row[1]) < threshold:
                    count+=1
                    output_file.write(row[0] + '\t' + row[1] + '\n')
            print("Number of filtered forms: " + str(count))



main()