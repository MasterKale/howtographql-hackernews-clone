import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from django.db.models import Q

from apps.user.schema import UserType

from .models import Link, Vote


"""
GraphQL types for our models
"""


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote


"""
Queries
"""


class Query(graphene.ObjectType):
    links = graphene.List(LinkType, search=graphene.String())
    votes = graphene.List(VoteType)

    def resolve_links(self, info, search=None, **kwargs):
        """
        Allow for searching URL or description
        """
        if search:
            filter = (
                Q(url__icontains=search) |
                Q(description__icontains=search)
            )
            return Link.objects.filter(filter)
        # Default to returning all links
        return Link.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()


"""
Mutations
"""


class CreateLink(graphene.Mutation):
    class Arguments:
        # Specify data that can be passed in when calling this mutation
        url = graphene.String()
        description = graphene.String()

    # Specify fields that will be returned after creating a link
    link = graphene.Field(LinkType)

    # Handle the actual mutation request
    def mutate(self, info, url, description):
        # Create the Django object
        user = info.context.user
        link = Link.objects.create(
            url=url,
            description=description,
            posted_by=user,
        )

        # kwargs here should match the fields defined above when the class is initially defined
        return CreateLink(
            link=link,
        )


class CreateVote(graphene.Mutation):
    class Arguments:
        link_id = graphene.Int()

    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to vote!')

        link = Link.objects.get(id=link_id)
        if not link:
            raise Exception('Invalid link ID!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(
            user=user,
            link=link,
        )


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
