import graphene
from graphene_django import DjangoObjectType

from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


"""
Queries
"""


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()


"""
Mutations
"""


class CreateLink(graphene.Mutation):
    # Specify which fields will be returned after creating a link
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    class Arguments:
        # Specify data that can be passed in when calling this mutation
        url = graphene.String()
        description = graphene.String()

    # Handle the actual mutation request
    def mutate(self, info, url, description):
        # Create the Django object
        link = Link(url=url, description=description)
        link.save()

        # kwargs here should match the fields defined above when the class is initially defined
        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description
        )


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
