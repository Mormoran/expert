from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
)

from impedans_expert.expert_algorithms.models import (
    Algorithm,
    AlgorithmRun,
    AlgorithmRunResult,
    AlgorithmTimeResult,
    AlgorithmState
)

from impedans_expert.expert_import.models import Run

###################################################################################
# Define API serializers for Algorithm related operations create, detail and list #
###################################################################################

class AlgorithmCreateSerializer(ModelSerializer):
    # customer = SerializerMethodField()
    class Meta:
        model = Algorithm
        fields = [
            'id',
            'algorithm_name',
            'algorithm_src',
            'algorithm_description'
        ]
    # def get_customer(self, obj):
    #     return str(obj.customer.company_name)

class AlgorithmDetailSerializer(ModelSerializer):
    customer = SerializerMethodField()
    class Meta:
        model = Algorithm
        fields = [
            'id',
            'algorithm_name',
            'algorithm_src',
            'algorithm_description'
        ]
    def get_customer(self, obj):
        return str(obj.customer.company_name)

class AlgorithmListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='algorithms_api:algorithms_list_detail',
        lookup_field='pk'
    )
    delete_url = HyperlinkedIdentityField(
        view_name='algorithms_api:algorithms_list_delete',
        lookup_field='pk'
    )
    class Meta:
        model = Algorithm
        fields = [
            'url',
            'id',
            'algorithm_name',
            'algorithm_src',
            'algorithm_description',
            'delete_url'
        ]

##################################################################################
# Define API serializers for Algorithm Run related operations create, detail and list #
##################################################################################

class AlgorithmRunCreateSerializer(ModelSerializer):
    # algorithm = SerializerMethodField()
    # customer = SerializerMethodField()
    class Meta:
        model = AlgorithmRun
        fields = [
            'id',
            'algorithm',
            'customer',
            'date_time'
        ]
    # def get_algorithm(self, obj):
    #     return str(obj.algorithm.algorithm_name)
    # def get_customer(self, obj):
    #     return str(obj.customer.company_name)

class AlgorithmRunDetailSerializer(ModelSerializer):
    algorithm = SerializerMethodField()
    customer = SerializerMethodField()
    class Meta:
        model = AlgorithmRun
        fields = [
            'id',
            'algorithm',
            'customer',
            'date_time'
        ]
    def get_algorithm(self, obj):
        return str(obj.algorithm.algorithm_name)
    def get_customer(self, obj):
        return str(obj.customer.company_name)

class AlgorithmRunListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='algorithms_api:algorithm_run_list_detail',
        lookup_field='pk'
    )
    delete_url = HyperlinkedIdentityField(
        view_name='algorithms_api:algorithm_run_list_delete',
        lookup_field='pk'
    )
    algorithm = SerializerMethodField()
    customer = SerializerMethodField()
    class Meta:
        model = AlgorithmRun
        fields = [
            'id',
            'url',
            'id',
            'algorithm',
            'customer',
            'date_time',
            'delete_url'
        ]
    def get_algorithm(self, obj):
        return str(obj.algorithm.algorithm_name)
    def get_customer(self, obj):
        return str(obj.customer.company_name)

###############################################################################################
# Define API serializers for Algorithm Run Results related operations create, detail and list #
###############################################################################################

class AlgorithmRunResultsCreateSerializer(ModelSerializer):
    # runs = SerializerMethodField()
    # algorithm_run = SerializerMethodField()
    # parameter = SerializerMethodField()
    class Meta:
        model = AlgorithmRunResult
        fields = [
            'id',
            'runs',
            'algorithm_run',
            'parameter',
            'value'
        ]
    # def get_runs(self, obj):
    #     return str(obj.runs)
    # def get_algorithm_run(self, obj):
    #     return str(obj.algorithm_run)
    # def get_parameter(self, obj):
    #     return str(obj.parameter.parameter_name)

class AlgorithmRunResultsDetailSerializer(ModelSerializer):
    runs = SerializerMethodField()
    algorithm_run = SerializerMethodField()
    parameter = SerializerMethodField()
    class Meta:
        model = AlgorithmRunResult
        fields = [
            'id',
            'runs',
            'algorithm_run',
            'parameter',
            'value'
        ]
    def get_runs(self, obj):
        return str(obj.runs)
    def get_algorithm_run(self, obj):
        return str(obj.algorithm_run)
    def get_parameter(self, obj):
        return str(obj.parameter.parameter_name)

class AlgorithmRunResultsListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='algorithms_api:algorithm_run_results_list_detail',
        lookup_field='pk'
    )
    delete_url = HyperlinkedIdentityField(
        view_name='algorithms_api:algorithm_run_results_list_delete',
        lookup_field='pk'
    )
    runs = SerializerMethodField()
    algorithm_run = SerializerMethodField()
    parameter = SerializerMethodField()
    start_time = SerializerMethodField()
    class Meta:
        model = AlgorithmRunResult
        fields = [
            'url',
            'id',
            'runs',
            'start_time',
            'algorithm_run',
            'parameter',
            'value',
            'delete_url'
        ]
    def get_runs(self, obj):
        return str(obj.runs)
    def get_algorithm_run(self, obj):
        return str(obj.algorithm_run)
    def get_parameter(self, obj):
        return str(obj.parameter.parameter_name)
    def get_start_time(self, obj):
        return str(obj.runs.start_time)

###############################################################################################
# Define API serializers for Algorithm Time Results related operations create, detail and list #
###############################################################################################

class AlgorithmTimeResultsCreateSerializer(ModelSerializer):
    # algorithm_run = SerializerMethodField()
    # parameter = SerializerMethodField()
    # chamber = SerializerMethodField()
    class Meta:
        model = AlgorithmTimeResult
        fields = [
            'id',
            'algorithm_run',
            'parameter',
            'value',
            'start_time',
            'end_time',
            'chamber'
        ]
    # def get_algorithm_run(self, obj):
    #     return str(obj.algorithm_run)
    # def get_parameter(self, obj):
    #     return str(obj.parameter.parameter_name)
    # def get_chamber(self, obj):
    #     return str(obj.chamber.chamber_name)

class AlgorithmTimeResultsDetailSerializer(ModelSerializer):
    algorithm_run = SerializerMethodField()
    parameter = SerializerMethodField()
    chamber = SerializerMethodField()
    class Meta:
        model = AlgorithmTimeResult
        fields = [
            'id',
            'algorithm_run',
            'parameter',
            'value',
            'start_time',
            'end_time',
            'chamber'
        ]
    def get_algorithm_run(self, obj):
        return str(obj.algorithm_run)
    def get_parameter(self, obj):
        return str(obj.parameter.parameter_name)
    def get_chamber(self, obj):
        return str(obj.chamber.chamber_name)

class AlgorithmTimeResultsListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='algorithms_api:algorithm_time_results_list_detail',
        lookup_field='pk'
    )
    delete_url = HyperlinkedIdentityField(
        view_name='algorithms_api:algorithm_time_results_list_delete',
        lookup_field='pk'
    )
    algorithm_run = SerializerMethodField()
    parameter = SerializerMethodField()
    chamber = SerializerMethodField()
    class Meta:
        model = AlgorithmTimeResult
        fields = [
            'url',
            'id',
            'algorithm_run',
            'parameter',
            'value',
            'start_time',
            'end_time',
            'chamber',
            'delete_url'
        ]
    def get_algorithm_run(self, obj):
        return str(obj.algorithm_run)
    def get_parameter(self, obj):
        return str(obj.parameter.parameter_name)
    def get_chamber(self, obj):
        return str(obj.chamber.chamber_name)

#########################################################################################
# Define API serializers for Algorithm State related operations create, detail and list #
#########################################################################################

class AlgorithmStateCreateSerializer(ModelSerializer):
    # algorithm_run = SerializerMethodField()
    class Meta:
        model = AlgorithmState
        fields = [
            'id',
            'algorithm_run',
            'state'
        ]
    # def get_algorithm_run(self, obj):
    #     return str(obj.algorithm_run)

class AlgorithmStateDetailSerializer(ModelSerializer):
    algorithm_run = SerializerMethodField()
    class Meta:
        model = AlgorithmState
        fields = [
            'id',
            'algorithm_run',
            'state'
        ]
    def get_algorithm_run(self, obj):
        return str(obj.algorithm_run)

class AlgorithmStateListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='algorithms_api:algorithm_state_list_detail',
        lookup_field='pk'
    )
    delete_url = HyperlinkedIdentityField(
        view_name='algorithms_api:algorithm_state_list_delete',
        lookup_field='pk'
    )
    algorithm_run = SerializerMethodField()
    class Meta:
        model = AlgorithmState
        fields = [
            'url',
            'id',
            'algorithm_run',
            'state',
            'delete_url'
        ]
    def get_algorithm_run(self, obj):
        return str(obj.algorithm_run)
