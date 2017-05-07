from face_detect import detect_video
from qingstor.sdk.service.qingstor import QingStor
from qingstor.sdk.config import Config

qc_access_key_id = 'EZSEHOOJINMNLKCEHPTA'
qc_access_key = 'nx7v6jfHIjz0xVJQatCuT8F5dVCxy9631ebQj3BC'

bucket_name = 'zhenjing'

config = Config(qc_access_key_id, qc_access_key)
service = QingStor(config)
bucket = service.Bucket(bucket_name, 'sh1a')

objects = bucket.list_objects()['keys']

video_files = map(lambda f: f['key'], filter(lambda f: 'video' in f['mime_type'], objects))
all_files = map(lambda f: f['key'], objects)

for video_file in video_files:
    dat_file = video_file + '.dat'
    if not dat_file in all_files:
        print "Found new video {0}, download...".format(video_file)
        output = bucket.get_object(video_file)
        with open(video_file, 'wb') as file:
            file.write(output.content)

        print "Detect video..."
        detect_video(video_file)

        print "Upload data..."
        with open(dat_file, 'rb') as file:
            bucket.put_object(dat_file, body=file)
