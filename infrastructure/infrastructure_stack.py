from aws_cdk import (
    # Duration,
    Stack,
    aws_ecs as ecs,
    aws_logs as logs,
    aws_sqs as sqs,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_apigateway as apigateway,
    aws_sns as sns,
    aws_s3_notifications as s3n,
    aws_sns_subscriptions as subs,
    aws_lambda_event_sources as lambda_event_sources,
    aws_athena as athena,
    aws_glue as glue,
    aws_lambda as _lambda,
    CfnOutput
)
from constructs import Construct
from infrastructure.resources.resources import *
class CovidForecastStack2(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        ROLE_LAMBDA = template_role(self,'role_lambda_covid_forecast','role_lambda_covid_forecast2','lambda')
        # def data_pipeline():
        #     def stack_raw_to_stage_serverless():
        #         sns_topic_raw= template_sns_topic(self,"topic_sns_raw_to_stage","topic_sns_raw_to_stage_covid_forecast")
        #         bucket_raw_covid_forecast =  template_s3(self,"covid-forecast-raw-4288","covid-forecast-raw-4288",False,True)
        #         bucket_raw_covid_forecast.add_event_notification(s3.EventType.OBJECT_CREATED_PUT,s3n.SnsDestination(sns_topic_raw))
        #         sqs_raw_to_stage = template_sqs_queue(self,'sqs_raw_to_stage','sqs_raw_to_stage',visibility_timeout=120)
        #         lambda_raw = template_lambda(scope=self
        #                                         ,iam_role=ROLE_LAMBDA
        #                                         ,lambda_name='raw_to_stage'
        #                                         ,lambda_handler='raw_to_stage.lambda_handler'
        #                                         ,code_path = 'src/cloud_infrastructure/raw_to_stage/'
        #                                         ,id_name='lambda_raw_to_stage'
        #                                         ,minutes=2)


        #         sns_topic_raw.add_subscription(subs.SqsSubscription(sqs_raw_to_stage))
        #         lambda_raw.add_event_source(lambda_event_sources.SqsEventSource(sqs_raw_to_stage))

        #     def stack_stage_to_processed_serverless():
        #         sns_topic_stage = template_sns_topic(self,"topic_sns_stage_to_processed","topic_sns_stage_to_processed_covid_forecast")
        #         bucket_stage_covid_forecast =  template_s3(self,"covid-forecast-stage-4288","covid-forecast-stage-4288",False,True)
        #         bucket_stage_covid_forecast.add_event_notification(s3.EventType.OBJECT_CREATED_PUT,s3n.SnsDestination(sns_topic_stage))
        #         sqs_stage_to_processed = template_sqs_queue(self,'sqs_stage_to_processed','sqs_stage_to_processed',visibility_timeout=120)
        #         lambda_stage_none = template_lambda_none(self,ROLE_LAMBDA,'lambda_stage_to_processed','lambda_stage_to_processed',2)
        #         sns_topic_stage.add_subscription(subs.SqsSubscription(sqs_stage_to_processed))
        #         lambda_stage_none.add_event_source(lambda_event_sources.SqsEventSource(sqs_stage_to_processed,batch_size=1))
        #         bucket_stage_covid_forecast =  template_s3(self,"covid-forecast-processed-4288","covid-forecast-processed-4288",False,True)


            


        s3_actions = template_iam(
                actions=[
                    "*"
                ],
                resources=['*']    
            )
        #     logs_actions = template_iam(
        #         actions=[
        #             "logs:CreateLogGroup",
        #             "logs:CreateLogStream",
        #             "logs:PutLogEvents",



        #             "logs:DescribeLogGroups",
        #         ],
        #         resources=['*']    
        #     )

        policy_lambda = template_policy(
                scope=self,
                id_name = 'policy_lambda',
                statements=[
                    s3_actions                ]
            )

        ROLE_LAMBDA.attach_inline_policy(policy_lambda)
        #     stack_raw_to_stage_serverless()
        #     stack_stage_to_processed_serverless()

        #     glue_database = glue.CfnDatabase(self, "glue_database",
        #         catalog_id=self.account,
        #         database_input=glue.CfnDatabase.DatabaseInputProperty(
        #             name="covid_database_glue"
        #         )
        #     )

        #     glue_table = glue.CfnTable(self, "covid_report",
        #         catalog_id=self.account,
        #         database_name=glue_database.ref,
        #         table_input=glue.CfnTable.TableInputProperty(
        #             name="covid_weekly_report",
        #             table_type="EXTERNAL_TABLE",
        #             parameters={
        #                 "classification": "parquet",
        #                 "compressionType": "none",
        #                 "typeOfData": "file"
        #             },
        #             storage_descriptor=glue.CfnTable.StorageDescriptorProperty(
        #                 columns=[
        #                     glue.CfnTable.ColumnProperty(name="codigo_ibge", type="string"),
        #                     glue.CfnTable.ColumnProperty(name="semana_epidem", type="string"),
        #                     glue.CfnTable.ColumnProperty(name="casos", type="int"),
        #                     glue.CfnTable.ColumnProperty(name="casos_novos", type="int"),
        #                     glue.CfnTable.ColumnProperty(name="obitos", type="int"),
        #                     glue.CfnTable.ColumnProperty(name="obitos_novos", type="int"),
        #                     glue.CfnTable.ColumnProperty(name="casos_pc", type="double"),
        #                     glue.CfnTable.ColumnProperty(name="casos_mm4w", type="double"),
        #                     glue.CfnTable.ColumnProperty(name="obitos_pc", type="double"),
        #                     glue.CfnTable.ColumnProperty(name="obitos_mm4w", type="double"),
        #                     glue.CfnTable.ColumnProperty(name="letalidade", type="double"),
        #                     glue.CfnTable.ColumnProperty(name="nome_ra", type="string"),
        #                     glue.CfnTable.ColumnProperty(name="cod_ra", type="string"),
        #                     glue.CfnTable.ColumnProperty(name="pop", type="int"),
        #                     glue.CfnTable.ColumnProperty(name="pop60", type="int"),
        #                     glue.CfnTable.ColumnProperty(name="area", type="int"),
        #                     glue.CfnTable.ColumnProperty(name="map_leg", type="string"),
        #                     glue.CfnTable.ColumnProperty(name="map_leg_s", type="string"),
        #                     glue.CfnTable.ColumnProperty(name="latitude", type="double"),
        #                     glue.CfnTable.ColumnProperty(name="longitude", type="double"),
        #                     glue.CfnTable.ColumnProperty(name="datahora", type="datetime"),
        #                 ],
        #                 location=f"s3://covid-forecast-processed-4288/covid_daily/",
        #                 input_format="org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
        #                 output_format="org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
        #                 serde_info=glue.CfnTable.SerdeInfoProperty(
        #                     serialization_library="org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
        #                 )
        #             ),
        #             partition_keys=[
        #                 glue.CfnTable.ColumnProperty(name="nome_drs", type="string"),
        #                 glue.CfnTable.ColumnProperty(name="nome_munic", type="string")
        #             ]
        #         )
        #     )
        #     query_results_bucket = s3.Bucket(self, "AthenaQueryResultsBucket")
        #     athena_workgroup = athena.CfnWorkGroup(self, "AthenaWorkGroup",
        #         name="my_workgroup",
        #         work_group_configuration=athena.CfnWorkGroup.WorkGroupConfigurationProperty(
        #             result_configuration=athena.CfnWorkGroup.ResultConfigurationProperty(
        #                 output_location=query_results_bucket.s3_url_for_object()
        #             )
        #         )
        #     )

        def create_api_gateway(lambda_api):
            # auth = apigateway.RequestAuthorizer(
            #     scope=self,
            #     id='request_authorizer',
            #     handler=lambda_authorizer,
            #     identity_sources=['method.request.header.Authorization']
            # )
            lambda_authorizer = template_lambda(
                scope=self,
                iam_role=ROLE_LAMBDA,
                lambda_handler='auth.lambda_handler',
                lambda_name='ml-covid-api-authorizer2',
                code_path='src/cloud_infrastructure/ml/',
                id_name='ml-covid-api-authorizer2',
                minutes=2
            )
            auth = apigateway.RequestAuthorizer(
                scope=self,
                id='request_authorizer',
                handler=lambda_authorizer,
                identity_sources=['method.request.header.Authorization']
            )


            prd_log_group = logs.LogGroup(self, "PrdLogs")
            api = apigateway.RestApi(
                self, 'predict-covid-api2',
                default_cors_preflight_options={
                    "allow_origins": apigateway.Cors.ALL_ORIGINS,
                    "allow_methods": apigateway.Cors.ALL_METHODS,
                    "allow_headers": ["Content-Type", "X-Amz-Date", "Authorization", "X-Api-Key", "X-Amz-Security-Token"],
                    "expose_headers": ["X-Amz-Date", "X-Amz-Security-Token", "X-Api-Key"],
                    "allow_credentials": True
                },
                deploy_options=apigateway.StageOptions(
                    access_log_destination=apigateway.LogGroupLogDestination(prd_log_group),
                    access_log_format=apigateway.AccessLogFormat.json_with_standard_fields(
                        caller=False,
                        http_method=True,
                        ip=True,
                        protocol=True,
                        request_time=True,
                        resource_path=True,
                        response_length=True,
                        status=True,
                        user=True
                    )
                ),
                cloud_watch_role=True,
                
                api_key_source_type =apigateway.ApiKeySourceType.HEADER
            )
            deployment = apigateway.Deployment(self, "Deployment", api=api)

            
            # Add a resource and method to the API Gateway
            lambda_integration = apigateway.LambdaIntegration(lambda_api)
            ml_predict = api.root.add_resource('predict',default_integration=lambda_integration)
            ml_predict.add_method('POST')
            ml_predict.add_method('GET',authorizer=auth)
            CfnOutput(self, 'ApiUrl', value=api.url)

        def mlops_pipeline():
        
            lambda_ml_ops = _lambda.Function(
                scope=self,
                memory_size=2048,
                role=ROLE_LAMBDA,
                timeout=Duration.minutes(5),
                handler=_lambda.Handler.FROM_IMAGE,   # Específico para containers
                runtime=_lambda.Runtime.FROM_IMAGE,   # Define runtime como container
                id='lambda_mlops_pipeline2',
                function_name='lambda_mlops-covid2',
                code=_lambda.Code.from_ecr_image(
                    repository=ecr.Repository.from_repository_arn(
                        self, 
                        id='ecr_repo', 
                        repository_arn='arn:aws:ecr:us-east-1:428897232596:repository/mlopspipeline-covid'
                    ),
                    tag="latest"
                )
            )


            create_api_gateway(lambda_ml_ops)
        mlops_pipeline()
