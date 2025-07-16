
import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------------------------------------
# AUTO-UPDATER FOR NORMALIZED DATASET
# -------------------------------------------------------------

def update_normalized_dataset(force=False):
    """
    Checks if the normalized dataset exists. If not, or if 'force' is True,
    it regenerates it from the original dataset.

    Parameters:
    - force: If True, regenerates even if the file exists.
    """
    normalized_path = "normalized_encoded.csv"
    raw_path = "tenants_dataset.csv"

    if not os.path.exists(normalized_path) or force:
        print("⚙️ Regenerating normalized dataset...")

        # Load original tenant profiles
        df_raw = pd.read_csv(raw_path)

        # Split 'languages_spoken' into binary columns
        all_languages = ['English', 'Spanish', 'French', 'German', 'Italian']
        for lang in all_languages:
            df_raw[f'lang_{lang}'] = df_raw['languages_spoken'].apply(lambda x: int(lang in x))

        # Drop unused columns
        df_raw.drop(['id_tenant', 'languages_spoken'], axis=1, inplace=True)

        # Categorical columns to one-hot encode
        categorical_cols = [
            'sleep_schedule', 'work_shift', 'energy_rhythm', 'education_level',
            'social_level', 'cooking_preference', 'preferred_music_genre',
            'ideal_weekend_plan', 'noise_tolerance', 'relationship_status'
        ]
        df_encoded = pd.get_dummies(df_raw, columns=categorical_cols)

        # Convert Yes/No binary columns
        binary_cols = [
            'likes_reading', 'likes_cooking', 'on_diet', 'smoker', 'likes_pets',
            'pet_allergy', 'frequent_visits', 'remote_worker', 'plays_sports',
            'listens_loud_music', 'shares_common_items'
        ]
        for col in binary_cols:
            df_encoded[col] = df_encoded[col].map({'Yes': 1, 'No': 0})

        # Apply MinMaxScaler
        scaler = MinMaxScaler()
        normalized_array = scaler.fit_transform(df_encoded)
        df_normalized = pd.DataFrame(normalized_array, columns=df_encoded.columns)

        # Save to CSV
        df_normalized.to_csv(normalized_path, index=False)
        print("✅ Normalized dataset saved as 'normalized_encoded.csv'.")
    else:
        print("✅ Normalized dataset already exists.")

# Ensure the normalized dataset is available before anything else
update_normalized_dataset()

# Load preprocessed datasets
df_normalized = pd.read_csv("normalized_encoded.csv")
df_raw = pd.read_csv("tenants_dataset.csv")


# -------------------------------------------------------------
# MAIN COMPATIBILITY FUNCTION
# -------------------------------------------------------------

def compatible_tenants(tenant_ids, top_n=5):
    """
    Recommends the top N most compatible tenants based on cosine similarity.

    Parameters:
    - tenant_ids: List of tenant IDs (1-based, e.g., [12, 55])
    - top_n: Number of recommendations to return

    Returns:
    - Tuple:
        0. Transposed DataFrame with characteristics of seed + recommended tenants
        1. Series with similarity scores (index = recommended tenant IDs)
    """
    # Validate that tenant IDs are within range
    if any(t < 1 or t > len(df_normalized) for t in tenant_ids):
        return "One or more tenant IDs are out of range."

    # Convert 1-based IDs to 0-based indices
    seed_indices = [t - 1 for t in tenant_ids]

    # Extract vectors for seed tenants and full dataset
    X_seed = df_normalized.iloc[seed_indices].to_numpy()
    X_all = df_normalized.to_numpy()

    # Compute cosine similarity between seed and all profiles
    similarity_scores = cosine_similarity(X_seed, X_all)
    average_similarity = np.mean(similarity_scores, axis=0)

    # Exclude seed tenants from recommendations
    for idx in seed_indices:
        average_similarity[idx] = -1

    # Select top N most similar tenant indices
    top_indices = np.argsort(average_similarity)[-top_n:][::-1]
    top_tenant_ids = [i + 1 for i in top_indices]  # Convert back to 1-based

    # Extract raw profile data
    seed_profiles = df_raw[df_raw['id_tenant'].isin(tenant_ids)]
    top_profiles = df_raw[df_raw['id_tenant'].isin(top_tenant_ids)]

    # Combine into a single transposed DataFrame
    result_df = pd.concat([seed_profiles.set_index("id_tenant").T,
                           top_profiles.set_index("id_tenant").T], axis=1)

    # Prepare similarity scores
    similarities = pd.Series(average_similarity[top_indices],
                             index=top_tenant_ids, name="Similarity")

    return result_df, similarities
