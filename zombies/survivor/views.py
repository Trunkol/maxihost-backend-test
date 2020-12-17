from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from survivor.models import Survivor
from survivor.serializers import SurvivorSerializer

@csrf_exempt
def survivor_list(request):
    """
    List all survivors, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Survivor.objects.all()
        serializer = SurvivorSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SurvivorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def survivor_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        survivor = Survivor.objects.get(pk=pk)
    except Survivor.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SurvivorSerializer(Survivor)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SurvivorSerializer(Survivor, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        survivor.delete()
        return HttpResponse(status=204)
