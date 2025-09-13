from unidecode import unidecode
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
from sklearn.metrics import cohen_kappa_score, f1_score
from sklearn.preprocessing import MultiLabelBinarizer

## Constant variables
v=7

"""
Try:
- merging 'Institutional' and 'Fisheries management'
- merging 'Interview', 'Survey', 'Workshop' together. Change Observation to Ecological Observation and 'Case study/anecdotal'
"""


## Read in Data

# human answers
human_df = pd.read_excel(f'/homedata/dveytia/Product_4_data/data/raw-data/coding-anwers-human/testList_answers_df_v{v}_human.xlsx')
human_df = human_df[human_df['coder']=='Human']
human_df = human_df.sort_values(by=['id'])
human_results_df = pd.read_excel(f'/homedata/dveytia/Product_4_data/data/raw-data/coding-anwers-human/testList_answers_df_studyResults_v{v}_human.xlsx')
human_results_df = human_results_df[human_results_df['coder']=='Human']
human_results_df = human_results_df.sort_values(by=['id'])


# Deepseek answers
compiled_answer_directory = '/homedata/dveytia/Product_4_data/outputs/testListDeepseekAnswers_compiled/'
answers_df = pd.read_excel(f'{compiled_answer_directory}testList_answers_df_v{v}.xlsx')
answers_df['coder'] = 'DeepSeek 7B'
answers_df6 = pd.read_excel(f'{compiled_answer_directory}testList_answers_df_v6.xlsx')
answers_study_results_df = pd.read_excel(f'{compiled_answer_directory}testList_answers_df_studyResults_v6.xlsx')

# Combine deepseek answers (as v7 only updated ORO and study results columns)
newCols = [col for col in answers_df6.columns if col not in answers_df.columns]
newCols.append('id')
answers_df6 = answers_df6[newCols]
answers_df = answers_df.merge(answers_df6, how='outer', on='id')
answers_df = answers_df.sort_values(by=['id'])

## Format Data 
col2type = {
    'bool': ['include', 'procedural_equity'],
    'str': ['coder','spatial_scale','time_scale','comments',
            'data_type','result_effect'],
    'list': ['intervention_institutional',
             'intervention_technology',
             'intervention_infrastructure',
             'climatic_impact_driver',
             'study_method',
             'country_names',
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


        
## Apply function to convert columns
human_df = convert_columns(human_df, col2type)
human_df = mask_excluded_rows(human_df, list_columns=col2type.get('list'),id_cols = ['id', 'coder'])
human_results_df = convert_columns(human_results_df, col2type)
answers_df = convert_columns(answers_df, col2type)
answers_df = mask_excluded_rows(answers_df, list_columns=col2type.get('list'),id_cols = ['id', 'coder'])
answers_study_results_df = convert_columns(answers_study_results_df, col2type)


## Compute agreement statistic

def compute_krippendorff_alpha_multilabel(df1, df2, column, id_col='id', coder_col='coder'):
    """
    Compute Krippendorff's alpha for multi-label categorical data
    between two annotators (e.g., human and LLM).

    Args:
        df1, df2: DataFrames with annotations.
        column: Column name containing list-style labels.
        id_col: Column that uniquely identifies each document/unit.
        coder_col: Column that identifies the rater ('Human', 'LLM', etc.)

    Returns:
        Krippendorff's alpha (float)
    """
    
    # Combine both dataframes
    combined = pd.concat([df1[[id_col, column, coder_col]], df2[[id_col, column, coder_col]]])
    
    # Replace NaN lists with empty lists
    combined[column] = combined[column].apply(lambda x: x if isinstance(x, list) else [])
    
    # Explode into binary: each row = (id, coder, label)
    exploded = (combined
                .explode(column)
                .rename(columns={column: 'label'}))
    
    # Assign a value of 1 for presence of each label
    exploded['value'] = 1
    
    # Pivot: rows = labels, columns = (id, coder), values = 1 or NaN
    pivot = exploded.pivot_table(index='label', columns=[id_col, coder_col], values='value', fill_value=0)

    # Final matrix: each column is an annotation by a coder for a unit
    reliability_data = pivot.values

    # Compute alpha with nominal metric (categorical)
    alpha = krippendorff.alpha(reliability_data=reliability_data, level_of_measurement='nominal')
    
    return alpha


def compute_krippendorff_alpha_singlelabel(df1, df2, column, id_col='id', coder_col='coder'):
    """
    Compute Krippendorff's alpha for single-label categorical variables, safely handling
    booleans and strings by converting them to integer codes.
    """
    # Combine both dataframes
    combined = pd.concat([df1[[id_col, column, coder_col]], df2[[id_col, column, coder_col]]])
    
    # Drop missing values
    combined = combined.dropna(subset=[column])

    # Convert values to string (to unify booleans, categories, etc.)
    combined[column] = combined[column].astype(str)

    # Encode unique string labels to integers
    label_lookup = {label: idx for idx, label in enumerate(sorted(combined[column].unique()))}
    combined['coded'] = combined[column].map(label_lookup)

    # Pivot to matrix: rows = coder, columns = id
    pivot = combined.pivot_table(index=coder_col, columns=id_col, values='coded', aggfunc='first')

    # Drop columns with all missing
    pivot = pivot.dropna(axis=1, how='all')

    # Convert to numeric matrix
    data = pivot.to_numpy(dtype='float')

    # Ensure there's some variation
    if pd.DataFrame(data).nunique().sum() <= 1:
        return None

    return krippendorff.alpha(reliability_data=data, level_of_measurement='nominal')




def compute_alpha_for_columns_general(df1, df2, columns, multilabel_columns, id_col='id', coder_col='coder'):
    results = {}
    for col in columns:
        try:
            if col in multilabel_columns:
                alpha = compute_krippendorff_alpha_multilabel(df1, df2, col, id_col, coder_col)
            else:
                alpha = compute_krippendorff_alpha_singlelabel(df1, df2, col, id_col, coder_col)
            results[col] = alpha
        except Exception as e:
            results[col] = f"Error: {e}"
    return results



def classify_alpha_scores(alpha_dict):
    """
    Classify Krippendorff's alpha values into interpretation categories.

    Parameters:
        alpha_dict (dict): {variable_name: alpha_value}

    Returns:
        dict: {
            'Strong': [...],
            'Substantial': [...],
            'Moderate': [...],
            'Poor': [...],
            'Very Poor': [...],
            'Worse than Chance': [...]
        }
    """
    categories = {
        'Strong': [],
        'Substantial': [],
        'Moderate': [],
        'Poor': [],
        'Very Poor': [],
        'Worse than Chance': []
    }

    for var, alpha in alpha_dict.items():
        if alpha is None:
            continue  # Skip missing data
        elif alpha >= 0.80:
            categories['Strong'].append((var, alpha))
        elif 0.67 <= alpha < 0.80:
            categories['Substantial'].append((var, alpha))
        elif 0.41 <= alpha < 0.67:
            categories['Moderate'].append((var, alpha))
        elif 0.21 <= alpha < 0.40:
            categories['Poor'].append((var, alpha))
        elif 0.01 <= alpha < 0.21:
            categories['Very Poor'].append((var, alpha))
        elif alpha < 0.01:
            categories['Worse than Chance'].append((var, alpha))

    return categories


## Compute analysis

singleLabelColumns = ['include', 'spatial_scale', 'time_scale','procedural_equity'] 
idColumns = ['id','coder','comments']
labelColumns = [col for col in human_df.columns if col not in idColumns]
multiLabelColumns = [col for col in labelColumns if col not in singleLabelColumns]

# Compute alpha scores
alphas = compute_alpha_for_columns_general(
    human_df[human_df['coder']=='Human'], 
    answers_df, 
    columns=labelColumns, 
    multilabel_columns = multiLabelColumns,
    id_col='id', 
    coder_col='coder'
)


# classify them on level of agreement 
classified = classify_alpha_scores(alphas)

for category, items in classified.items():
    print(f"\n{category} ({len(items)}):")
    for var, alpha in sorted(items, key=lambda x: x[1], reverse=True):
        print(f"  {var}: {alpha:.3f}")

"""
Strong (0):

Substantial (0):

Moderate (2):
  time_scale: 0.487
  spatial_scale: 0.432

Poor (2):
  procedural_equity: 0.278
  include: 0.266

Very Poor (1):
  climatic_impact_driver: 0.050

Worse than Chance (7):
  country_names: -0.060
  intervention_institutional: -0.092
  study_method: -0.103
  governance_body: -0.169
  intervention_infrastructure: -0.333
  rules_of_law: -0.519
  intervention_technology: -0.654
"""


## PERFORM ANALAGOUS ASSESSMENT USING OTHER METRICS----------

# score classification helper
def classify_score(score):
    if score is None:
        return 'Missing'
    elif score >= 0.80:
        return 'Strong'
    elif score >= 0.67:
        return 'Substantial'
    elif score >= 0.41:
        return 'Moderate'
    elif score >= 0.21:
        return 'Poor'
    elif score >= 0.01:
        return 'Very Poor'
    else:
        return 'Worse than Chance'


def compute_agreement_scores(human_df, model_df, columns, multilabel_columns, id_col='id'):
    results = {
        'kappa': {},     # {column: {'average': float, 'by_label': {label: score}}}
        'f1': {},        # same structure
    }

    for col in columns:
        human = human_df[[id_col, col]].copy()
        model = model_df[[id_col, col]].copy()

        # Align and join on ID
        merged = pd.merge(human, model, on=id_col, suffixes=('_human', '_model'))
        if merged.empty:
            continue

        y_true = merged[f"{col}_human"]
        y_pred = merged[f"{col}_model"]

        if col in multilabel_columns:
            # Ensure list type
            y_true = y_true.apply(lambda x: x if isinstance(x, list) else [])
            y_pred = y_pred.apply(lambda x: x if isinstance(x, list) else [])

            mlb = MultiLabelBinarizer()
            all_labels = list(set().union(*y_true, *y_pred))
            mlb.fit([all_labels])

            y_true_bin = mlb.transform(y_true)
            y_pred_bin = mlb.transform(y_pred)
            labels = mlb.classes_

            # Compute scores per label
            kappa_scores = {}
            f1_scores = {}
            for i, label in enumerate(labels):
                try:
                    kappa = cohen_kappa_score(y_true_bin[:, i], y_pred_bin[:, i])
                except ValueError:
                    kappa = None
                kappa_scores[label] = kappa

                try:
                    f1 = f1_score(y_true_bin[:, i], y_pred_bin[:, i])
                except ValueError:
                    f1 = None
                f1_scores[label] = f1

            # Store averages
            avg_kappa = np.nanmean([v for v in kappa_scores.values() if v is not None])
            avg_f1 = np.nanmean([v for v in f1_scores.values() if v is not None])

            results['kappa'][col] = {
                'average': avg_kappa,
                'classification': classify_score(avg_kappa),
                'by_label': {label: (score, classify_score(score)) for label, score in kappa_scores.items()}
            }

            results['f1'][col] = {
                'average': avg_f1,
                'classification': classify_score(avg_f1),
                'by_label': {label: (score, classify_score(score)) for label, score in f1_scores.items()}
            }

        else:
            # Single-label case
            y_true = y_true.astype(str)
            y_pred = y_pred.astype(str)

            try:
                kappa = cohen_kappa_score(y_true, y_pred)
            except ValueError:
                kappa = None

            try:
                f1 = f1_score(y_true, y_pred, average='macro')
            except ValueError:
                f1 = None

            results['kappa'][col] = {
                'average': kappa,
                'classification': classify_score(kappa),
                'by_label': None
            }

            results['f1'][col] = {
                'average': f1,
                'classification': classify_score(f1),
                'by_label': None
            }

    return results



agreement_results = compute_agreement_scores(
    human_df[human_df['coder']=='Human'], 
    answers_df,
    columns=labelColumns, 
    multilabel_columns = multiLabelColumns,
    id_col = 'id'
)

## Print results summary
for metric in ['kappa', 'f1']:
    print(f"\n=== {metric.upper()} Summary ===")
    for col, res in agreement_results[metric].items():
        print(f"{col}: {res['average']:.3f} ({res['classification']})")


"""
=== KAPPA Summary ===
include: 0.273 (Poor)
intervention_institutional: 0.306 (Poor)
intervention_technology: 0.375 (Poor)
intervention_infrastructure: 0.059 (Very Poor)
climatic_impact_driver: 0.555 (Moderate)
study_method: 0.084 (Very Poor)
spatial_scale: 0.338 (Poor)
country_names: 0.376 (Poor)
time_scale: 0.450 (Moderate)
procedural_equity: 0.130 (Very Poor)
governance_body: 0.337 (Poor)
rules_of_law: -0.008 (Worse than Chance)

=== F1 Summary ===
include: 0.625 (Moderate)
intervention_institutional: 0.453 (Moderate)
intervention_technology: 0.538 (Moderate)
intervention_infrastructure: 0.121 (Very Poor)
climatic_impact_driver: 0.656 (Moderate)
study_method: 0.150 (Very Poor)
spatial_scale: 0.381 (Poor)
country_names: 0.378 (Poor)
time_scale: 0.396 (Poor)
procedural_equity: 0.308 (Poor)
governance_body: 0.428 (Moderate)
rules_of_law: 0.133 (Very Poor)
"""


