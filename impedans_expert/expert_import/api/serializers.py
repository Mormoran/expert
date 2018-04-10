from rest_framework.serializers import (
	HyperlinkedIdentityField,
	ModelSerializer,
	SerializerMethodField,
)

from impedans_expert.expert_import.models import (
	RunProperty,
	Run,
)

##############################################################################
# Define API serializers for Runs related operations create, detail and list #
##############################################################################

class RunsCreateSerializer(ModelSerializer):
	class Meta:
		model = Run
		fields = [
			'id',
			'chamber',
			'start_time',
			'end_time',
			'recipe'
		]
	#########################################################################
	# First try at attempting to validate inserted data for existing values #
	#########################################################################

	# def create(self, validated_data):
	# 	run = Run.objects.update_or_create(
	# 						file=validated_data.get('file', None),
	# 						chamber=validated_data.get('chamber'),
	# 						start_time=validated_data.get('start_time'),
	# 						end_time=validated_data.get('end_time'),
	# 						step_time=validated_data.get('step_time'))
	# 	return run

class RunsDetailSerializer(ModelSerializer):
	chamber = SerializerMethodField()
	recipe = SerializerMethodField()
	class Meta:
		model = Run
		fields = [
			'id',
			'chamber',
			'start_time',
			'end_time',
			'recipe'
		]
	def get_chamber(self, obj):
		return str(obj.chamber.chamber_name)
	def get_recipe(self, obj):
		try:
			recipe = str(obj.recipe.name)
		except:
			recipe = None
		return recipe

class RunsListSerializer(ModelSerializer):
	url = HyperlinkedIdentityField(
		view_name='import_api:runs_list_detail',
		lookup_field='pk'
	)
	delete_url = HyperlinkedIdentityField(
		view_name='import_api:runs_list_delete',
		lookup_field='pk'
	)
	chamber = SerializerMethodField()
	recipe = SerializerMethodField()
	class Meta:
		model = Run
		fields = [
			'url',
			'id',
			'chamber',
			'start_time',
			'end_time',
			'recipe',
			'delete_url',
		]
	def get_chamber(self, obj):
		return str(obj.chamber.chamber_name)
	def get_recipe(self, obj):
		try:
			recipe = str(obj.recipe.name)
		except:
			recipe = None
		return recipe

########################################################################################
# Define API serializers for Run Properties related operations create, detail and list #
########################################################################################

class RunPropertiesCreateSerializer(ModelSerializer):
	class Meta:
		model = RunProperty
		fields = [
			'id',
			'runs',
			'property_name',
			'property_value'
		]

class RunPropertiesDetailSerializer(ModelSerializer):
	runs = SerializerMethodField()
	class Meta:
		model = RunProperty
		fields = [
			'id',
			'runs',
			'property_name',
			'property_value'
		]
	def get_runs(self, obj):
		return str(obj.runs)

class RunPropertiesListSerializer(ModelSerializer):
	url = HyperlinkedIdentityField(
		view_name='import_api:properties_list_detail',
		lookup_field='pk'
	)
	delete_url = HyperlinkedIdentityField(
		view_name='import_api:properties_list_delete',
		lookup_field='pk'
	)
	runs = SerializerMethodField()
	class Meta:
		model = RunProperty
		fields = [
			'url',
			'id',
			'runs',
			'property_name',
			'property_value',
			'delete_url'
		]
	def get_runs(self, obj):
		return str(obj.runs)