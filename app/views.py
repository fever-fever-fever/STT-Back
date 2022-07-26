
from django.shortcuts import render
from rest_framework.response import Response
from .models import Video, Video_word
from rest_framework.views import APIView
from .serializers import VideoWordSerializer, VideoSerializer


import os    
credential_path = "C:/Users/82104/OneDrive/창업동아리/speech-to-text-333411-f6c9847c1934.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

import subprocess
import shlex
import datetime

#영상 목록 보여주기

class fileUpload(APIView):
    
    def upload_blob(bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
     
        
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )

# 영상 업로드
    def put(self, request, pk, format=None):

        bucket_name = "sttbucket-fever"
            # The path to your file to uplo
        source_file_name = "C:/10.wav"
        #os.path.abspath(source_file_name)
            # The ID of your GCS object
        destination_blob_name = "test"
        upload_blob(bucket_name, source_file_name, destination_blob_name)
            

    def get(self, request):
        queryset = Product.objects.all()
        print(queryset)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

def transcribe_gcs(gcs_uri):
        from google.cloud import speech

        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            #sample_rate_hertz=16000,
            audio_channel_count=2,
            enable_word_time_offsets=True,
            language_code='ko-KR')
        operation = client.long_running_recognize(config=config,audio=audio)
        response = operation.result(timeout=3000)
        #return response
    #response = transcribe_gcs("gs://sttbucket-fever/10.wav")

        import json
        from collections import OrderedDict
        file_data = OrderedDict()

        for result in response.results:
            alternative = result.alternatives[0]
            print("Transcript: {}".format(alternative.transcript))
            print("Confidence: {}".format(alternative.confidence))

            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time.total_seconds()
                end_time = word_info.end_time.total_seconds()
                file_data['video_id'] = 1
                file_data['word'] = word
                file_data['start_time'] = start_time
                file_data['end_time'] = end_time
                file_data['date'] = "2021-11-29"

                serializer = VideoWordSerializer(data=file_data)

                if serializer.is_valid(): #유효성 검사
                    serializer.save() # 저장

        
#영상 편집하기
class VideoEdit(APIView):
    # 참가 인원 추가하기
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = VideoWordSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response({"MESSAGE" : "Success!"}, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"MESSAGE" : "ERORR"}, status=status.HTTP_400_BAD_REQUEST)


    
    #영상 스크립트 생성
    def get(self, request):
        
        #transcribe_gcs("gs://sttbucket-fever/10.wav")
        queryset = Video_word.objects.all()
        serializer = VideoWordSerializer(queryset, many=True)
        return Response(serializer.data)
        

                
#특정 단어 없애기
class ScriptDelete(APIView):
    def delete(self, request, format=None):

        cid = Video_word.objects.filter(video_id = request.data["video_id"]).filter(wid = request.data["wid"])
        #print(cid,"에러에러에러에러에러에러에러")
        cid.delete()
        return Response({"MESSAGE" : "Success!"}) 

#영상 합치기
class VideoPlus(APIView):

    def get(self, request):
        #transcribe_gcs("gs://sttbucket-fever/10.wav")

        queryset = Video_word.objects.filter(video_id = request.data["video_id"]).values('start_time','end_time','wid')
        #serializer = VideoWordSerializer(queryset, many=True)
        #print(queryset)


        delete = {}
        i = 0
        
        for idx, val in enumerate(queryset):    
            #print(idx,val)
            

            #wid가 +1이 아니면..
            try:
                next = queryset[idx+1]
            except:
                break

            try:
                front = queryset[idx-1]
            except:
                break

            #삭제된 구간찾기
            if(val['wid']+1 != next['wid']):
                
                delete['idx'] = i
                delete['start'] = val['end_time']
                delete['end'] = next['start_time']
                i=i+1

            
            start = "0"
            hall = []
            if(val['wid']+1 != next['wid']):
                

                time = {}
                time['start'] = 0
                time['end'] = val["end_time"]


                hall +=time

                time['start']

            
        print(delete,"에러에러에러에러에러에러에러에러")

        start = '0'
        
        for idx, val in enumerate(delete):
            
            try:
                next = delete[idx+1]
            except:
                break
            
            end = val['start']
            vname = idx+'.mp4'
            

            #동영상 자르기
            command="ffmpeg -i input.mp4 -ss "+start+"-to "+end+ "-c copy "+ vname
            

            #동영상 합치기
            command2 = "ffmpeg -f concat -i 'list.txt' -c copy output.mp4"

            process = subprocess.Popen(shlex.split(command), stdout = subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            
            for line in process.stdout:
                now = datetime.datetime.now()
                print(now, line)


        return Response({"MESSAGE" : "Success!"}) 

        #return Response(serializer.data)