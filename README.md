*Should've titled this repo as 'check_url_status'.

# URL Checker Lambda Function

This AWS Lambda function checks the availability of a given URL and sends notifications using Amazon SNS. The function is designed to notify users via email using SNS topics. Depending on the response, the function will send different messages for successful access, failures, or exceptions.

## Features
- Sends an SNS notification when the specified URL is accessible.
- Sends a different SNS notification when the URL is unavailable or redirected.
- Handles exceptions gracefully and sends an error notification via SNS.

## Requirements

- **AWS SNS Topic ARN for Email**: The SNS topic ARN to which the email notifications will be sent.
- **URL**: The URL that needs to be checked.

## Environment Variables
The Lambda function relies on the following environment variables:

1. `SNS_TOPIC_ARN_EMAIL`: The ARN of the SNS topic used to send email notifications.
2. `URL`: The URL to be checked by the Lambda function.

Ensure these environment variables are set in your Lambda function configuration.

## Lambda Execution Role Permissions
To use this function effectively, the Lambda function must have the following IAM permissions:

- `sns:Publish` on the SNS topic to send notifications.

### Example IAM Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sns:Publish",
      "Resource": "arn:aws:sns:<region>:<account-id>:<topic-name>"
    }
  ]
}
```
Replace `<region>`, `<account-id>`, and `<topic-name>` with appropriate values for your setup.

## Deployment Instructions
1. **Create an SNS Topic** for email notifications if you haven't done so already.
   - Subscribe your email to the topic to receive notifications.

2. **Create a Lambda Function** in the AWS Management Console.
   - Use the provided Python script as the Lambda function code.

3. **Set Environment Variables**
   - `SNS_TOPIC_ARN_EMAIL`: The ARN of the SNS topic for email notifications.
   - `URL`: The URL that you want to monitor.

4. **Assign Permissions** to the Lambda execution role to allow publishing to the SNS topic as described in the Example IAM Policy above.

5. **Test the Function** to ensure it behaves as expected. You can create a test event in the AWS Lambda console to manually trigger the function.

## Python Code Summary
- **Libraries Used**:
  - `urllib.request`: Used to make HTTP requests and check the URL status.
  - `boto3`: AWS SDK for Python to interact with SNS.
  - `os`: To retrieve environment variables.

- **Logic**: The function sends a `HEAD` request to the specified URL to check its status.
  - If the URL is accessible (`HTTP 200`) and no redirect occurred, it sends a success notification.
  - If the URL is not accessible or gets redirected, it sends a failure notification.
  - Any exceptions are caught, logged, and trigger an error notification.

## Example Notifications
- **Success**: When the URL is accessible, an email with the subject "サイトアクセス通知" will be sent containing the message:
  - "サイトにアクセス可能になりました！ URL: <URL>"

- **Failure**: If the URL is unavailable or redirected, an email with the subject "サイトアクセス失敗通知" will be sent containing the message:
  - "サイトにアクセスできませんでした。リダイレクトされたか、ステータスコードが期待通りではありませんでした。 URL: <URL>, ステータスコード: <status_code>"

- **Error**: In case of an unexpected error, an email with the subject "サイトアクセスエラーメッセージ" will be sent containing the message:
  - "サイトにアクセス中にエラーが発生しました。 URL: <URL>, エラー: <error_message>"

## Notes
- The function uses a `HEAD` request to minimize data transfer while checking the URL.
- The `timeout` is set to 5 seconds to ensure prompt responses and prevent long delays.
- Ensure the correct SNS topic and URL are used to avoid unnecessary notifications.

