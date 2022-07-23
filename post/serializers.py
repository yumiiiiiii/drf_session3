from rest_framework import serializers

from .models import *

class PostSimpleSerializer(serializers.ModelSerializer):
    # 공지글 전체 조회 시리얼라이저
    class Meta:
        model = Post
        fields = ('id', 'title')


class PostDetailSerializer(serializers.ModelSerializer):
    # 공지글 상세 조회 시리얼라이저
    class Meta:
        model = Post
        fields = ('id' ,'title' , 'content' , 'created')


class PostCreateSerializer(serializers.ModelSerializer):
    # 공지글 생성 시리얼라이저
    class Meta:
        model = Post
        fields = ('title', 'content','created', 'author')


class CalSimpleSerializer(serializers.ModelSerializer):
    # 일정 전체 조회 시리얼라이저
    class Meta:
        model = Calendar
        fields = ('id', 'calendar_title','calendar_final' ,'calendar_damdang')


class CalDetailSerializer(serializers.ModelSerializer):
    # 일정 상세 조회 시리얼라이저
    class Meta:
        model = Calendar
        fields = ('id' ,'calendar_title','calendar_final', 'calendar_damdang','calendar_created')


class CalCreateSerializer(serializers.ModelSerializer):
    # 일정 생성 시리얼라이저
    class Meta:
        model = Calendar
        fields = ('calendar_title','calendar_final', 'calendar_damdang', 'calendar_created', 'calender_author')

#--------------------------------

class UserSerializer(serializers.ModelSerializer):
    #user 회원가입
    class Meta:
        model=User
        fields=['id','username','email','password','club']

    def create(self, validated_data):
        user=User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            club=validated_data['club'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserLoginSerializer(serializers.Serializer):
    #user login
    email=serializers.CharField(max_length=64)
    password=serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email=data.get("email",None)
        password=data.get("password", None)

        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)

            if not user.check_password(password):
                raise serializers.ValidationError()
            else:
                return user
        else:
            raise serializers.ValidationError()

# {
# "username":"lion",
# "email":"jain@likelion.org",
# "password":"yumi1226",
# "club":"멋쟁이사자처럼"
# }


class TodoCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=TodoComment
        fields=['id','post','author','content','created_at']

#  {
# "post":"4",
#  "author":2,
#  "content":"댓글"
#  }


class TodoSerializer(serializers.ModelSerializer):
    Todo_comment=TodoCommentSerializer(many=True, read_only=True)

    class Meta:
        model=Todo
        fields=['id','Todo_content','Todo_complete','Todo_created_at','Todo_comment']

# {
# "Todo_content":"할일1",
# "Todo_complete":"True",
# "Todo_comment":"댓글1"
# }

        



