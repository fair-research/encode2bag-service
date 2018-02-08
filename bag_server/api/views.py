from flask import jsonify, make_response, send_from_directory,request, render_template, abort
import uuid
import datetime
from app import app
import boto3
from encode2bag import encode2bag_api as e2b
from minid_client import minid_client_api as minid_client

GLOBUS_FILE="https://www.globus.org/app/transfer?origin_id=6a84efa0-4a94-11e6-8233-22000b97daec&origin_path=%2Ffdab4915-a1f0-42f1-8579-e1999d0648ca%2F"

def upload_to_s3(filename, key):
    s3 = boto3.resource('s3', aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'], aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])
    data = open(filename, 'rb')
    s3.Bucket(BUCKET_NAME).put_object(Key=key, Body=data)

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

@app.route('/')
def root():
    print "Root"
    return app.send_static_file('index.html')

@app.route('/js/<path:path>')
def send_js(path):
        return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
        return send_from_directory('static/css', path)

@app.route('/images/<path:path>')
def send_images(path):
            return send_from_directory('static/images', path)



@app.route('/encode', methods=['POST'])
def get_entity():
    if not request_wants_json():
        print "Only JSON repsonses are supported"

    query, metadata, ro_manifest = None, None, True

    if "q" in request.json:
        query = request.json["q"]
    if "m" in request.json:
        metadata = request.json["m"]
    if "ro" in request.json:
        ro_manifest = request.json["ro"]

    print ("Request: Q: %s; M: %s; RO: %s" % (query, metadata, ro_manifest))

    key = str(uuid.uuid4())
    
    try:
        if query is not None:
            print ("Creating from query")
            e2b.create_bag_from_url(query,
                output_name=key,
                output_path='/tmp',
                archive_format='zip',
                creator_name="Encode2BDBag Service",
                create_ro_manifest=ro_manifest)

        elif metadata is not None:
            print ("Creating from metadata file")
            tmp_file = str(uuid.uuid4())
            with open("/tmp/%s" % tmp_file, 'w') as f:
                f.write(metadata)
            e2b.create_bag_from_metadata_file("/tmp/%s" % tmp_file,
                    output_name=key,
                    output_path='/tmp',
                    archive_format='zip',
                    creator_name="Encode2BDBag Service",
                    create_ro_manifest=ro_manifest)

    except Exception as e:
        print ("Exception creating bag %s" %e)
        return "Error creating Bag: %s" %e, 404

    upload_to_s3("/tmp/%s.zip" % key, "%s.zip" % key)
    
    response_dict = {"uri" : "https://s3.amazonaws.com/%s/%s.zip" % (BUCKET_NAME, key)}

    if app.config['CREATE_MINID']:
        print "Creating Minid"
        checksum = minid_client.compute_checksum("/tmp/%s.zip" % key)
        minid = minid_client.register_entity(
                app.config['MINID_SERVER'], 
                checksum,
                app.config['MINID_EMAIL'],
                app.config['MINID_CODE'],
                ["https://s3.amazonaws.com/%s/%s.zip" % (app.config['BUCKET_NAME'], key)],
                "ENCODE BDBag", 
                app.config['MINID_TEST'])

        response_dict["minid"] = minid

    response_dict["globus_uri"] = GLOBUS_FILE
    return jsonify(response_dict), 200
