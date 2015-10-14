from stream_framework.feeds.redis import RedisFeed
from stream_framework.feed_managers.base import Manager
from stream_framework.verbs import register
from stream_framework.verbs.base import Verb
from stream_framework.activity import Activity
from datetime import datetime, date, time

class PinVerb(Verb):
    id = 5
    infinitive = 'pin'
    past_tense = 'pinned'

register(PinVerb)

####################

class PinFeed(RedisFeed):
    key_format = 'feed:normal:%(user_id)s'

class UserPinFeed(PinFeed):
    key_format = 'feed:user:%(user_id)s'

####################

class PinManager(Manager):
    feed_classes = dict(
        normal=PinFeed,
    )
    user_feed_class = UserPinFeed

    def add_pin(self, pin):
        activity = pin.create_activity()
        # add user activity adds it to the user feed, and starts the fanout
        self.add_user_activity(pin.user_id, activity)

    def get_user_follower_ids(self, user_id):
        ids = Follow.objects.filter(target=user_id).values_list('user_id', flat=True)
        return {FanoutPriority.HIGH:ids}

manager = PinManager()

####################

activity = Activity(
        actor=13, # Thierry's user id
        verb=PinVerb, # The id associated with the Pin verb
        object=1, # The id of the newly created Pin object
        target=1, # The id of the Surf Girls board
        time=datetime.utcnow(), # The time the activity occured
)

feed = UserPinFeed(13)
feed.insert_activity(activity)
feed.add(activity)
print feed.count() # correct, show 5
#print feed[:5]    # ERROR
#print feed.get_activity_slice() # ERROR
#print feed.index_of(14448039590200000000001005L) # output: index
activities = feed[:10]
print activities

# ERROR: same as above
#feed2 = manager.get_user_feed(13)
#print feed2[:25]

# SUCCESS but empty
#feed3 = manager.get_feeds(13)['normal']
#print feed3[:10]
