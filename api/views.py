from django.http import JsonResponse #to get json response

def getRoutes(request):

    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},

        {'POST':'/api/users/token'}, # build in class
        {'POST':'/api/users/token/refresh'}, # build in class 
    ]

    return JsonResponse(routes, safe=False)