from django.shortcuts import render, redirect,render_to_response
from .models import user,notes,sharedNotes
from django.http import HttpResponse
from datetime import date
from django.core.cache import cache
from django.contrib import messages
# Create your views here.mplat

def loginRequired(methodName):
	def wrapper(*args,**keywords):
		request = args[0]
		if 'username_key' in request.session:
			return methodName(*args,**keywords)
		else:
			return redirect(login)
	return wrapper

def register(request):
	if request.method == 'GET':
		return render(request,'register.html')
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		confpassword=request.POST['conf_password']
		email = request.POST['email']
		if password==confpassword:
			u = user.registerUser(username,email,password)
			if isinstance(u,user):
				message = '{0} registered'.format(username)
				return redirect(login)

			elif u == -1:
				messages.info(request,'User Already Exists')
				return render(request,'register.html')
			else:
				print(u)
				messages.info(request,'Unexpected error occured')
				return render(request,'register.html')
		else:
			messages.info(request,"Passwords Don't Match")
			return render(request,'register.html')

def login(request):
	if request.method == 'GET':
		return render(request,'login.html')
	elif request.method == 'POST':
		email= request.POST['email']
		password = request.POST['password']
		u = user.loginUser(email,password)
		if isinstance(u,user):
			#request.session['username_key'] = u.username
			request.session['username_key'] = email
			return redirect(submitNotes)
			#want to send username
			#return render(request, 'index.html',{'message':message})
		elif u == -1:
			messages.info(request,'Username or password is invalid')
			return render(request,'login.html')
		else:
			messages.info(request,'Unexpected error occured')
			return render(request,'login.html')
		
@loginRequired
def submitNotes(request):
	if request.method == 'GET':
		username = request.session['username_key']
		all_notes = notes.objects.filter(username1=username)
		message = 'Welcome ' + username
		return render(request,'index.html',{'notes': all_notes,'Username':username})
	elif request.method == 'POST':
		email_id = request.session['username_key']
		title = request.POST['title']
		content = request.POST['content']
		date_of_creation = str(date.today())
		u = notes.registerNotes(email_id,title,content,date_of_creation)
		if isinstance(u,notes):
			return redirect(submitNotes)
		else:
			message = 'Unexpected error occured'
		return HttpResponse(message)

def addNotes(request):
	if request.method == 'GET':
		username = request.session['username_key']
		return render(request,'add_note.html')
	elif request.method == 'POST':
		return render(request,'add_note.html')


def updatenotesView(request):
	if request.method == 'POST':
		id1 = request.POST['update']
		u = notes.objects.filter(id=id1)
		obj = u[0]
		return render(request,'add_note.html',{'obj':obj})
	elif request.method == 'GET':
		return redirect(updatenotesView)


def updateView(request):
	if request.method == 'POST':
		id1 = request.POST['update']
		title = request.POST['title']
		content = request.POST['content']
		date_of_creation = str(date.today())			
		i = notes.updateNotes(id1,title,content,date_of_creation)
		if i==1:
			return redirect(submitNotes)
		else:
			messages.info(request,"Unexpected error")
			return redirect(submitNotes)

	elif request.method == 'GET':
		return redirect(updateView)	
		
		

def deleteNote(request):
	if request.method == 'POST':
		id1 = request.POST['delete']
		notes.objects.filter(id=id1).delete()
		return redirect(submitNotes)

def deleteshareNote(request):
	if request.method == 'POST':
		id1 = request.POST['delete']
		sharedNotes.objects.filter(id=id1).delete()
		return redirect(sharewithme)

def logout(request):
	del request.session['username_key']
	cache.clear()
	return redirect(login)

def shareNote(request):
	if request.method=='GET':
		username=request.session['username_key']
		all_notes=notes.objects.filter(username1=username)
		all_users=user.objects.all()
		return render(request,'share_note.html',{'notes':all_notes,'users':all_users,'Username':username})

	elif request.method=='POST':
		note_id=request.POST['note_id']
		email_id=request.POST['user']
		u = sharedNotes.share_note(note_id,email_id)
		if isinstance(u,sharedNotes):
			return redirect(submitNotes)
		elif u==0:
			messages.info(request,"File Already Shared")
			return render(request,'share_note.html')
		else:
			messages.info(request,"Unexpected error")
			return render(request,'share_note.html')
	return redirect(submitNotes)

def sharewithme(request):
	if request.method=='GET':
		username=request.session['username_key']
		all_notes=notes.objects.all()
		all_shared_notes = sharedNotes.objects.filter(email_id_id=username)
		return render(request,'sharewithme.html',{'shared_notes':all_shared_notes,'notes':all_notes,'Username':username})
	elif request.method=='POST':
		username=request.session['username_key']
		all_notes=notes.objects.all()
		all_shared_notes = sharedNotes.objects.filter(email_id_id=username)
		return render(request,'sharewithme.html',{'shared_notes':all_shared_notes,'notes':all_notes})				






