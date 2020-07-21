from src.common.database import Database
import uuid
import datetime


class Post:

    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None):
        self.blog_id = blog_id           # we can give default value by id=None so id will be none if no value is given
        self.title = title   # default value can be given at end only. so( title, content=None, date, id) this is wrong
        self.content = content
        self.author = author
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id  # uuid generates a random id. we use it when no id is given

    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

    def json(self):
        return{
            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='posts', query={'_id': id})
        return cls(**post_data)

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]
# from_blog method use find method not find_one so it returns a cursor not element so we use for loop to collect
# all the posts in blog


''' return cls(**post_data)=cls(blog_id=post_data['blog_id'],
                               title=post_data['title'],
                               content=post_data['description'],
                               author=post_data['author'],
                               created_date=post_data['created_date'],
                               _id=post_data['_id'])'''