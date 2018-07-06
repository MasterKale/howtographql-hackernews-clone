import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Link, Vote


"""
Filters
"""


class LinkFilter(django_filters.FilterSet):
    """
    Enable filtering when requesting Links
    """
    class Meta:
        model = Link
        fields = ['url', 'description']


"""
Nodes
"""


class LinkNode(DjangoObjectType):
    class Meta:
        model = Link
        interfaces = (graphene.relay.Node,)


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (graphene.relay.Node,)


"""
Queries
"""


class RelayQuery(graphene.ObjectType):
    relay_link = graphene.relay.Node.Field(LinkNode)
    relay_links = DjangoFilterConnectionField(LinkNode, filterset_class=LinkFilter)


"""
Mutations
"""


class RelayCreateLink(graphene.relay.ClientIDMutation):
    class Input:
        url = graphene.String()
        description = graphene.String()

    link = graphene.Field(LinkNode)

    def mutate_and_get_payload(self, info, **input):
        user = info.context.user

        link = Link.objects.create(
            url=input.get('url'),
            description=input.get('description'),
            posted_by=user,
        )

        return RelayCreateLink(link=link)


class RelayMutation(graphene.AbstractType):
    relay_create_link = RelayCreateLink.Field()
