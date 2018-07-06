import graphene
from graphene_django import DjangoObjectType

from apps.user.schema import UserType

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
    posted_by = graphene.Field(UserType)

    class Arguments:
        # Specify data that can be passed in when calling this mutation
        url = graphene.String()
        description = graphene.String()

    # Handle the actual mutation request
    def mutate(self, info, url, description):
        # Create the Django object
        user = info.context.user
        link = Link(
            url=url,
            description=description,
            posted_by=user,
        )
        link.save()

        # kwargs here should match the fields defined above when the class is initially defined
        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by,
        )


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
