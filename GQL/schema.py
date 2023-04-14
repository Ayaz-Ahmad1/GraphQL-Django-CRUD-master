import graphene
from graphene_django import DjangoObjectType
from gql_app.models import Category, Ingredient

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


#---------------------------- FETCHING QUERIES ----------------------------------------
class Query(graphene.ObjectType):
    #fetch the list of all ingredients
    ingredient = graphene.List(IngredientType, id=graphene.ID(), name=graphene.String())
    category = graphene.List(CategoryType, id=graphene.ID(), name=graphene.String() )

    def resolve_category(self, info, id=None, name=None):
        
        # Checks if id is available then, return category by id otherwise none.
        if id:
            try:
                return Category.objects.filter(id=id)
            except Category.DoesNotExist:
                return Category.objects.none
            
        # Checks if name is available then, return category by name otherwise none.
        elif name:
            try:
                return Category.objects.filter(name=name)
            except Category.DoesNotExist:
                return Category.objects.none
        
        # Returns all category if no name or id is provided 
        else:   
            return Category.objects.all()
        
        
    def resolve_ingredient(self, info, name=None, id=None):
        # Checks if id is available then, return Ingredient by id otherwise none.
        if id:
            try:
                return Ingredient.objects.filter(id=id)
            except Ingredient.DoesNotExist:
                return Ingredient.objects.none
            
        # Checks if name is available then, return Ingredient by name otherwise none.
        elif name:
            try:
                return Ingredient.objects.filter(name=name)
            except Ingredient.DoesNotExist:
                return Ingredient.objects.none

        # Returns all category if no name is provided 
        else:
            return Ingredient.objects.select_related("category").all()
        
        # Checks if name is available then, return Ingredient by name otherwise none.
        
        
#--------------------------------------- CATEGORY TABLE MUTATIONS ----------------------------------------
class CreateCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
    category = graphene.Field(CategoryType)
        
    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CreateCategoryMutation(category=category)
    
class UpdateCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
    category = graphene.Field(CategoryType)
    
    @classmethod
    def mutate(cls, root, info, id, name):
        data = Category.objects.get(id=id)
        data.name = name
        data.save()
        return UpdateCategoryMutation(category=data)
    
class DeleteCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    category = graphene.Field(CategoryType)
    
    @classmethod
    def mutate(cls, root, info, id):
        data = Category.objects.get(id=id)
        data.delete()
        return 
    
#----------------------------------------- INGREDIENT TABLE MUTATION -----------------------------------------
class CreateIngredientsMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        notes = graphene.String(required=True)
        category_id = graphene.Int()
    ingredients = graphene.Field(IngredientType)
    
    @classmethod
    def mutate(cls, root, info, name, notes, category_id):
        category = Category.objects.get(id=category_id)
        ingredient = Ingredient(name=name, notes=notes, category=category)
        ingredient.save()
        return CreateIngredientsMutation(ingredients=ingredient)
            
class UpdateIngredientsMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
        notes = graphene.String()
    Ingredient = graphene.Field(IngredientType)
    
    @classmethod
    def mutate(cls, root, info, id, name, notes):
        data = Ingredient.objects.get(id=id)
        data.name = name
        data.notes = notes
        data.save()
        return UpdateIngredientsMutation(Ingredient=data)
    
class DeleteIngredientsMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    Ingredient = graphene.Field(IngredientType)
    
    @classmethod
    def mutate(cls, root, info, id):
        get_ingredient = Ingredient.objects.get(id=id)
        get_ingredient.delete()
        return 
            
            
class Mutation(graphene.ObjectType):
    #CATEGORY MUTATION
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()
    #INGREDIENT MUTATION
    create_ingredients = CreateIngredientsMutation.Field()
    update_ingredients = UpdateIngredientsMutation.Field()
    delete_ingredients = DeleteIngredientsMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
