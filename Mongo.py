#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from web import form
import numpy as np
import matplotlib.pyplot as plt
from web.contrib.template import render_mako
import pymongo
import feedparser
import urllib
import tweepy
        
urls = (
   '/hello', 'hello',
	'/mia', 'mia',
	'/index', 'index',
	'/fractal', 'fractal',
	'/formi', 'p3_formulario',
	'/inicio', 'inicio',
	'/logout', 'logout',
	'/registro', 'registro',
	'/insercion', 'insercion',
	'/datos', 'datos',
	'/modificar', 'modificar',
	'/cambio', 'cambio',
	'/rss', 'rss',
	'/maps', 'maps',
	'/charts', 'charts',
	'/mostrarcharts', 'mostrarcharts',
	'/twitter', 'twitter',
	'/mashup', 'mashup',
	'/(.*)', 'error'
)

#Para poder usar sesiones con web.py
web.config.debug = False

plantilla = web.template.render('./templates/')

app = web.application(urls, globals())

session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'usuario':'', 'sesion1':'', 'sesion2':'', 'sesion3':''})

try:
	conn=pymongo.MongoClient()
	print "Conexión realizada con éxito"
except pymongo.errors.ConnectionFailure, e:
	print "No se pudo conectar a MongoDB: %s" %e
conn

db = conn.usuarios
db

coll=db.datos
coll

# Consumer keys and access tokens, used for OAuth
consumer_key = 'RmKIVUCEetZ1izCq5w1xig'
consumer_secret = 'QV8vBC2laPpSFJTs2f6HF7VhFyAF9kGJRMjvQGpSp4Y'
access_token = '2245460426-UD0iEwCUJKivjYQ6LmppZF1BL5LFhFe20rriJhZ'
access_token_secret = 'tqhb8WtqXWpNsZLmCqhmW2brO2YcfxmtjQ8YuiPpvvn3t'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

#Templates de mako
render = render_mako(
	directories = ['templates'],
	input_encoding = 'utf-8',
	output_encoding = 'utf-8')

myform = form.Form(
	form.Textbox("nombre"),
	form.Textbox("apellido"),
	form.Button("Enviar datos")
)

form_fractal = form.Form(
	form.Textbox("x_min", form.notnull),
	form.Textbox("x_max", form.notnull),
	form.Textbox("y_min", form.notnull),
	form.Textbox("y_max", form.notnull),
	form.Textbox("pixeles", form.notnull),
	form.Textbox("iteraciones", form.notnull),
	form.Button("Enviar datos")
)

form_p3 = form.Form(
	form.Textbox("nombre", form.notnull, description="Nombre de usuario"),
	form.Textbox("apellidos", form.notnull, description="Apellidos del usuario"),
	form.Textbox("dni", form.notnull, form.regexp('^([0-9]{8}[A-Z])$', 'Formato de DNI incorrecto'), description="DNI del usuario"),
	form.Textbox("correo", form.notnull, form.regexp('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', 'Formato de correo electronico incorrecto'), description="Correo electronico"),
	form.Dropdown("dia", [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31], description="Dia de nacimiento"),
	form.Dropdown("mes", ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'], description="Mes de nacimiento"),
	form.Dropdown("anio", [1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013], description="Anio de nacimiento"),
	form.Textarea("direccion", form.notnull, description="Direccion completa"),
	form.Password("contrasenia", form.notnull, description="Introduzca su contrasenia", post="Se requiere una contrasenia de al menos 7 caracteres"),
	form.Password("verificacion", form.notnull, description="Repita su contrasenia"),
	form.Radio("pago", ['Contra reembolso', 'VISA'], form.notnull, description="Forma de pago"),
	form.Textbox("visa", form.notnull, form.regexp('^([0-9]{4}) ([0-9]{4}) ([0-9]{4}) ([0-9]{4})|([0-9]{4})-([0-9]{4})-([0-9]{4})-([0-9]{4})$', 'Numero de Visa incorrecto'), description="Numero de VISA"),
	form.Checkbox("aceptacion", form.Validator("Debes aceptar las clausulas de proteccion de datos", lambda i: "aceptacion" not in i), description="Aceptacion de las clausulas de proteccion de datos"),
	form.Button("Mandar datos"),
	validators = [form.Validator("La contrasenia no coincide", lambda i: i.contrasenia == i.verificacion), form.Validator("Tamanio de contrasenia incorrecto", lambda i: len(i.contrasenia) >= 7), form.Validator("Fecha de nacimiento incorrecta", lambda i: (((str(i.mes) == 'febrero') and ((int(i.dia) <= 28) and ((int(i.anio) % 4) != 0) or (int(i.dia) <= 29) and ((int(i.anio) % 4) == 0))) or ((int(i.dia) <= 31) and ((str(i.mes) == 'enero') or (str(i.mes) == 'marzo') or (str(i.mes) == 'julio') or (str(i.mes) == 'agosto') or (str(i.mes) == 'octubre') or (str(i.mes) == 'diciembre'))) or ((int(i.dia) <= 30) and ((str(i.mes) == 'abril') or (str(i.mes) == 'junio') or (str(i.mes) == 'septiembre') or (str(i.mes) == 'noviembre')))))]
)

login_form = form.Form(
	form.Textbox ('usuario', form.notnull, description='Usuario: '),
	form.Password ('contrasenia', form.notnull, description='Contrasenia: '),
	form.Button ('Ingresar'),
)

datos_form = form.Form(
	form.Textbox ('nombre', form.notnull, description='Nombre de usuario para visualizar datos: '),
	form.Button ('Entrar'),
)

modi_form = form.Form(
	form.Textbox ('nombre', form.notnull, description='Nombre de usuario para modificar sus datos: '),
	form.Button ('Entrar'),
)

charts_form = form.Form(
	form.Textbox('id', form.notnull, description='Identificador del grafico: '),
	form.Textbox('c', form.notnull, description='Numero de usuarios que saben utilizar el lenguaje C++: '),
	form.Textbox('java', form.notnull, description='Numero de usuarios que saben utilizar el lenguaje Java: '),
	form.Textbox('small', form.notnull, description='Numero de usuarios que saben utilizar el lenguaje Smalltalk: '),
	form.Textbox('piton', form.notnull, description='Numero de usuarios que saben utilizar el lenguaje Python: '),
	form.Textbox('html', form.notnull, description='Numero de usuarios que saben utilizar el lenguaje HTML: '),
	form.Textbox('php', form.notnull, description='Numero de usuarios que saben utilizar el lenguaje PHP: '),
	form.Textbox('j', form.notnull, description='Numero de usuarios que saben utilizar el lenguaje JQuery: '),
	form.Button('Enviar datos'),
)

id_form = form.Form(
	form.Textbox('id', form.notnull, description='Identificador del grafico: '),
	form.Button('Entrar'),
)

tuit_form = form.Form(
	form.Textbox('tuit', form.notnull, description='Introduce un Twitter: '),
	form.Button('Entrar'),
)

def correct_password (usuario):
	return usuario + '3' #concateno un 3 al nombre de usuario para definir la contraseña inicial del usuario

def comprueba_identificacion ():
	usuario = session.usuario
	return usuario

def mandelbrot(x_min, x_max, y_min, y_max, pixeles, iteraciones):
	# Cuadricula uniforme
	x, y = np.meshgrid(np.linspace(x_min, x_max, pixeles),
		                np.linspace(y_min, y_max, pixeles))

	# Funcion de recurrencia para el conjunto de mandelbrot
	def znn(z, cc):
		     return z**2 + cc

	c = x + 1j*y # Cuadricula compleja
	z = c.copy()
	fractal = np.zeros(z.shape, dtype=np.uint8) + 255 # Color inicial (lo que no pertenece al fractal)

	# Iterar
	for n in range(iteraciones):
		     # Se actualiza z recursivamente
		     z = znn(z, c)

		     # Mascara
		     mask = (np.abs(z) > 2)

		     # Actualizar el color del fractal
		     # Color depende de la iteracion actual
		     fractal[mask] =  255 *  (n / float(iteraciones))

	# Mostrar la imagen usando como pixeles el fractal y mapa de colores "hot"
	plt.imshow(np.log(fractal), cmap=plt.cm.hot, extent=(x_min, x_max, y_min, y_max))
	plt.title('Conjunto de Mandelbrot')
	plt.xlabel('Eje X')
	plt.ylabel('Eje Y')

	plt.show()

class logout:
	def GET(self):
		usuario = session.usuario
		session.kill()
		return 'Adios ' + usuario

class inicio:
	def GET(self):
		usuario = comprueba_identificacion () #Comprobamos que el usuario esté identificado, sino le pedimos al usuario que se identifique
		if usuario: 
			return web.seeother('/registro')
		else:
			form = login_form()
			return render.login(form = form, usuario = usuario)

	def POST(self):
		form = login_form()
		if not form.validates():
			return render.login(form = form, usuario = '')

		i = web.input()
		usuario = i.usuario
		password = i.contrasenia

		if password == correct_password (usuario):
			session.usuario = usuario
			return web.seeother('/registro')
		else:
			form = login_form()	
			return render.login(form = form, usuario = '', mensaje = u'Contraseña incorrecta, tu contraseña correcta sería ' + correct_password (usuario))
	
class registro:
	def GET(self):
		usuario = comprueba_identificacion ()
		form = form_p3()
		session.sesion3 = session.sesion2
		session.sesion2 = session.sesion1
		session.sesion1 = 'registro'

		if usuario:
			return render.index(form = form, usuario = usuario, mensaje = '', sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)
		else:
			return web.seeother('/inicio')

class insercion:
	def GET(self):
		usuario = comprueba_identificacion ()
		form = form_p3()
		session.sesion3 = session.sesion2
		session.sesion2 = session.sesion1
		session.sesion1 = 'insercion'
		return render.registro(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

	def POST(self):
		usuario = comprueba_identificacion ()
		form = form_p3()
		if not form.validates():
			return render.registro(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)
		else:
			nombres = {"nombre": form.d.nombre,
						"apellidos": form.d.apellidos,
						"dni": form.d.dni,
						"correo": form.d.correo,
						"dia": form.d.dia,
						"mes": form.d.mes,
						"anio": form.d.anio,
						"direccion": form.d.direccion,
						"contrasenia": form.d.contrasenia,
						"visa": form.d.visa,
						"pago": form.d.pago}

			coll.insert(nombres)

			return render.index(form = form, usuario = usuario, mensaje = 'Registro del usuario realizado correctamente', sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

class datos:
	def GET(self):
		usuario = comprueba_identificacion ()
		form = datos_form()
		session.sesion3 = session.sesion2
		session.sesion2 = session.sesion1
		session.sesion1 = 'datos'
		return render.datos(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

	def POST(self):
		usuario = comprueba_identificacion ()
		form = datos_form()

		if not form.validates():
			return render.datos(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)
		else:
			try:
				cursor = coll.find({"nombre":form.d.nombre})
				nombre = cursor[0]["nombre"]
				apellidos = cursor[0]["apellidos"]
				dni = cursor[0]["dni"]
				correo = cursor[0]["correo"]
				dia = cursor[0]["dia"]
				mes = cursor[0]["mes"]
				anio = cursor[0]["anio"]
				nacimiento = dia + '/' + mes + '/' + anio
				direccion = cursor[0]["direccion"]
				contrasenia = cursor[0]["contrasenia"]
				visa = cursor[0]["visa"]
				pago = cursor[0]["pago"]

				return render.visualizar(form = form, usuario = usuario, nombre = nombre, apellidos = apellidos, dni = dni, correo = correo, nacimiento = nacimiento, direccion = direccion, contrasenia = contrasenia, visa = visa, pago = pago, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)
			except:
				return render.index(form = form, usuario = usuario, mensaje = 'Nombre de usuario no existente en la base de datos', sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

class modificar:
	def GET(self):
		usuario = comprueba_identificacion ()
		form = modi_form()
		session.sesion3 = session.sesion2
		session.sesion2 = session.sesion1
		session.sesion1 = 'modificar'
		return render.modificar(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

	def POST(self):
		usuario = comprueba_identificacion ()
		form = modi_form()	
		formi = form_p3()

		if not form.validates():
			return render.modificar(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)	
		else:
			try:
				cursor = coll.find({"nombre":form.d.nombre})
				nombre = cursor[0]["nombre"]
				apellidos = cursor[0]["apellidos"]
				dni = cursor[0]["dni"]
				correo = cursor[0]["correo"]
				dia = cursor[0]["dia"]
				mes = cursor[0]["mes"]
				anio = cursor[0]["anio"]
				nacimiento = dia + '/' + mes + '/' + anio
				direccion = cursor[0]["direccion"]
				contrasenia = cursor[0]["contrasenia"]
				visa = cursor[0]["visa"]
				pago = cursor[0]["pago"]

				formi.nombre.value = nombre
				formi.apellidos.value = apellidos
				formi.dni.value = dni
				formi.correo.value = correo
				formi.dia.value = int(dia)
				formi.mes.value = mes
				formi.anio.value = int(anio)	
				formi.direccion.value = direccion
				formi.contrasenia.value = contrasenia
				formi.verificacion.value = contrasenia
				formi.visa.value = visa
				formi.pago.value = pago

				return render.modi(form = formi, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)
			except:
				return render.index(form = form, usuario = usuario, mensaje = 'Nombre de usuario no existente en la base de datos', sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)
		
class cambio:
	def GET(self):
		usuario = comprueba_identificacion ()
		form = modi_form()
		formi = form_p3()
		session.sesion3 = session.sesion2
		session.sesion2 = session.sesion1
		session.sesion1 = 'cambio'

		if not form.validates():
			return render.modificar(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)	
		else:	
			try:
				cursor = coll.find({"nombre":form.d.nombre})
				nombre = cursor[0]["nombre"]
				apellidos = cursor[0]["apellidos"]
				dni = cursor[0]["dni"]
				correo = cursor[0]["correo"]
				dia = cursor[0]["dia"]
				mes = cursor[0]["mes"]
				anio = cursor[0]["anio"]
				nacimiento = dia + '/' + mes + '/' + anio
				direccion = cursor[0]["direccion"]
				contrasenia = cursor[0]["contrasenia"]
				visa = cursor[0]["visa"]
				pago = cursor[0]["pago"]

				formi.nombre.value = nombre
				formi.apellidos.value = apellidos
				formi.dni.value = dni
				formi.correo.value = correo
				formi.dia.value = int(dia)
				formi.mes.value = mes
				formi.anio.value = int(anio)	
				formi.direccion.value = direccion
				formi.contrasenia.value = contrasenia
				formi.verificacion.value = contrasenia
				formi.visa.value = visa
				formi.pago.value = pago

				return render.modi(form = formi, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)
			except:
				return render.index(form = form, usuario = usuario, mensaje = 'Nombre de usuario no existente en la base de datos', sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

	def POST(self):
		usuario = comprueba_identificacion ()
		form = form_p3()
		if not form.validates():
			return render.modi(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)
		else:
			nombres = {"nombre": form.d.nombre,
						"apellidos": form.d.apellidos,
						"dni": form.d.dni,
						"correo": form.d.correo,
						"dia": form.d.dia,
						"mes": form.d.mes,
						"anio": form.d.anio,
						"direccion": form.d.direccion,
						"contrasenia": form.d.contrasenia,
						"visa": form.d.visa,
						"pago": form.d.pago}

			coll.remove({"nombre":form.d.nombre})
			coll.insert(nombres)

			return render.index(form = form, usuario = usuario, mensaje = 'Registro del usuario realizado correctamente', sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

class rss:
	def GET(self):
		usuario = comprueba_identificacion ()
		session.sesion3 = session.sesion2
		session.sesion2 = session.sesion1
		session.sesion1 = 'rss'

		url = 'http://ep00.epimg.net/rss/elpais/portada.xml'

		urllib.urlretrieve(url, "portada.xml")

		d = feedparser.parse('portada.xml')
		tam = len(d.entries)
		pos = 0
		lista = []

		while pos < tam:
			lista.insert(pos, d.entries[pos].title)
			pos = pos + 1

		return render.rss(lista = lista, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

class maps:
	def GET(self):
		usuario = comprueba_identificacion ()
		session.sesion3 = session.sesion2
		session.sesion2 = session.sesion1
		session.sesion1 = 'maps'

		return render.prueba(usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

class charts:
	def GET(self):
		usuario = comprueba_identificacion ()
		form = charts_form()
		session.sesion3 = session.sesion2
		session.sesion2 = session.sesion1
		session.sesion1 = 'charts'
		return render.chartsdatos(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

	def POST(self):
		usuario = comprueba_identificacion ()
		form = charts_form()
		if not form.validates():
			return render.chartsdatos(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)
		else:
			cantidad = {"id": form.d.id,
						"c": form.d.c,
						"java": form.d.java,
						"small": form.d.small,
						"piton": form.d.piton,
						"html": form.d.html,
						"php": form.d.php,
						"j": form.d.j}

			coll.insert(cantidad)

			return render.index(form = form, usuario = usuario, mensaje = 'Insercion de datos realizado correctamente', sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

class mostrarcharts:
	def GET(self):
		usuario = comprueba_identificacion ()
		form = id_form()
		session.sesion3 = session.sesion2
		session.sesion2 = session.sesion1
		session.sesion1 = 'mostrarcharts'
		return render.datoscharts(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

	def POST(self):
		usuario = comprueba_identificacion ()
		form = id_form()

		if not form.validates():
			return render.datoscharts(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)
		else:
			try:
				cursor = coll.find({"id":form.d.id})
				c = int(cursor[0]["c"])
				java = int(cursor[0]["java"])
				small = int(cursor[0]["small"])
				piton = int(cursor[0]["piton"])
				html = int(cursor[0]["html"])
				php = int(cursor[0]["php"])
				j = int(cursor[0]["j"])

				return render.charts(usuario = usuario, c = c, java = java, small = small, piton = piton, html = html, php = php, j = j, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)
			except:
				return render.index(form = form, usuario = usuario, mensaje = 'Identificador de grafica no existente en la base de datos', sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

class twitter:
	def GET(self):
		usuario = comprueba_identificacion ()
		form = tuit_form()
		session.sesion3 = session.sesion2
		session.sesion2 = session.sesion1
		session.sesion1 = 'twitter'

		return render.datostwitter(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

	def POST(self):
		usuario = comprueba_identificacion ()
		form = tuit_form()

		if not form.validates():
			return render.datostwitter(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)
		else:
			tweets = api.search(q=form.d.tuit)

			tuit = tweets[0].text
			autor = tweets[0].author.name
			lugar = tweets[0].author.location
		
			return render.twitter(tuit = tuit, autor = autor, lugar = lugar, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

class mashup:
	def GET(self):
		usuario = comprueba_identificacion ()
		form = tuit_form()
		session.sesion3 = session.sesion2
		session.sesion2 = session.sesion1
		session.sesion1 = 'mashup'

		return render.mashup(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

	def POST(self):
		usuario = comprueba_identificacion ()
		form = tuit_form()

		if not form.validates():
			return render.mashup(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)
		else:
			tweets = api.search(q=form.d.tuit, count = 10)

			for tweet in tweets:
				coordenadas = tweet.geo

				latitud = 0
				longitud = 0

				if str(coordenadas) != "None": 
					nulo,nulo,nulo,latitud,longitud = str(coordenadas).split() 
					latitud = latitud.strip('[,') 
					longitud = longitud.strip(']}')

					return render.mapsmashup(form = form, usuario = usuario, sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3, latitud = latitud, longitud = longitud)

			return render.index(form = form, usuario = usuario, mensaje = 'Con el twitter introducido no se ha podido encontrar ningun tuit con geolocalizacion', sesion1 = session.sesion1, sesion2 = session.sesion2, sesion3 = session.sesion3)

class p3_formulario:
	def GET(self):
		form = form_p3()
		return plantilla.formulario(form)

	def POST(self):
		form = form_p3()
		if not form.validates():
			return plantilla.formulario(form)
		else:
			return "Datos insertados correctamente"

class fractal:
	def GET(self):
		form = form_fractal()
		return plantilla.formulario(form)

	def POST(self):
		form = form_fractal()
		if not form.validates():
			return plantilla.formulario(form)
		else:
			return mandelbrot(float(form.d.x_min), float(form.d.x_max), float(form.d.y_min), float(form.d.y_max), int(form.d.pixeles), int(form.d.iteraciones))

class index:
	def GET(self):
		form = myform()
		return plantilla.formulario(form)

	def POST(self):
		form = myform()
		if not form.validates():
			return plantilla.formulario(form)
		else:
			return "Bienvenido %s %s" % (form.d.nombre, form.d.apellido)

class error:
	def GET(self, name):
		return '<!doctype html><html lang="es"><head><meta charset="utf-8"><title>ERROR</title></head><body><header>404 Not Found</header></body></html>'

class mia:        
    def GET(self):
        return '<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Prueba</title></head><body><header>Prueba de contenido estatico</header><img src="static/indice.jpeg" alt="Python"></body></html>'

class hello:        
    def GET(self): 
        name = 'World'
        return 'Hello, ' + name + '!'

if __name__ == "__main__":
    app.run()
