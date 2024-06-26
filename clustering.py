import lingpy
from levenshtein_dist_calc import LevenshteinDistanceCalculator
from alignment_calculator import AlignCalculator
import nltk
from read_tab_files import TabFileReader
import bcubed
from collections import defaultdict


# calculate distance matrix from cognate list (integrate with levenshtein distance calc maybe)
class Clustering:
    def __init__(
        self,
        cognacy_file,
        goldfile,
        threshold: float,
        distance_metric="levenshtein_nltk",
    ):
        self.cognacy_file = cognacy_file
        self.goldfile = goldfile
        self.threshold = threshold
        self.distance_metric = distance_metric

        self.clusters, self.gold_clusters = self.clustering()

    def get_distancematrix(self, cognate_list):
        n = len(cognate_list)
        distance_matrix = [[0] * n for _ in range(n)]

        if self.distance_metric == "levenshtein_custom":
            ldc = LevenshteinDistanceCalculator()
        elif self.distance_metric == "levenshtein_custom_phonetic":
            ldc = LevenshteinDistanceCalculator(use_phonetic=True)
        elif self.distance_metric in ["global_alignment", "local_alignment"]:
            ac = AlignCalculator()

        for i in range(n):
            for j in range(i, n):
                source = cognate_list[i]
                target = cognate_list[j]

                if (
                    source == "" or target == ""
                ):  # if one cognate in pair is missing, null value
                    distance_matrix[i][j] = distance_matrix[j][i] = float("nan")
                else:
                    if self.distance_metric == "levenshtein_nltk":
                        dist_score = nltk.edit_distance(source, target)
                    elif self.distance_metric == "levenshtein_custom":
                        dist_score = ldc.calculate_dl_distance(source, target)
                    elif self.distance_metric == "levenshtein_custom_phonetic":
                        dist_score = ldc.calculate_dl_distance(source, target)
                    elif self.distance_metric == "global_alignment":
                        dist_score, _, _ = ac.global_alignment(source, target)
                    elif self.distance_metric == "local_alignment":
                        dist_score, _, _, _ = ac.local_alignment(source, target)

                    distance_matrix[i][j] = distance_matrix[j][i] = dist_score / max(
                        len(source), len(target)
                    )
        return distance_matrix

    # gold file clustering to taxa:cluster dictionary transformer for bcubed comparisons
    def gold_clust2taxa_dict(self, taxa, clusters):
        cluster_dict = {}
        for lang, cluster in zip(taxa, clusters):
            cluster_dict[lang] = set([cluster])
        return cluster_dict

    # lingpy.upgma_flat output to taxa:cluster dictionary transformer for bcubed comparisons
    def upgma2taxa_dict(self, calculated_dict):
        output_clusters = {}
        for clus, langs in calculated_dict.items():
            for lang in langs:
                output_clusters[lang] = set(str(clus))
        return output_clusters

    def remove_gaps(self, cognates, gold_cognates, taxa):
        """Removes the cognate from both lists where either
        list has a gap. Should work for all families"""
        # Save the indices where at least one of the files have a gap
        assert len(cognates) == len(gold_cognates) == len(taxa)
        empty_indices = []
        new_cognates, new_gold, new_taxa = (
            cognates.copy(),
            gold_cognates.copy(),
            taxa.copy(),
        )
        for i in range(len(cognates)):
            if cognates[i] == "":
                empty_indices.append(i)
            elif gold_cognates[i] == "":
                empty_indices.append(i)
        # Pop the items last to first
        for n in reversed(empty_indices):
            new_cognates.pop(n)
            new_gold.pop(n)
            new_taxa.pop(n)
        assert len(new_cognates) == len(new_gold) == len(new_taxa)
        return new_cognates, new_gold, new_taxa

    def prepare_comparison(self, gold_row: list, cognates: list, taxa: list) -> tuple:
        distance_matrix = self.get_distancematrix(cognates)
        cluster_dict = lingpy.flat_upgma(self.threshold, distance_matrix, taxa)
        taxa_dict = self.upgma2taxa_dict(cluster_dict)
        gold_taxadict = self.gold_clust2taxa_dict(taxa, gold_row)
        return taxa_dict, gold_taxadict

    def score(self):
        precision = 0
        recall = 0
        fscore = 0
        for i in range(len(self.clusters)):
            precision += bcubed.precision(self.clusters[i], self.gold_clusters[i])
            recall += bcubed.recall(self.clusters[i], self.gold_clusters[i])
        n_rows = len(self.clusters)
        precision /= n_rows
        recall /= n_rows
        fscore = bcubed.fscore(precision, recall)
        return round(precision, 4), round(recall, 4), round(fscore, 4)

    def clustering(self):
        """Prepares the cluster dictionaries for comparison"""
        full_taxa = list(self.cognacy_file.iloc[0][1:])
        clusters = []
        gold_clusters = []
        for i in range(1, len(self.cognacy_file)):
            cognates = list(self.cognacy_file.iloc[i][1:])
            gold_cognates = list(self.goldfile.iloc[i][1:])
            cognates, gold_cognates, cut_taxa = self.remove_gaps(
                cognates, gold_cognates, full_taxa
            )  # Remove gaps
            if cognates:  # If the list is not empty after gaps are removed
                taxa_dict, gold_taxadict = self.prepare_comparison(
                    gold_cognates, cognates, cut_taxa
                )
                clusters.append(taxa_dict)
                gold_clusters.append(gold_taxadict)
        assert len(clusters) == len(gold_clusters)
        return clusters, gold_clusters


if __name__ == "__main__":

    barb_cognacy = TabFileReader.tab_reader(
        "chl2024_barbacoandata/chl2023_barbacoan_cognacy.tab"
    )
    barb_forms = TabFileReader.tab_reader(
        "chl2024_barbacoandata/chl2023_barbacoan_forms.tab"
    )

    eau_cognacy = TabFileReader.tab_reader(
        "chl2024_eastern-austronesiandata/chl2023_eastern-austronesian_cognacy.tab"
    )
    eau_forms = TabFileReader.tab_reader(
        "chl2024_eastern-austronesiandata/chl2023_eastern-austronesian_forms.tab"
    )

    ie_cognacy = TabFileReader.tab_reader("chl2024_iedata/chl2023_iedata_cognacy.tab")
    ie_forms = TabFileReader.tab_reader("chl2024_iedata/chl2023_iedata_forms.tab")

    barb_clusters = Clustering(barb_forms, barb_cognacy, threshold=0.8)
    eau_clusters = Clustering(eau_forms, eau_cognacy, threshold=0.6)
    ie_clusters = Clustering(ie_forms, ie_cognacy, threshold=0.8)

    print("Clustering of 'dog':", ie_clusters.clusters[31])
    print("Knows cognate groups:", ie_clusters.gold_clusters[31])
    print(
        "Prec:",
        bcubed.precision(ie_clusters.clusters[31], ie_clusters.gold_clusters[31]),
    )
    print(
        "Rec:",
        bcubed.recall(ie_clusters.clusters[31], ie_clusters.gold_clusters[31]),
    )

    print("Family           Threshold Precision Recall F-score")
    print("Indo-European        .8  ", ie_clusters.score())
    print("Barbacoan            .8  ", barb_clusters.score())
    print("Eastern Austronesian .6  ", eau_clusters.score())

    # Trying Eastern Austronesian data gives weird error - why?
    # Scores are the same with different thresholds + why?
