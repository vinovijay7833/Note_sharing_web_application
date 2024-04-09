from django.db import models
import hashlib
import uuid

def hash_password(password):
	salt = uuid.uuid4().hex
	return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password,user_password):
	password,salt = hashed_password.split(':')
	return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

# Create your models here.

class user(models.Model):
	username = models.CharField(max_length=20)
	email_id = models.CharField(max_length=50,unique=True,primary_key=True)
	password = models.CharField(max_length=512)

	def __str__(self):
		return (self.username)

	@classmethod
	def checkUserExists(cls,email_id):
		s = cls.objects.filter(email_id=email_id)
		if s:
			return 1
		else:
			return 0

	@classmethod
	def registerUser(cls,username,email_id,password):
		try:
			if cls.checkUserExists(email_id):
				return -1
			else:
				#password = hash_password(password)
				u = cls(username=username,email_id=email_id,password=password)
				u.save()
				return u
		except Exception as e:
			return e

	@classmethod
	def loginUser(cls,email_id,password):
		s = cls.objects.filter(email_id=email_id)
		if s:
			if s[0].password==password:

				return s[0]
			else:
				return -1
		else:
			return -1

class notes(models.Model):
	"""docstring for notes"""
	title = models.CharField(max_length=20)
	username1 = models.CharField(max_length=20)
	content = models.CharField(max_length=2000)
	date_of_creation = models.CharField(max_length=200)
	@classmethod
	def registerNotes(cls,username1,title,content,date_of_creation):
		try:
			n = cls(username1=username1,title=title,content=content,date_of_creation=date_of_creation)
			n.save()
			return n
		except Exception as e:
			return e
	@classmethod
	def updateNotes(cls,id1,title,content,date_of_creation):
		try:
			n = cls.objects.filter(id=id1)
			n.update(title=title,content=content,date_of_creation=date_of_creation)
			return 1
		except Exception as e:
			return e

	


class sharedNotes(models.Model):
	"""docstring for notes"""
	
	note_id = models.ForeignKey(notes, on_delete=models.CASCADE)
	email_id = models.ForeignKey(user, on_delete=models.CASCADE)
	@classmethod
	def share_note(cls,note_id,email_id):
		try:
			n = cls.objects.filter(email_id_id=email_id,note_id_id=note_id)
			if n:
				return 0 #already shared
			else:
				n = cls(note_id_id=note_id,email_id_id=email_id)
				n.save()
				return n	
		except Exception as e:
			return e
		