from .serializers import JobSerializers
from .models import Job
from rest_framework import generics


# def joblistapi(request):
#     all_jobs=Job.objects.all()
#     data=JobSerializers(all_jobs,many=True).data
#     return  Response({'data':data})
# @api_view(["GET"])

# class Job_List_Api(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = JobSerializers
#     queryset = Job.objects.all()
#     lookup_field = 'id'
    
    
# class Job_Create_Api(generics.ListCreateAPIView):
#     serializer_class = JobSerializers
#     queryset = Job.objects.all()
#     lookup_field = 'id'
    
class JobListApi(generics.ListAPIView):
    queryset=Job.objects.all()
    serializer_class = JobSerializers
    
    
class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializers
    queryset = Job.objects.all()
    lookup_field = 'id'