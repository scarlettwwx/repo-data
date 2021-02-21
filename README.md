# repo-data
Introduction to the files

`main-database-scores` stores whole data processing steps, including ryan,richard,blick scores, normalizations of them and representativeness. There are about 29694 entries after deleting the overlaps. 

`scores_sorted_blick_repre`, `scores_sorted_richard_repre`, `scores_sorted_ryan_repre` have no difference than `main-database-scores`, except they are sorted in different representativeness score.

`master-list-words(ipa)` has only one column with IPAs, extracted from the IPA column of `scores_sorted_blick_repre`

`vanna dropbox` folder includes the raw data. `RichardScores-BLICKtop20000` is richard scores for top 20000 of blick model. `RichardScores-ryantop20000` is richard scores for top 20000 of ryan model (actually there are only 15162 entries in it). There are quite a few overlapped entries between them, so after removing them, only 29694 entries left in `main-database-scores`

`generation.py` is the script to generate the monosyllabic words in IPA with given rules.
