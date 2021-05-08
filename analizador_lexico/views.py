from django.shortcuts import render, redirect, HttpResponse
from analizador_lexico import analizadorLex

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def Index (request):
    listTokensValidos = []
    listErrors        = []

    if request.method == 'POST':
        entrada = request.POST['editor']

        #Analizar tokens
        listtResult = analizadorLex.analisar(entrada)
        for i in listtResult:
            if i[0] == "error":
                listErrors.append([i[0],i[1],i[2],i[3]])
            else:
                listTokensValidos.append([i[0],i[1],i[2],i[3]])
        #objeto = listtResult

    return render (request, 'editor.html',{
        'title': 'ANALIZADOR LÉXICO',
        'tokensValidos': listTokensValidos,
        'tokensError': listErrors
    })

def Login (respuesta):

    if respuesta.method == 'POST':

        nombre = respuesta.POST['user']
        passw = respuesta.POST['password']
        
        user = authenticate(respuesta, username=nombre, password=passw)

        if user is not None:
            login(respuesta, user)
            messages.success(respuesta, f'Bienvenido { respuesta.user }!')
            return redirect('index')
        else:
            messages.error(respuesta, 'Usuario incorrecto!')

    return render(respuesta, 'login.html')

def Logout (respuesta):

    logout(respuesta)

    return redirect('login')