from flask_restx import Api

api = Api(version='1.0', title='Library Management System Api',description='This is a sample API documentation for Library Management System. This documentation will provide all details related to the operations performed in a library.')
ns = api.namespace('api/v1', description="Version 1.0 of API")