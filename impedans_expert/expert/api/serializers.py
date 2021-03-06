from rest_framework.serializers import (
	HyperlinkedIdentityField,
	ModelSerializer,
	SerializerMethodField,
	PrimaryKeyRelatedField
)

from impedans_expert.expert.models import (
	Chamber,
	ChamberProperty,
	Customer,
	Data,
	Marker,
	Parameter,
	Sensor,
	SensorType,
)

#################################################################################
# Define API serializers for Chamber related operations create, detail and list #
#################################################################################

class ChamberCreateSerializer(ModelSerializer):
	class Meta:
		model = Chamber
		fields = [
			'id',
			'chamber_name',
			'customer'
		]

class ChamberDetailSerializer(ModelSerializer):
	customer = SerializerMethodField()
	class Meta:
		model = Chamber
		fields = [
			'id',
			'chamber_name',
			'customer'
		]
	def get_customer(self, obj):
		return str(obj.customer.company_name)

class ChamberListSerializer(ModelSerializer):
	url = HyperlinkedIdentityField(
		view_name='expert_api:chamber_list_detail',
		lookup_field='pk'
	)
	delete_url = HyperlinkedIdentityField(
		view_name='expert_api:chamber_list_delete',
		lookup_field='pk'
	)
	customer = SerializerMethodField()
	class Meta:
		model = Chamber
		fields = [
			'id',
			'url',
			'chamber_name',
			'customer',
			'delete_url'
		]
	def get_customer(self, obj):
		return str(obj.customer.company_name)

############################################################################################
# Define API serializers for Chamber Properties related operations create, detail and list #
############################################################################################

class ChamberPropertiesCreateSerializer(ModelSerializer):
	class Meta:
		model = ChamberProperty
		fields = [
			'id',
			'chamber',
			'property_name',
			'property_value'
		]

class ChamberPropertiesDetailSerializer(ModelSerializer):
	chamber = SerializerMethodField()
	class Meta:
		model = ChamberProperty
		fields = [
			'id',
			'chamber',
			'property_name',
			'property_value'
		]
	def get_chamber(self, obj):
		return str(obj.chamber.chamber_name)

class ChamberPropertiesListSerializer(ModelSerializer):
	url = HyperlinkedIdentityField(
		view_name='expert_api:chamber_properties_list_detail',
		lookup_field='pk'
	)
	delete_url = HyperlinkedIdentityField(
		view_name='expert_api:chamber_properties_list_delete',
		lookup_field='pk'
	)
	chamber = SerializerMethodField()
	class Meta:
		model = ChamberProperty
		fields = [
			'url',
			'id',
			'chamber',
			'property_name',
			'property_value',
			'delete_url'
		]
	def get_chamber(self, obj):
		return str(obj.chamber.chamber_name)

##################################################################################
# Define API serializers for Customer related operations create, detail and list #
##################################################################################

class CustomerCreateSerializer(ModelSerializer):
	class Meta:
		model = Customer
		fields = [
			'id',
			'company_name',
			'contact_name',
			'contact_email',
			'user'
		]

class CustomerDetailSerializer(ModelSerializer):
	user = SerializerMethodField()
	class Meta:
		model = Customer
		fields = [
			'id',
			'company_name',
			'contact_name',
			'contact_email',
			'user'
		]
	def get_user(self, obj):
		return str(obj.user.name)

class CustomerListSerializer(ModelSerializer):
	url = HyperlinkedIdentityField(
		view_name='expert_api:customer_list_detail',
		lookup_field='pk'
	)
	delete_url = HyperlinkedIdentityField(
		view_name='expert_api:customer_list_delete',
		lookup_field='pk'
	)
	user = SerializerMethodField()
	class Meta:
		model = Customer
		fields = [
			'url',
			'id',
			'company_name',
			'contact_name',
			'contact_email',
			'user',
			'delete_url'
		]
	def get_user(self, obj):
		return str(obj.user.name)

##############################################################################
# Define API serializers for Data related operations create, detail and list #
##############################################################################

class DataCreateSerializer(ModelSerializer):
	class Meta:
		model = Data
		fields = [
			'id',
			'time',
			'sensor_parameter',
			'parameter_value'
		]

	@staticmethod
	def setup_eager_loading(queryset):
		queryset = queryset.prefetch_related('sensor_parameter')
		# queryset = queryset.select_related('sensor', 'parameter')
		return queryset

class DataDetailSerializer(ModelSerializer):
	
	sensor_parameter = SerializerMethodField()
	
	class Meta:
		model = Data
		fields = [
			'id',
			'time',
			'sensor_parameter',
			'parameter_value',
		]
	def get_sensor_parameter(self, obj):
		return str(obj.sensor_parameter)

class DataListSerializer(ModelSerializer):
	# url = HyperlinkedIdentityField(
	#     view_name='expert_api:data_list_detail',
	#     lookup_field='pk'
	# )
	# delete_url = HyperlinkedIdentityField(
	#     view_name='expert_api:data_list_delete',
	#     lookup_field='pk'
	# )
	
	sensor_parameter = SerializerMethodField()
	class Meta:
		model = Data
		fields = [
			# 'url',
			'id',
			'time',
			'sensor_parameter',
			'parameter_value',
			# 'delete_url'
		]
	def get_sensor_parameter(self, obj):
		return str(obj.sensor_parameter)
	
################################################################################
# Define API serializers for Marker related operations create, detail and list #
################################################################################

class MarkerCreateSerializer(ModelSerializer):
	# chamber = SerializerMethodField()
	class Meta:
		model = Marker
		fields = [
			'id',
			'time',
			'chamber',
			'marker_name',
			'marker_string'
		]
	# def get_chamber(self, obj):
	# 	return str(obj.chamber.chamber_name)

class MarkerDetailSerializer(ModelSerializer):
	chamber = SerializerMethodField()
	class Meta:
		model = Marker
		fields = [
			'id',
			'time',
			'chamber',
			'marker_name',
			'marker_string'
		]
	def get_chamber(self, obj):
		return str(obj.chamber.chamber_name)

class MarkerListSerializer(ModelSerializer):
	url = HyperlinkedIdentityField(
		view_name='expert_api:marker_list_detail',
		lookup_field='pk'
	)
	delete_url = HyperlinkedIdentityField(
		view_name='expert_api:marker_list_delete',
		lookup_field='pk'
	)
	chamber = SerializerMethodField()
	class Meta:
		model = Marker
		fields = [
			'url',
			'id',
			'time',
			'chamber',
			'marker_name',
			'marker_string',
			'delete_url'
		]
	def get_chamber(self, obj):
		return str(obj.chamber.chamber_name)

###################################################################################
# Define API serializers for Parameter related operations create, detail and list #
###################################################################################

class ParameterCreateSerializer(ModelSerializer):
	class Meta:
		model = Parameter
		fields = [
			'id',
			'parameter_short_name',
			'parameter_name',
			'parameter_position',
			'parameter_type',
			'parameter_unit'
		]

class ParameterDetailSerializer(ModelSerializer):
	class Meta:
		model = Parameter
		fields = [
			'id',
			'parameter_short_name',
			'parameter_name',
			'parameter_position',
			'parameter_type',
			'parameter_unit'
		]

class ParameterListSerializer(ModelSerializer):
	url = HyperlinkedIdentityField(
		view_name='expert_api:parameter_list_detail',
		lookup_field='pk'
	)
	delete_url = HyperlinkedIdentityField(
		view_name='expert_api:parameter_list_delete',
		lookup_field='pk'
	)
	class Meta:
		model = Parameter
		fields = [
			'url',
			'id',
			'parameter_short_name',
			'parameter_name',
			'parameter_position',
			'parameter_type',
			'parameter_unit',
			'delete_url'
		]

################################################################################
# Define API serializers for Sensor related operations create, detail and list #
################################################################################

class SensorCreateSerializer(ModelSerializer):
	# chamber = SerializerMethodField()
	# sensor_type = SerializerMethodField()
	class Meta:
		model = Sensor
		fields = [
			'id',
			'chamber',
			'sensor_type',
			'serial_number'
		]
	# def get_chamber(self, obj):
	# 	return str(obj.chamber.chamber_name)
	# def get_sensor_type(self, obj):
	# 	return str(obj.sensor_type)

class SensorDetailSerializer(ModelSerializer):
	chamber = SerializerMethodField()
	sensor_type = SerializerMethodField()
	class Meta:
		model = Sensor
		fields = [
			'id',
			'chamber',
			'sensor_type',
			'serial_number'
		]
	def get_chamber(self, obj):
		return str(obj.chamber.chamber_name)
	def get_sensor_type(self, obj):
		return str(obj.sensor_type)

class SensorListSerializer(ModelSerializer):
	url = HyperlinkedIdentityField(
		view_name='expert_api:sensor_list_detail',
		lookup_field='pk'
	)
	delete_url = HyperlinkedIdentityField(
		view_name='expert_api:sensor_list_delete',
		lookup_field='pk'
	)
	chamber = SerializerMethodField()
	sensor_type = SerializerMethodField()
	class Meta:
		model = Sensor
		fields = [
			'url',
			'id',
			'chamber',
			'sensor_type',
			'serial_number',
			'delete_url'
		]
	def get_chamber(self, obj):
		return str(obj.chamber.chamber_name)
	def get_sensor_type(self, obj):
		return str(obj.sensor_type)

#####################################################################################
# Define API serializers for Sensor Type related operations create, detail and list #
#####################################################################################

class SensorTypeCreateSerializer(ModelSerializer):
	class Meta:
		model = SensorType
		fields = [
			'id',
			'sensor_type'
		]

class SensorTypeDetailSerializer(ModelSerializer):
	class Meta:
		model = SensorType
		fields = [
			'id',
			'sensor_type'
		]

class SensorTypeListSerializer(ModelSerializer):
	url = HyperlinkedIdentityField(
		view_name='expert_api:sensor_type_list_detail',
		lookup_field='pk'
	)
	delete_url = HyperlinkedIdentityField(
		view_name='expert_api:sensor_type_list_delete',
		lookup_field='pk'
	)
	class Meta:
		model = SensorType
		fields = [
			'url',
			'id',
			'sensor_type',
			'delete_url'
		]