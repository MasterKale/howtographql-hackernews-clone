import graphene

import apps.links.schema


"""
Defining these seemingly simple classes here helps keep queries/mutations/etc... isolated to their
respective apps
"""


class Query(apps.links.schema.Query, graphene.ObjectType):
    pass


class Mutation(apps.links.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
