import lingpy
from levenshtein_dist_calc import LevenshteinDistanceCalculator
import nltk
from read_tab_files import TabFileReader
import bcubed
from collections import defaultdict

#calculate distance matrix from cognate list (integrate with levenshtein distance calc maybe)
def get_distancematrix(cognate_list):
    distance_matrix = [[0 for i in range(len(cognate_list))]
                           for j in range(len(cognate_list))]
    for i, source in enumerate(cognate_list):
        for j, target in enumerate(cognate_list):
            if (source == ""
                or target == ""):  # if one cognate in pair is missing, null value
                distance_matrix[i][j] = float("nan")
            else:
                distance_matrix[i][j] = nltk.edit_distance(source, target)/max(len(source),len(target))

    return distance_matrix

#gold file clustering to taxa:cluster dictionary transformer for bcubed comparisons
def gold_clust2taxa_dict(taxa, clusters):
    cluster_dict = {}
    for lang, cluster in zip(taxa, clusters):
        cluster_dict[lang] = set([cluster])
    return cluster_dict

#lingpy.upgma_flat output to taxa:cluster dictionary transformer for bcubed comparisons
def upgma2taxa_dict(calculated_dict):
    output_clusters = {}
    for clus, langs in calculated_dict.items():
        for lang in langs:
            output_clusters[lang] = set(str(clus))
    return output_clusters

def prepare_comparison(threshold:float, gold_row:list, cognates:list, taxa:list)->tuple:
    distance_matrix = get_distancematrix(cognates)
    cluster_dict = lingpy.flat_upgma(threshold,distance_matrix,taxa)
    taxa_dict = upgma2taxa_dict(cluster_dict)
    gold_taxadict = gold_clust2taxa_dict(taxa, gold_row)
    return taxa_dict, gold_taxadict

def main(language_fam, fam_gold, threshold=4, remove_gaps=True):
    precision = 0
    recall = 0
    fscore = 0
    taxa = list(language_fam.iloc[0][1:])
    for i in range(1, len(language_fam)):
        cognates = list(language_fam.iloc[i][1:])
        gold_row = list(fam_gold.iloc[i][1:])
        if remove_gaps == True:
            if "" in gold_row:
                gold_row.remove("")
            if "" in cognates:
                cognates.remove("")
        taxa_dict, gold_taxadict = prepare_comparison(threshold, gold_row, cognates, taxa)
        precision += bcubed.precision(taxa_dict, gold_taxadict)
        recall += bcubed.recall(taxa_dict, gold_taxadict)
    n_rows = len(language_fam)-1
    precision /= n_rows
    recall /= n_rows
    fscore = bcubed.fscore(precision, recall)
    return precision, recall, fscore

#####

barb_cognacy = TabFileReader.tab_reader(
    "chl2024_barbacoandata/chl2023_barbacoan_cognacy.tab")
barb_forms = TabFileReader.tab_reader(
    "chl2024_barbacoandata/chl2023_barbacoan_forms.tab")

eau_cognacy = TabFileReader.tab_reader(
    "chl2024_eastern-austronesiandata/chl2023_eastern-austronesian_cognacy.tab")
eau_forms = TabFileReader.tab_reader(
    "chl2024_eastern-austronesiandata/chl2023_eastern-austronesian_forms.tab")

ie_cognacy = TabFileReader.tab_reader("chl2024_iedata/chl2023_iedata_cognacy.tab")
ie_forms = TabFileReader.tab_reader("chl2024_iedata/chl2023_iedata_forms.tab")

barb_scores_4 = main(barb_forms, barb_cognacy)
barb_scores_2 = main(barb_forms, barb_cognacy, threshold=2)
#eau_scores_4 = main(eau_forms, eau_cognacy)
#eau_scores_2 = main(eau_forms, eau_cognacy, threshold=2)
ie_scores_4 = main(ie_forms, ie_cognacy)
ie_scores_2 = main(ie_forms, ie_cognacy, threshold=2)

print("Family        Threshold  Precision     Recall           F-score")
print("Barbacoan     2  ", barb_scores_2)
print("Barbacoan     4  ", barb_scores_4)
print("Indo-European 2  ", ie_scores_2)
print("Indo-European 4  ", ie_scores_4)

# Trying Eastern Austronesian data gives weird error - why?
# Scores are the same with different thresholds + why?

