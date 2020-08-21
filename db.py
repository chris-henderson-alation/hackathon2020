from definitions import *

class Column(Deserialize):
	name = String
	type = String
	comments = String.optional()

class Table(Deserialize):
    name = String
    columns = ArrayOf(Column)
    comments = String.optional()

class StoredProcedure(Deserialize):
    code = String
    comments = String.optional()

class Schema(Deserialize):
    name = String
    tables = ArrayOf(Table)
    procedures = ArrayOf(StoredProcedure).default([])
    comments = String.optional()

class Database(Deserialize):
    schemas = ArrayOf(Schema)
    fp_groups = ArrayOf(ArrayOf(Integer, length=2))
















































database = '''
{
    "fp_groups": [[1,2], [5,6]],
    "schemas": [
        {
            "name": "Healthcare",
            "tables": [
                {
                    "name": "Dentists",
                    "columns": [
                        {
                            "name": "SSN",
                            "type": "int",
                            "comment": "secret"
                        },
                        {
                            "name": "name",
                            "type": "string"
                        }
                    ]
                },
                {
                    "name": "MDs",
                    "columns": [
                        {
                            "name": "SSN",
                            "type": "int",
                            "comment": "secret"
                        },
                        {
                            "name": "name",
                            "type": "string"
                        }
                    ]
                }
            ]
        },
        {
            "name": "Alation",
            "procedures": [
                {
                    "code": "SELECT * FROM Winning",
                    "comment": "Documented code is best code"
                },
                {
                    "code": "SELECT revenue, growth FROM SalesProjections"
                }
            ],
            "tables": [
                {
                    "name": "Engineering",
                    "columns": [
                        {
                            "name": "SSN",
                            "type": "int",
                            "comment": "secret"
                        },
                        {
                            "name": "name",
                            "type": "string"
                        }
                    ]
                },
                {
                    "name": "SalesProjections",
                    "columns": [
                        {
                            "name": "revenue",
                            "type": "float",
                            "comment": "secret"
                        },
                        {
                            "name": "growth",
                            "type": "float"
                        }
                    ]
                }
            ]
        }
    ]
}

'''

try:
    print(Database.deserialize(database).schemas[1].procedures[0].code)
except Exception as e:
    print(e)
