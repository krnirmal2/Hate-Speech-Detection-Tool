# Project Test Cases

This document outlines the test cases implemented for various sections of the Jihadist Detection System project.

## 1. `test_data_loader.py`

This file contains unit tests for the `load_data` function in `src/service/data_loader.py`. It ensures that the data loading mechanism works as expected under different scenarios.

### Test Cases:
- **`test_load_data_success`**: Verifies successful loading of a valid CSV file, including initial cleaning, dropping of missing data, and duplicate removal.
- **`test_load_data_file_not_found`**: Checks how the function handles cases where the specified CSV file does not exist.
- **`test_load_data_empty_file`**: Ensures proper behavior when an empty CSV file is provided.
- **`test_load_data_missing_columns`**: Tests the function's robustness when the input CSV is missing required columns like 'username', 'tweets', or 'followers'.

## 2. `test_graph_analysis.py`

This file contains unit tests for the social graph building and centrality computation functions in `src/service/graph_analysis.py`. It ensures the accuracy of graph construction and centrality metric calculations.

### Test Cases:
- **`test_build_social_graph_sample_data`**: Verifies the correct construction of a social graph from a DataFrame with sample user and tweet data.
- **`test_build_social_graph_empty_data`**: Checks the behavior when attempting to build a graph from an empty DataFrame.
- **`test_compute_all_centrality_metrics_connected_graph`**: Tests the accurate computation of eigenvector, closeness, and betweenness centrality for a connected graph.
- **`test_compute_all_centrality_metrics_disconnected_graph`**: Ensures that centrality metrics are correctly handled (e.g., returning 0 or NaN for unreachable nodes) in a disconnected graph.

## 3. `test_fuzzy_clustering.py`

This file contains unit tests for the fuzzy clustering algorithms and related utility functions in `src/service/clusteringStrategy/fuzzy_clustering.py`. It validates the normalization, clustering, and scoring functionalities.

### Test Cases:
- **`test_normalize_series`**: Tests the `normalize_series` function to ensure values are scaled correctly between 0 and 1.
- **`test_perform_fuzzy_clustering_default_k`**: Verifies the `perform_fuzzy_clustering` (Fuzzy C-Means) function with default parameters.
- **`test_perform_fuzzy_clustering_specified_k`**: Checks FCM with a specified number of clusters.
- **`test_gustafson_kessel_clustering`**: Tests the `gustafson_kessel_clustering` function for its accuracy in cluster assignment and FPC calculation.
- **`test_fuzzy_silhouette_score`**: Validates the `fuzzy_silhouette_score` calculation, ensuring it provides a meaningful measure of cluster quality.

## 4. `test_database.py`

This file contains unit tests for the MongoDB database integration functions in `src/repository/database.py`. It ensures reliable connection, data saving, and data retrieval.

### Test Cases:
- **`test_get_database`**: Verifies that the `get_database` function successfully connects to MongoDB and returns a database object.
- **`test_save_classified_users`**: Tests the ability to save classified user data (including risk categories, sentiment, and centrality) to the MongoDB collection.
- **`test_get_users_by_risk_category`**: Ensures that users can be retrieved correctly based on their assigned risk category.

## 5. `test_api.py`

This file contains unit tests for the FastAPI endpoints defined in `src/controller/api.py`. It ensures that the API functions as expected, handling requests and responses correctly.

### Test Cases:
- **`test_get_users_by_risk_category_high_risk`**: Verifies the `/users/{risk_category}` endpoint for retrieving high-risk users.
- **`test_get_users_by_risk_category_low_risk`**: Checks the same endpoint for low-risk users.
- **`test_get_users_by_risk_category_invalid_category`**: Tests how the API handles requests with invalid risk categories.
- **`test_analyze_tweet_success`**: Ensures that the `/analyze_tweet` endpoint correctly processes a tweet, performs sentiment analysis, and assigns a risk category.
- **`test_analyze_tweet_missing_fields`**: Verifies error handling when required fields are missing in the `/analyze_tweet` request.
- **`test_analyze_tweet_no_username_in_graph_data`**: Checks behavior when the username from a tweet is not found in graph centrality data.

## 6. `test_dashboard.py`

This file contains unit tests for the Streamlit dashboard components in `src/dashboard/dashboard.py`. It ensures that data retrieval and processing for display purposes are correct.

### Test Cases:
- **`test_get_user_risk_distribution`**: Verifies the function that retrieves the distribution of users across different risk categories.
- **`test_get_top_influential_users`**: Checks the function that identifies and returns the top influential users.
- **`test_get_classified_tweets_data`**: Ensures the correct retrieval and formatting of all classified tweet data.
- **`test_get_live_updates_from_mongodb`**: Tests the aggregation of all dashboard data functions to simulate live updates from MongoDB.

## 7. `test_alerts.py`

This file contains unit tests for the real-time alerting system in `src/logs/alerts.py`. It validates the email alert sending mechanism and the risk level spike monitoring.

### Test Cases:
- **`test_send_email_alert`**: Verifies the functionality of sending email alerts, including SMTP connection and message formatting.
- **`test_monitor_risk_level_spikes_no_spike`**: Ensures that no alert is triggered when the number of high-risk tweets does not exceed the threshold within the time window.
- **`test_monitor_risk_level_spikes_with_spike`**: Checks that an alert is correctly triggered when a spike in high-risk tweets is detected.
- **`test_monitor_risk_level_spikes_old_messages_ignored`**: Confirms that messages outside the defined time window are ignored when calculating spikes.

## 8. `test_text_preprocessing.py`

This file contains unit tests for the text preprocessing functions in `src/service/text_preprocessing.py`, including sentiment analysis, keyword extraction, and engagement calculation.

### Test Cases:
- **`test_analyze_sentiment_bert_positive`**: Verifies the BERT sentiment analysis for positive text.
- **`test_analyze_sentiment_bert_negative`**: Checks BERT sentiment analysis for negative text.
- **`test_analyze_sentiment_bert_neutral`**: Tests BERT sentiment analysis for neutral text.
- **`test_analyze_sentiment_bert_empty_text`**: Ensures proper handling of empty text input for sentiment analysis.
- **`test_extract_keywords`**: Verifies the extraction of relevant keywords from text.
- **`test_extract_keywords_empty_text`**: Checks keyword extraction for empty text.
- **`test_calculate_engagement`**: Tests the calculation of engagement scores based on retweet count, reply count, and followers.
- **`test_calculate_engagement_zero_followers`**: Ensures correct handling of division by zero when a user has no followers.

## 9. `test_main_pipeline.py`

This file serves as an integration test for the overall data processing pipeline orchestrated by `src/service/main.py`. It simulates the end-to-end execution of the system with mocked dependencies.

### Test Cases:
- **`test_run_pipeline_fcm`**: Verifies the pipeline's execution when the Fuzzy C-Means clustering strategy is selected.
- **`test_run_pipeline_gk`**: Checks the pipeline's execution when the Gustafson-Kessel clustering strategy is selected.
- **`test_run_pipeline_invalid_strategy`**: Ensures that the pipeline raises an error when an unsupported clustering strategy is provided.