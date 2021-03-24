#VOWELS
peak_vowels   = ['i', 'ɪ', 'ɛ', 'ɑ', 'æ', 'u', 'ʊ', 'oʊ', 'ʌ', 'ɔ', 'aɪ', 'aʊ', 'ɔɪ', 'eɪ', 'ə', 'ɝ', 'ɚ']

peak_T = ['i', 'ɑ', 'u', 'ɔ']
peak_D = ['oʊ', 'aɪ', 'aʊ', 'ɔɪ', 'eɪ']


#CONSONANTS
consonants  = ['p','b','t','d','k','g','f','v','θ','ð','s','z','ʃ','ʒ','h','m','n','ŋ','l','r','w','j','tʃ','dʒ']
consonants_minus_g = ['p','b','t','d','k','f','v','θ','ð','s','z','ʃ','ʒ','h','m','n','ŋ','l','r','w','j','tʃ','dʒ'] # since the 'g' character is wacky

obstruents = ['p','b','t','d','k','g','f','v','θ','ð','s','z','ʃ','ʒ','h','tʃ','dʒ']
voiced_obstruent = ['b', 'd', 'g','v', 'ð', 'z','ʒ','dʒ']
liquid_glide =['l','r','w','j']

#ONSET
onset_consonants = ['p','b','t','d','k','g','f','v','θ','ð','s','z','ʃ',    'h','m','n',    'l','r','w','j','tʃ','dʒ'] #Rule 3: exclude ʒ, ŋ
onset_appendices = ['s']
onset_j_clusters = ['pj', 'bj', 'fj', 'vj', 'kj', 'gj', 'hj', 'mj'] #can only occur before 'u'

#CODA
#Rule 10: No glides in syllable codas: /j/ /w/
coda_consonants       = ['p','b','t','d','k','ɡ','f','v','θ','ð','s','z','ʃ','ʒ',    'm','n','ŋ','l', 'r', 'w','j','tʃ','dʒ'] #Rule 4: h never occurs in the coda of a syllable.
coda_R = ['r']
coda_L = ['l']
coda_N = ['n', 'm', 'ŋ']
coda_F = ['f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ']
coda_P = ['p', 'b', 't', 'd', 'k', 'g','tʃ','dʒ']
coda_appendices     = ['t', 'd', 'θ', 's', 'z', 'dʒ']


#ONSET CLUSTERS, 1/2/3 consonats
onsets_l0 = ['']
onsets_l1 = onset_consonants
#rule 6: The first consonant in a two-consonant onset must be an obstruent.
#rule 7: The second consonant in a two-consonant onset must not be a voiced obstruent.
#Rule 8: If the first consonant of a two-consonant onset is not an /s/, the second consonant must be a liquid or a glide
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
#here coda_appendices are all consonants.
rhyme_l4 = [R + A for R in rhyme_l3 for A in coda_appendices]
rhyme_l5 = [R + A for R in rhyme_l4 for A in coda_appendices]
rhyme_l6 = [R + A for R in rhyme_l5 for A in coda_appendices] #改一下R+A

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


def constraint_check(syllable):
    #Rule 2: Sequences of repeated consonants are not possible.
  #consonant  = ['g','r','z']
  flag = 0
  for i in range(len(syllable)):
    if(syllable[i] in peak_vowels): 
      flag = i
  
  list1 = []
  list2 = []
  for k in range(flag, len(syllable)-1):
    list1.append(syllable[k])
  for j in range(flag+1, len(syllable)):
    list2.append(syllable[j])
  outcome = list(zip(list1,list2))
  for (a,b) in outcome:
    if (a in consonants and a==b):
      return False
    else:
      continue
  return True

#print(constraint_check('strɛŋθθθs'))
def write_all_IPA():
    # Generate monosyllables in IPA
    with open("english_monosyllabic_nonce_IPA.csv", 'w') as output_file:

        #most of the monosyllables
        for onset in onsets_all:
            for rhyme in rhymes_all:
              word = onset + rhyme
              if (constraint_check(word)):
                output_file.write(onset + rhyme + "\n")
              else:
                continue

        #onset clusters with /j/ in the second position
        for j_cluster in onset_j_clusters:
            for rhyme in rhymes_all:
                if rhyme[0] == 'u' and constraint_check(j_cluster + rhyme):
                    output_file.write(j_cluster + rhyme + "\n")

write_all_IPA()
