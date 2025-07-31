import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from src.service.main import run_pipeline

@pytest.fixture
def mock_pipeline_dependencies():
    with (
        patch('src.data_loader.load_data') as mock_load_data,
        patch('src.text_preprocessing.analyze_sentiment_bert') as mock_sentiment,
        patch('src.text_preprocessing.extract_keywords') as mock_keywords,
        patch('src.text_preprocessing.calculate_engagement') as mock_engagement,
        patch('src.service.graph_analysis.build_social_graph') as mock_build_graph,
        patch('src.service.graph_analysis.compute_all_centrality_metrics') as mock_centrality,
        patch('src.service.clusteringStrategy.fuzzy_clustering.perform_fuzzy_clustering') as mock_fcm_clustering,
        patch('src.service.clusteringStrategy.fuzzy_clustering.gustafson_kessel_clustering') as mock_gk_clustering,
        patch('src.service.clusteringStrategy.fuzzy_clustering.fuzzy_silhouette_score') as mock_silhouette_score,
        patch('src.repository.database.save_classified_users') as mock_save_users,
        patch('src.service.main.visualize_clusters') as mock_visualize_clusters, # Patch the imported visualize_clusters
        patch('time.time', side_effect=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]) # For time tracking
    ) as mocks:
        yield mocks

def test_run_pipeline_fcm(mock_pipeline_dependencies):
    (
        mock_load_data, mock_sentiment, mock_keywords, mock_engagement,
        mock_build_graph, mock_centrality, mock_fcm_clustering, mock_gk_clustering,
        mock_silhouette_score, mock_save_users, mock_visualize_clusters, _
    ) = mock_pipeline_dependencies

    # Setup mock return values
    mock_load_data.return_value = pd.DataFrame({
        'username': ['user1', 'user2', 'user3'],
        'tweets': ['tweet1', 'tweet2', 'tweet3'],
        'followers': [100, 200, 50],
        'retweet_count': [10, 20, 5],
        'reply_count': [2, 4, 1]
    })
    mock_sentiment.return_value = 0.5
    mock_keywords.return_value = ['keyword']
    mock_engagement.return_value = pd.Series([0.1, 0.2, 0.3])
    mock_build_graph.return_value = MagicMock()
    mock_centrality.return_value = {'user1': {'eigenvector_centrality': 0.1, 'closeness_centrality': 0.2, 'betweenness_centrality': 0.3}}
    mock_fcm_clustering.return_value = (np.array([0, 1, 2]), None, 0.8, None) # cluster_labels, centers, fpc, membership_matrix
    mock_gk_clustering.return_value = (np.array([0, 1, 2]), None, 0.7, None, None) # cluster_labels, centers, fpc, membership_matrix, covariances
    mock_silhouette_score.return_value = 0.5

    # Call the pipeline with FCM strategy
    run_pipeline(clustering_strategy='fuzzy_c_means', max_samples=3)

    # Assertions for FCM path
    mock_load_data.assert_called_once()
    assert mock_sentiment.call_count == 3 # Called for each tweet
    assert mock_keywords.call_count == 3
    mock_engagement.assert_called_once()
    mock_build_graph.assert_called_once()
    mock_centrality.assert_called_once()
    mock_fcm_clustering.assert_called_once()
    mock_gk_clustering.assert_not_called() # Should not be called for FCM
    mock_silhouette_score.assert_called_once()
    mock_save_users.assert_called_once()
    mock_visualize_clusters.assert_called_once()

def test_run_pipeline_gk(mock_pipeline_dependencies):
    (
        mock_load_data, mock_sentiment, mock_keywords, mock_engagement,
        mock_build_graph, mock_centrality, mock_fcm_clustering, mock_gk_clustering,
        mock_silhouette_score, mock_save_users, mock_visualize_clusters, _
    ) = mock_pipeline_dependencies

    # Setup mock return values (same as FCM test for common mocks)
    mock_load_data.return_value = pd.DataFrame({
        'username': ['user1', 'user2', 'user3'],
        'tweets': ['tweet1', 'tweet2', 'tweet3'],
        'followers': [100, 200, 50],
        'retweet_count': [10, 20, 5],
        'reply_count': [2, 4, 1]
    })
    mock_sentiment.return_value = 0.5
    mock_keywords.return_value = ['keyword']
    mock_engagement.return_value = pd.Series([0.1, 0.2, 0.3])
    mock_build_graph.return_value = MagicMock()
    mock_centrality.return_value = {'user1': {'eigenvector_centrality': 0.1, 'closeness_centrality': 0.2, 'betweenness_centrality': 0.3}}
    mock_fcm_clustering.return_value = (np.array([0, 1, 2]), None, 0.8, None) # cluster_labels, centers, fpc, membership_matrix
    mock_gk_clustering.return_value = (np.array([0, 1, 2]), None, 0.7, None, None) # cluster_labels, centers, fpc, membership_matrix, covariances
    mock_silhouette_score.return_value = 0.5

    # Call the pipeline with Gustafson-Kessel strategy
    run_pipeline(clustering_strategy='gustafson_kessel', max_samples=3)

    # Assertions for GK path
    mock_load_data.assert_called_once()
    assert mock_sentiment.call_count == 3 # Called for each tweet
    assert mock_keywords.call_count == 3
    mock_engagement.assert_called_once()
    mock_build_graph.assert_called_once()
    mock_centrality.assert_called_once()
    mock_fcm_clustering.assert_not_called() # Should not be called for GK
    mock_gk_clustering.assert_called_once()
    mock_silhouette_score.assert_called_once()
    mock_save_users.assert_called_once()
    mock_visualize_clusters.assert_called_once()

def test_run_pipeline_invalid_strategy(mock_pipeline_dependencies):
    mock_load_data = mock_pipeline_dependencies[0]
    mock_load_data.return_value = pd.DataFrame({
        'username': ['user1'], 'tweets': ['tweet1'], 'followers': [100], 'retweet_count': [10], 'reply_count': [2]
    })
    with pytest.raises(ValueError, match="Invalid clustering strategy: unknown_strategy"): # Ensure the error message matches
        run_pipeline(clustering_strategy='unknown_strategy', max_samples=1)