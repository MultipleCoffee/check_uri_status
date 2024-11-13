import urllib.request
import boto3
import os

sns_client = boto3.client('sns')

# 環境変数からSNSトピックのARNを取得
sns_topic_arn_email = os.getenv('SNS_TOPIC_ARN_EMAIL')  # メール用トピック
url = os.getenv('URL')  # URL

if not sns_topic_arn_email:
    raise ValueError("Environment variable 'SNS_TOPIC_ARN_EMAIL' is not set")

def lambda_handler(event, context):
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as response:  # タイムアウトを5秒に設定
            if response.status == 200 and response.geturl() == url:
                # サイトにアクセス可能で、リダイレクトされていないときにSNSに通知（メール用）
                sns_client.publish(
                    TopicArn=sns_topic_arn_email,
                    Message=f"サイトにアクセス可能になりました！ URL: {url}",
                    Subject="サイトアクセス通知"
                )
                return {"status": "Notification sent"}
            else:
                # アクセスできなかった場合のSNS通知（メール用）
                sns_client.publish(
                    TopicArn=sns_topic_arn_email,
                    Message=f"サイトにアクセスできませんでした。リダイレクトされたか、ステータスコードが期待通りではありませんでした。 URL: {url}, ステータスコード: {response.status}",
                    Subject="サイトアクセス失敗通知"
                )
                return {"status": f"Redirected or unavailable, status code: {response.status}"}
    except Exception as e:
        print(f"エラー: {e}")
        # 例外が発生した場合のSNS通知（メール用）
        sns_client.publish(
            TopicArn=sns_topic_arn_email,
            Message=f"サイトにアクセス中にエラーが発生しました。 URL: {url}, エラー: {e}",
            Subject="サイトアクセスエラーメッセージ"
        )
        return {"status": "Error", "error": str(e)}
