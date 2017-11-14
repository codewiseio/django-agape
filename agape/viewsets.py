from agape.signals import trigger
from rest_framework import permissions,status,views,viewsets
from rest_framework.response import Response



class ModelViewSet(viewsets.ModelViewSet):

	def create(self, request, *args, **kwargs):
		trigger(self.context+'.create:before',request,*args,**kwargs)

		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		instance = self.perform_create(serializer)
		trigger(self.context+'.create:success',instance)
		

		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	def perform_create(self, serializer):
		instance = serializer.save()
		return instance

	def retrieve(self, request, *args, **kwargs):
		trigger(self.context+'.retrieve:before',request,*args,**kwargs)

		instance = self.get_object()
		trigger(self.context+'.retrieve:success',instance)

		serializer = self.get_serializer(instance)
		data = serializer.data
		trigger(self.context+'.retrieve:serialize',data)

		response = Response(data)
		trigger(self.context+'.retrieve:response',response)
		return response

	def update(self, request, *args, **kwargs):
		trigger(self.context+'.update:before',request,*args,**kwargs)

		partial = kwargs.pop('partial', False)        
		instance = self.get_object()
		trigger(self.context+'.update:retrieve',request,*args,**kwargs)

		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		instance = self.perform_update(serializer)
		trigger(self.context+'.update:success',instance)
        
		data = serializer.data
		trigger(self.context+'.update:serialize',data)	

		response = Response(data)
		trigger(self.context+'.update:response',response)
		return response

	def perform_update(self, serializer):
		instance = serializer.save()
		return instance

	def destroy(self, request, *args, **kwargs):
		trigger(self.context+'.destroy:before',request,*args,**kwargs)

		instance = self.get_object()
		trigger(self.context+'.destroy:retrieve',instance)

		self.perform_destroy(instance)
		trigger(self.context+'.destroy:success',instance)

		response = Response(status=status.HTTP_204_NO_CONTENT)
		trigger(self.context+'.destroy:response',response)

		return response

	def perform_destroy(self, instance):
		instance.delete()