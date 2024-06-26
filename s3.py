import os
import boto3
import dotenv
from PIL import Image
from io import BytesIO
import io
import pyperclip as pc

dotenv.load_dotenv()

S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_REGION_NAME = os.getenv('S3_REGION_NAME')
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')

s3_client = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name=S3_REGION_NAME
)

def get_object_from_s3(object_name):
    object_name = object_name.split('/')[-1]
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=object_name)
        object_data = response['Body'].read()

        with open(object_name, 'wb') as file:
            file.write(object_data)

        return object_name
    except Exception as e:
        print(f"Error: {e}")
        return None

def copy_image_to_clipboard(image_path):
    from io import BytesIO
    import win32clipboard
    from PIL import Image
    image = Image.open(image_path)

    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


# Пример использования функции
object_url = 'https://s3.timeweb.cloud/931dbb93-olegpash/Снимок экрана 2024-06-24 в 16.30.14.png'
object_name = object_url.split('/')[-1]

image_data = get_object_from_s3(object_name)
if image_data:
    copy_image_to_clipboard(image_data)
else:
    print("Failed to retrieve object data.")
