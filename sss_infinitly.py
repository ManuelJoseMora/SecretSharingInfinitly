#!/usr/bin/env python

#Librerias usadas
import shamirs
import time



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

def get_generation(participants):
    i = 1
    generation_limit = i * (2 ** (int(k) - 1))
    for people in participants:

        if (participants.index(people)) < generation_limit:
            print(people + " está en la generación  " + str(i))
        else:

            i = i + 1
            generation_limit =  generation_limit + (i * (2 ** (int(k) - 1)))
            print(people + " está en la generación " + str(i))



# ---------------------------------------------------------------------------------------------------------------------
# Funciones de Desencriptado
# ---------------------------------------------------------------------------------------------------------------------

def decrypt_diff_generations(lista_final):
    generaciones_decrypt = []
    for miembro in lista_final:
        generaciones_decrypt.append(participant_generation(miembro))

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


    for miembro in lista_final:
        lista_shares.append(globals()[miembro][gen_idx[lista_final.index(miembro)]])

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

                lista_shares.append(globals()[i][0])

            desencriptado = shamirs.interpolate(lista_shares, threshold=int(k))
        else:
            # Si pertenecen a generaciones diferentes

            print("Los candidatos son de diferentes generaciones")
            decrypt_diff_generations
            desencriptado = decrypt_diff_generations(lista_final)

    return desencriptado



def desencriptacion():


    recovered_key = desencripta(lista_desencryptar)
    print("La clave es: ")
    time.sleep(1)
    print(".")
    time.sleep(1)
    print("..")
    time.sleep(1)
    print("...")
    time.sleep(1)

    print("---------------------------------------")
    print(recovered_key)
    print("---------------------------------------")





def desencriptado():



    # Ya tenemos una lista con los participantes, otra con los candidatos a desencriptar, la clave y el k threshold.


    n_participantes = len(participants)
    n_candidatos = len(lista_desencryptar)
    if n_participantes == 0:
        print("La lista de participantes debe contener particpantes. \n")
    elif n_candidatos == 0:
        print("La lista de cadidatos debe contener nombres de candidatos. \n")
    else:
        print("...")





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

            idx_g = 1
            while (idx_g <= size_g):
                idx_participant = n - 1
                if idx_participant < len(participants):
                    participant_i = participants[idx_participant]
                    globals()[participant_i] = [sss[n_shares]]

                n_shares = n_shares + 1
                n = n + 1
                idx_g = idx_g + 1

            n_generacion = n_generacion + 1
        Fin = False



    # Chequeamos los shares de nivel 0 (intra-generation) de cada participante
    #for participant in participants:
    #    print(participant)
    #    print(globals()[participant])


    # ---------------------------------------------------------------------------------------------------------------------
    # Caso 2 - Entre diferentes Generaciones.
    # ---------------------------------------------------------------------------------------------------------------------
    # Hay que generar (s_1, ...., s_k-1) shares para cada
    # generación g y compartir s_i con SSS(i,size(g))
    # ---------------------------------------------------------------------------------------------------------------------


    # Generamos (k-1)*numero_generaciones shares
    numero_generaciones = n_generacion - 1

    print("Numero de generaciones: " + str(numero_generaciones))

    if(numero_generaciones > 1):
        numero_shares = numero_generaciones * (int(k) - 1)
        sss_inter_g = shamirs.shares(int(key), quantity=int(numero_shares), threshold=int(k))

        # Seleccionamos k-1 shares que se han de repartir en g1,
        # los k-1 siguientes shares se reparten en g2 y asi sucesivamente.

        start_p = 0
        inicio_g = 0
        end_p = int(k) - 1
        index_sss = 1
        for i in range(numero_generaciones):

            participants_in_g = participants[inicio_g:(inicio_g + generation_size(i + 1, int(k)))]

            shares_for_g = sss_inter_g[start_p:end_p]

            # Hay que repartir cada share s_i entre los miembros de la generación g
            # usando SSS(i, size(g))
            idx_threshold = 1
            for share in shares_for_g:

                sss_share_i = shamirs.shares(share.value, quantity=generation_size(i + 1, int(k)), threshold=idx_threshold)

                # Falta guardar en cada participante su share en el nivel que le corresponda
                t = 0
                for participant in participants_in_g:

                    sss_share_i[t].index = index_sss

                    globals()[participant].append(sss_share_i[t])
                    t = t + 1

                idx_threshold = idx_threshold + 1
                index_sss = index_sss + 1

            start_p = end_p
            end_p = start_p + (int(k) - 1)
            inicio_g = inicio_g + generation_size(i + 1, int(k))



    # ----------------------------------------------------------------------------------------------------------------
    desencriptacion()
    # ----------------------------------------------------------------------------------------------------------------




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
k = input("Ahora introduce el k-threshold como un numero entero positivo:\n")

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
     4-  Visualizar la lista de Participantes. \n
     5 - Visualizar la lista de Participantes que desean desencriptar. \n
     6 - Desencriptar. \n
     7 - Visualizar participantes y generaciones. \n
    **************************************************\n""")

    if participant == '1':
        time.sleep(2)
        nombre_participante = input("Introduce el nombre del nuevo participante.\n")
        if nombre_participante not in participants:
            participants.append(nombre_participante)
            print("Muy bien, seguimos...\n")
        else:
            print("Ese participante ya ha sido incluido.\n")

    elif participant == '2':
        time.sleep(2)
        input_lista = input("Introduce una lista con los nombres de los partipantes separados por una coma.\n" +
                            "Por Ejemplo: Pedro, Luis, Manuel \n")
        lista_desencryptar = [s for s in input_lista.split(",")]
    elif participant == '3':
        time.sleep(2)
        print("Hasta Luego...")
        time.sleep(1)
        quit()
    elif participant == '4':
        time.sleep(2)
        print("\n")
        print(participants)
    elif participant == '5':
        time.sleep(2)
        print("\n")
        print(lista_desencryptar)
    elif participant == '6':
        time.sleep(2)
        desencriptado()
        seguimos = True
    elif participant == '7':
        get_generation(participants)
        #for user in participants:
        #    print("User: " + str(user) + " is in generation " + str(participant_generation(user)))

    else:
        time.sleep(2)
        print("Las opciones son 1, 2, 3, 4 y 5. Vuelve a empezar.")
        seguimos = False
