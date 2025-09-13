import pandas as pd
import json
import os
import gc
import re
import time
import numpy as np
import unicodedata
import math
import datetime
import pickle
import ast
import krippendorff
from sklearn.metrics import cohen_kappa_score, f1_score, multilabel_confusion_matrix, recall_score, precision_score
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelBinarizer



"""
Modifications:
- make sure pdf reading errors are not assessed.
- Make rule of law just T/F law-binding
- Merge institutional and fisheries management
- what about ordinal labels? 
"""

## Constant variables
v=9


## Read in Data

# human answers
human_df = pd.read_excel(f'/homedata/dveytia/Product_4_data/data/raw-data/coding-anwers-human/testList_answers_df_v{v}_human.xlsx')
human_df = human_df.loc[np.where(human_df['pdf reading error'].str.contains('PDF corruption detected')==True, False, True),]
human_df['coder'] = 'Human'
human_df = human_df.sort_values(by=['id'])

human_results_df = pd.read_excel(f'/homedata/dveytia/Product_4_data/data/raw-data/coding-anwers-human/testList_answers_df_studyResults_v{v}_human.xlsx')
human_results_df['coder'] = 'Human'
human_results_df = human_results_df.sort_values(by=['id'])
human_results_df = human_results_df[human_results_df['id'].isin(human_df.id.to_list())]


# Deepseek answers
compiled_answer_directory = '/homedata/dveytia/Product_4_data/outputs/testListDeepseekAnswers_compiled/'
answers_df = pd.read_excel(f'{compiled_answer_directory}testList_answers_df_v{v}_cleaned.xlsx')
answers_df['coder'] = 'DeepSeek 7B'
answers_df = answers_df[answers_df['id'].isin(human_df.id.to_list())]

answers_study_results_df = pd.read_excel(f'{compiled_answer_directory}testList_answers_df_studyResults_v{v}_cleaned.xlsx')
answers_study_results_df['coder'] = 'DeepSeek 7B'
answers_study_results_df = answers_study_results_df[answers_study_results_df['id'].isin(human_df.id.to_list())]


## Format Data 
col2type = {
    'bool': ['include', 'procedural_equity'],
    'str': ['coder','spatial_scale','time_scale',
            'data_type','result_effect'],
    'list': ['intervention_institutional',
             'intervention_technology',
             'intervention_infrastructure',
             'climatic_impact_driver',
             'study_method',
             'continent',
             'governance_body',
             'rules_of_law',
             'result_type'
            ],
    'int':['id']
}

# Convert to columns
def parse_list(value):
    if pd.isna(value):
        return []
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []

# convert column types
def convert_columns(data,col2type):
    # Loop through the dict and cast each column appropriately
    for dtype, columns in col2type.items():
        for col in columns:
            if col not in data.columns:
                continue  # Skip missing columns
            if dtype == 'bool':
                data[col] = data[col].astype(bool)
            elif dtype == 'str':
                data[col] = data[col].astype(str)
            elif dtype == 'int':
                data[col] = pd.to_numeric(data[col], errors='coerce').astype('Int64')
            elif dtype == 'list':
                data[col] = data[col].apply(parse_list)
    return data




def mask_excluded_rows(df, list_columns=None, include_col='include', id_cols=None):
    df = df.copy()
    if list_columns is None:
        list_columns = []
    if id_cols is None:
        id_cols = ['id', 'coder']

    # Rows where inclusion is False (bool or str 'False')
    mask = df[include_col].astype(str).str.lower() == 'false'

    for col in df.columns:
        if col in id_cols or col == include_col:
            continue
        if col in list_columns:
            df.loc[mask, col] = df.loc[mask, col].apply(lambda _: [])
        else:
            df.loc[mask, col] = np.nan

    return df




def mask_excluded_rows_by_human(human_df, answers_df, list_columns=None, include_col='include', id_cols=None):
    if list_columns is None:
        list_columns = []
    if id_cols is None:
        id_cols = ['id', 'coder']

    # Merge to bring the 'include' column from human_df into answers_df
    merged = answers_df.merge(
        human_df[id_cols + [include_col]],
        on='id',
        suffixes=('', '_human'),
        how='left',
        sort=False
    )

    # Create exclusion mask
    exclusion_mask = merged[f"{include_col}_human"].astype(str).str.lower().isin(['false', 'nan', 'none'])

    # Copy answers_df to modify
    masked_df = answers_df.copy()

    # Get the indices to mask
    # indices_to_mask = exclusion_mask[exclusion_mask].index
    indices_to_mask = merged.loc[exclusion_mask,'id'].to_list()

    for col in masked_df.columns:
        if col in id_cols or col == include_col:
            continue
        if col in list_columns:
            # Assign empty list for the correct number of rows
            # masked_df.loc[indices_to_mask, col] = masked_df.loc[indices_to_mask, col].apply(lambda _: [])
            masked_df.loc[masked_df['id'].isin(indices_to_mask), col] = masked_df.loc[masked_df['id'].isin(indices_to_mask), col].apply(lambda _: [])
        else:
            # masked_df.loc[indices_to_mask, col] = np.nan
            masked_df.loc[masked_df['id'].isin(indices_to_mask), col]

    return masked_df


def standardize_nans(df):
    return df.replace(
        to_replace=['nan', 'NaN', 'None', 'NULL', 'null', ''],
        value=np.nan
    ).astype(object)
        
## Apply function to convert columns
human_df = convert_columns(human_df, col2type)
human_df = mask_excluded_rows(human_df, list_columns=col2type.get('list'),id_cols = ['id', 'coder'])
human_df = standardize_nans(human_df)

human_results_df = convert_columns(human_results_df, col2type)
human_results_df = standardize_nans(human_results_df)


answers_df = convert_columns(answers_df, col2type)
# answers_df = mask_excluded_rows(answers_df, list_columns=col2type.get('list'), id_cols = ['id', 'coder'])
# for model, mask rows based on human decisions as well
answers_df = mask_excluded_rows_by_human(human_df=human_df, answers_df=answers_df, list_columns=col2type.get('list'), id_cols=['id', 'coder'])
answers_df = standardize_nans(answers_df)

answers_study_results_df = convert_columns(answers_study_results_df, col2type)
answers_study_results_df = standardize_nans(answers_study_results_df)

## Compute agreement statistic

def classify_kappa_score(kappa):
    if kappa < 0:
        return 'Poor'
    elif kappa < 0.20:
        return 'Slight'
    elif kappa < 0.40:
        return 'Fair'
    elif kappa < 0.60:
        return 'Moderate'
    elif kappa < 0.80:
        return 'Substantial'
    else:
        return 'Almost perfect'

def classify_f1_score(f1):
    if f1 < 0.20:
        return 'Poor'
    elif f1 < 0.40:
        return 'Fair'
    elif f1 < 0.60:
        return 'Moderate'
    elif f1 < 0.80:
        return 'Good'
    else:
        return 'Excellent'

def classify_alpha_score(alpha):
    if alpha < 0:
        return 'Less than chance'
    elif alpha < 0.21:
        return 'Poor'
    elif alpha < 0.41:
        return 'Fair'
    elif alpha < 0.61:
        return 'Moderate'
    elif alpha < 0.81:
        return 'Substantial'
    else:
        return 'Near-perfect'





def compute_cohen_kappa(human_df, model_df, col):
    mask = human_df[col].notna() & model_df[col].notna()
    if mask.sum() == 0:
        return None
    y_true = human_df.loc[mask, col].astype(str)
    y_pred = model_df.loc[mask, col].astype(str)
    return cohen_kappa_score(y_true, y_pred)




def compute_multilabel_cohen_kappa(human_df, model_df, col):
    mask = human_df[col].notna() & model_df[col].notna()
    if mask.sum() == 0:
        return None, {}

    # Ensure all entries are lists
    y_true = human_df.loc[mask, col].apply(lambda x: [x] if isinstance(x, str) else x)
    y_pred = model_df.loc[mask, col].apply(lambda x: [x] if isinstance(x, str) else x)
    
    
    y_true = y_true.apply(lambda x: x if isinstance(x, list) else [])
    y_pred = y_pred.apply(lambda x: x if isinstance(x, list) else [])

    # Fit binarizer across both datasets
    mlb = MultiLabelBinarizer()
    mlb.fit(y_true.tolist() + y_pred.tolist())

    y_true_bin = mlb.transform(y_true)
    y_pred_bin = mlb.transform(y_pred)

    # Compute Cohen's kappa per label
    label_kappas = {}
    for i, label in enumerate(mlb.classes_):
        try:
            kappa = cohen_kappa_score(y_true_bin[:, i], y_pred_bin[:, i])
            label_kappas[label] = kappa
        except Exception:
            label_kappas[label] = None

    # Compute macro-average (ignore None)
    valid_kappas = [k for k in label_kappas.values() if k is not None]
    kappa_macro = sum(valid_kappas) / len(valid_kappas) if valid_kappas else None

    return kappa_macro, label_kappas



def compute_f1_score(human_df, model_df, col):
    mask = human_df[col].notna() & model_df[col].notna()
    if mask.sum() == 0:
        return None
    
    y_true = human_df.loc[mask, col]
    y_pred = model_df.loc[mask, col]

    # # Single-label case
    # y_true = y_true.astype(str)
    # y_pred = y_pred.astype(str)

    f1 = f1_score(y_true.to_list(), y_pred.to_list())
    rec = recall_score(y_true.to_list(), y_pred.to_list())
    prec = precision_score(y_true.to_list(), y_pred.to_list())
   
    return f1, rec, prec, y_true.sum()





def compute_multilabel_f1_score(human_df, model_df, col):
    from sklearn.metrics import f1_score
    from sklearn.preprocessing import MultiLabelBinarizer

    mask = human_df[col].notna() & model_df[col].notna()
    if mask.sum() == 0:
        return None, {}

    y_true = human_df.loc[mask, col]
    y_pred = model_df.loc[mask, col]

    # 🛠️ Ensure each value is a list (even for single labels)
    def ensure_list(val):
        if isinstance(val, list):
            return val
        elif pd.isna(val):
            return []
        else:
            return [val]

    y_true = y_true.apply(ensure_list)
    y_pred = y_pred.apply(ensure_list)

    mlb = MultiLabelBinarizer()
    mlb.fit(y_true.tolist() + y_pred.tolist())

    y_true_bin = mlb.transform(y_true)
    y_pred_bin = mlb.transform(y_pred)

    f1_macro = f1_score(y_true_bin, y_pred_bin, average='macro', zero_division=0)
    rec_macro = recall_score(y_true_bin, y_pred_bin, average = 'macro')
    prec_macro = precision_score(y_true_bin, y_pred_bin, average = 'macro')
    
    f1_labels = f1_score(y_true_bin, y_pred_bin, average=None, zero_division=0)
    rec_labels = recall_score(y_true_bin, y_pred_bin, average=None, zero_division=0)
    prec_labels = precision_score(y_true_bin, y_pred_bin, average=None, zero_division=0)

    
    label_nsamples = np.sum(y_true_bin, axis=0)

    return f1_macro, rec_macro, prec_macro, dict(zip(mlb.classes_, f1_labels)), dict(zip(mlb.classes_, rec_labels)), dict(zip(mlb.classes_, prec_labels)), dict(zip(mlb.classes_, label_nsamples))




def compute_krippendorff_alpha(human_df, model_df, col):
    mask = human_df[col].notna() & model_df[col].notna()
    if mask.sum() == 0:
        return None

    vals = [
        list(human_df.loc[mask, col].astype(str)),
        list(model_df.loc[mask, col].astype(str))
    ]
    try:
        return krippendorff.alpha(
            reliability_data=vals,
            level_of_measurement='nominal',
            value_domain=None
        )
    except Exception as e:
        print(f"Error computing alpha for {col}: {e}")
        return None



def compute_multilabel_krippendorff_alpha(human_df, model_df, col):
    # Mask rows where either side is missing
    mask = human_df[col].notna() & model_df[col].notna()
    if mask.sum() == 0:
        return None, {}

    # Ensure all entries are lists
    y_true = human_df.loc[mask, col].apply(lambda x: x if isinstance(x, list) else [])
    y_pred = model_df.loc[mask, col].apply(lambda x: x if isinstance(x, list) else [])

    # Binarize multilabels
    mlb = MultiLabelBinarizer()
    mlb.fit(y_true.tolist() + y_pred.tolist())

    y_true_bin = mlb.transform(y_true)
    y_pred_bin = mlb.transform(y_pred)

    label_alphas = {}
    for i, label in enumerate(mlb.classes_):
        try:
            # reliability_data: rows = raters, columns = items
            reliability_data = np.array([y_true_bin[:, i], y_pred_bin[:, i]])
            alpha = krippendorff.alpha(
                reliability_data=reliability_data,
                level_of_measurement='nominal',
                value_domain=[0, 1]  # Binary: present or absent
            )
            label_alphas[label] = alpha
        except Exception as e:
            print(f"Error for label '{label}': {e}")
            label_alphas[label] = None

    # Compute macro alpha (ignore None)
    valid_alphas = [a for a in label_alphas.values() if a is not None]
    macro_alpha = sum(valid_alphas) / len(valid_alphas) if valid_alphas else None

    return macro_alpha, label_alphas



def run_agreement_analysis(human_df, model_df, single_label_cols, multi_label_cols):
    results = {}

    for col in single_label_cols:
        kappa = compute_cohen_kappa(human_df, model_df, col)
        alpha = compute_krippendorff_alpha(human_df, model_df, col)
        f1, rec, prec, n_samples = compute_f1_score(human_df, model_df, col)
        results[col] = {
            'label_n_samples': {col: n_samples},
            'kappa': kappa,
            'kappa_level': classify_kappa_score(kappa) if kappa is not None else None,
            'alpha': alpha,
            'alpha_level': classify_alpha_score(alpha) if alpha is not None else None,
            'f1': f1,
            'recall':rec,
            'precision':prec,
            'f1_level': classify_f1_score(f1) if f1 is not None else None,
        }

    for col in multi_label_cols:
        kappa, kappa_label = compute_multilabel_cohen_kappa(human_df, model_df, col)
        f1,rec, prec, f1_label,rec_label, prec_label, label_samples = compute_multilabel_f1_score(human_df, model_df, col)
        # alpha, alpha_label = compute_multilabel_krippendorff_alpha(human_df, model_df, col)
        alpha = compute_krippendorff_alpha(human_df, model_df, col)
        results[col] = {
            'label_n_samples': label_samples,
            'kappa': kappa,
            'kappa_level': classify_kappa_score(kappa) if kappa is not None else None,
            'kappa_label': {label: (score, classify_kappa_score(score)) for label, score in kappa_label.items()},
            'f1': f1,
            'recall':rec,
            'precision':prec,
            'f1_level': classify_f1_score(f1) if f1 is not None else None,
            'f1_label': {label: (score, classify_f1_score(score)) for label, score in f1_label.items()},
            'recall_label': rec_label,
            'precision_label': prec_label,
            'alpha': alpha,
            'alpha_level': classify_alpha_score(alpha) if alpha is not None else None,
            # 'alpha_label': {label: (score, classify_f1_score(score)) for label, score in alpha_label.items()},
        }

    return results



## Compute analysis


# For general results ---------------
single_label_cols = col2type.get('bool') #'spatial_scale', 'time_scale', 

multi_label_cols = ['spatial_scale','time_scale','intervention_institutional',
                    'intervention_technology','intervention_infrastructure',
                    'climatic_impact_driver','study_method',
                    'continent','governance_body','rules_of_law'
                   ]

results = run_agreement_analysis(human_df, answers_df, single_label_cols, multi_label_cols)
pd.DataFrame(results).T  # To view results nicely


## Just display F1 values ----
f1_rows = []
for variable, result in results.items():
    f1_macro = result.get("f1")
    recall_macro = result.get("recall")
    precision_macro = result.get("precision")
    f1_labels = result.get("f1_label")
    f1_level = result.get("f1_level")
    recall_labels = result.get("recall_label")
    precision_labels = result.get("precision_label")
    label_n_samples = result.get("label_n_samples")

    if f1_labels is None:
        for label, n in label_n_samples.items():
            f1_rows.append({
                "Variable": variable,
                "F1 macro": None,
                "Label": label,
                "F1 label": f1_macro,
                "Recall label": recall_macro,
                "Precision label": precision_macro,
                "N samples": n,
                "F1 label class": f1_level,
                
            })
    else:
        for label, (score, level) in f1_labels.items():
            n = label_n_samples.get(label, 0)
            f1_rows.append({
                "Variable": variable,
                "F1 macro": f1_macro,
                "Label": label,
                "F1 label": score,
                "Recall label": recall_labels.get(label),
                "Precision label": precision_labels.get(label),
                "N samples": n,
                "F1 label class": level,
            })

f1_df = pd.DataFrame(f1_rows)
f1_df['Variable'] = f1_df.Variable.apply(lambda x: x.replace("_"," "))

f1_df.to_excel(f'/homedata/dveytia/Product_4_data/outputs/testList_f1_scores_v{v}.xlsx', index=False)

## Keep: include, procedural_equity, spatial_scale, all the interventions, climatic_impact_driver, study_method, governance_body, rules_of_law
# Remove: time_scale 
f1_df[f1_df['F1 label']> 0.5]



# For study results
study_results = run_agreement_analysis(
    human_results_df, 
    answers_study_results_df, 
    single_label_cols = [],
    multi_label_cols = ['result_type', 'data_type', 'result_effect']
)

pd.DataFrame(study_results).T 


f1_results_rows = []
for variable, result in study_results.items():
    f1_macro = result.get("f1")
    recall_macro = result.get("recall")
    precision_macro = result.get("precision")
    f1_labels = result.get("f1_label")
    f1_level = result.get("f1_level")
    recall_labels = result.get("recall_label")
    precision_labels = result.get("precision_label")
    label_n_samples = result.get("label_n_samples")

    if f1_labels is None:
        for label, n in label_n_samples.items():
            f1_results_rows.append({
                "Variable": variable,
                "F1 macro": None,
                "Label": label,
                "F1 label": f1_macro,
                "Recall label": recall_macro,
                "Precision label": precision_macro,
                "N samples": n,
                "F1 label class": f1_level,
                
            })
    else:
        for label, (score, level) in f1_labels.items():
            n = label_n_samples.get(label, 0)
            f1_results_rows.append({
                "Variable": variable,
                "F1 macro": f1_macro,
                "Label": label,
                "F1 label": score,
                "Recall label": recall_labels.get(label),
                "Precision label": precision_labels.get(label),
                "N samples": n,
                "F1 label class": level,
            })

f1_results_df = pd.DataFrame(f1_results_rows)
f1_results_df['Variable'] = f1_results_df.Variable.apply(lambda x: x.replace("_"," "))
f1_results_df

f1_results_df.to_excel(f'/homedata/dveytia/Product_4_data/outputs/testList_studyResults_f1_scores_v{v}.xlsx', index=False)


# So suggest to keep result_type, and effect Positive vs other. 
f1_results_df[f1_results_df['Recall label']> 0.4]
f1_results_df[f1_results_df['F1 label']> 0.4]


### Try regrouping labels -- not needed
"""
relabel_map = {
    'Fisheries management': 'Institutional',
    'Fishing technologies':'Technologies',
    'Disaster response technologies': 'Technologies',
    'Interview':'Social primary',
    'Survey': 'Social primary',
    'Workshop': 'Social primary',
    'Regional': '> Local',
    'National': '> Local',
    'Global': '> Local',
}

def relabel_dataframe(df, relabel_map):
    def relabel_value(val):
        # Handle list-like values first
        if isinstance(val, list):
            new_vals = [relabel_map.get(v, v) for v in val]
            return list(dict.fromkeys(new_vals))  # Remove duplicates, keep order
        # Handle NaN values for scalar inputs
        if pd.isna(val):
            return val
        # Handle scalar string values
        return relabel_map.get(val, val)
    
    df = df.copy()
    for col in df.columns:
        df[col] = df[col].apply(relabel_value)
    
    return df


results_relabel = run_agreement_analysis(
    relabel_dataframe(human_df, relabel_map), 
    relabel_dataframe(answers_df, relabel_map), 
    single_label_cols, multi_label_cols
)
pd.DataFrame(results_relabel).T  # To view results nicely
"""

