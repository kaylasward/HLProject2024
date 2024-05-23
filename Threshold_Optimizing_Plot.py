# TOP
from clustering import Clustering
from read_tab_files import TabFileReader
import matplotlib.pyplot as plt

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

def get_score_lists(cognacy_file, goldfile, thresholds:list):
    precisions = []
    recalls = []
    fscores = []
    for t in thresholds:
        clustering = Clustering(cognacy_file, goldfile, t)
        prec, rec, fscore = clustering.score()
        precisions.append(prec)
        recalls.append(rec)
        fscores.append(fscore)
    return precisions, recalls, fscores


thresholds = [0,.1,.2,.3,.4,.5,.6,.7,.8,.9, 1]
barb_precisions, barb_recalls, barb_fscores = get_score_lists(barb_forms, barb_cognacy, thresholds)
eau_precisions, eau_recalls, eau_fscores = get_score_lists(eau_forms, eau_cognacy, thresholds)
ie_precisions, ie_recalls, ie_fscores = get_score_lists(ie_forms, ie_cognacy, thresholds)

print(ie_precisions)
print(ie_recalls)
print(ie_fscores)