from read_tab_files import TabFileReader
from trimming import trim, trim_all

import pandas as pd
import matplotlib.pyplot as plt

from clustering import Clustering
from read_tab_files import TabFileReader

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
    "local_alignment"
]

trimming_strategies = ["core-oriented", "gap-oriented"]

optimal_thresholds = {
    "barb": 0.8,
    "eau": 0.6,
    "ie": 0.8,
}


precision_df = pd.DataFrame(columns=distance_metrics+trimming_strategies, index=form_data.keys())
recall_df = pd.DataFrame(columns=distance_metrics+trimming_strategies, index=form_data.keys())
f1_df = pd.DataFrame(columns=distance_metrics+trimming_strategies, index=form_data.keys())

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
    for strategy in trimming_strategies:
        print(f"Calculating scores for {form_name} forms using trimming {strategy}...")
        trimmed_forms = trim_all(forms, threshold=.75, strategy=strategy)
        trimmed_clusters = Clustering(
            trimmed_forms, cognacy, threshold=optimal_thresholds[form_name])
        precision, recall, f1 = trimmed_clusters.score()
        precision_df.loc[form_name, "Trimming"] = precision
        recall_df.loc[form_name, "Trimming"] = recall
        f1_df.loc[form_name, "Trimming"] = f1

## Add new label #TODO
legend_labels = [
    "Levenshtein NLTK",
    "Levenshtein Custom",
    "Levenshtein Phonetic",
    "Global Alignment",
    "Local Alignment", 
    "Core-oriented trimming",
    "Gap-oriented trimming"
]

x_labels = [
    "Barbacoan\n(threshold: 0.8)",
    "Eastern Austronesian\n(threshold:0.6)",
    "Indo-European\n(threshold:0.8)",
]

## Add any new color #TODO
color_palette = ["#4daf4a", "#377eb8", "#ff7f00", "#984ea3", "#e41a1c"]

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
plt.savefig("./plots/precision_incl_trim")
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
plt.savefig("./plots/recall_incl_trimming")
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
plt.savefig("./plots/f1_incl_trimming")
plt.show()
