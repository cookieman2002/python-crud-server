import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db, User

class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)

class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        age = graphene.Int(required=True)

    user = graphene.Field(lambda: UserObject)

    def mutate(self, info, name, age):
        user = User(name=name, age=age)
        db.session.add(user)
        db.session.commit()
        return CreateUser(user=user)

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        age = graphene.Int()

    user = graphene.Field(lambda: UserObject)

    def mutate(self, info, id, name=None, age=None):
        user = User.query.get(id)
        if user is None:
            raise Exception("User not found")
        if name:
            user.name = name
        if age:
            user.age = age
        db.session.commit()
        return UpdateUser(user=user)

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        user = User.query.get(id)
        if user is None:
            raise Exception("User not found")
        db.session.delete(user)
        db.session.commit()
        return DeleteUser(ok=True)

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserObject.connection)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
