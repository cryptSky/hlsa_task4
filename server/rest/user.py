from flask import Response, request
from flask import current_app as app
from db.models import User
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from errors import InternalServerError, SchemaValidationError, UserNotFoundError, EmailAlreadyExistError
from redis import Redis
from datetime import timedelta
import json
from random import randrange
import math

redis_cache = Redis("redis", 6379)

def cache_key():
   args = request.args
   key = request.path
  
   return key

CACHE_TIMEOUT = 100

class UsersApi(Resource):
	def get(self):

		#app.logger.info(cache_key())
		
		cached_user = redis_cache.get(cache_key())
		if cached_user is not None:
			#app.logger.info("Users in the cache")
			#app.logger.info(cached_user)

			ttl = redis_cache.ttl(cache_key())
			rnd = randrange(CACHE_TIMEOUT)
			if rnd < CACHE_TIMEOUT - ttl:
				users = User.objects().to_json()
				redis_cache.setex(cache_key(), timedelta(seconds=CACHE_TIMEOUT), value=users,)
			else:
				cdata = json.loads(cached_user.decode("UTF-8"))
				users = json.dumps(cdata)
		else:
			#app.logger.info("No users in the cache")
			users = User.objects().to_json()
			redis_cache.setex(cache_key(), timedelta(seconds=CACHE_TIMEOUT), value=users,)

		return Response(users, mimetype="application/json", status=200)

	def delete(self):
		redis_cache.delete(cache_key())
		user = User.objects.delete()
		return '', 200

	def post(self):
		try:
			body = request.get_json()
			user = User(**body).save()
			id = user.id

			redis_cache.delete(cache_key())
			redis_cache.setex(str(id), timedelta(seconds=CACHE_TIMEOUT), value=json.dumps(body),)

			return {'id': str(id)}, 201
		except NotUniqueError:
			raise EmailAlreadyExistError
		except ValidationError:
			raise SchemaValidationError
		except Exception as e:
			app.logger.error(e)
			raise InternalServerError

#class UserApi(Resource):
#	def put(self, id):
#		body = request.get_json()
#		User.objects.get(id=id).update(**body)
#		return '', 200
#
#	def get(self, id):
#		try:
#			users = User.objects.get(id=id).to_json()
#			return Response(users, mimetype="application/json", status=200)
#		except DoesNotExist:
#			raise UserNotFoundError
#
#	def delete(self, id):
#		user = User.objects.get(id=id).delete()
#		return '', 200

class UserApi(Resource):
	def put(self, id):
		body = request.get_json()
		
		redis_cache.delete(cache_key())
		redis_cache.setex(id, timedelta(seconds=CACHE_TIMEOUT), value=body,)

		User.objects.get(id=id).update(**body)

		return '', 200

	def get(self, id):
		try:
			cached_user = redis_cache.get(id)
			if cached_user is not None:
				#app.logger.info("User {0} in the cache".format(id))
				#app.logger.info(cached_user)

				cdata = json.loads(cached_user.decode("UTF-8"))
				users = json.dumps(cdata)
			else:
				#app.logger.info("No user {0} in the cache".format(id))
				users = User.objects.get(id=id).to_json()
			return Response(users, mimetype="application/json", status=200)
		except DoesNotExist:
			raise UserNotFoundError

	def delete(self, id):
		redis_cache.delete(id)
		redis_cache.delete(cache_key())
		user = User.objects.get(id=id).delete()
		return '', 200