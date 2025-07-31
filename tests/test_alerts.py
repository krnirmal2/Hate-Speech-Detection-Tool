import pytest
from unittest.mock import patch, MagicMock
import datetime
from src.logs.alerts import (
    monitor_risk_level_spikes,
    send_email_alert,
    RISK_SPIKE_THRESHOLD,
    TIME_WINDOW_MINUTES,
)


@pytest.fixture
def mock_kafka_consumer():
    with patch("kafka.KafkaConsumer") as mock_consumer:
        yield mock_consumer


@pytest.fixture
def mock_smtp_lib():
    with patch("smtplib.SMTP_SSL") as mock_smtp:
        yield mock_smtp


@pytest.fixture
def mock_email_message():
    with patch("email.message.EmailMessage") as mock_msg:
        yield mock_msg


def test_send_email_alert(mock_smtp_lib, mock_email_message):
    mock_smtp_instance = mock_smtp_lib.return_value.__enter__.return_value

    subject = "Test Alert"
    body = "This is a test alert body."
    recipient_email = "test@example.com"

    send_email_alert(subject, body, recipient_email)

    mock_email_message.assert_called_once()
    msg_instance = mock_email_message.return_value
    assert msg_instance["Subject"] == subject
    assert (
        msg_instance["From"] == "your_email@example.com"
    )  # Ensure this matches the env var mock
    assert msg_instance["To"] == recipient_email
    msg_instance.set_content.assert_called_once_with(body)

    mock_smtp_lib.assert_called_once_with("smtp.gmail.com", 465)
    mock_smtp_instance.login.assert_called_once_with(
        "your_email@example.com", "your_app_password"
    )
    mock_smtp_instance.send_message.assert_called_once_with(msg_instance)
    mock_smtp_instance.quit.assert_called_once()


def test_monitor_risk_level_spikes_no_spike(mock_kafka_consumer):
    mock_consumer_instance = mock_kafka_consumer.return_value

    # Simulate messages over time, but not enough to trigger a spike
    current_time = datetime.datetime.now()
    mock_consumer_instance.__iter__.return_value = [
        MagicMock(
            value='{"risk_category": "High Risk", "timestamp": "'
            + (current_time - datetime.timedelta(minutes=1)).isoformat()
            + '"}'.encode("utf-8")
        ),
        MagicMock(
            value='{"risk_category": "Low Risk", "timestamp": "'
            + current_time.isoformat()
            + '"}'.encode("utf-8")
        ),
    ]

    with patch("src.logs.alerts.send_email_alert") as mock_send_email:
        # Run for a very short duration to process mocked messages
        monitor_risk_level_spikes(num_messages=2)
        mock_send_email.assert_not_called()


def test_monitor_risk_level_spikes_with_spike(mock_kafka_consumer):
    mock_consumer_instance = mock_kafka_consumer.return_value

    # Simulate many 'High Risk' messages within the time window
    current_time = datetime.datetime.now()
    messages = []
    for i in range(RISK_SPIKE_THRESHOLD + 1):  # One more than the threshold to trigger
        messages.append(
            MagicMock(
                value='{"risk_category": "High Risk", "timestamp": "'
                + (current_time - datetime.timedelta(seconds=i)).isoformat()
                + '"}'.encode("utf-8")
            )
        )
    messages.append(
        MagicMock(
            value='{"risk_category": "Low Risk", "timestamp": "'
            + (
                current_time - datetime.timedelta(minutes=TIME_WINDOW_MINUTES + 1)
            ).isoformat()
            + '"}'.encode("utf-8")
        )
    )

    mock_consumer_instance.__iter__.return_value = messages

    with patch("src.logs.alerts.send_email_alert") as mock_send_email:
        # Run for a very short duration to process mocked messages
        monitor_risk_level_spikes(num_messages=len(messages))
        mock_send_email.assert_called_once()  # Should be called once for the spike


def test_monitor_risk_level_spikes_old_messages_ignored(mock_kafka_consumer):
    mock_consumer_instance = mock_kafka_consumer.return_value

    # Simulate some 'High Risk' messages, but outside the time window
    current_time = datetime.datetime.now()
    messages = []
    for i in range(RISK_SPIKE_THRESHOLD + 1):  # Enough to trigger if in window
        messages.append(
            MagicMock(
                value='{"risk_category": "High Risk", "timestamp": "'
                + (
                    current_time - datetime.timedelta(minutes=TIME_WINDOW_MINUTES + 5)
                ).isoformat()
                + '"}'.encode("utf-8")
            )
        )

    mock_consumer_instance.__iter__.return_value = messages

    with patch("src.logs.alerts.send_email_alert") as mock_send_email:
        monitor_risk_level_spikes(num_messages=len(messages))
        mock_send_email.assert_not_called()
