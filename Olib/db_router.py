# class MultiDBRouter:
#     """
#     A router to control database operations for different models in the same app.
#     """

#     def db_for_read(self, model, **hints):
#         if model._meta.model_name == 'user_collection':
#             return 'mongo'
#         return 'default'

#     def db_for_write(self, model, **hints):
#         if model._meta.model_name == 'user_collection':
#             return 'mongo'
#         return 'default'

#     def allow_relation(self, obj1, obj2, **hints):
#         # Allow relations if both objects belong to the same database
#         if (obj1._meta.model_name == 'user_collection' and obj2._meta.model_name == 'user_collection'):
#             return True
#         elif (obj1._state.db == 'mongo' and obj2._state.db == 'mongo'):
#             return True
#         elif (obj1._state.db == 'default' and obj2._state.db == 'default'):
#             return True
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         if model_name == 'user_collection':
#             return db == 'mongo'
#         return db == 'default'
