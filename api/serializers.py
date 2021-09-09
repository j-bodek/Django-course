from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'



# that's gonna convert project model into json object
class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False) #extends owner with name,email etc
    tags = TagSerializer(many=True) #extends tags with name,created 
    reviews = serializers.SerializerMethodField() #set new attribute to json object

    class Meta:
        model = Project 
        fields = '__all__' 

    def get_reviews(self, obj): #def must starts from get_
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many = True)
        return serializer.data