#!/usr/bin/env python

#Librerias usadas
import shamirs




# Introducimos los datos, key, threshold y participantes
key = input("Por favor, introduce la clave como un número entero positivo:\n")

# Comprobamos que la clave sea un numero entero posotivo
try:
    if int(key) > 0:
        print("Seguimos...")
    else:    
        print("La clave debe ser un entero positivo. Vuelve a empezar.")
        
except:
    print("La clave debe ser un entero positivo. Vuelve a empezar y prueba de nuevo.")

# Se introducen el k threhsold del esquema
k = input("Ahora introduce el k-threshold como un numeor entero positivo:\n")

# Comprobamos que el threshold k es un numero positivo
try:
    if int(k) > 0:
        print("Seguimos...")
    else:    
        print("El threshold debe ser un entero positivo. Vuelve a empezar.")
        
except:
    print("El threshold debe ser un entero positivo. Vuelve a empezar y prueba de nuevo.")

# Menu de entrada de datos
participants = []
lista_desencryptar = []
seguimos = True

while (seguimos):
    
    participant = input("""
    **************************************************
     Por favor, elige una opción para continuar:\n
     1 - Añadir un nuevo Participante. \n
     2 - Pasar un lista de participantes para tratar de desencriptar la clave.\n 
     3 - Finalizar. \n
    **************************************************\n\n""")
    
    
    if participant == '1':
        nombre_participante = input("Introduce el nombre del nuevo participante.\n\n")
        if nombre_participante not in participants:
            participants.append(nombre_participante)
            print("Muy bien, seguimos...\n")
        else:
            print("Ese participante ya ha sido incluido.\n")
        
    elif participant == '2':
        input_lista = input("Introduce una lista con los nombres de los partipantes separados por una coma.\n\n")
        lista_desencryptar = [ s for s in input_lista.split(",") ]
    elif participant == '3':
        seguimos = False        
    else:
        print("Las opciones son 1, 2 ó 3. Vuelve a empezar.")
        seguimos = False

# Cargamos participantes de manera manual
participants = ['Pedro', 'Manuel', 'Maria', 'Luis', 'Ana', 'Rocio', 'Kevin', 'Jorge', 'Mario', 'Guillermo', 'Sara', 'Rebeca']

# Ya tenemos una lista con los participantes, otra con los candidatos a desencriptar, la clave y el k threshold.

n_participantes = len(participants)
n_candidatos = len(lista_desencryptar)


# Funciones de apoyo.
# Gestion de las Generaciones.

def generation_size( i, k):
    size_g_i = i*(2**(k-1))
    return size_g_i


def participant_idx(participant_name, participants):
    participant_index = participants.index(participant_name)
    return participant_index


def participant_generation(participant_name):
    idx = participant_idx(participant_name, participants)
    init = 1
    generation_size_value_limit = generation_size(init, int(k)) - 1
    while idx > generation_size_value_limit:
        init = init + 1
        generation_size_value_limit = generation_size_value_limit + (generation_size(init, int(k)) - 1)

    return init

# ---------------------------------------------------------------------------------------------------------------------
# Cargamos las lista de los shares en listas para cada Particnant.
# Primero, en el primer nivel (index 0 de la lista) de cada Participante el share correspondiente a su generación.
# En el resto de niveles de cada partipante estan los shares compartidos entre generaciones:
#     nivel 1 --> Share(s_1, size(g), threshold = 1)
#     nivel 1 --> Share(s_2, size(g), threshold = 2)
#     ...
#     nivel 1 --> Share(s_k-1, size(g), threshold = k-1)
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
# Caso 1 - Dentro de una misma generación.
# ---------------------------------------------------------------------------------------------------------------------
# Hay que ejecutar Shamir para cada generación.
# Y cada Partipante tendrá aociada una lista donde en la 
# primera posicicón tendra el share de su generación que
# le corresponda.
# ---------------------------------------------------------------------------------------------------------------------

n = 1
n_generacion = 1
Fin = True
while (Fin):
    while (n <= n_participantes):
        size_g = generation_size(int(n_generacion), int(k))
        sss = shamirs.shares(int(key), quantity=int(size_g), threshold=int(k))
        n_shares = 0
        print(sss)
        print("\n")
        idx_g = 1
        while (idx_g <= size_g):
            idx_participant = n - 1
            participant_i = participants[idx_participant]
            print("- Generación: " + str(n_generacion))
            print("- Size of g: " + str(size_g))
            print("- Participante: " + str(participant_i))
            print(" -Share: " + str(sss[n_shares]))
            globals()[participant_i] = [sss[n_shares]]

            n_shares = n_shares + 1
            n = n + 1
            idx_g = idx_g + 1

        n_generacion = n_generacion + 1
    Fin = False



# Chequeamos los shares de nivel 0 (intra-generation) de cada participante
for participant in participants:
    print(participant)
    print(globals()[participant])

# ---------------------------------------------------------------------------------------------------------------------
# Caso 2 - Entre diferentes Generaciones.
# ---------------------------------------------------------------------------------------------------------------------
# Hay que generar (s_1, ...., s_k-1) shares para cada
# generación g y compartir s_i con SSS(i,size(g))
# ---------------------------------------------------------------------------------------------------------------------

# Generamos (k-1)*numero_generaciones shares
numero_generaciones = n_generacion - 1
numero_shares = numero_generaciones * (int(k) - 1)
sss_inter_g = shamirs.shares(int(key), quantity=int(numero_shares), threshold=int(k))
print("Shares a compartir entre generaciones: \n")
print(sss_inter_g)

# Seleccionamos k-1 shares que se han de repartir en g1,
# los k-1 siguientes shares se reparten en g2 y asi sucesivamente.

start_p = 0
inicio_g = 0
end_p = int(k) - 1
index_sss = 1
for i in range(numero_generaciones):
    print("Generacion " + str(i + 1))
    print("from " + str(inicio_g) + "  " + str(generation_size(i + 1, int(k))) + " posiciones")
    print(participants[inicio_g:(inicio_g + generation_size(i + 1, int(k)))])
    participants_in_g = participants[inicio_g:(inicio_g + generation_size(i + 1, int(k)))]
    print("\n")
    shares_for_g = sss_inter_g[start_p:end_p]
    print("k -1 shares..." + str(shares_for_g))
    print("\n")

    # Hay que repartir cada share s_i entre los miembros de la generación g
    # usando SSS(i, size(g))
    idx_threshold = 1
    for share in shares_for_g:

        sss_share_i = shamirs.shares(share.value, quantity=generation_size(i + 1, int(k)), threshold=idx_threshold)
        print("Shares para cada miembro de Generación " + str(i + 1) + " " + " en el nivel " + str(
            idx_threshold) + " " + str(sss_share_i))
        print("\n")

        # Falta guardar en cada participante su share en el nivel que le corresponda
        t = 0
        for participant in participants_in_g:
            print("Particpant")
            print("\n")
            print(participant)

            print("\n")
            print("threshold")
            print(idx_threshold)
            print("\n")

            print("Share")
            print("\n")
            sss_share_i[t].index = index_sss
            print(sss_share_i[t])
            globals()[participant].append(sss_share_i[t])
            t = t + 1

        idx_threshold = idx_threshold + 1
        index_sss = index_sss + 1

    start_p = end_p
    end_p = start_p + (int(k) - 1)
    inicio_g = inicio_g + generation_size(i + 1, int(k))



# Chequeamos los shares repartidos a cada partipante entre generaciones:
for participant in participants:
    print(participant)
    print(globals()[participant])

# ---------------------------------------------------------------------------------------------------------------------
# Funciones de Desencriptado
# ---------------------------------------------------------------------------------------------------------------------

def decrypt_diff_generations(lista_final):
    generaciones_decrypt = []
    for miembro in lista_final:
        generaciones_decrypt.append(participant_generation(miembro))
    print("Participants: \n")
    print(lista_final)
    print("Generations: \n")
    print(generaciones_decrypt)
    lista_shares = []
    gen_aux = []
    gen_idx = []

    for gen in generaciones_decrypt:
        if gen not in gen_aux:
            gen_aux.append(gen)
            gen_idx.append(1)
        else:
            gen_count = gen_aux.count(gen)
            gen_aux.append(gen)
            gen_idx.append(gen_count + 1)

    print("Lista de ocurrencias por generación: \n")
    print(gen_idx)
    for miembro in lista_final:
        lista_shares.append(globals()[miembro][gen_idx[lista_final.index(miembro)]])
    print(lista_shares)
    print("Desencpritamos....\n")
    desencriptado = shamirs.interpolate(lista_shares, threshold=int(k))

    return desencriptado


def desencripta(lista_desencryptar):
    if len(lista_desencryptar) < int(k):
        print("""El numero de partipantes para poder obtener la clava ha de ser mayor o igual \n
        al threshold k, cuyo valor actual es: """ + str(k))
    else:
        lista_final = lista_desencryptar[0:int(k)]
        generaciones_decrypt = []
        for miembro in lista_final:
            generaciones_decrypt.append(participant_generation(miembro))
        # Si todos los participantes para desencrptar pertenecen a la misma generación
        if all(element == generaciones_decrypt[0] for element in generaciones_decrypt):
            lista_shares = []
            print("Los candidatos son de la misma generación")
            for i in lista_final:
                # print(i)
                # print(locals()[i][0])
                lista_shares.append(globals()[i][0])

            # desencriptado= lista_shares
            desencriptado = shamirs.interpolate(lista_shares, threshold=int(k))
        else:
            # Si pertenecen a generaciones diferentes

            print("Los candidatos son de diferentes generaciones")
            decrypt_diff_generations
            desencriptado = decrypt_diff_generations(lista_final)

    return desencriptado

# ---------------------------------------------------------------------------------------------------------------------
#Lista de Participantes que optan al desencriptado
lista_desencryptar = ["Pedro", "Manuel", "Sara"]
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
desencripta(lista_desencryptar)
# ---------------------------------------------------------------------------------------------------------------------
