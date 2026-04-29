from json import dumps
from os import getenv


from flask import Flask, jsonify, request
from boto3 import client

app = Flask(__name__)

LOCALSTACK_URL = getenv("LOCALSTACK_URL", "http://localhost:4566")
BUCKET_NAME = getenv("BUCKET_NAME", "amzn-s3-bucket")
SQS_URL = getenv(
        "SQS_URL", 
        "http://sqs.eu-south-2.localhost.localstack.cloud:4566/000000000000/s3-notification-queue")

"""API to interact with S3 bucket in LocalStack."""

def get_s3_client():
    return client(
        "s3",
        endpoint_url=LOCALSTACK_URL,
        region_name="eu-south-2"
    )


@app.route("/terraform/s3/bucket/objects", methods=["GET"])
def list_objects_terraform_bucket():
    """List all objects inside the S3 bucket created by Terraform."""
    s3 = get_s3_client()
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        
        objects = response.get("Contents", [])

        if not objects:
            return jsonify({
                "status": "OK",
                "message": "The bucket exists, but it is empty.",
                "objects": []
            }), 200

        return jsonify({
            "status": "OK",
            "bucket": BUCKET_NAME,
            "objects": [obj["Key"] for obj in objects] 
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/terraform/s3/bucket/objects", methods=["POST"])
def upload_object_to_terraform_s3_bucket():
    """Upload a JSON object to the S3 bucket created by Terraform"""
    s3 = get_s3_client()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "The request body should be in JSON format."}), 400

        filename = data.get("filename")

        if not filename:
            return jsonify({
                "status": "error",
                "message": "The body must include a filename field"
            }), 400
        
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=dumps(data),
            ContentType="application/json"
        )

        return jsonify({
            "status": "OK",
            "message": f"The file has been successfully created with the name {filename}"
        }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

@app.route("/terraform/s3/bucket/objects/<string:filename>", methods=["DELETE"])
def delete_object_from_terraform_s3_bucket(filename):
    """Delete a specific object from the S3 bucket created by Terraform."""
    s3 = get_s3_client()
    try:
        s3.head_object(Bucket=BUCKET_NAME, Key=filename)
        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)

        return jsonify({
            "status": "OK",
            "message": f"The file {filename} has been successfully deleted from the bucket."
        }), 200

    except s3.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return jsonify({
                "status": "error",
                "message": f"The file {filename} does not exist in the bucket."
            }), 404
        return jsonify({"status": "error", "message": str(e)}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True) 