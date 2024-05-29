import pandas as pd
import matplotlib.pyplot as plt

from clustering import Clustering
from read_tab_files import TabFileReader

from trimming import trim_all

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


#######


form_data = {
    "barb": (barb_forms, barb_cognacy),
    "eau": (eau_forms, eau_cognacy),
    "ie": (ie_forms, ie_cognacy),
}


## Add new metric #TODO
distance_metrics = [
    "levenshtein_nltk",
    "levenshtein_custom",
    "levenshtein_custom_phonetic",
    "global_alignment",
    "local_alignment",
]

optimal_thresholds = {
    "barb": 0.8,
    "eau": 0.6,
    "ie": 0.8,
}

optimal_trim_thresholds = {
    "barb": {"core": (0.0,0.8),
             "gap": (0.7,0.7)},
    "eau": {"core": (0.1,0.4),
            "gap": (1.0,0.7)},
    "ie": {"core": (0.0,0.7),
           "gap": (0.8,0.8)},
}

precision_df = pd.DataFrame(columns=distance_metrics, index=form_data.keys())
recall_df = pd.DataFrame(columns=distance_metrics, index=form_data.keys())
f1_df = pd.DataFrame(columns=distance_metrics, index=form_data.keys())

core_prec = []
core_recall = []
core_f1 = []
gap_prec = []
gap_recall = []
gap_f1 = []

for form_name, (forms, cognacy) in form_data.items():
    for distance_metric in distance_metrics:
        print(f"Calculating scores for {form_name} forms using {distance_metric}...")

        clusters = Clustering(
            forms,
            cognacy,
            threshold=optimal_thresholds[form_name],
            distance_metric=distance_metric,
        )

        precision, recall, f1 = clusters.score()
        precision_df.loc[form_name, distance_metric] = precision
        recall_df.loc[form_name, distance_metric] = recall
        f1_df.loc[form_name, distance_metric] = f1
        
    #gap-oriented
    gap_form = trim_all(
        forms,
        threshold=optimal_trim_thresholds[form_name]["gap"][0],
        strategy='gap-oriented'
    )
    
    clusters = Clustering(
        gap_form,
        cognacy,
        threshold=optimal_trim_thresholds[form_name]["gap"][1],
    )

    precision, recall, f1 = clusters.score()
    gap_prec.append(precision)
    gap_recall.append(recall)
    gap_f1.append(f1)
    
    #core-oriented
    core_form = trim_all(
        forms,
        threshold=optimal_trim_thresholds[form_name]["core"][0]
    )
    clusters = Clustering(
        core_form,
        cognacy,
        threshold=optimal_trim_thresholds[form_name]["core"][1],
    )

    precision, recall, f1 = clusters.score()
    core_prec.append(precision)
    core_recall.append(recall)
    core_f1.append(f1)
    
precision_df["gap_trim"] = gap_prec
precision_df["core_trim"] = core_prec

recall_df["gap_trim"] = gap_recall
recall_df["core_trim"] = core_recall

f1_df["gap_trim"] = gap_f1
f1_df["core_trim"] = core_f1

## Add new label #TODO
legend_labels = [
    "Levenshtein NLTK",
    "Levenshtein Custom",
    "Levenshtein Phonetic",
    "Global Alignment",
    "Local Alignment",
    "NLTK w/ Gap-trim",
    "NLTK w/ Core-trim"
]

x_labels = [
    "Barbacoan\n(cluster threshold: 0.8)\n(gap t.hold: 0.7, cluster t.hold:0.7)\n(core t.hold: 0.0, cluster t.hold:0.8)",
    "Eastern Austronesian\n(cluster threshold:0.6)\n(gap t.hold: 1.0, cluster t.hold:0.7)\n(core t.hold: 0.1, cluster t.hold:0.4)",
    "Indo-European\n(cluster threshold:0.8)\n(gap t.hold: 0.8, cluster t.hold:0.8)\n(core t.hold: 0.0, cluster t.hold:0.7)",
]

## Add any new color #TODO
color_palette = ["#4daf4a", "#377eb8", "#ff7f00", "#984ea3", "#e41a1c", "0.5", "0"]

ax = precision_df.plot(kind="bar", figsize=(12, 5), width=0.7, color=color_palette)
plt.title("Precision Scores")
# plt.xlabel("Form Data")
plt.ylabel("Precision")
plt.legend(
    title="Distance Metric",
    labels=legend_labels,
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
)
plt.xticks(rotation=0)
plt.xticks(ticks=range(len(precision_df.index)), labels=x_labels)
plt.ylim(0, 1.05)
for p in ax.patches:
    ax.annotate(
        str(round(p.get_height(), 2)),
        (p.get_x() + p.get_width() / 2.0, p.get_height()),
        ha="center",
        va="center",
        xytext=(0, 5),
        textcoords="offset points",
    )
plt.tight_layout()
plt.savefig("./plots/precision_all")
plt.show()


ax = recall_df.plot(kind="bar", figsize=(12, 5), width=0.7, color=color_palette)
plt.title("Recall Scores")
# plt.xlabel("Form Data")
plt.ylabel("Recall")
plt.legend(
    title="Distance Metric",
    labels=legend_labels,
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
)
plt.xticks(rotation=0)
plt.xticks(ticks=range(len(recall_df.index)), labels=x_labels)
plt.ylim(0, 1.05)
for p in ax.patches:
    ax.annotate(
        str(round(p.get_height(), 2)),
        (p.get_x() + p.get_width() / 2.0, p.get_height()),
        ha="center",
        va="center",
        xytext=(0, 5),
        textcoords="offset points",
    )
plt.tight_layout()
plt.savefig("./plots/recall_all")
plt.show()


ax = f1_df.plot(kind="bar", figsize=(12, 5), width=0.7, color=color_palette)
plt.title("F1 Scores")
# plt.xlabel("Form Data")
plt.ylabel("F1 Score")
plt.legend(
    title="Distance Metric",
    labels=legend_labels,
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
)
plt.xticks(rotation=0)
plt.xticks(ticks=range(len(f1_df.index)), labels=x_labels)
plt.ylim(0, 1.05)
for p in ax.patches:
    ax.annotate(
        str(round(p.get_height(), 2)),
        (p.get_x() + p.get_width() / 2.0, p.get_height()),
        ha="center",
        va="center",
        xytext=(0, 5),
        textcoords="offset points",
    )
plt.tight_layout()
plt.savefig("./plots/f1_all")
plt.show()
